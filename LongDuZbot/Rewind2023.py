import discord
from discord.ext import commands
import sys
import os
import requests

import datetime
from dateutil.relativedelta import relativedelta
import locale

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

first_january_2023_timestamp = 1672531200
thirtyfirst_decemeber_2023_timestamp = 1704067199

def drawCenterText(text, font, text_max_width, img, image_width, fill=(255, 255, 255, 255),origin_y=10):
	current_h = origin_y + 40
	interline = 10
	para = textwrap.wrap(text, width=text_max_width)
	draw = ImageDraw.Draw(img)

	for line in para:
		# w = draw.textlength(line, font=font) ## HERE
		# h = 10 #TemP cHANGE mE
		_, _, w, h = draw.textbbox((0, 0), text=line, font=font)
		draw_text = ImageDraw.Draw(img)
		draw_text.text(((image_width - w) // 2, current_h), line, font=font, fill=fill)
		current_h += h + interline

def create_bar_graph(data, img, image_width, origin_x=0, bar_width=30, spacers=5, colors=["cyan","blue"], nodatacolors=["pink", "red"]):
	# Calculate image size based on data
	#image_width = len(data) * bar_width
	image_height = 660 #max(data) * bar_height_multiplier
	max_pix_height = 400
	if max(data) == 0: #If no data at all
		bar_height_multiplier = max_pix_height
	else:
		bar_height_multiplier=max_pix_height / max(data)

	# Create a blank image
	draw = ImageDraw.Draw(img)

	# Draw bars
	for i, value in enumerate(data):
		y1 = image_height - 1
		if (value > 0):
			y1 = image_height - value * bar_height_multiplier
		x1 = i * (bar_width + spacers) + origin_x
		x2 = x1 + bar_width - 1 
		y2 = image_height - 1
		
			#draw.rectangle([x1, y1, x2, y2], fill='blue')
		if (value > 0):
			draw.rounded_rectangle([x1, y1, x2, y2], fill=colors[0], outline=colors[1], width=3, radius=7)
		else:
			draw.rounded_rectangle([x1, y1, x2, y2], fill=nodatacolors[0], outline=nodatacolors[1], width=3, radius=7)

	ImageDraw.Draw(img)

class Rewind2023(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
		self.database = self.bot.get_cog('Database')
		if self.database is None:
			ggr_utilities.logger("Missing Database Cog", self, ggr_utilities.LogType.CRIT)

	def __del__(self):
		ggr_utilities.logger(self.__class__.__name__ + " Cog Unloaded!" , self, None, ggr_utilities.LogType.WARN)

	@commands.command()
	async def rewind(self, ctx):
		ctx.guild = self.bot.get_guild(806284513583169596)

		print("generating slides...")
		for slide in range(0, 6):
			self.gen_slide_2023_wrapped(slide, ctx)
			print("slide " + str(slide) +" done...")
			await ctx.send(file = discord.File('tmp/animated_tile.gif'))
		print("done generating slides for @" + ctx.author.name)

	def profile_and_server(self, ctx, img, size=(256,256), origin=None, mode="profile"):
		if (mode == "profile"):
			url = ctx.author.avatar_url_as(format='png')
		else:
			url = ctx.guild.icon_url_as(format='png')

		profile = Image.open(requests.get(url, stream=True).raw).convert("RGBA") #profile pic
		profile = profile.resize(size) #just to be sure


		profile_w, profile_h  = profile.size
		# profileg_w, profileg_h = certif.size
		# tampon_w, tampon_h = tampon.size
		# signature_w, signature_h = signature.size
		certif.genRoundImg(profile)
		if (origin == None):
			img.paste(profile, ((image_width//2)-(256//2), 256), mask=profile)
		else:
			img.paste(profile, origin, mask=profile)

	def genSalopeiresListYear(self, user, guild):
		monthsSaloperies = []
		month = 1
		for month in range(1, 13):
			start_month = datetime.datetime(2023, month, 1)
			end_month = datetime.datetime(2023, month, 1)	+ relativedelta(months=+1)
			monthsSaloperies.append(self.database.getStatsSaloperiesMegaArmyOnPeriod(user, guild, start_month.timestamp(), end_month.timestamp())) #[0][0])		
		return monthsSaloperies

	def gen_slide_2023_wrapped(self, slide, ctx):
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
		m = 8
		cnt = 0

		mydate = datetime.datetime.now()
		locale.setlocale(locale.LC_TIME, "fr_FR")

		if (slide == 0):
			pass
		elif (slide == 1):
			times_MegaArmy_command = self.database.getStatsCountSaloperiesMegaArmyOnPeriod(ctx.author, ctx.guild, first_january_2023_timestamp, thirtyfirst_decemeber_2023_timestamp)
			percent_MegaArmy_more = round(self.database.getStatsPercentileCommandMegaArmyOnPeriod(ctx.author, ctx.guild, first_january_2023_timestamp, thirtyfirst_decemeber_2023_timestamp)["percentile_rank"], 1)
			lilian_bouche_img = Image.open('img/lilian_bouche.png', 'r')

		elif (slide == 2):
			number_saloperies_total = self.database.getStatsSaloperiesMegaArmyOnPeriod(ctx.author, ctx.guild, first_january_2023_timestamp, thirtyfirst_decemeber_2023_timestamp)
			list_saloperie_month = self.genSalopeiresListYear(ctx.author, ctx.guild)
			month_nbr = max(enumerate(list_saloperie_month),key=lambda x: x[1])[0] + 1
			month_datetime = datetime.datetime(2023, month_nbr, 1)
			slide_2_month_most_active = month_datetime.strftime("%B").title()

		elif (slide == 3):
			statsBestDaySaloperiesMegaArmyOnPeriod = self.database.getStatsBestDaySaloperiesMegaArmyOnPeriod(ctx.author, ctx.guild, first_january_2023_timestamp, thirtyfirst_decemeber_2023_timestamp)
			dayStatsBestDaySaloperiesMegaArmyOnPeriod = datetime.datetime.fromtimestamp(statsBestDaySaloperiesMegaArmyOnPeriod["timestamp"]).strftime("%A %d %B %Y") #day of most saloperies
			saloperiesStatsBestDaySaloperiesMegaArmyOnPeriod = statsBestDaySaloperiesMegaArmyOnPeriod["saloperies"] #number of saloperies that day
			mat_big = Image.open('img/mat_big.png', 'r')

		elif (slide == 4):
			statsBestMegaArmyOnPeriod = self.database.getBestMegaArmyOnPeriod(ctx.author, ctx.guild, first_january_2023_timestamp, thirtyfirst_decemeber_2023_timestamp)
			statsWorstMegaArmyOnPeriod = self.database.getWorstMegaArmyOnPeriod(ctx.author, ctx.guild, first_january_2023_timestamp, thirtyfirst_decemeber_2023_timestamp)
			guogur = Image.open('img/guogur.png', 'r')

		elif (slide == 5):
			statsWadsOnPeriod = self.database.getStatsWadsOnPeriod(ctx.author, ctx.guild, first_january_2023_timestamp, thirtyfirst_decemeber_2023_timestamp)
			money_rich_persentile = round(self.database.getStatsPercentileWads(ctx.author, ctx.guild), 1)
			alex_voiture = Image.open('img/alex_voiture.png', 'r')
			
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

			if (slide == 0): #bare done
				slide_0_big_text = "Bonjour, @" + ctx.author.name
				slide_0_small_text = "Voyons un peu comment vous avez utilisé votre temps cette année."
				drawCenterText(slide_0_big_text, big_font, 20, frame, image_width, (255, 255, 255, 255), 10)
				drawCenterText(slide_0_small_text, medium_font, 32, frame, image_width, (255, 255, 255, 255), 630)
				self.profile_and_server(ctx, frame)

			elif (slide == 1): #bare done
				slide_1_big_text = "Vous avez saisi " + str(times_MegaArmy_command) + " fois la commande !MegaArmy cette année."
				slide_1_small_text = "C'est plus que " + str(percent_MegaArmy_more) + "% des membres du serveur."
				drawCenterText(slide_1_big_text, big_font, 20, frame, image_width, (255, 255, 255, 255), 10)
				drawCenterText(slide_1_small_text, medium_font, 32, frame, image_width, (255, 255, 255, 255), 630)

				slide_1_overlay = Image.new('RGBA', (image_width, image_height))
				slide_1_overlay.paste(lilian_bouche_img, ((image_width - lilian_bouche_img.size[0]) // 2, (image_height - lilian_bouche_img.size[1]) // 2))
				frame = Image.alpha_composite(frame, slide_1_overlay)

			elif (slide == 2):
				
				if (cnt < number_saloperies_total):
					cnt = 6 * i * (number_saloperies_total) // (tile_width//m)
				elif cnt > number_saloperies_total:
					cnt = number_saloperies_total

				slide_2_big_text = "Vous avez invoqué " + str(cnt) + " saloperies en 2023 !"
				slide_2_small_text = slide_2_month_most_active  + " à été votre mois le plus actif."

				drawCenterText(slide_2_big_text, big_font, 20, frame, image_width, (255, 255, 255, 255), 10)
				create_bar_graph(list_saloperie_month, frame, image_width, 5, 30, 10, ["#3F48A8", "#353C89"])
				drawCenterText(slide_2_small_text, medium_font, 32, frame, image_width, (255, 255, 255, 255), 630)

			elif (slide == 3): #bare minimum done ?
				slide_3_big_text = "Votre journée la plus productive à été le " + dayStatsBestDaySaloperiesMegaArmyOnPeriod + "."
				slide_3_small_text = "Avec un nombre impressionant de " + str(saloperiesStatsBestDaySaloperiesMegaArmyOnPeriod) + " saloperies invoquées ce jour-là."
				drawCenterText(slide_3_big_text, big_font, 20, frame, image_width, (255, 255, 255, 255), 10)
				drawCenterText(slide_3_small_text, medium_font, 32, frame, image_width, (255, 255, 255, 255), 600)

				slide_3_overlay = Image.new('RGBA', (image_width, image_height))
				slide_3_overlay.paste(mat_big, ((image_width - mat_big.size[0]) // 2, (image_height - mat_big.size[1]) // 2))
				frame = Image.alpha_composite(frame, slide_3_overlay)

			elif (slide == 4): #bare minimum done
				slide_4_big_text = "Votre meilleure !MegaArmy cette année comptait " + str(statsBestMegaArmyOnPeriod) + " saloperies."
				slide_4_small_text = "Et votre pire en avait seulement " + str(statsWorstMegaArmyOnPeriod) + "."
				drawCenterText(slide_4_big_text, big_font, 20, frame, image_width, (255, 255, 255, 255), 10)
				drawCenterText(slide_4_small_text, medium_font, 32, frame, image_width, (255, 255, 255, 255), 630)
				
				slide_4_overlay = Image.new('RGBA', (image_width, image_height))
				slide_4_overlay.paste(guogur, ((image_width - guogur.size[0]) // 2, (image_height - guogur.size[1]) // 2))
				frame = Image.alpha_composite(frame, slide_4_overlay)

			elif (slide == 5): #missing percents
				slide_5_big_text = "Vous avez raflé " + str(statsWadsOnPeriod) + " WADs en 2023."
				slide_5_small_text = "Vous faites partie des " + str(money_rich_persentile) +"% les plus riches de la communauté."
				drawCenterText(slide_5_big_text, big_font, 20, frame, image_width, (255, 255, 255, 255), 10)
				drawCenterText(slide_5_small_text, medium_font, 32, frame, image_width, (255, 255, 255, 255), 630)

				slide_5_overlay = Image.new('RGBA', (image_width, image_height))
				slide_5_overlay.paste(alex_voiture, ((image_width - alex_voiture.size[0]) // 2, (image_height - alex_voiture.size[1]) // 2))
				frame = Image.alpha_composite(frame, slide_5_overlay)


			slides_username_text = "@" + ctx.author.name + " | 2023 Rewind"


			overlay = Image.new('RGBA', (image_width, image_height))
			draw_rect = ImageDraw.Draw(overlay)
			draw_rect.rectangle([0, 854-96, 480, 854], (0, 0, 0, 127))
			frame = Image.alpha_composite(frame, overlay)

			draw_text = ImageDraw.Draw(frame)
			draw_text.text((16+64+64-8+16, 854-64), slides_username_text, font=medium_font, fill=(255, 255, 255, 255))
			
			self.profile_and_server(ctx, frame, (64, 64), (16+64-8, 854-(64+16)), mode="server")
			self.profile_and_server(ctx, frame, (64, 64), (16, 854-(64+16)))

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


def setup(bot):
	bot.add_cog(Rewind2023(bot))

def teardown(bot):
	print('I am being unloaded!')
