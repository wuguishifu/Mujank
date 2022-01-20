import discord
import dataloader

colors = {
    2: discord.Colour.from_rgb(24, 204, 0),
    3: discord.Colour.from_rgb(0, 112, 221),
    4: discord.Colour.from_rgb(163, 53, 238),
    5: discord.Colour.from_rgb(255, 128, 0),
    6: discord.Colour.from_rgb(255, 237, 0)
}


class Card:
    def __init__(self, card_id: str, image_url: str, title: str, rating: int, tags: str):
        self.id = card_id
        self.image_url = image_url
        self.title = title
        self.rating = rating
        self.tags = tags

    def to_embed(self, author: discord.member.Member):
        rolls_left = dataloader.get_num_rolls(author.id)
        if rolls_left == 1:
            rolls_left_text = f'⚠️{rolls_left} roll left! ⚠️'
        else:
            rolls_left_text = f'⚠️{rolls_left} rolls left! ⚠️'

        stars = ''
        for i in range(self.rating):
            stars += '★'

        color = colors.get(self.rating)
        file = discord.File(self.image_url, filename='image.png')
        embed = discord.Embed(
            title=f'{self.title}',
            description=f'{stars}\n{self.tags}',
            colour=color,
        )

        num_owned = dataloader.get_num(author.id, self.id)
        embed.set_footer(text=f'{num_owned} owned by {author.name}\n{rolls_left_text}')
        embed.set_image(url='attachment://image.png')
        return embed, file

    def to_display_embed(self, author: discord.member.Member):
        stars = ''
        for i in range(self.rating):
            stars += '★'

        color = colors.get(self.rating)
        if 'gif' in self.image_url:
            file = discord.File(self.image_url, filename='image.gif')
        else:
            file = discord.File(self.image_url, filename='image.png')
        embed = discord.Embed(
            title=f'{self.title}',
            description=f'{stars}\n{self.tags}',
            colour=color,
        )

        num_owned = dataloader.get_num(author.id, self.id)
        embed.set_footer(text=f'{num_owned} owned by {author.name}')
        if 'gif' in self.image_url:
            embed.set_image(url='attachment://image.gif')
        else:
            embed.set_image(url='attachment://image.png')
        return embed, file


def to_search_slideshow_embed(query: str, card_list: [], cur_page: int):
    card = card_list[cur_page]
    stars = ''
    for i in range(card.rating):
        stars += '★'

    color = colors.get(card.rating)
    file = discord.File(card.image_url, filename='image.png')
    embed = discord.Embed(
        title=f'Search: {query} - Page {cur_page + 1}/{len(card_list)}\n'
              f'{card.title}',
        description=f'{stars}\n{card.tags}',
        colour=color,
    )
    embed.set_image(url='attachment://image.png')
    return embed, file


def to_owned_embed(user: discord.user.User, owned_list: [], page: int, num_pages: int):
    description = ''
    index_first = 10 * page
    index_last = 10 * (page + 1)
    for i in owned_list[index_first:index_last]:
        num = i.val()
        card = card_deck.get(i.key()).title
        description += f'{num}x **{card}**\n'
    embed = discord.Embed(
        title=f"{user.name}’s Deck - Page {page + 1}/{num_pages}",
        description=description,
        colour=discord.Colour.red()
    )
    displayed_id = dataloader.get_displayed_card(user.id)
    if displayed_id == 'c_id_-1':
        file = discord.File('mujank-logo.jpg', 'image.png')
    else:
        file = discord.File(card_deck.get(displayed_id).image_url, 'image.png')
    embed.set_thumbnail(url='attachment://image.png')
    return embed, file


def to_wishlist_embed(user: discord.user.User, wishlist: [], page: int, num_pages: int):
    description = ''
    index_first = 10 * page
    index_last = 10 * (page + 1)
    for i in wishlist[index_first:index_last]:
        card = card_deck.get(i.key()).title
        description += f'{wishlist.index(i) + 1}. **{card}**\n'
    embed = discord.Embed(
        title=f"{user.name}’s Wishlist - Page {page + 1}/{num_pages}",
        description=description,
        colour=discord.Colour.red()
    )
    display_id = dataloader.get_displayed_card(user.id)
    if display_id == 'c_id_-1':
        file = discord.File('mujank-logo.jpg', 'image.png')
    else:
        file = discord.File(card_deck.get(display_id).image_url, 'image.png')
    embed.set_thumbnail(url='attachment://image.png')
    return embed, file


def to_search_embed(search_query: str, card_list: [], page: int, num_pages):
    description = ''
    index_first = 10 * page
    index_last = 10 * (page + 1)
    for i in card_list[index_first:index_last]:
        card = i.title
        stars = ''
        for j in range(i.rating):
            stars += '★'
        description += f'{card_list.index(i) + 1}. **{card}** - {stars}\n'
    embed = discord.Embed(
        title=f"Search: {search_query} - Page {page + 1}/{num_pages}",
        description=description,
        colour=discord.Colour.red()
    )
    display_id = card_list[0].id
    file = discord.File(card_deck.get(display_id).image_url, 'image.png')
    embed.set_thumbnail(url='attachment://image.png')
    return embed, file


def name_search(query: []):
    card_list = []
    for card in card_deck.values():
        if card.tags.lower() in query:
            card_list.append(card)
    return card_list


def rating_search(query: int):
    card_list = []
    for card in card_deck.values():
        if card.rating == query:
            card_list.append(card)
    return card_list


