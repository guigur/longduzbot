import discord
from discord.ext import commands
import sys
import os

import ggr_utilities, ggr_emotes
import Eco, Com, Database
import certif

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap

# Set the tile size
tile_width = 512
tile_height = 512
tile_color = (0, 0, 0, 128)  # Red tile color with 50% transparency
image_width = 480
image_height = 854
target_cnt = 3000


def drawCenterText(text, font, text_max_width, img, image_width, fill=(255, 255, 255, 255),origin_y=10):
	current_h = origin_y + 40
	interline = 10
	para = textwrap.wrap(text, width=text_max_width)
	draw = ImageDraw.Draw(img)

	for line in para:
		w, h = draw.textsize(line, font=font)
		draw_text = ImageDraw.Draw(img)
		draw_text.text(((image_width - w) // 2, current_h), line, font=font, fill=fill)
		current_h += h + interline

def create_bar_graph(data, img, image_width, origin_x=0, bar_width=30, bar_height_multiplier=10, spacers=5, colors=["cyan","blue"]):
	# Calculate image size based on data
	#image_width = len(data) * bar_width
	image_height = 760 #max(data) * bar_height_multiplier
	# Create a blank image
	draw = ImageDraw.Draw(img)

	# Draw bars
	for i, value in enumerate(data):
		x1 = i * (bar_width + spacers) + origin_x
		y1 = image_height - value * bar_height_multiplier
		x2 = x1 + bar_width - 1 
		y2 = image_height - 1
		if (value > 0):
			#draw.rectangle([x1, y1, x2, y2], fill='blue')
			draw.rounded_rectangle([x1, y1, x2, y2], fill=colors[0], outline=colors[1], width=3, radius=7)

	# Save the image
	ImageDraw.Draw(img)

# List to store each frame of the GIF
def gen_slide_2023_wrapped(slide, user):
	image = Image.new("RGBA", (image_width, image_height), tile_color)
	draw = ImageDraw.Draw(image)

	background_image_path = "img/wad_texture.png"
	tile = Image.open(background_image_path).convert("RGBA")
	tile.putalpha(127)  # Half alpha; alpha argument must be an int

	# Load a font for the text
	font_path = "font/Montserrat-SemiBold.ttf"  # Replace with the path to your TrueType font file
	big_font_size = 42
	big_font = ImageFont.truetype(font_path, big_font_size)
	medium_font_size = 24
	medium_font = ImageFont.truetype(font_path, medium_font_size)

	frames = []
	m = 4
	cnt = 0

	import datetime
	mydate = datetime.datetime.now()
	import locale
	locale.setlocale(locale.LC_TIME, "fr_FR")

	# Create frames for the animation
	for i in range(tile_width//m):
		# Create a new frame by pasting tiles side by side on the background image
		frame = image.copy()
		frame.paste(tile, ((i * m) - tile_width, i * m), mask=tile)
		frame.paste(tile, (i * m, (i * m) - tile_height), mask=tile)
		frame.paste(tile, (i * m, i * m), mask=tile) #down right
		frame.paste(tile, ((i * m) - tile_width, (i * m) - tile_height), mask=tile)
		frame.paste(tile, (i * m, (i * m) + tile_height), mask=tile)
		frame.paste(tile, ((i * m) - tile_width, (i * m) + tile_height), mask=tile)

		if (cnt < target_cnt):
			cnt = 6 * i * (target_cnt) // (tile_width//m)
		elif cnt > target_cnt:
			cnt = target_cnt

		slide_0_big_text = "Bonjour, @" + user.name
		slide_0_small_text = "Voyons un peu comment vous avez utilisé votre temps cette année."

		slide_1_big_text = "Vous avez saisi " #+ str(times_megaarmy_command) + " fois la commande !megaaarmy cette année."
		slide_1_small_text = "C'est plus que " #+ str(percent_megaarmy_more) + "% des membres du serveur."
		
		slide_2_big_text = "Vous avez invoqué " + str(cnt) + " saloperies en 2023 !"
		slide_2_small_text = mydate.strftime("%B").title()  + " à été votre mois le plus actif."

		slide_3_big_text = "Votre journée la plus productive à été le " + mydate.strftime("%A %d %B %Y") + "."
		slide_3_small_text = "Avec un nombre impressionant de XXX saloperies invoquées ce jour-là."

		slide_4_big_text = "Votre meilleure !megaarmy cette année comptait XXX saloperies."
		slide_4_small_text = "Et votre pire en avait seulement XXX."

		#Parlons finaces
		slide_5_big_text = "Vous avez raflé XX WADs en 2023."
		slide_5_small_text = "Vous faites partie des XX% les plus riches de la communauté."
		
		if (slide == 0):
			drawCenterText(slide_0_big_text, big_font, 20, frame, image_width, (255, 255, 255, 255), 10)
			drawCenterText(slide_0_small_text, medium_font, 32, frame, image_width, (255, 255, 255, 255), 730)
		elif (slide == 1):
			drawCenterText(slide_1_big_text, big_font, 20, frame, image_width, (255, 255, 255, 255), 10)
			drawCenterText(slide_1_small_text, medium_font, 32, frame, image_width, (255, 255, 255, 255), 730)
		elif (slide == 2):
			drawCenterText(slide_2_big_text, big_font, 20, frame, image_width, (255, 255, 255, 255), 10)
			create_bar_graph([10, 20, 40, 100, 0, 10, 14, 66, 345, 44, 67, 23], frame, image_width, 5, 30, 1, 10, ["#3F48A8", "#353C89"])
			drawCenterText(slide_2_small_text, medium_font, 32, frame, image_width, (255, 255, 255, 255), 730)
		elif (slide == 3):
			drawCenterText(slide_3_big_text, big_font, 20, frame, image_width, (255, 255, 255, 255), 10)
			drawCenterText(slide_3_small_text, medium_font, 32, frame, image_width, (255, 255, 255, 255), 730)
		elif (slide == 4):
			drawCenterText(slide_4_big_text, big_font, 20, frame, image_width, (255, 255, 255, 255), 10)
			drawCenterText(slide_4_small_text, medium_font, 32, frame, image_width, (255, 255, 255, 255), 730)
		elif (slide == 5):
			drawCenterText(slide_5_big_text, big_font, 20, frame, image_width, (255, 255, 255, 255), 10)
			drawCenterText(slide_5_small_text, medium_font, 32, frame, image_width, (255, 255, 255, 255), 730)
		# text = f"Counter: {i}"
		# text_width, text_height = draw.textsize(text, font)
		# x = (400 - text_width) // 2
		# y = (500 - text_height) // 2

		# # Apply Gaussian blur to the text
		# blurred_text = frame.copy()
		# blurred_draw = ImageDraw.Draw(blurred_text)
		# blurred_draw.text((x, y), text, fill="black", font=font)
		# blurred_text = blurred_text.filter(ImageFilter.GaussianBlur(radius=3))
		# # Composite the blurred text onto the original image
		# frame.paste(blurred_text, (0, 0), blurred_text)

		frames.append(frame)

	# Save the frames as an animated GIF
	frames[0].save("tmp/animated_tile.gif", save_all=True, append_images=frames[1:], optimize = True, duration=50, loop=0)

class Rewind2023(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	async def rewind(self, ctx):
		print("generating slides...")
		for slide in range(6):
			gen_slide_2023_wrapped(slide, ctx.author)
			print("slide " + str(slide) +" done...")
			await ctx.send(file = discord.File('tmp/animated_tile.gif'))
		print("done")


def setup(bot):
	bot.add_cog(Rewind2023(bot))

def teardown(bot):
	print('I am being unloaded!')
