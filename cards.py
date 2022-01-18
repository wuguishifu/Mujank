import discord
import dataloader


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

        color = discord.Colour.greyple()
        if self.rating == 3:
            color = discord.Colour.red()
        elif self.rating == 4:
            color = discord.Colour.yellow()
        elif self.rating == 5:
            color = discord.Colour.green()
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

        file = discord.File(self.image_url, filename='image.png')
        embed = discord.Embed(
            title=f'{self.title}',
            description=f'{stars}\n{self.tags}',
            colour=discord.Colour.red(),
        )

        num_owned = dataloader.get_num(author.id, self.id)
        embed.set_footer(text=f'{num_owned} owned by {author.name}')
        embed.set_image(url='attachment://image.png')
        return embed, file


def to_owned_embed(user: discord.user.User, owned_list: [], page: int):
    description = ''
    index_start = 10 * page
    index_last = 10 * (page + 1)
    for i in owned_list[index_start:index_last]:
        num = i.val()
        card = card_deck.get(i.key()).title
        description += f'{num}x **{card}**\n'
    embed = discord.Embed(
        title=f"{user.name}'s deck",
        description=description,
        colour=discord.Colour.red()
    )
    displayed_id = dataloader.get_displayed_card(user.id)
    if displayed_id == 'c_id_-1':
        file = discord.File('jank-logo.png', 'image.png')
    else:
        file = discord.File(card_deck.get(displayed_id).image_url, 'image.png')
    embed.set_thumbnail(url='attachment://image.png')
    return embed, file


