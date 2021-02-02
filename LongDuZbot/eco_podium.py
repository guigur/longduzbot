from PIL import Image, ImageOps, ImageDraw, ImageFont
from datetime import datetime
import locale

locale.setlocale(locale.LC_ALL, 'fr_FR') #For the french date

textColor = (0,0,0,255)

def ecoPodium():
	podium = Image.open('img/template/leader_money.png', 'r')
	texture = Image.open('img/wad-texture.png', 'r')


	#im = Image.new('RGB', (500, 300), (128, 128, 128))
	draw = ImageDraw.Draw(podium)
	draw.rectangle((300, 300, 600, 1240), fill=(0, 192, 192), outline=(255, 255, 255))
	#Left Top Right Bot

	podium.show()

	#return podium.save("tmp/podium.png")

ecoPodium()