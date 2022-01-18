import cards
import os

for card in cards.card_deck.values():
    image_file_url = card.image_url
    if not os.path.exists(image_file_url):
        print(image_file_url)