cards = [
    ['c_id_0000', "cards/alex- _3.jpg", "Much Love", 3, "Alex"],
    ['c_id_0001', "cards/alex- puppy.jpg", "Wassup Dog", 3, "Alex"],
    ['c_id_0002', "cards/anteatery_cup_tower.png", "The Legendary Tower", 3, "Misc."],
    ['c_id_0003', "cards/bo- ac_A.jpg", "A", 3, "Bo"],
    ['c_id_0004', "cards/bo- airpods.jpg", "Hey, Look at my Airpods!", 3, "Bo"],
    ['c_id_0005', "cards/bo- beard.jpg", "Hey, Look at my Beard!", 3, "Bo"],
    ['c_id_0006', "cards/bo- bomomo.png", "BOmomo", 3, "Bo"],
    ['c_id_0007', "cards/bo- cream.jpg", "Oops, cream!", 3, "Bo"],
    ['c_id_0008', "cards/bo- dead_inside_outside.PNG", "he's dead on the inside and the outside", 3, "Bo"],
    ['c_id_0009', "cards/bo- death_stare.png", "Death Stare", 3, "Bo"],
    ['c_id_0010', "cards/bo- eggplant.jpg", "Hey, Look at my Eggplant!", 3, "Bo"],
    ['c_id_0011', "cards/bo- full.jpg", "Oh man, I'm optimally full", 3, "Bo"],
    ['c_id_0012', "cards/bo- glasses.jpg", "Hey, Look at my Glasses!", 3, "Bo"],
    ['c_id_0013', "cards/bo- golfer_tshirt.jpg", "I'm a Golfer", 3, "Bo"],
    ['c_id_0014', "cards/bo- high_tide.jpg", "High Tide", 3, "Bo"],
    ['c_id_0015', "cards/bo- hs_band.jpg", "Band Nerd Bo", 3, "Bo"],
    ['c_id_0016', "cards/bo- late_night_peace.jpg", "Late Night Peace Out", 3, "Bo"],
    ['c_id_0017', "cards/bo- mask.jpg", "Don't Forget a Mask", 3, "Bo"],
    ['c_id_0018', "cards/bo- no_sleep.jpg", "All these beds but you still won't sleep with me", 3, "Bo"],
    ['c_id_0019', "cards/bo- on_the_phone.jpg", "Oh no, I Lost a Follower", 3, "Bo"],
    ['c_id_0020', "cards/bo- oreos_bos_cookies.jpg", "Oreos > Bo's Cookies", 3, "Bo"],
    ['c_id_0021', "cards/bo- peace_out.jpg", "Peace Out - from Bo", 3, "Bo"],
    ['c_id_0022', "cards/bo- red_cup.jpg", "Dad Bo", 3, "Bo"],
    ['c_id_0023', "cards/bo_smol_version.jpg", "smol Bo", 3, "Bo"],
    ['c_id_0024', "cards/bo- takoyaki_chef.JPG", "Hey, I'm a Takoyaki Chef!", 3, "Bo"],
    ['c_id_0025', "cards/bo- towel_wrap.jpg", "Don't Look at me I'm Shy", 3, "Bo"],
    ['c_id_0026', "cards/bo- uci_commit.jpg", "Commitment", 3, "Bo"],
    ['c_id_0027', "cards/bo- zoom.png", "Bo Douglas Bramer", 3, "Bo"],
    ['c_id_0028', "cards/combo- ac_bed.jpg", "Sleeping with the Homies", 3, "Combo"],
    ['c_id_0029', "cards/combo- ac_fam.JPG", "Animal Crossing Party", 3, "Combo"],
    ['c_id_0030', "cards/combo- ac_fish.JPG", "Fishing with the Homies", 3, "Combo"],
    ['c_id_0031', "cards/combo- among_us_steven_bo.jpg", "Sus Squad", 3, "Combo"],
    ['c_id_0032', "cards/combo- awkward_smile.png", "haha say cheese", 3, "Combo"],
    ['c_id_0033', "cards/combo- bo_kyran_wing_chun.jpg", "wing chun", 3, "Combo"],
    ['c_id_0034', "cards/combo- bo_nina_spoon.png", "nina spoon", 3, "Combo"],
    ['c_id_0035', "cards/combo- bo_steven_hand_update.PNG", "cookin up in the lab", 3, "Combo"],
    ['c_id_0036', "cards/combo- bowling_in_hell.jpg", "Bowling Time!", 3, "Combo"],
    ['c_id_0037', "cards/combo- business_casual_pho.jpg", "Back to Business", 3, "Combo"],
    ['c_id_0038', "cards/combo- cdeeznuts.png", "CDeezNuts", 3, "Combo"],
    ['c_id_0039', "cards/combo- fire_glasses.jpg", "We Fire Out Here", 3, "Combo"],
    ['c_id_0040', "cards/combo- flynn_steven_snapchat.JPG", "It's Just Me and My Shorty", 3, "Combo"],
    ['c_id_0041', "cards/combo- ft_matt_bo_steven_mikey.PNG", "FaceTime Time", 3, "Combo"],
    ['c_id_0042', "cards/combo- good_day.png", "Good Day", 3, "Combo"],
    ['c_id_0043', "cards/combo- idiot.jpg", "idiot", 3, "Combo"],
    ['c_id_0044', "cards/combo- steven_jenn_koifish.jpg", "We at The Pond", 3, "Combo"],
    ['c_id_0045', "cards/combo- kbbq_peace.png", "KBBQ peace", 3, "Combo"],
    ['c_id_0046', "cards/combo- matt_tommy_thumbs_up.jpg", "Matt & Tommy Covid Crossover", 3, "Combo"],
    ['c_id_0047', "cards/combo- mikey_marth_steven_min_min.png", "Mikey & Steven as Smash Characters", 3, "Combo"],
    ['c_id_0048', "cards/combo- mikey_noah_drip_check.jpg", "Mikey & Noah Drip", 3, "Combo"],
    ['c_id_0049', "cards/combo- mikey_porcupine_steven_dog.png", "Mikey & Steven as Furries", 3, "Combo"],
    ['c_id_0050', "cards/combo- nina_palming_tommy.jpg", "Nina palming Tommy", 3, "Combo"],
    ['c_id_0051', "cards/combo- patrick_alyssa_jenn_steven_poke.JPG", "Poke Time", 3, "Combo"],
    ['c_id_0052', "cards/combo- petr_steven_jenn_will.png", "Petr Weather", 3, "Combo"],
    ['c_id_0053', "cards/combo- piggyback_bo_will.jpg", "Piggyback Attack", 3, "Combo"],
    ['c_id_0054', "cards/combo- rec_room_bo_steven_mikey.jpg", "Rec Room", 3, "Combo"],
    ['c_id_0055', "cards/combo- red_bull.jpg", "Red Bull Gives You Wings", 3, "Combo"],
    ['c_id_0056', "cards/combo- shopping.png", "Shoplifters", 3, "Combo"],
    ['c_id_0057', "cards/combo- steven_furry_with_haroon.jfif", "Beauty and the Beast", 3, "Combo"],
    ['c_id_0058', "cards/combo- target.jpg", "Caught in 4K", 3, "Combo"],
    ['c_id_0059', "cards/combo- uci_selfie.jpg", "Fountain Selfie", 3, "Combo"],
    ['c_id_0060', "cards/combo- why_hello_there.png", "Why Hello There", 3, "Combo"],
    ['c_id_0061', "cards/combo- will_bo_fingerguns.jpg", "Finger Guns pewpew", 3, "Combo"],
    ['c_id_0062', "cards/combo- will_bo_hs_band.jpg", "Band Nerds", 3, "Combo"],
    ['c_id_0063', "cards/combo- will_nina_sleeping.jpg", "Knocked Out", 3, "Combo"],
    ['c_id_0064', "cards/combo- will_patrick_plushie.jpg", "Plushies", 3, "Combo"],
    ['c_id_0065', "cards/combo- will_tommy_pumpkin_patch.jpg", "We're inside a pumpkin lol", 3, "Combo"],
    ['c_id_0066', "cards/flynn- birthday_time.jpg", "Happy Birthday Flynn", 3, "Flynn"],
    ['c_id_0067', "cards/flynn- blurry.jpg", "Blurry Flynn", 3, "Flynn"],
    ['c_id_0068', "cards/flynn- crossbody.JPG", "Sit Back and Smile", 3, "Flynn"],
    ['c_id_0069', "cards/flynn- drip_check.jpg", "Drip Check", 3, "Flynn"],
    ['c_id_0070', "cards/flynn- side_profile.jpg", "Side Profile", 3, "Flynn"],
    ['c_id_0071', "cards/flynn- sleep.jpg", "Schleep", 3, "Flynn"],
    ['c_id_0072', "cards/flynn- sushi.jpg", "Damn, this Sushi Bussin'", 3, "Flynn"],
    ['c_id_0073', "cards/flynn- waiting.jpg", "Waiting for the T'sane Cashier", 3, "Flynn"],
    ['c_id_0074', "cards/haroon- hello.jpg", "Hello?", 3, "Haroon"],
    ['c_id_0075', "cards/haroon- jumpscare.jpg", "Jumpscare Haroon", 3, "Haroon"],
    ['c_id_0076', "cards/haroon- shy_guy.jpg", "Shy Guy with a Shy Guy", 3, "Haroon"],
    ['c_id_0077', "cards/jenn- facetime.png", "Pixelated Jenn", 3, "Jenn"],
    ['c_id_0078', "cards/jenn- hello.jpg", "Hello my Friends", 3, "Jenn"],
    ['c_id_0079', "cards/jenn- peace.jpg", "Peace Out - from Jenn", 3, "Jenn"],
    ['c_id_0080', "cards/matt- asmr.jpg", "ASMR", 3, "Matt"],
    ['c_id_0081', "cards/matt- dbz.png", "DBZ Matt", 3, "Matt"],
    ['c_id_0082', "cards/matt- petr_run.jpg", "On the Run", 3, "Matt"],
    ['c_id_0083', "cards/matt- plushie.jpg", "Seal's Best Friend", 3, "Matt"],
    ['c_id_0084', "cards/matt- starbucks.png", "Starbucks", 3, "Matt"],
    ['c_id_0085', "cards/matt- thumbs_up.jpg", "Thumbs Up", 3, "Matt"],
    ['c_id_0086', "cards/matt- uci_commit.jpg", "Committed", 3, "Matt"],
    ['c_id_0087', "cards/matt- vr.jpg", "Metaverse", 3, "Matt"],
    ['c_id_0088', "cards/matt- widelens.jpg", "Widelens Matt", 3, "Matt"],
    ['c_id_0089', "cards/mikey- boba.png", "Boba Boba Masta Yoda", 3, "Mikey"],
    ['c_id_0090', "cards/mikey- bread.jpg", "Munching", 3, "Mikey"],
    ['c_id_0091', "cards/mikey- cooking.png", "He's a Chef", 3, "Mikey"],
    ['c_id_0092', "cards/mikey- corndogs.jpg", "Mikey and the Weenies", 3, "Mikey"],
    ['c_id_0093', "cards/mikey- disappointed.jpg", "Disappointment", 3, "Mikey"],
    ['c_id_0094', "cards/mikey- full.jpg", "Stuffed", 3, "Mikey"],
    ['c_id_0095', "cards/mikey- i_support_daves.jpg", "Dave's Hot Chicken > All", 3, "Mikey"],
    ['c_id_0096', "cards/mikey- its_beat_saber_i_swear.jpg", "Beat Saber 240p", 3, "Mikey"],
    ['c_id_0097', "cards/mikey- jello_shot.jpg", "Jello Shot", 3, "Mikey"],
    ['c_id_0098', "cards/mikey- leg.jpg", "Hairy Leg", 3, "Mikey"],
    ['c_id_0099', "cards/mikey- mid_shoulder.png", "The Shoulder", 3, "Mikey"],
    ['c_id_0100', "cards/mikey- philippines.jpg", "In The Philippines", 3, "Mikey"],
    ['c_id_0101', "cards/mikey- pho_night.jpg", "This Picture is Pho You", 3, "Mikey"],
    ['c_id_0102', "cards/mikey- phonelight.PNG", "Flashlight", 3, "Mikey"],
    ['c_id_0103', "cards/mikey- really.png", "Really?", 3, "Mikey"],
    ['c_id_0104', "cards/mikey- rec_room.jpg", "Billiards is not a Hobby. Billiards is my Life.", 3, "Mikey"],
    ['c_id_0105', "cards/mikey- soma.jpg", "Shokugeki no Soma", 3, "Mikey"],
    ['c_id_0106', "cards/mikey- thats_too_small.jpg", "Concerned Mikey", 3, "Mikey"],
    ['c_id_0107', "cards/mikey- widelens.jpg", "Widelens Mikey", 3, "Mikey"],
    ['c_id_0108', "cards/mikey- with_fam.jpg", "Mikey's Fam", 3, "Mikey"],
    ['c_id_0109', "cards/mikey- zotcon_vr.png", "Baby's First VR", 3, "Mikey"],
    ['c_id_0110', "cards/nayoung- pooped.jpg", "I'm Pooped", 3, "Nayoung"],
    ['c_id_0111', "cards/nina- aquarium.jpg", "Fish are Friends, not Food", 3, "Nina"],
    ['c_id_0112', "cards/nina- burger.jpg", "Borgar", 3, "Nina"],
    ['c_id_0113', "cards/nina- chopsticks.jpg", "You Caught me While I was Eating my BCD!", 3, "Nina"],
    ['c_id_0114', "cards/nina- gang_signs.jfif", "Gang Gang", 3, "Nina"],
    ['c_id_0115', "cards/nina- iced.png", "Iced", 3, "Nina"],
    ['c_id_0116', "cards/nina- pho_chef.jpg", "Pho Real?", 3, "Nina"],
    ['c_id_0117', "cards/nina- picnic.jpg", "Picnic", 3, "Nina"],
    ['c_id_0118', "cards/nina- red_cup_and_shrimp_toast.jfif", "Shrimp Toast?", 3, "Nina"],
    ['c_id_0119', "cards/nina- shabu.png", "That's a Lotta Beef", 3, "Nina"],
    ['c_id_0120', "cards/nina- sharetea.jpg", "OMG this gotta get on the gram", 3, "Nina"],
    ['c_id_0121', "cards/nina- sus.jpg", "What's on Your Window?", 3, "Nina"],
    ['c_id_0122', "cards/noah- selfie.png", "Check the Drip", 3, "Noah"],
    ['c_id_0123', "cards/noah- warning.jpg", "Warning Sign", 3, "Noah"],
    ['c_id_0124', "cards/patrick- content.jpg", "Patrick is Content", 3, "Patrick"],
    ['c_id_0125', "cards/patrick- ice_cream.jpg", "Patrick likes Ice Cream", 3, "Patrick"],
    ['c_id_0126', "cards/patrick- ladder.jpg", "Chutes and Ladders", 3, "Patrick"],
    ['c_id_0127', "cards/patrick- sweater.png", "Who Dat", 3, "Patrick"],
    ['c_id_0128', "cards/steven- 2008_version.JPG", "Steven circa 2008", 3, "Steven"],
    ['c_id_0129', "cards/steven- alcoholic.jpg", "Alcoholic", 3, "Steven"],
    ['c_id_0130', "cards/steven- arc_steven.jpg", "Gains", 3, "Steven"],
    ['c_id_0131', "cards/steven- back_profile.png", "On the Streets", 3, "Steven"],
    ['c_id_0132', "cards/steven- bcd.JPG", "Hi Guys, I'm here at BCD!", 3, "Steven"],
    ['c_id_0133', "cards/steven- black_mask.JPG", "Black Mask", 3, "Steven"],
    ['c_id_0134', "cards/steven- blinked.jpg", "mid blink", 3, "Steven"],
    ['c_id_0135', "cards/steven- blue_mask.png", "Blue Mask", 3, "Steven"],
    ['c_id_0136', "cards/steven- boba.PNG", "Slurp", 3, "Steven"],
    ['c_id_0137', "cards/steven- covid.png", "Covid is alive and well", 3, "Steven"],
    ['c_id_0138', "cards/steven- cowboy.JPG", "It's High Noon", 3, "Steven"],
    ['c_id_0139', "cards/steven- dat_hair_tho.jpg", "Hair", 3, "Steven"],
    ['c_id_0140', "cards/steven- disco.png", "Rave Slave", 3, "Steven"],
    ['c_id_0141', "cards/steven- driving.JPG", "Fast and Furious", 3, "Steven"],
    ['c_id_0142', "cards/steven- eating.jpg", "MONCh", 3, "Steven"],
    ['c_id_0143', "cards/steven- egg_buying.JPG", "So many eggs", 3, "Steven"],
    ['c_id_0144', "cards/steven- eyeroll.jpg", "Eyeroll", 3, "Steven"],
    ['c_id_0145', "cards/steven- f_boi.jpg", "Sweater Weather", 3, "Steven"],
    ['c_id_0146', "cards/steven- golf_ball.jpg", "Golf Ball", 3, "Steven"],
    ['c_id_0147', "cards/steven- grill.png", "KBBQ @ home", 3, "Steven"],
    ['c_id_0148', "cards/steven- judging.png", "judging", 3, "Steven"],
    ['c_id_0149', "cards/steven- mouth_cover.jpg", "cough cough", 3, "Steven"],
    ['c_id_0150', "cards/steven- peace.png", "Peace Out - from Steven", 3, "Steven"],
    ['c_id_0151', "cards/steven- poke.jpg", "Poke ain't bad", 3, "Steven"],
    ['c_id_0152', "cards/steven- ponyo_pal.jpg", "Ponyo Pal", 3, "Steven"],
    ['c_id_0153', "cards/steven- puppy_shirt.png", "Pug Life", 3, "Steven"],
    ['c_id_0154', "cards/steven- sad_sushi.jpg", "Sad Sushi", 3, "Steven"],
    ['c_id_0155', "cards/steven- scheming.png", "Scheming", 3, "Steven"],
    ['c_id_0156', "cards/steven- side_smile.jpg", "Side Smile", 3, "Steven"],
    ['c_id_0157', "cards/steven- sleepy.JPG", "Sleepy", 3, "Steven"],
    ['c_id_0158', "cards/steven- sunny.jpg", "Sunny Smile", 3, "Steven"],
    ['c_id_0159', "cards/steven- surprised_look.jpg", "Surprised Look", 3, "Steven"],
    ['c_id_0160', "cards/steven- thinking_about_not_being_blind.jpg",
     "Thinking About How Nice the Picture Would be if I Wasn't BLIND", 3, "Steven"],
    ['c_id_0161', "cards/steven- tuxedo.jpg", "Fancy Steven", 3, "Steven"],
    ['c_id_0162', "cards/steven- vr_coat.JPG", "Link Start", 3, "Steven"],
    ['c_id_0163', "cards/steven- waiting.jpg", "Waiting for Anything to Happen", 3, "Steven"],
    ['c_id_0164', "cards/steven- widelens.jpg", "Widelens Steven", 3, "Steven"],
    ['c_id_0165', "cards/steven- zotcon_vr.png", "Man's First VR", 3, "Steven"],
    ['c_id_0166', "cards/tim- indoor_bike.jpg", "Biker Gang", 3, "Tim"],
    ['c_id_0167', "cards/tim- lick.jpg", "Lickitung", 3, "Tim"],
    ['c_id_0168', "cards/tim- thumbs_up.jpg", "Timmy Thumby", 3, "Tim"],
    ['c_id_0169', "cards/tommy- churros_with_daniel.jpg", "Churros", 3, "Tommy"],
    ['c_id_0170', "cards/tommy- hair_dye_prep.png", "I'm Ready", 3, "Tommy"],
    ['c_id_0171', "cards/tommy- picnic.jpg", "There's a Fly in My Cup", 3, "Tommy"],
    ['c_id_0172', "cards/wendy- blurb.JPG", "Blurb", 3, "Wendy"],
    ['c_id_0173', "cards/wendy- pancakes.jpg", "Stacks on Stacks", 3, "Wendy"],
    ['c_id_0174', "cards/wendy- presenter.JPG", "Hello and Welcome to my TEDTalk", 3, "Wendy"],
    ['c_id_0175', "cards/will- dorm_desk.jpg", "Oh, didn't see you there", 3, "Will"],
    ['c_id_0176', "cards/will- flipped.jpg", "Fuck You Will", 3, "Will"],
    ['c_id_0177', "cards/will- is_that_will.jpg", "Who tf is That", 3, "Will"],
    ['c_id_0178', "cards/will- mid_blink.jpg", "haha are my eyes closed or open", 3, "Will"],
    ['c_id_0179', "cards/will- no_smile.jpg", "Serious Will", 3, "Will"],
    ['c_id_0180', "cards/will- packing.jpg", "Packing in More Ways than One", 3, "Will"],
    ['c_id_0181', "cards/will- rolling_in_grass.jpg", "Ouch this grass isn't Soft", 3, "Will"],
    ['c_id_0182', "cards/will- sitting_but_its_birthday_time.jpg", "Happy Birthday Will", 3, "Will"],
    ['c_id_0183', "cards/will- sitting_on_grass.jpg", "Hey There", 3, "Will"],
    ['c_id_0184', "cards/will- sleepy_with_alyssa.jpg", "How Does he Sleep like That?", 3, "Will"],
    ['c_id_0185', "cards/will- tongue_out.jpg", "Look, I'm Yoshi", 3, "Will"],
    ['c_id_0186', "cards/will- vr.jpg", "GET DOWN", 3, "Will"],
    ['c_id_0187', "cards/will- yardhouse.jpg", "glug glug", 3, "Will"],
    ['c_id_0188', "cards/alex- plate.jpg", "Bonk", 4, "Alex"],
    ['c_id_0189', "cards/bo- amogus.png", "Among Us - Bo", 4, "Bo"],
    ['c_id_0190', "cards/bo- anti_cancer.png", "Anti Cancer Bo", 4, "Bo"],
    ['c_id_0191', "cards/bo- beach_day.JPG", "Beach Day Bo", 4, "Bo"],
    ['c_id_0192', "cards/bo- blimp.PNG", "Blimp Bo", 4, "Bo"],
    ['c_id_0193', "cards/bo- bo_with_mini_bos.png", "Check out my Mini Bos", 4, "Bo"],
    ['c_id_0194', "cards/bo- braided.jpg", "Braided Bo", 4, "Bo"],
    ['c_id_0195', "cards/bo- cast.PNG", "Samus Bramer", 4, "Bo"],
    ['c_id_0196', "cards/bo- cilantro.jpg", "Cilantro", 4, "Bo"],
    ['c_id_0197', "cards/bo- failed.jpg", "Failure Bo", 4, "Bo"],
    ['c_id_0198', "cards/bo- graph_happy.jpg", "Graph Happy", 4, "Bo"],
    ['c_id_0199', "cards/bo- graph_shocked.jpg", "Graph Shocked", 4, "Bo"],
    ['c_id_0200', "cards/bo- hand_cast.jpg", "Hi I'm Dying", 4, "Bo"],
    ['c_id_0201', "cards/bo- hey_horses.png", "Hey is for Horses", 4, "Bo"],
    ['c_id_0202', "cards/bo- in_snow.jpg", "Bo in the Snow", 4, "Bo"],
    ['c_id_0203', "cards/bo- labcoat.jpg", "Chemical Engineering", 4, "Bo"],
    ['c_id_0204', "cards/bo- minnie.jpg", "Cute Bo", 4, "Bo"],
    ['c_id_0205', "cards/bo- phonecase.png", "I couldn't afford a phone so I just bought a case", 4, "Bo"],
    ['c_id_0206', "cards/bo- pocky.jpg", "Pocky", 4, "Bo"],
    ['c_id_0207', "cards/bo- shrimp.PNG", "Simp on a Shrimp", 4, "Bo"],
    ['c_id_0208', "cards/bo- snapchat_filter.jpg", "Snapchat Filter", 4, "Bo"],
    ['c_id_0209', "cards/bo- the_look.jpg", "The Look", 4, "Bo"],
    ['c_id_0210', "cards/bo- triple_threat.jpg", "Triple Threat", 4, "Bo"],
    ['c_id_0211', "cards/bo- when_the_photographer_says_cheese.png", "When the photographer says \"Cheese\"", 4, "Bo"],
    ['c_id_0212', "cards/combo- bo_tim_peace.jpg", "I'm Out", 4, "Combo"],
    ['c_id_0213', "cards/combo- boba_drinkers.JPG", "Boba Drinkers", 4, "Combo"],
    ['c_id_0214', "cards/combo- chubby_mikey_bo.JPG", "Chubby Bunny", 4, "Combo"],
    ['c_id_0215', "cards/combo- covid_gang.png", "Covid Gang", 4, "Combo"],
    ['c_id_0216', "cards/combo- grad_buddies.jpg", "Grad Buddies", 4, "Combo"],
    ['c_id_0217', "cards/combo- hair_dye_night.png", "Hair Dye Night", 4, "Combo"],
    ['c_id_0218', "cards/combo- insane_yell.jpg", "Insane YELLING", 4, "Combo"],
    ['c_id_0219', "cards/combo- janksmas_candid_1.png", "Janksmas 1", 4, "Combo"],
    ['c_id_0220', "cards/combo- janksmas_candid_2.png", "Janksmas 2", 4, "Combo"],
    ['c_id_0221', "cards/combo- janksmas.png", "Janksmas 3", 4, "Combo"],
    ['c_id_0222', "cards/combo- lighthouse.jpg", "Lighthouse Cafe", 4, "Combo"],
    ['c_id_0223', "cards/combo- midvale.jpg", "Midvale", 4, "Combo"],
    ['c_id_0224', "cards/combo- mikey_steven_cookies.PNG", "Look at Those Cookies", 4, "Combo"],
    ['c_id_0225', "cards/combo- people_in_line.JPG", "In a Line", 4, "Combo"],
    ['c_id_0226', "cards/combo- shoulder_massage.jpg", "Shoulder Massage", 4, "Combo"],
    ['c_id_0227', "cards/combo- snack_time.jpg", "Snack Time", 4, "Combo"],
    ['c_id_0228', "cards/combo- tote_bag.JPG", "Tote Bag", 4, "Combo"],
    ['c_id_0229', "cards/combo- totem_pole.jpg", "Totem Pole", 4, "Combo"],
    ['c_id_0230', "cards/combo- UCI_jerk_chicken.png", "Jerk Chicken", 4, "Combo"],
    ['c_id_0231', "cards/combo- UCI_patty_melt.png", "Patty Melt", 4, "Combo"],
    ['c_id_0232', "cards/combo- will_nina_gamers.png", "will sun and nina nina", 4, "Combo"],
    ['c_id_0233', "cards/combo- you_like_that_huh.jpg", "You Like that Huh?", 4, "Combo"],
    ['c_id_0234', "cards/elijah- amogus.png", "Among Us - Elijah", 4, "Elijah"],
    ['c_id_0235', "cards/elijah- glaring.jpg", "Glare", 4, "Elijah"],
    ['c_id_0236', "cards/emre- 5head.png", "5Head", 4, "Emre"],
    ['c_id_0237', "cards/flynn- amogus.png", "Among Us - Flynn", 4, "Flynn"],
    ['c_id_0238', "cards/flynn- dennys.jpg", "Dennys Late Night", 4, "Flynn"],
    ['c_id_0239', "cards/flynn- snoop_dog.JPG", "Snoop Dog???", 4, "Flynn"],
    ['c_id_0240', "cards/haroon- amogus.png", "Among Us - Haroon", 4, "Haroon"],
    ['c_id_0241', "cards/haroon- kbbq_pay_for_your_meal.jpg", "Big Boi", 4, "Haroon"],
    ['c_id_0242', "cards/jenn- amogus.png", "Among Us - Jenn", 4, "Jenn"],
    ['c_id_0243', "cards/jenn- gun_shopping.png", "Gun Shopping", 4, "Jenn"],
    ['c_id_0244', "cards/jenn- interested.jpg", "Interested Jenn", 4, "Jenn"],
    ['c_id_0245', "cards/jenn- jurassic_world.jpg", "AHHHHHHHHHHHHHHHHHH", 4, "Jenn"],
    ['c_id_0246', "cards/jenn- scammed.jpg", "Scammed", 4, "Jenn"],
    ['c_id_0247', "cards/john- full.jpg", "I'm Stuffed", 4, "John"],
    ['c_id_0248', "cards/john- punch.jpg", "One Punch Man", 4, "John"],
    ['c_id_0249', "cards/matt- 5_26.png", "5:26 AM", 4, "Matt"],
    ['c_id_0250', "cards/matt- im_not_gay.jpg", "I'm not Gay", 4, "Matt"],
    ['c_id_0251', "cards/matt- phonelight.PNG", "Phonelight", 4, "Matt"],
    ['c_id_0252', "cards/matt- sus_bathroom_activity.jpg", "Sus Imposter Vented", 4, "Matt"],
    ['c_id_0253', "cards/matt- UCI_zoturation_II.png", "Zoturation II", 4, "Matt"],
    ['c_id_0254', "cards/matt- yellow_converse.jpg", "Yellow Converse", 4, "Matt"],
    ['c_id_0255', "cards/mikey- amogus.png", "Among Us - Mikey", 4, "Mikey"],
    ['c_id_0256', "cards/mikey- arc_mikey.jpg", "Arc Mikey", 4, "Mikey"],
    ['c_id_0257', "cards/mikey- boba2.jpg", "Boba Mikey", 4, "Mikey"],
    ['c_id_0258', "cards/mikey- chef.PNG", "Chef Mikey", 4, "Mikey"],
    ['c_id_0259', "cards/mikey- drawing.png", "Doodle Mikey", 4, "Mikey"],
    ['c_id_0260', "cards/mikey- kazoo.jpg", "Kazoo Mikey", 4, "Mikey"],
    ['c_id_0261', "cards/mikey- library.jpg", "Library Mikey", 4, "Mikey"],
    ['c_id_0262', "cards/mikey- lightbulb.PNG", "How many Mikeys does it take to screw in a Lightbulb?", 4, "Mikey"],
    ['c_id_0263', "cards/mikey- omen.jpg", "Omen", 4, "Mikey"],
    ['c_id_0264', "cards/mikey- shopping_hard.jpg", "Hard Shopping", 4, "Mikey"],
    ['c_id_0265', "cards/mikey- smol_version.jpg", "Smol Mikey", 4, "Mikey"],
    ['c_id_0266', "cards/mikey- yellow_jacket.jpg", "Alpha Mikey", 4, "Mikey"],
    ['c_id_0267', "cards/nayoung- made_you_look.jpg", "Made You Look", 4, "Nayoung"],
    ['c_id_0268', "cards/nina- back_in_america.jpg", "Back in America", 4, "Nina"],
    ['c_id_0269', "cards/nina- chewing.jpg", "I'm boutta Vomit", 4, "Nina"],
    ['c_id_0270', "cards/nina- heart_glasses.jpg", "Heart Glasses", 4, "Nina"],
    ['c_id_0271', "cards/nina- shocked.jpg", "ohmygawsh", 4, "Nina"],
    ['c_id_0272', "cards/nina- stare.JPG", "Cursed Nina", 4, "Nina"],
    ['c_id_0273', "cards/nina- zoom.jpg", "Zoom Nina", 4, "Nina"],
    ['c_id_0274', "cards/noah- highlights.jpg", "Swaggy Noah", 4, "Noah"],
    ['c_id_0275', "cards/patrick- dead.jpg", "Dead Patrick 1", 4, "Patrick"],
    ['c_id_0276', "cards/patrick- sleepy.jpg", "Dead Patrick 2", 4, "Patrick"],
    ['c_id_0277', "cards/ponyo- attack.png", "she attack", 4, "Misc."],
    ['c_id_0278', "cards/radish.PNG", "Radish", 4, "Misc."],
    ['c_id_0279', "cards/steven- amogus.png", "Among Us - Steven", 4, "Steven"],
    ['c_id_0280', "cards/steven- anime.png", "Anime Steven", 4, "Steven"],
    ['c_id_0281', "cards/steven- chef.jpg", "Chef Steven", 4, "Steven"],
    ['c_id_0282', "cards/steven- disaster_hair.png", "Disaster Hair", 4, "Steven"],
    ['c_id_0283', "cards/steven- edgy_tanktop.jpg", "Edgy Steven", 4, "Steven"],
    ['c_id_0284', "cards/steven- slurp.JPG", "Slurping Steven", 4, "Steven"],
    ['c_id_0285', "cards/steven- thug_lyfe.png", "Thug Lyfe", 4, "Steven"],
    ['c_id_0286', "cards/steven- UCI_zoturation.png", "Zoturation", 4, "Steven"],
    ['c_id_0287', "cards/susie- peace.jpg", "Peace Out - from Susie", 4, "Susie"],
    ['c_id_0288', "cards/tim- 3stock.jpg", "3 Stock", 4, "Tim"],
    ['c_id_0289', "cards/tim- big_smile.PNG", "Big Tim with Big Smile", 4, "Tim"],
    ['c_id_0290', "cards/tim- bike.jpg", "Biker Tim Comes in for a Repair", 4, "Tim"],
    ['c_id_0291', "cards/tim- neckless.png", "No Neck Tim", 4, "Tim"],
    ['c_id_0292', "cards/tommy- amogus.png", "Among Us - Tommy", 4, "Tommy"],
    ['c_id_0293', "cards/tommy- fridge.JPG", "Where tf is the Milk", 4, "Tommy"],
    ['c_id_0294', "cards/tommy- hi_im_tommy.jpg", "Hi I'm Tommy", 4, "Tommy"],
    ['c_id_0295', "cards/tommy- peace.png", "Peace Out - from Tommy", 4, "Tommy"],
    ['c_id_0296', "cards/tommy- vape_place.png", "Vape Tommy", 4, "Tommy"],
    ['c_id_0297', "cards/wendy- learn_produce.jpg", "Learn Produce", 4, "Wendy"],
    ['c_id_0298', "cards/will- amogus.png", "Among Us - Will", 4, "Will"],
    ['c_id_0299', "cards/will- boba.jpg", "This Some Good Boba", 4, "Will"],
    ['c_id_0300', "cards/will- body_pillows.jpg", "uwu Rem uwu", 4, "Will"],
    ['c_id_0301', "cards/will- cooking_like_bo.jpg", "Call me Bo Bramer", 4, "Will"],
    ['c_id_0302', "cards/will- dillmeme.png", "DillPickleDillPickleDillPickleDillPickleDillPickleDillPickle", 4, "Will"],
    ['c_id_0303', "cards/will- get_on_our_level.png", "Get on our Level", 4, "Will"],
    ['c_id_0304', "cards/will- happy_birthday_poster.png", "18th Birthday", 4, "Will"],
    ['c_id_0305', "cards/will- ice_cream_fail.jpg", "I Scream", 4, "Will"],
    ['c_id_0306', "cards/will- ice_cream.jpg", "Experienced Will", 4, "Will"],
    ['c_id_0307', "cards/will- its_hot.jpg", "Willgasm", 4, "Will"],
    ['c_id_0308', "cards/will- old_facebook_pfp.jpg", "Band Nerds 2", 4, "Will"],
    ['c_id_0309', "cards/will- panda_express.jpg", "Panda", 4, "Will"],
    ['c_id_0310', "cards/will- pigtails.jpg", "Pigtails", 4, "Will"],
    ['c_id_0311', "cards/will- sleepy.jpg", "Sleepy Will", 4, "Will"],
    ['c_id_0312', "cards/will- TMNT.jpg", "TMNT", 4, "Will"],
    ['c_id_0313', "cards/will- whistling.jpg", "Whistling Will", 4, "Will"],
    ['c_id_0314', "cards/will- witch.jpg", "Witch Will", 4, "Will"],
    ['c_id_0315', "cards/alex- sage.jpg", "I Am Not Just Your Healer", 5, "Alex"],
    ['c_id_0316', "cards/bo- hospital.jpeg", "The Hospital Told me to Lift My Spirits.. so I did.", 5, "Bo"],
    ['c_id_0317', "cards/bo- macarons.png", "Macaron PTSD", 5, "Bo"],
    ['c_id_0318', "cards/bo- po_breamer.png", "Po Breamer", 5, "Bo"],
    ['c_id_0319', "cards/chibi_bo.png", "Chibi Bo", 5, "Bo"],
    ['c_id_0320', "cards/chibi_flynn.png", "Chibi Flynn", 5, "Flynn"],
    ['c_id_0321', "cards/chibi_haroon.png", "Chibi Haroon", 5, "Haroon"],
    ['c_id_0322', "cards/chibi_jenn.png", "Chibi Jenn", 5, "Jenn"],
    ['c_id_0323', "cards/chibi_john.png", "Chibi John", 5, "John"],
    ['c_id_0324', "cards/chibi_mikey.png", "Chibi Mikey", 5, "Mikey"],
    ['c_id_0325', "cards/chibi_nina.png", "Chibi Nina", 5, "Nina"],
    ['c_id_0326', "cards/chibi_steven.png", "Chibi Steven", 5, "Steven"],
    ['c_id_0327', "cards/chibi_tommy.png", "Chibi Tommy", 5, "Tommy"],
    ['c_id_0328', "cards/chibi_will.png", "Chibi Will", 5, "Will"],
    ['c_id_0329', "cards/combo- bo_matt_blowing_smoke.jpg", "Matt and Bo share their experiences", 5, "Combo"],
    ['c_id_0330', "cards/flynn- lighthouse_drip.jpg", "Lighthouse Drip", 5, "Flynn"],
    ['c_id_0331', "cards/haroon- zot.JPG", "Zot.", 5, "Haroon"],
    ['c_id_0332', "cards/jenn- iced.PNG", "Jenn Iced", 5, "Jenn"],
    ['c_id_0333', "cards/jenn- meme.jpg", "Meme Jenn", 5, "Jenn"],
    ['c_id_0334', "cards/john- swimmer.jpg", "John Phelps", 5, "John"],
    ['c_id_0335', "cards/matt- carwash.png", "Carwash Matt", 5, "Matt"],
    ['c_id_0336', "cards/matt- nose_goes.jpg", "Nose Goes", 5, "Matt"],
    ['c_id_0337', "cards/matt- poptart.jpg", "Poptart *in a British accent*", 5, "Matt"],
    ['c_id_0338', "cards/matt- visor.jpg", "SAO Matt", 5, "Matt"],
    ['c_id_0339', "cards/mikey- cool.JPG", "Cool Mikey", 5, "Mikey"],
    ['c_id_0340', "cards/mikey- fortune.jpg", "You Light Up The Room With Your Smile", 5, "Mikey"],
    ['c_id_0341', "cards/mikey- girl.JPG", "Female Mikey", 5, "Mikey"],
    ['c_id_0342', "cards/mikey- gottem.PNG", "Gottem", 5, "Mikey"],
    ['c_id_0343', "cards/mikey- L.jpg", "L", 5, "Mikey"],
    ['c_id_0344', "cards/mikey- solar_eclipse.jpg", "When my Future is Too Bright", 5, "Mikey"],
    ['c_id_0345', "cards/mikey- yoshis.jpg", "YoshiYoshiYoshiYoshiYoshiYoshiYoshiYoshiYoshiYoshi", 5, "Mikey"],
    ['c_id_0346', "cards/nayoung- gun.jpg", "kms", 5, "Nayoung"],
    ['c_id_0347', "cards/nina- flossing.png", "Nina Flossing", 5, "Nina"],
    ['c_id_0348', "cards/nina- wine_chug.png", "Alcoholic Nina", 5, "Nina"],
    ['c_id_0349', "cards/patrick- schoolgirl.png", "Female Shiffty", 5, "Patrick"],
    ['c_id_0350', "cards/patrick- sunglasses_pat.jpg", "Patrol Patrick", 5, "Patrick"],
    ['c_id_0351', "cards/steven- f_u.png", "f u", 5, "Steven"],
    ['c_id_0352', "cards/steven- f_word.PNG", "Steven Slander", 5, "Steven"],
    ['c_id_0353', "cards/steven- game_mode.jpg", "Final Form Steven", 5, "Steven"],
    ['c_id_0354', "cards/steven- gay.PNG", "Gay Steven", 5, "Steven"],
    ['c_id_0355', "cards/steven- hospital.jpg", "Hospitalized Steven", 5, "Steven"],
    ['c_id_0356', "cards/steven- sup_faggies.JPG", "sup", 5, "Steven"],
    ['c_id_0357', "cards/tommy- hello_kitty_hat.jpg", "Hello Kitty Kawaii Tommy", 5, "Tommy"],
    ['c_id_0358', "cards/will- beta_bitch.png", "Beta Bitch", 5, "Will"],
    ['c_id_0359', "cards/will- thicc.jpg", "Thicc Will", 5, "Will"],
]


card_deck = {}
name_deck = {}
card_deck_3 = {}
card_deck_4 = {}
card_deck_5 = {}


for c in cards:
    card_deck[c[0]] = Card(c[0], c[1], c[2], c[3], c[4])
    name_deck[c[2].lower()] = Card(c[0], c[1], c[2], c[3], c[4])
    if c[3] == 3:
        card_deck_3[c[0]] = Card(c[0], c[1], c[2], c[3], c[4])
    elif c[3] == 4:
        card_deck_4[c[0]] = Card(c[0], c[1], c[2], c[3], c[4])
    elif c[3] == 5:
        card_deck_5[c[0]] = Card(c[0], c[1], c[2], c[3], c[4])