cards = [
    ["c_id_0000", "cards/alex- _3.jpg", "Much Love", 3, "Alex"],
    ["c_id_0001", "cards/alex- puppy.jpg", "Wassup Dog", 3, "Alex"],
    ["c_id_0002", "cards/anteatery_cup_tower.png", "The Legendary Tower", 2, "Misc"],
    ["c_id_0003", "cards/bo- ac_A.jpg", "A", 3, "Bo"],
    ["c_id_0004", "cards/bo- airpods.jpg", "Hey, Look at my Airpods!", 2, "Bo"],
    ["c_id_0005", "cards/bo- beard.jpg", "Hey, Look at my Beard!", 2, "Bo"],
    ["c_id_0006", "cards/bo- bomomo.png", "BOmomo", 3, "Bo"],
    ["c_id_0007", "cards/bo- cream.jpg", "Oops, cream!", 3, "Bo"],
    ["c_id_0008", "cards/bo- dead_inside_outside.PNG", "he’s dead on the inside and the outside", 2, "Bo"],
    ["c_id_0009", "cards/bo- death_stare.png", "Death Stare", 2, "Bo"],
    ["c_id_0010", "cards/bo- eggplant.jpg", "Hey, Look at my Eggplant!", 2, "Bo"],
    ["c_id_0011", "cards/bo- full.jpg", "Oh man, I’m optimally full", 3, "Bo"],
    ["c_id_0012", "cards/bo- glasses.jpg", "Hey, Look at my Glasses!", 2, "Bo"],
    ["c_id_0013", "cards/bo- golfer_tshirt.jpg", "I’m a Golfer", 2, "Bo"],
    ["c_id_0014", "cards/bo- high_tide.jpg", "High Tide", 2, "Bo"],
    ["c_id_0015", "cards/bo- hs_band.jpg", "Band Nerd Bo", 2, "Bo"],
    ["c_id_0016", "cards/bo- late_night_peace.jpg", "Late Night Peace Out", 2, "Bo"],
    ["c_id_0017", "cards/bo- mask.jpg", "Don’t Forget a Mask", 2, "Bo"],
    ["c_id_0018", "cards/bo- no_sleep.jpg", "All these beds but you still won’t sleep with me", 2, "Bo"],
    ["c_id_0019", "cards/bo- on_the_phone.jpg", "Oh no, I Lost a Follower", 3, "Bo"],
    ["c_id_0020", "cards/bo- oreos_bos_cookies.jpg", "Oreos > Bo’s Cookies", 3, "Bo"],
    ["c_id_0021", "cards/bo- peace_out.jpg", "Peace Out - from Bo", 2, "Bo"],
    ["c_id_0022", "cards/bo- red_cup.jpg", "Dad Bo", 3, "Bo"],
    ["c_id_0023", "cards/bo- smol_version.jpg", "smol Bo", 3, "Bo"],
    ["c_id_0024", "cards/bo- takoyaki_chef.JPG", "Hey, I’m a Takoyaki Chef!", 2, "Bo"],
    ["c_id_0025", "cards/bo- towel_wrap.jpg", "Don’t Look at me I’m Shy", 3, "Bo"],
    ["c_id_0026", "cards/bo- uci_commit.jpg", "Commitment", 3, "Bo"],
    ["c_id_0027", "cards/bo- zoom.png", "Bo Douglas Bramer", 2, "Bo"],
    ["c_id_0028", "cards/combo- ac_bed.jpg", "Sleeping with the Homies", 3, "Combo"],
    ["c_id_0029", "cards/combo- ac_fam.JPG", "Animal Crossing Party", 3, "Combo"],
    ["c_id_0030", "cards/combo- ac_fish.JPG", "Fishing with the Homies", 3, "Combo"],
    ["c_id_0031", "cards/combo- among_us_steven_bo.jpg", "Sus Squad", 3, "Combo"],
    ["c_id_0032", "cards/combo- awkward_smile.png", "haha say cheese", 2, "Combo"],
    ["c_id_0033", "cards/combo- bo_kyran_wing_chun.jpg", "wing chun", 2, "Combo"],
    ["c_id_0034", "cards/combo- bo_nina_spoon.png", "nina spoon", 3, "Combo"],
    ["c_id_0035", "cards/combo- bo_steven_hand_update.PNG", "cookin up in the lab", 2, "Combo"],
    ["c_id_0036", "cards/combo- bowling_in_hell.jpg", "Bowling Time!", 2, "Combo"],
    ["c_id_0037", "cards/combo- business_casual_pho.jpg", "Back to Business", 3, "Combo"],
    ["c_id_0038", "cards/combo- cdeeznuts.png", "CDeezNuts", 2, "Combo"],
    ["c_id_0039", "cards/combo- fire_glasses.jpg", "We Fire Out Here", 3, "Combo"],
    ["c_id_0040", "cards/combo- flynn_steven_snapchat.JPG", "It’s Just Me and My Shorty", 3, "Combo"],
    ["c_id_0041", "cards/combo- ft_matt_bo_steven_mikey.PNG", "FaceTime Time", 3, "Combo"],
    ["c_id_0042", "cards/combo- good_day.png", "Good Day", 2, "Combo"],
    ["c_id_0043", "cards/combo- idiot.jpg", "idiot", 3, "Combo"],
    ["c_id_0044", "cards/combo- jenn_steven_koifish.jpg", "We at The Pond", 2, "Combo"],
    ["c_id_0045", "cards/combo- kbbq_peace.png", "KBBQ peace", 2, "Combo"],
    ["c_id_0046", "cards/combo- matt_tommy_thumbs_up.jpg", "Matt & Tommy Covid Crossover", 3, "Combo"],
    ["c_id_0047", "cards/combo- mikey_marth_steven_min_min.png", "Mikey & Steven as Smash Characters", 2, "Combo"],
    ["c_id_0048", "cards/combo- mikey_noah_drip_check.jpg", "Mikey & Noah Drip", 2, "Combo"],
    ["c_id_0049", "cards/combo- mikey_porcupine_steven_dog.png", "Mikey & Steven as Furries", 2, "Combo"],
    ["c_id_0050", "cards/combo- nina_palming_tommy.jpg", "Nina palming Tommy", 3, "Combo"],
    ["c_id_0051", "cards/combo- patrick_alyssa_jenn_steven_poke.JPG", "Poke Time", 2, "Combo"],
    ["c_id_0052", "cards/combo- petr_steven_jenn_will.png", "Petr Weather", 2, "Combo"],
    ["c_id_0053", "cards/combo- piggyback_bo_will.jpg", "Piggyback Attack", 3, "Combo"],
    ["c_id_0054", "cards/combo- rec_room_bo_steven_mikey.jpg", "Rec Room", 2, "Combo"],
    ["c_id_0055", "cards/combo- red_bull.jpg", "Red Bull Gives You Wings", 3, "Combo"],
    ["c_id_0056", "cards/combo- shopping.png", "Shoplifters", 2, "Combo"],
    ["c_id_0057", "cards/combo- steven_furry_with_haroon.jfif", "Beauty and the Beast", 3, "Combo"],
    ["c_id_0058", "cards/combo- target.jpg", "Caught in 4K", 3, "Combo"],
    ["c_id_0059", "cards/combo- uci_selfie.jpg", "Fountain Selfie", 3, "Combo"],
    ["c_id_0060", "cards/combo- why_hello_there.png", "Why Hello There", 2, "Combo"],
    ["c_id_0061", "cards/combo- will_bo_fingerguns.jpg", "Finger Guns pewpew", 3, "Combo"],
    ["c_id_0062", "cards/combo- will_bo_hs_band.jpg", "Band Nerds", 2, "Combo"],
    ["c_id_0063", "cards/combo- will_nina_sleeping.jpg", "Knocked Out", 3, "Combo"],
    ["c_id_0064", "cards/combo- will_patrick_plushie.jpg", "Plushies", 2, "Combo"],
    ["c_id_0065", "cards/combo- will_tommy_pumpkin_patch.jpg", "We’re inside a pumpkin lol", 2, "Combo"],
    ["c_id_0066", "cards/flynn- birthday_time.jpg", "Happy Birthday Flynn", 3, "Flynn"],
    ["c_id_0067", "cards/flynn- blurry.jpg", "Blurry Flynn", 2, "Flynn"],
    ["c_id_0068", "cards/flynn- crossbody.JPG", "Sit Back and Smile", 3, "Flynn"],
    ["c_id_0069", "cards/flynn- drip_check.jpg", "Drip Check", 2, "Flynn"],
    ["c_id_0070", "cards/flynn- side_profile.jpg", "Side Profile", 2, "Flynn"],
    ["c_id_0071", "cards/flynn- sleep.jpg", "Schleep", 3, "Flynn"],
    ["c_id_0072", "cards/flynn- sushi.jpg", "Damn, this Sushi Bussin’", 3, "Flynn"],
    ["c_id_0073", "cards/flynn- waiting.jpg", "Waiting for the T’sane Cashier", 3, "Flynn"],
    ["c_id_0074", "cards/haroon- hello.jpg", "Hello?", 3, "Haroon"],
    ["c_id_0075", "cards/haroon- jumpscare.jpg", "Jumpscare Haroon", 3, "Haroon"],
    ["c_id_0076", "cards/haroon- shy_guy.jpg", "Shy Guy with a Shy Guy", 3, "Haroon"],
    ["c_id_0077", "cards/jenn- facetime.png", "Pixelated Jenn", 2, "Jenn"],
    ["c_id_0078", "cards/jenn- hello.jpg", "Hello my Friends", 3, "Jenn"],
    ["c_id_0079", "cards/jenn- peace.jpg", "Peace Out - from Jenn", 2, "Jenn"],
    ["c_id_0080", "cards/matt- asmr.jpg", "ASMR", 3, "Matt"],
    ["c_id_0081", "cards/matt- dbz.png", "DBZ Matt", 2, "Matt"],
    ["c_id_0082", "cards/matt- petr_run.jpg", "On the Run", 2, "Matt"],
    ["c_id_0083", "cards/matt- plushie.jpg", "Seal’s Best Friend", 2, "Matt"],
    ["c_id_0084", "cards/matt- starbucks.png", "Starbucks", 3, "Matt"],
    ["c_id_0085", "cards/matt- thumbs_up.jpg", "Thumbs Up", 2, "Matt"],
    ["c_id_0086", "cards/matt- uci_commit.jpg", "Committed", 3, "Matt"],
    ["c_id_0087", "cards/matt- vr.jpg", "Metaverse", 3, "Matt"],
    ["c_id_0088", "cards/matt- widelens.jpg", "Widelens Matt", 3, "Matt"],
    ["c_id_0089", "cards/mikey- boba.png", "Boba Boba Masta Yoda", 2, "Mikey"],
    ["c_id_0090", "cards/mikey- bread.jpg", "Munching", 3, "Mikey"],
    ["c_id_0091", "cards/mikey- cooking.png", "He’s a Chef", 2, "Mikey"],
    ["c_id_0092", "cards/mikey- corndogs.jpg", "Mikey and the Weenies", 3, "Mikey"],
    ["c_id_0093", "cards/mikey- disappointed.jpg", "Disappointment", 3, "Mikey"],
    ["c_id_0094", "cards/mikey- full.jpg", "Stuffed", 3, "Mikey"],
    ["c_id_0095", "cards/mikey- i_support_daves.jpg", "Dave’s Hot Chicken > All", 2, "Mikey"],
    ["c_id_0096", "cards/mikey- its_beat_saber_i_swear.jpg", "Beat Saber 240p", 2, "Mikey"],
    ["c_id_0097", "cards/mikey- jello_shot.jpg", "Jello Shot", 2, "Mikey"],
    ["c_id_0098", "cards/mikey- leg.jpg", "Hairy Leg", 2, "Mikey"],
    ["c_id_0099", "cards/mikey- mid_shoulder.png", "The Shoulder", 2, "Mikey"],
    ["c_id_0100", "cards/mikey- philippines.jpg", "In The Philippines", 2, "Mikey"],
    ["c_id_0101", "cards/mikey- pho_night.jpg", "This Picture is Pho You", 2, "Mikey"],
    ["c_id_0102", "cards/mikey- phonelight.PNG", "Flashlight", 2, "Mikey"],
    ["c_id_0103", "cards/mikey- really.png", "Really?", 2, "Mikey"],
    ["c_id_0104", "cards/mikey- rec_room.png", "Billiards is not a Hobby. Billiards is my Life.", 2, "Mikey"],
    ["c_id_0105", "cards/mikey- soma.jpg", "Shokugeki no Soma", 2, "Mikey"],
    ["c_id_0106", "cards/mikey- thats_too_small.jpg", "Concerned Mikey", 2, "Mikey"],
    ["c_id_0107", "cards/mikey- widelens.jpg", "Widelens Mikey", 3, "Mikey"],
    ["c_id_0108", "cards/mikey- with_fam.jpg", "Mikey’s Fam", 2, "Mikey"],
    ["c_id_0109", "cards/mikey- zotcon_vr.png", "Baby’s First VR", 2, "Mikey"],
    ["c_id_0110", "cards/nayoung- pooped.jpg", "I’m Pooped", 3, "Nayoung"],
    ["c_id_0111", "cards/nina- aquarium.jpg", "Fish are Friends, not Food", 3, "Nina"],
    ["c_id_0112", "cards/nina- burger.jpg", "Borgar", 3, "Nina"],
    ["c_id_0113", "cards/nina- chopsticks.jpg", "You Caught me While I was Eating my BCD!", 3, "Nina"],
    ["c_id_0114", "cards/nina- gang_signs.jfif", "Gang Gang", 3, "Nina"],
    ["c_id_0115", "cards/nina- iced.png", "Iced", 3, "Nina"],
    ["c_id_0116", "cards/nina- pho_chef.jpg", "Pho Real?", 2, "Nina"],
    ["c_id_0117", "cards/nina- picnic.jpg", "Picnic", 2, "Nina"],
    ["c_id_0118", "cards/nina- red_cup_and_shrimp_toast.jfif", "Shrimp Toast?", 2, "Nina"],
    ["c_id_0119", "cards/nina- shabu.png", "That’s a Lotta Beef", 3, "Nina"],
    ["c_id_0120", "cards/nina- sharetea.jpg", "OMG this gotta get on the gram", 2, "Nina"],
    ["c_id_0121", "cards/nina- sus.jpg", "What’s on Your Window?", 3, "Nina"],
    ["c_id_0122", "cards/noah- selfie.png", "Check the Drip", 3, "Noah"],
    ["c_id_0123", "cards/noah- warning.jpg", "Warning Sign", 3, "Noah"],
    ["c_id_0124", "cards/patrick- content.jpg", "Patrick is Content", 2, "Patrick"],
    ["c_id_0125", "cards/patrick- ice_cream.jpg", "Patrick likes Ice Cream", 3, "Patrick"],
    ["c_id_0126", "cards/patrick- ladder.jpg", "Chutes and Ladders", 2, "Patrick"],
    ["c_id_0127", "cards/patrick- sweater.png", "Who Dat", 3, "Patrick"],
    ["c_id_0128", "cards/steven- 2008_version.JPG", "Steven circa 2008", 3, "Steven"],
    ["c_id_0129", "cards/steven- alcoholic.jpg", "Alcoholic", 3, "Steven"],
    ["c_id_0130", "cards/steven- arc_steven.jpg", "Gains", 3, "Steven"],
    ["c_id_0131", "cards/steven- back_profile.png", "On the Streets", 2, "Steven"],
    ["c_id_0132", "cards/steven- bcd.JPG", "Hi Guys, I’m here at BCD!", 3, "Steven"],
    ["c_id_0133", "cards/steven- black_mask.JPG", "Black Mask", 2, "Steven"],
    ["c_id_0134", "cards/steven- blinked.jpg", "mid blink", 2, "Steven"],
    ["c_id_0135", "cards/steven- blue_mask.png", "Blue Mask", 2, "Steven"],
    ["c_id_0136", "cards/steven- boba.PNG", "Slurp", 2, "Steven"],
    ["c_id_0137", "cards/steven- covid.png", "Covid is alive and well", 2, "Steven"],
    ["c_id_0138", "cards/steven- cowboy.JPG", "It’s High Noon", 2, "Steven"],
    ["c_id_0139", "cards/steven- dat_hair_tho.jpg", "Hair", 3, "Steven"],
    ["c_id_0140", "cards/steven- disco.png", "Rave Slave", 3, "Steven"],
    ["c_id_0141", "cards/steven- driving.JPG", "Fast and Furious", 2, "Steven"],
    ["c_id_0142", "cards/steven- eating.jpg", "MONCh", 2, "Steven"],
    ["c_id_0143", "cards/steven- egg_buying.JPG", "So many eggs", 2, "Steven"],
    ["c_id_0144", "cards/steven- eyeroll.jpg", "Eyeroll", 2, "Steven"],
    ["c_id_0145", "cards/steven- f_boi.jpg", "Sweater Weather", 2, "Steven"],
    ["c_id_0146", "cards/steven- golf_ball.jpg", "Golf Ball", 3, "Steven"],
    ["c_id_0147", "cards/steven- grill.png", "KBBQ @ home", 2, "Steven"],
    ["c_id_0148", "cards/steven- judging.png", "judging", 2, "Steven"],
    ["c_id_0149", "cards/steven- mouth_cover.jpg", "cough cough", 2, "Steven"],
    ["c_id_0150", "cards/steven- peace.png", "Peace Out - from Steven", 2, "Steven"],
    ["c_id_0151", "cards/steven- poke.jpg", "Poke ain’t bad", 2, "Steven"],
    ["c_id_0152", "cards/steven- ponyo_pal.jpg", "Ponyo Pal", 2, "Steven"],
    ["c_id_0153", "cards/steven- puppy_shirt.png", "Pug Life", 2, "Steven"],
    ["c_id_0154", "cards/steven- sad_sushi.jpg", "Sad Sushi", 3, "Steven"],
    ["c_id_0155", "cards/steven- scheming.png", "Scheming", 2, "Steven"],
    ["c_id_0156", "cards/steven- side_smile.jpg", "Side Smile", 2, "Steven"],
    ["c_id_0157", "cards/steven- sleepy.JPG", "Sleepy", 3, "Steven"],
    ["c_id_0158", "cards/steven- sunny.jpg", "Sunny Smile", 2, "Steven"],
    ["c_id_0159", "cards/steven- surprised_look.jpg", "Surprised Look", 2, "Steven"],
    ["c_id_0160", "cards/steven- thinking_about_not_being_blind.jpg",
     "Thinking About How Nice the Picture Would be if I Wasn’t BLIND", 2, "Steven"],
    ["c_id_0161", "cards/steven- tuxedo.jpg", "Fancy Steven", 3, "Steven"],
    ["c_id_0162", "cards/steven- vr_coat.JPG", "Link Start", 3, "Steven"],
    ["c_id_0163", "cards/steven- waiting.jpg", "Waiting for Anything to Happen", 2, "Steven"],
    ["c_id_0164", "cards/steven- widelens.jpg", "Widelens Steven", 3, "Steven"],
    ["c_id_0165", "cards/steven- zotcon_vr.png", "Man’s First VR", 2, "Steven"],
    ["c_id_0166", "cards/tim- indoor_bike.jpg", "Biker Gang", 2, "Tim"],
    ["c_id_0167", "cards/tim- lick.jpg", "Lickitung", 3, "Tim"],
    ["c_id_0168", "cards/tim- thumbs_up.jpg", "Timmy Thumby", 2, "Tim"],
    ["c_id_0169", "cards/tommy- churros_with_daniel.jpg", "Churros", 3, "Tommy"],
    ["c_id_0170", "cards/tommy- hair_dye_prep.png", "I’m Ready", 3, "Tommy"],
    ["c_id_0171", "cards/tommy- picnic.jpg", "There’s a Fly in My Cup", 2, "Tommy"],
    ["c_id_0172", "cards/wendy- blurb.JPG", "Blurb", 2, "Wendy"],
    ["c_id_0173", "cards/wendy- pancakes.jpg", "Stacks on Stacks", 3, "Wendy"],
    ["c_id_0174", "cards/wendy- presenter.JPG", "Hello and Welcome to my TEDTalk", 3, "Wendy"],
    ["c_id_0175", "cards/will- dorm_desk.jpg", "Oh, didn’t see you there", 3, "Will"],
    ["c_id_0176", "cards/will- flipped.jpg", "Fuck You Will", 3, "Will"],
    ["c_id_0177", "cards/will- is_that_will.jpg", "Who tf is That", 2, "Will"],
    ["c_id_0178", "cards/will- mid_blink.jpg", "haha are my eyes closed or open", 3, "Will"],
    ["c_id_0179", "cards/will- no_smile.jpg", "Serious Will", 2, "Will"],
    ["c_id_0180", "cards/will- packing.jpg", "Packing in More Ways than One", 2, "Will"],
    ["c_id_0181", "cards/will- rolling_in_grass.jpg", "Ouch this grass isn’t Soft", 2, "Will"],
    ["c_id_0182", "cards/will- sitting_but_its_birthday_time.jpg", "Happy Birthday Will", 2, "Will"],
    ["c_id_0183", "cards/will- sitting_on_grass.jpg", "Hey There", 3, "Will"],
    ["c_id_0184", "cards/will- sleepy_with_alyssa.jpg", "How Does he Sleep like That?", 3, "Will"],
    ["c_id_0185", "cards/will- tongue_out.jpg", "Look, I’m Yoshi", 3, "Will"],
    ["c_id_0186", "cards/will- vr.jpg", "GET DOWN", 2, "Will"],
    ["c_id_0187", "cards/will- yardhouse.jpg", "glug glug", 3, "Will"],
    ["c_id_0188", "cards/alex- plate.jpg", "Bonk", 4, "Alex"],
    ["c_id_0189", "cards/bo- amogus.png", "Among Us - Bo", 4, "Bo"],
    ["c_id_0190", "cards/bo- anti_cancer.png", "Anti Cancer Bo", 4, "Bo"],
    ["c_id_0191", "cards/bo- beach_day.JPG", "Beach Day Bo", 4, "Bo"],
    ["c_id_0192", "cards/bo- blimp.PNG", "Blimp Bo", 4, "Bo"],
    ["c_id_0193", "cards/bo- bo_with_mini_bos.png", "Check out my Mini Bos", 4, "Bo"],
    ["c_id_0194", "cards/bo- braided.jpg", "Braided Bo", 4, "Bo"],
    ["c_id_0195", "cards/bo- cast.PNG", "Samus Bramer", 4, "Bo"],
    ["c_id_0196", "cards/bo- cilantro.jpg", "Cilantro", 4, "Bo"],
    ["c_id_0197", "cards/bo- failed.jpg", "Failure Bo", 4, "Bo"],
    ["c_id_0198", "cards/bo- graph_happy.jpg", "Graph Happy", 4, "Bo"],
    ["c_id_0199", "cards/bo- graph_shocked.jpg", "Graph Shocked", 4, "Bo"],
    ["c_id_0200", "cards/bo- hand_cast.jpg", "Hi I’m Dying", 4, "Bo"],
    ["c_id_0201", "cards/bo- hey_horses.png", "Hey is for Horses", 4, "Bo"],
    ["c_id_0202", "cards/bo- in_snow.jpg", "Bo in the Snow", 4, "Bo"],
    ["c_id_0203", "cards/bo- labcoat.jpg", "Chemical Engineering", 4, "Bo"],
    ["c_id_0204", "cards/bo- minnie.jpg", "Cute Bo", 4, "Bo"],
    ["c_id_0205", "cards/bo- phonecase.png", "I couldn’t afford a phone so I just bought a case", 4, "Bo"],
    ["c_id_0206", "cards/bo- pocky.jpg", "Pocky", 4, "Bo"],
    ["c_id_0207", "cards/bo- shrimp.PNG", "Simp on a Shrimp", 4, "Bo"],
    ["c_id_0208", "cards/bo- snapchat_filter.jpg", "Snapchat Filter", 4, "Bo"],
    ["c_id_0209", "cards/bo- the_look.jpg", "The Look", 4, "Bo"],
    ["c_id_0210", "cards/bo- triple_threat.jpg", "Triple Threat", 4, "Bo"],
    ["c_id_0211", "cards/bo- when_the_photographer_says_cheese.png", "When the photographer says \"Cheese\"", 4, "Bo"],
    ["c_id_0212", "cards/combo- bo_tim_peace.jpg", "I’m Out", 4, "Combo"],
    ["c_id_0213", "cards/combo- boba_drinkers.JPG", "Boba Drinkers", 4, "Combo"],
    ["c_id_0214", "cards/combo- chubby_mikey_bo.JPG", "Chubby Bunny", 4, "Combo"],
    ["c_id_0215", "cards/combo- covid_gang.png", "Covid Gang", 4, "Combo"],
    ["c_id_0216", "cards/combo- grad_buddies.jpg", "Grad Buddies", 4, "Combo"],
    ["c_id_0217", "cards/combo- hair_dye_night.png", "Hair Dye Night", 4, "Combo"],
    ["c_id_0218", "cards/combo- insane_yell.jpg", "Insane YELLING", 4, "Combo"],
    ["c_id_0219", "cards/combo- janksmas_candid_1.png", "Janksmas 1", 4, "Combo"],
    ["c_id_0220", "cards/combo- janksmas_candid_2.png", "Janksmas 2", 4, "Combo"],
    ["c_id_0221", "cards/combo- janksmas.png", "Janksmas 3", 4, "Combo"],
    ["c_id_0222", "cards/combo- lighthouse.jpg", "Lighthouse Cafe", 4, "Combo"],
    ["c_id_0223", "cards/combo- midvale.jpg", "Midvale", 4, "Combo"],
    ["c_id_0224", "cards/combo- mikey_steven_cookies.PNG", "Look at Those Cookies", 4, "Combo"],
    ["c_id_0225", "cards/combo- people_in_line.JPG", "In a Line", 4, "Combo"],
    ["c_id_0226", "cards/combo- shoulder_massage.jpg", "Shoulder Massage", 4, "Combo"],
    ["c_id_0227", "cards/combo- snack_time.jpg", "Snack Time", 4, "Combo"],
    ["c_id_0228", "cards/combo- tote_bag.JPG", "Tote Bag", 4, "Combo"],
    ["c_id_0229", "cards/combo- totem_pole.jpg", "Totem Pole", 4, "Combo"],
    ["c_id_0230", "cards/combo- UCI_jerk_chicken.png", "Jerk Chicken", 4, "Combo"],
    ["c_id_0231", "cards/combo- UCI_patty_melt.png", "Patty Melt", 4, "Combo"],
    ["c_id_0232", "cards/combo- will_nina_gamers.png", "will sun and nina nina", 4, "Combo"],
    ["c_id_0233", "cards/combo- you_like_that_huh.jpg", "You Like that Huh?", 4, "Combo"],
    ["c_id_0234", "cards/elijah- amogus.png", "Among Us - Elijah", 4, "Elijah"],
    ["c_id_0235", "cards/elijah- glaring.jpg", "Glare", 4, "Elijah"],
    ["c_id_0236", "cards/emre- 5head.png", "5Head", 4, "Emre"],
    ["c_id_0237", "cards/flynn- amogus.png", "Among Us - Flynn", 4, "Flynn"],
    ["c_id_0238", "cards/flynn- dennys.jpg", "Dennys Late Night", 4, "Flynn"],
    ["c_id_0239", "cards/flynn- snoop_dog.JPG", "Snoop Dog???", 4, "Flynn"],
    ["c_id_0240", "cards/haroon- amogus.png", "Among Us - Haroon", 4, "Haroon"],
    ["c_id_0241", "cards/haroon- kbbq_pay_for_your_meal.jpg", "Big Boi", 4, "Haroon"],
    ["c_id_0242", "cards/jenn- amogus.png", "Among Us - Jenn", 4, "Jenn"],
    ["c_id_0243", "cards/jenn- gun_shopping.png", "Gun Shopping", 4, "Jenn"],
    ["c_id_0244", "cards/jenn- interested.jpg", "Interested Jenn", 4, "Jenn"],
    ["c_id_0245", "cards/jenn- jurassic_world.jpg", "AHHHHHHHHHHHHHHHHHH", 4, "Jenn"],
    ["c_id_0246", "cards/jenn- scammed.jpg", "Scammed", 4, "Jenn"],
    ["c_id_0247", "cards/john- full.jpg", "I’m Stuffed", 4, "John"],
    ["c_id_0248", "cards/john- punch.jpg", "One Punch Man", 4, "John"],
    ["c_id_0249", "cards/matt- 5_26.png", "5:26 AM", 4, "Matt"],
    ["c_id_0250", "cards/matt- im_not_gay.jpg", "I’m not Gay", 4, "Matt"],
    ["c_id_0251", "cards/matt- phonelight.PNG", "Phonelight", 4, "Matt"],
    ["c_id_0252", "cards/matt- sus_bathroom_activity.jpg", "Sus Imposter Vented", 4, "Matt"],
    ["c_id_0253", "cards/matt- UCI_zoturation_II.png", "Zoturation II", 4, "Matt"],
    ["c_id_0254", "cards/matt- yellow_converse.jpg", "Yellow Converse", 4, "Matt"],
    ["c_id_0255", "cards/mikey- amogus.png", "Among Us - Mikey", 4, "Mikey"],
    ["c_id_0256", "cards/mikey- arc_mikey.jpg", "Arc Mikey", 4, "Mikey"],
    ["c_id_0257", "cards/mikey- boba2.jpg", "Boba Mikey", 4, "Mikey"],
    ["c_id_0258", "cards/mikey- chef.PNG", "Chef Mikey", 4, "Mikey"],
    ["c_id_0259", "cards/mikey- drawing.png", "Doodle Mikey", 4, "Mikey"],
    ["c_id_0260", "cards/mikey- kazoo.jpg", "Kazoo Mikey", 4, "Mikey"],
    ["c_id_0261", "cards/mikey- library.jpg", "Library Mikey", 4, "Mikey"],
    ["c_id_0262", "cards/mikey- lightbulb.PNG", "How many Mikeys does it take to screw in a Lightbulb?", 4, "Mikey"],
    ["c_id_0263", "cards/mikey- omen.jpg", "Omen", 4, "Mikey"],
    ["c_id_0264", "cards/mikey- shopping_hard.jpg", "Hard Shopping", 4, "Mikey"],
    ["c_id_0265", "cards/mikey- smol_version.jpg", "Smol Mikey", 4, "Mikey"],
    ["c_id_0266", "cards/mikey- yellow_jacket.jpg", "Alpha Mikey", 4, "Mikey"],
    ["c_id_0267", "cards/nayoung- made_you_look.jpg", "Made You Look", 4, "Nayoung"],
    ["c_id_0268", "cards/nina- back_in_america.jpg", "Back in America", 4, "Nina"],
    ["c_id_0269", "cards/nina- chewing.jpg", "I’m boutta Vomit", 4, "Nina"],
    ["c_id_0270", "cards/nina- heart_glasses.jpg", "Heart Glasses", 4, "Nina"],
    ["c_id_0271", "cards/nina- shocked.jpg", "ohmygawsh", 4, "Nina"],
    ["c_id_0272", "cards/nina- stare.JPG", "Cursed Nina", 4, "Nina"],
    ["c_id_0273", "cards/nina- zoom.jpg", "Zoom Nina", 4, "Nina"],
    ["c_id_0274", "cards/noah- highlights.jpg", "Swaggy Noah", 4, "Noah"],
    ["c_id_0275", "cards/patrick- dead.jpg", "Dead Patrick 1", 4, "Patrick"],
    ["c_id_0276", "cards/patrick- sleepy.jpg", "Dead Patrick 2", 4, "Patrick"],
    ["c_id_0277", "cards/ponyo- attack.png", "she attack", 4, "Misc"],
    ["c_id_0278", "cards/radish.PNG", "Raddish", 4, "Misc"],
    ["c_id_0279", "cards/steven- amogus.png", "Among Us - Steven", 4, "Steven"],
    ["c_id_0280", "cards/steven- anime.png", "Anime Steven", 4, "Steven"],
    ["c_id_0281", "cards/steven- chef.jpg", "Chef Steven", 4, "Steven"],
    ["c_id_0282", "cards/steven- disaster_hair.png", "Disaster Hair", 4, "Steven"],
    ["c_id_0283", "cards/steven- edgy_tanktop.jpg", "Edgy Steven", 4, "Steven"],
    ["c_id_0284", "cards/steven- slurp.JPG", "Slurping Steven", 4, "Steven"],
    ["c_id_0285", "cards/steven- thug_lyfe.png", "Thug Lyfe", 4, "Steven"],
    ["c_id_0286", "cards/steven- UCI_zoturation.png", "Zoturation", 4, "Steven"],
    ["c_id_0287", "cards/susie- peace.jpg", "Peace Out - from Susie", 4, "Susie"],
    ["c_id_0288", "cards/tim- 3stock.jpg", "3 Stock", 4, "Tim"],
    ["c_id_0289", "cards/tim- big_smile.PNG", "Big Tim with Big Smile", 4, "Tim"],
    ["c_id_0290", "cards/tim- bike.jpg", "Biker Tim Comes in for a Repair", 4, "Tim"],
    ["c_id_0291", "cards/tim- neckless.png", "No Neck Tim", 4, "Tim"],
    ["c_id_0292", "cards/tommy- amogus.png", "Among Us - Tommy", 4, "Tommy"],
    ["c_id_0293", "cards/tommy- fridge.JPG", "Where tf is the Milk", 4, "Tommy"],
    ["c_id_0294", "cards/tommy- hi_im_tommy.jpg", "Hi I’m Tommy", 4, "Tommy"],
    ["c_id_0295", "cards/tommy- peace.png", "Peace Out - from Tommy", 4, "Tommy"],
    ["c_id_0296", "cards/tommy- vape_place.png", "Vape Tommy", 4, "Tommy"],
    ["c_id_0297", "cards/wendy- learn_produce.jpg", "Learn Produce", 4, "Wendy"],
    ["c_id_0298", "cards/will- amogus.png", "Among Us - Will", 4, "Will"],
    ["c_id_0299", "cards/will- boba.jpg", "This Some Good Boba", 4, "Will"],
    ["c_id_0300", "cards/will- body_pillows.jpg", "uwu Rem uwu", 4, "Will"],
    ["c_id_0301", "cards/will- cooking_like_bo.jpg", "Call me Bo Bramer", 4, "Will"],
    ["c_id_0302", "cards/will- dillmeme.png", "DillPickleDillPickleDillPickleDillPickleDillPickleDillPickle", 4,
     "Will"],
    ["c_id_0303", "cards/will- get_on_our_level.png", "Get on our Level", 4, "Will"],
    ["c_id_0304", "cards/will- happy_birthday_poster.png", "18th Birthday", 4, "Will"],
    ["c_id_0305", "cards/will- ice_cream_fail.jpg", "I Scream", 4, "Will"],
    ["c_id_0306", "cards/will- ice_cream.jpg", "Experienced Will", 4, "Will"],
    ["c_id_0307", "cards/will- its_hot.jpg", "Willgasm", 4, "Will"],
    ["c_id_0308", "cards/will- old_facebook_pfp.jpg", "Band Nerds 2", 4, "Will"],
    ["c_id_0309", "cards/will- panda_express.jpg", "Panda", 4, "Will"],
    ["c_id_0310", "cards/will- pigtails.jpg", "Pigtails", 4, "Will"],
    ["c_id_0311", "cards/will- sleepy.jpg", "Sleepy Will", 4, "Will"],
    ["c_id_0312", "cards/will- TMNT.jpg", "TMNT", 4, "Will"],
    ["c_id_0313", "cards/will- whistling.jpg", "Whistling Will", 4, "Will"],
    ["c_id_0314", "cards/will- witch.jpg", "Witch Will", 4, "Will"],
    ["c_id_0315", "cards/alex- sage.jpg", "I Am Not Just Your Healer", 5, "Alex"],
    ["c_id_0316", "cards/bo- hospital.jpeg", "The Hospital Told me to Lift My Spirits.. so I did.", 5, "Bo"],
    ["c_id_0317", "cards/bo- macarons.png", "Macaron PTSD", 5, "Bo"],
    ["c_id_0318", "cards/bo- po_breamer.png", "Po Breamer", 5, "Bo"],
    ["c_id_0319", "cards/chibi_bo.png", "Chibi Bo", 5, "Bo"],
    ["c_id_0320", "cards/chibi_flynn.png", "Chibi Flynn", 5, "Flynn"],
    ["c_id_0321", "cards/chibi_haroon.png", "Chibi Haroon", 5, "Haroon"],
    ["c_id_0322", "cards/chibi_jenn.png", "Chibi Jenn", 5, "Jenn"],
    ["c_id_0323", "cards/chibi_john.png", "Chibi John", 5, "John"],
    ["c_id_0324", "cards/chibi_mikey.png", "Chibi Mikey", 5, "Mikey"],
    ["c_id_0325", "cards/chibi_nina.png", "Chibi Nina", 5, "Nina"],
    ["c_id_0326", "cards/chibi_steven.png", "Chibi Steven", 5, "Steven"],
    ["c_id_0327", "cards/chibi_tommy.png", "Chibi Tommy", 5, "Tommy"],
    ["c_id_0328", "cards/chibi_will.png", "Chibi Will", 5, "Will"],
    ["c_id_0329", "cards/combo- bo_matt_blowing_smoke.jpg", "Matt and Bo share their experiences", 5, "Combo"],
    ["c_id_0330", "cards/flynn- lighthouse_drip.jpg", "Lighthouse Drip", 5, "Flynn"],
    ["c_id_0331", "cards/haroon- zot.JPG", "Zot.", 5, "Haroon"],
    ["c_id_0332", "cards/jenn- iced.PNG", "Jenn Iced", 5, "Jenn"],
    ["c_id_0333", "cards/jenn- meme.jpg", "Meme Jenn", 5, "Jenn"],
    ["c_id_0334", "cards/john- swimmer.jpg", "John Phelps", 5, "John"],
    ["c_id_0335", "cards/matt- carwash.png", "Carwash Matt", 5, "Matt"],
    ["c_id_0336", "cards/matt- nose_goes.jpg", "Nose Goes", 5, "Matt"],
    ["c_id_0337", "cards/matt- poptart.jpg", "Poptart \*in a British accent\*", 5, "Matt"],
    ["c_id_0338", "cards/matt- visor.jpg", "SAO Matt", 5, "Matt"],
    ["c_id_0339", "cards/mikey- cool.JPG", "Cool Mikey", 5, "Mikey"],
    ["c_id_0340", "cards/mikey- fortune.jpg", "You Light Up The Room With Your Smile", 5, "Mikey"],
    ["c_id_0341", "cards/mikey- girl.JPG", "Female Mikey", 5, "Mikey"],
    ["c_id_0342", "cards/mikey- gottem.PNG", "Gottem", 5, "Mikey"],
    ["c_id_0343", "cards/mikey- L.jpg", "L", 5, "Mikey"],
    ["c_id_0344", "cards/mikey- solar_eclipse.jpg", "When my Future is Too Bright", 5, "Mikey"],
    ["c_id_0345", "cards/mikey- yoshis.jpg", "YoshiYoshiYoshiYoshiYoshiYoshiYoshiYoshiYoshiYoshi", 5, "Mikey"],
    ["c_id_0346", "cards/nayoung- gun.jpg", "kms", 5, "Nayoung"],
    ["c_id_0347", "cards/nina- flossing.png", "Nina Flossing", 5, "Nina"],
    ["c_id_0348", "cards/nina- wine_chug.png", "Alcoholic Nina", 5, "Nina"],
    ["c_id_0349", "cards/patrick- schoolgirl.png", "Female Shiffty", 5, "Patrick"],
    ["c_id_0350", "cards/patrick- sunglasses_pat.jpg", "Patrol Patrick", 5, "Patrick"],
    ["c_id_0351", "cards/steven- f_u.png", "f u", 5, "Steven"],
    ["c_id_0352", "cards/steven- f_word.PNG", "Steven Slander", 5, "Steven"],
    ["c_id_0353", "cards/steven- game_mode.jpg", "Final Form Steven", 5, "Steven"],
    ["c_id_0354", "cards/steven- gay.PNG", "Gay Steven", 5, "Steven"],
    ["c_id_0355", "cards/steven- hospital.jpg", "Hospitalized Steven", 5, "Steven"],
    ["c_id_0356", "cards/steven- sup_faggies.JPG", "sup", 5, "Steven"],
    ["c_id_0357", "cards/tommy- hello_kitty_hat.jpg", "Hello Kitty Kawaii Tommy", 5, "Tommy"],
    ["c_id_0358", "cards/will- beta_bitch.png", "Beta Bitch", 5, "Will"],
    ["c_id_0359", "cards/will- thicc.jpg", "Thicc Will", 5, "Will"],
    ["c_id_0360", "cards/bo- fingernails.jpg", "Yup that’s me", 2, "Bo"],
    ["c_id_0361", "cards/bo- gas_mask.jpg", "Gas Mask Bo", 3, "Bo"],
    ["c_id_0362", "cards/bo- joe_bo.jpeg", "Joe Bo", 3, "Bo"],
    ["c_id_0363", "cards/bo- labcoat_two.jpg", "Labcoat Bo", 2, "Bo"],
    ["c_id_0364", "cards/combo- 3girls.png", "Girls on the Shore", 3, "Combo"],
    ["c_id_0365", "cards/combo- 2019.JPG", "2019", 3, "Combo"],
    ["c_id_0366", "cards/combo- chillin_like_villians.jpeg", "Chillin’ Like Villians", 3, "Combo"],
    ["c_id_0367", "cards/combo- flynn_bitmoji.JPG", "Flynn’s Bitmoji and Friends", 3, "Combo"],
    ["c_id_0368", "cards/combo- formal_hipster_besties.JPG", "Hipsters", 3, "Combo"],
    ["c_id_0369", "cards/combo- grad_sheesh.jpeg", "Sheesh Zot", 3, "Combo"],
    ["c_id_0370", "cards/combo- grouped_up.jpeg", "Grouped Up", 2, "Combo"],
    ["c_id_0371", "cards/combo- hackathon.jpeg", "Hackthon Picture", 2, "Combo"],
    ["c_id_0372", "cards/combo- halloween.png", "Halloween Hype", 2, "Combo"],
    ["c_id_0373", "cards/combo- janksgiving_feast.jpeg", "Janksgiving Feast", 3, "Combo"],
    ["c_id_0374", "cards/combo- matt_nina_joes.jpg", "3-pronged Italian Ice", 3, "Combo"],
    ["c_id_0375", "cards/combo- mikey_sushi_wow.jpeg", "WOW Sushi!", 3, "Combo"],
    ["c_id_0376", "cards/combo- Milk_T.JPG", "Milk+T", 3, "Combo"],
    ["c_id_0377", "cards/combo- moorpark_grad_buddies.JPG", "Moorpark Graduation Pals", 3, "Combo"],
    ["c_id_0378", "cards/combo- moorpark_peace.jpeg", "Peace Out - from Moorparkians", 3, "Combo"],
    ["c_id_0379", "cards/combo- oh_look_a_loser.jpeg", "Oh Look, it’s a Loser!", 3, "Combo"],
    ["c_id_0380", "cards/combo- paint.png", "Made With Love", 2, "Combo"],
    ["c_id_0381", "cards/combo- peace_from_camino.jpeg", "Having Fun", 3, "Combo"],
    ["c_id_0382", "cards/combo- poster_hanging.jpeg", "Poster Hanging", 3, "Combo"],
    ["c_id_0383", "cards/combo- prepare_for_trouble.JPG", "Prepare for Trouble", 2, "Combo"],
    ["c_id_0384", "cards/combo- sad_in_the_dark.JPG", "Sad in the Dark", 3, "Combo"],
    ["c_id_0385", "cards/combo- shame.jpeg", "Shame Squat", 3, "Combo"],
    ["c_id_0386", "cards/combo- shocked.JPG", "Shocking", 2, "Combo"],
    ["c_id_0387", "cards/combo- steven_and_steven.jpg", "Steven and Steven", 3, "Combo"],
    ["c_id_0388", "cards/combo- sup_my_homies.jpeg", "Wassup my Homies", 3, "Combo"],
    ["c_id_0389", "cards/combo- technostevefriends.jpeg", "Techno Steve & Friends", 2, "Combo"],
    ["c_id_0390", "cards/combo- tommymatt.jpeg", "Tommy and Matt hate COVID", 2, "Combo"],
    ["c_id_0391", "cards/combo- two_little_piggies.JPG", "Two Little Piggies", 3, "Combo"],
    ["c_id_0392", "cards/combo- universal_line.jpeg", "Universal Family", 3, "Combo"],
    ["c_id_0393", "cards/combo- will_tommy_ghosts.JPG", "Boo!", 2, "Combo"],
    ["c_id_0394", "cards/elijah- american_eagle.JPG", "Elijah!", 3, "Elijah"],
    ["c_id_0395", "cards/haroon- raccoon_haroon.jpeg", "Raccoon Haroon", 3, "Haroon"],
    ["c_id_0396", "cards/haroon- tuxedo.jpg", "Tuxedo Haroon", 3, "Haroon"],
    ["c_id_0397", "cards/matt- you_better_love_frank_ocean.PNG", "You’d better love Frank Ocean", 3, "Matt"],
    ["c_id_0398", "cards/nina- interested.jpg", "Interesting Post", 2, "Nina"],
    ["c_id_0399", "cards/noah- rosie_riveter.png", "Noah Riveter", 3, "Noah"],
    ["c_id_0400", "cards/steven- backwards_hat.jpeg", "Backwards Hat Steven", 2, "Steven"],
    ["c_id_0401", "cards/steven- griddle_chef.jpeg", "Griddle Chef Steven", 2, "Steven"],
    ["c_id_0402", "cards/steven- im_a_ninja.jpeg", "I’m a ninja", 3, "Steven"],
    ["c_id_0403", "cards/steven- ringring.jpeg", "Ring Ring", 2, "Steven"],
    ["c_id_0404", "cards/steven- roses_are_red.jpeg", "Roses are Red", 3, "Steven"],
    ["c_id_0405", "cards/steven- scared.jpeg", "Spooked", 2, "Steven"],
    ["c_id_0406", "cards/steven- spam_musubi.jpeg", "Spam Musubi Making", 2, "Steven"],
    ["c_id_0407", "cards/steven- techno.jpeg", "Techno Steve", 2, "Steven"],
    ["c_id_0408", "cards/bo- balloon_swords.jpg", "Genji Bo", 4, "Bo"],
    ["c_id_0409", "cards/combo- are_you_ok.png", "Nina, are you okay?", 4, "Combo"],
    ["c_id_0410", "cards/combo- disgusted.png", "Disgusted with this Shit", 4, "Combo"],
    ["c_id_0411", "cards/combo- dog_ritual.jpeg", "Dog Ritual", 4, "Combo"],
    ["c_id_0412", "cards/combo- get_away_from_me.png", "Get Away From Me", 4, "Combo"],
    ["c_id_0413", "cards/combo- i_dont_wanna_get_lost.png", "I Don’t Wanna Get Lost", 4, "Combo"],
    ["c_id_0414", "cards/combo- laughing_hurts.JPG", "Laughing Hurts", 4, "Combo"],
    ["c_id_0415", "cards/combo- mikey_flynn_nerf_buddies.jpg", "Double O Seven", 4, "Combo"],
    ["c_id_0416", "cards/combo- spikeball.jpeg", "Spikeball", 4, "Combo"],
    ["c_id_0417", "cards/elijah- elijah_stand.png", "Elijah Stand", 4, "Elijah"],
    ["c_id_0418", "cards/haroon- feasting_kbbq.jpeg", "KBBQ Feasting", 4, "Haroon"],
    ["c_id_0419", "cards/haroon- makeup.JPG", "Makeup Haroon", 4, "Haroon"],
    ["c_id_0420", "cards/matt- female_matt.png", "Female Matt", 4, "Matt"],
    ["c_id_0421", "cards/matt- good_morning.jpg", "Good Morning", 4, "Matt"],
    ["c_id_0422", "cards/nayoung- clout_game_strong.jpg", "Clout", 4, "Nayoung"],
    ["c_id_0423", "cards/nina- lunch_break.png", "Lunch Break", 4, "Nina"],
    ["c_id_0424", "cards/steven- cars_ride.JPG", "Vroom", 4, "Steven"],
    ["c_id_0425", "cards/steven- female_steven.png", "Stephanie", 4, "Steven"],
    ["c_id_0426", "cards/steven- pool_shitting.jpg", "Shitting in the Pool", 4, "Steven"],
    ["c_id_0427", "cards/tommy- pumpkin_stack.jpg", "Pumpkin Stack", 4, "Tommy"],
    ["c_id_0428", "cards/will- furry_club.JPG", "Furry Club Will", 4, "Will"],
    ["c_id_0429", "cards/will- tuba.jpg", "Tuba Will", 4, "Will"],
    ["c_id_0430", "cards/haroon- big_dick_haroon.jpeg", "Big Dick Haroon", 5, "Haroon"],
    ["c_id_0431", "cards/john- sandy_ass.jpeg", "Sandy Ass John", 5, "John"],
    ["c_id_0432", "cards/nina- kayak.jpg", "Kayaking Nina", 5, "Nina"],
    ["c_id_0433", "cards/ashwin- failed.JPG", "Failure Ashwin", 3, "Ashwin"],
    ["c_id_0434", "cards/combo- boo_i_scared_you.JPG", "Steven Surprise", 2, "Combo"],
    ["c_id_0435", "cards/combo- coaster.JPG", "Coaster", 3, "Combo"],
    ["c_id_0436", "cards/combo- dland.JPG", "D Land", 2, "Combo"],
    ["c_id_0437", "cards/combo- dland2.JPG", "D Land 2", 2, "Combo"],
    ["c_id_0438", "cards/combo- double_v_chin.jpeg", "Double Check Chin", 2, "Combo"],
    ["c_id_0439", "cards/combo- fancy_zotters.JPG", "Fancy Zotters", 3, "Combo"],
    ["c_id_0440", "cards/combo- friendship.JPG", "Friendship", 2, "Combo"],
    ["c_id_0441", "cards/combo- friendzone.JPG", "Friendzone", 3, "Combo"],
    ["c_id_0442", "cards/combo- frozen_lemonade.JPG", "Frozen Lemonade", 2, "Combo"],
    ["c_id_0443", "cards/combo- goin_up.jpeg", "Goin’ Up?", 3, "Combo"],
    ["c_id_0444", "cards/combo- grad_pose_fun.JPG", "Grad Pose Fun", 3, "Combo"],
    ["c_id_0445", "cards/combo- haha_look_lame.JPG", "haha this guy sucks", 3, "Combo"],
    ["c_id_0446", "cards/combo- in_line.PNG", "Hello pls pick up", 4, "Combo"],
    ["c_id_0447", "cards/combo- judging_nay.JPG", "Judging Nayoung", 2, "Combo"],
    ["c_id_0448", "cards/combo- kawaii_filter.JPG", "Kawaii Filter", 3, "Combo"],
    ["c_id_0449", "cards/combo- korean_heart.JPG", "Korean Heart", 2, "Combo"],
    ["c_id_0450", "cards/combo- lookoverthere.jpeg", "Look Over There", 2, "Combo"],
    ["c_id_0451", "cards/combo- mattandnayoung.JPG", "Matt and Nayoung", 2, "Combo"],
    ["c_id_0452", "cards/combo- mattandnayoung2.jpeg", "Matt and Nayoung 2", 2, "Combo"],
    ["c_id_0453", "cards/combo- mirror_shot.jpeg", "Mirror Shot", 3, "Combo"],
    ["c_id_0454", "cards/combo- on_the_wheel.jpeg", "On the Wheel", 2, "Combo"],
    ["c_id_0455", "cards/combo- peacepeace.JPG", "Peace Peace", 2, "Combo"],
    ["c_id_0456", "cards/combo- picture_of_picture.JPG", "Picture of a Picture", 2, "Combo"],
    ["c_id_0457", "cards/combo- purikura1.JPG", "Purikura 1", 3, "Combo"],
    ["c_id_0458", "cards/combo- purikura2.JPG", "Purikura 2", 3, "Combo"],
    ["c_id_0459", "cards/combo- purikura3.JPG", "Purikura 3", 3, "Combo"],
    ["c_id_0460", "cards/combo- purikura4.JPG", "Purikura 4", 3, "Combo"],
    ["c_id_0461", "cards/combo- purikura5.JPG", "Purikura 5", 3, "Combo"],
    ["c_id_0462", "cards/combo- reflections.JPG", "Reflections", 2, "Combo"],
    ["c_id_0463", "cards/combo- rush.jpeg", "Rush", 2, "Combo"],
    ["c_id_0464", "cards/combo- screaming_matt.jpeg", "Screaming Matt", 3, "Combo"],
    ["c_id_0465", "cards/combo- selfie_naymatt.jpeg", "NayMatt", 2, "Combo"],
    ["c_id_0466", "cards/combo- sitting_chilling.JPG", "Sitting and Chilling", 2, "Combo"],
    ["c_id_0467", "cards/combo- splash.JPG", "Splash", 3, "Combo"],
    ["c_id_0468", "cards/combo- staircase_friends.JPG", "Staircase Friends", 2, "Combo"],
    ["c_id_0469", "cards/combo- swaggy_pose.JPG", "Swaggy Pose", 2, "Combo"],
    ["c_id_0470", "cards/combo- target_time.JPG", "Target Time", 2, "Combo"],
    ["c_id_0471", "cards/combo- visitors.JPG", "Visitors", 2, "Combo"],
    ["c_id_0472", "cards/combo- waiting_sushi.jpeg", "Waiting for Sushi", 2, "Combo"],
    ["c_id_0473", "cards/combo- wowow.PNG", "Nayoung Hyped", 2, "Combo"],
    ["c_id_0474", "cards/elijah- hold_my_zot2.JPG", "Hold My Zot - Ellijah", 3, "Elijah"],
    ["c_id_0475", "cards/haroon- audacity.jpeg", "Audacity", 2, "Haroon"],
    ["c_id_0476", "cards/haroon- grad_ready.jpeg", "Grad Ready Haroon", 2, "Haroon"],
    ["c_id_0477", "cards/haroon- irides.jpeg", "iridescence Haroon", 2, "Haroon"],
    ["c_id_0478", "cards/haroon- youre_joking.JPG", "Shook Haroon", 2, "Haroon"],
    ["c_id_0479", "cards/matt- angel.JPG", "Angel Matt", 2, "Matt"],
    ["c_id_0480", "cards/matt- comfy.jpeg", "Comfy Matt", 2, "Matt"],
    ["c_id_0481", "cards/matt- concerned.JPG", "Concerned Matt", 2, "Matt"],
    ["c_id_0482", "cards/matt- garden.JPG", "Garden Matt", 2, "Matt"],
    ["c_id_0483", "cards/matt- genji.JPG", "Genji Matt", 3, "Matt"],
    ["c_id_0484", "cards/matt- happy_new_year_hat.jpeg", "Happy New Year Hat", 3, "Matt"],
    ["c_id_0485", "cards/matt- inventor.JPG", "Inventor Matt", 3, "Matt"],
    ["c_id_0486", "cards/matt- obama.jpeg", "Obama and VP Matt", 3, "Matt"],
    ["c_id_0487", "cards/matt- ramen_matt.JPG", "Ramen Matt", 2, "Matt"],
    ["c_id_0488", "cards/matt- too_sunny.jpeg", "Too Sunny", 2, "Combo"],
    ["c_id_0489", "cards/matt- upset.JPG", "Upset Matt", 3, "Matt"],
    ["c_id_0490", "cards/misc- bonnieandmary.jpeg", "Bonnie and Mary", 3, "Misc"],
    ["c_id_0491", "cards/misc- vrchat.jpeg", "VRChat", 3, "Misc"],
    ["c_id_0492", "cards/nayoung- cursed.PNG", "Cursed Nayoung", 4, "Nayoung"],
    ["c_id_0493", "cards/nayoung- dont_look.jpeg", "Dont Look", 3, "Nayoung"],
    ["c_id_0494", "cards/nayoung- eyes.jpeg", "Glaring Nayoung", 3, "Nayoung"],
    ["c_id_0495", "cards/nayoung- flipping.jpg", "Flipping Nayoung", 2, "Nayoung"],
    ["c_id_0496", "cards/nayoung- hold_my_zot.JPG", "Hold My Zot - Nayoung", 4, "Nayoung"],
    ["c_id_0497", "cards/nayoung- jungkook_shook.JPG", "Nayoung JungShook", 4, "Nayoung"],
    ["c_id_0498", "cards/nayoung- nooo.jpeg", "Noooooooooooooo", 4, "Nayoung"],
    ["c_id_0499", "cards/Nayoung- phone_case.jpeg", "Hi Hello", 2, "Nayoung"],
    ["c_id_0500", "cards/nayoung- up_the_slide.jpeg", "Climbing Up the Slide", 3, "Nayoung"],
    ["c_id_0501", "cards/nayoung- zot.JPG", "Zotting Nayoung", 3, "Nayoung"],
    ["c_id_0502", "cards/steven- sad_with_towel.JPG", "Sad Steven with Towel", 4, "Steven"],
    ["c_id_0503", "cards/steven- squat.jpeg", "Squatting Steven", 2, "Steven"],
    ["c_id_0504", "cards/steven- swingset.JPG", "Swingset Steven", 2, "Steven"],
    ["c_id_0505", "cards/flynn- split_conversion_gif.gif", "Flynn Bowling Popoff", 6, "Flynn"],
    ["c_id_0506", "cards/haroon- jumpscare_gif.gif", "Haroon Jumpscare", 6, "Haroon"],
    ["c_id_0507", "cards/jenn- iced_gif.gif", "Iced Up", 6, "Jenn"],
    ["c_id_0508", "cards/kiki_u_good_bro_gif.gif", "Kiki", 6, "Misc"],
    ["c_id_0509", "cards/matt- vr_pong_gif.gif", "Matt Metaverse", 6, "Matt"],
    ["c_id_0510", "cards/matt- fish_gif.gif", "Matt = Fish", 6, "Matt"],
    ["c_id_0511", "cards/mikey- arc_mikey_gif.gif", "Arc Mikey Animated", 6, "Mikey"],
    ["c_id_0512", "cards/mikey- basketball_mikey_gif.gif", "Basketball Mikey", 6, "Mikey"],
    ["c_id_0513", "cards/mikey- bowling_gif.gif", "Bowling Mikey", 6, "Mikey"],
    ["c_id_0514", "cards/mikey- vr_gangnam_gif.gif", "Gangnam Style Mikey", 6, "Mikey"],
    ["c_id_0515", "cards/nina- flossing_gif.gif", "Nina Flossing Animated", 6, "Nina"],
    ["c_id_0516", "cards/steven- am_i_oh_hello.gif", "Am I, oh hello there", 6, "Steven"],
    ["c_id_0517", "cards/will- beat_saber_gif.gif", "Will Beat Saber", 6, "Will"],
    ["c_id_0518", "cards/combo- zot_gif.gif", "Zot Squad", 6, "Combo"],
    ["c_id_0519", "cards/combo- hae_jang_chon_gif.gif", "HJC Shoulders", 6, "Combo"],
    ["c_id_0520", "cards/steven- sugar_gif.gif", "Inhaling Sugar", 6, "Combo"],
    ["c_id_0521", "cards/bo- cane_gif.gif", "Bo and Cane", 6, "Bo"],
    ["c_id_0522", "cards/combo- john_slaps_gif.gif", "John Slaps Flynn", 6, "Combo"],
    ["c_id_0523", "cards/flynn- vr_chat_sus_gif.gif", "Spicy VRChat", 6, "Flynn"],
    ["c_id_0524", "cards/combo- star_bbq_gif.gif", "KBBQ Hangout", 6, "Combo"],
    ["c_id_0525", "cards/nayoung- korean_snack_gif.gif", "Korean Snack", 6, "Nayoung"],
    ["c_id_0526", "cards/matt- silent_disco_gif.gif", "Silent Disco", 6, "Matt"],
    ["c_id_0527", "cards/haroon- hot_shot_gif.gif", "Buckets", 6, "Haroon"],
]

card_deck = {}
name_deck = {}
rating_decks = {2: {}, 3: {}, 4: {}, 5: {}, 6: {}}

for c in cards:
    card_deck[c[0]] = Card(c[0], c[1], c[2], c[3], c[4])
    name_deck[c[2].lower()] = Card(c[0], c[1], c[2], c[3], c[4])
    name_deck[c[2].lower().replace('’', "'")] = Card(c[0], c[1], c[2], c[3], c[4])
    rating_decks[c[3]][c[0]] = Card(c[0], c[1], c[2], c[3], c[4])
