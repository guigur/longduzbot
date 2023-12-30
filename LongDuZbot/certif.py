from PIL import Image, ImageOps, ImageDraw, ImageFont
from datetime import datetime
import locale
import random
import enum
import Eco
import ggr_utilities
from collections import namedtuple 
import os

secure_random = random.SystemRandom()

locale.setlocale(locale.LC_ALL, 'fr_FR') #For the french date format

textColor = (0,0,0,255)
ligneOffset = [20, 40, 75, 105, 135, 153]

userStruct = namedtuple("userStruct", ["name", "discriminator", "icon", "balance"])

class BestWorst(enum.Enum):
	best = 1
	worst = 2

def folderMaker():
	if not os.path.exists("tmp"):
		ggr_utilities.logger("Creating the folder tmp")
		os.makedirs("tmp")

def genRoundImg(source):
	bigsize = (source.size[0] * 3, source.size[1] * 3)
	mask = Image.new('L', bigsize, 0)
	draw = ImageDraw.Draw(mask) 
	draw.ellipse((0, 0) + bigsize, fill=255)
	mask = mask.resize(source.size, Image.ANTIALIAS)
	source.putalpha(mask)

def generateCertifMaster(profilePictureLink, pseudo, score):
	profile = Image.open(profilePictureLink).convert("RGBA") #profileg profile
	profile = profile.resize([512, 512]) #just to be sure

	certif = Image.open('img/template/certif_best.png', 'r')
	tampon = Image.open('img/academie_best.png', 'r')
	signature = Image.open('img/signature.png', 'r')

	profile_w, profile_h  = profile.size
	profileg_w, profileg_h = certif.size
	tampon_w, tampon_h = tampon.size
	signature_w, signature_h = signature.size
	
	genRoundImg(profile)

	certif.paste(profile, (768, 364, 768 + profile_w, 364 + profile_h), profile)

	draw = ImageDraw.Draw(certif)
	font = ImageFont.truetype(r'font/Times New Roman 400.ttf', 48) 

	now = datetime.now()
	date = now.strftime("%d %B %Y")
	time = now.strftime("%H:%M")

	W, H = certif.size
	text = "Au vu de la Mega Army exemplaire que vous avez invoqué le " + date + " à " + time
	w,h = font.getsize(text)
	draw.text(((W-w)/2, 1050), text=text, fill=textColor, font=font, anchor=None, spacing=0, align="left")

	text = "C'est avec honneur que le bot LongDuZbot décerne à " + pseudo + " le certificat de"
	w,h = font.getsize(text)
	draw.text(((W-w)/2, 1100), text=text, fill=textColor, font=font, anchor=None, spacing=0, align="left")

	text = "Maître des Saloperies avec un score de " + str(score) + " sur un maximum de 800 Saloperies."
	w,h = font.getsize(text)
	draw.text(((W-w)/2, 1150), text=text, fill=textColor, font=font, anchor=None, spacing=0, align="left")

	certif.paste(tampon, (1700, 750, 1700 + tampon_w, 750 + tampon_h), tampon)
	certif.paste(signature, (1400, 750, 1400 + signature_w, 750 + signature_h), signature)

	folderMaker()
	return certif.save("tmp/certif_best_filled.png")

def generateCertifBitch(profilePictureLink, pseudo, score):
	profile = Image.open(profilePictureLink).convert("RGBA") #profileg profile
	profile = profile.resize([512, 512]) #just to be sure

	certif = Image.open('img/template/certif_worst.png', 'r')
	tampon = Image.open('img/academie_worst.png', 'r')
	signature = Image.open('img/signature.png', 'r')

	profile_w, profile_h  = profile.size
	profileg_w, profileg_h = certif.size
	tampon_w, tampon_h = tampon.size
	signature_w, signature_h = signature.size

	genRoundImg(profile)

	certif.paste(profile, (768, 364, 768 + profile_w, 364 + profile_h), profile)

	draw = ImageDraw.Draw(certif)
	font = ImageFont.truetype(r'font/Times New Roman 400.ttf', 48) 

	now = datetime.now()
	date = now.strftime("%d %B %Y")
	time = now.strftime("%H:%M")
	
	W, H = certif.size
	text = "Au vu de la Mega Army de merde que vous avez invoqué le " + date + " à " + time
	w,h = font.getsize(text)
	draw.text(((W-w)/2, 1050), text=text, fill=textColor, font=font, anchor=None, spacing=0, align="left")

	text = "C'est avec déception que le bot LongDuZbot décerne à ce malchanceux " + pseudo + " le certificat de"
	w,h = font.getsize(text)
	draw.text(((W-w)/2, 1100), text=text, fill=textColor, font=font, anchor=None, spacing=0, align="left")

	text = "Jean-foutre des Saloperies avec un score de " + str(score) + " sur un maximum de 800 Saloperies."
	w,h = font.getsize(text)
	draw.text(((W-w)/2, 1150), text=text, fill=textColor, font=font, anchor=None, spacing=0, align="left")


	certif.paste(tampon, (1700, 750, 1700 + tampon_w, 750 + tampon_h), tampon)
	certif.paste(signature, (1400, 750, 1400 + signature_w, 750 + signature_h), signature)

	folderMaker()
	return certif.save("tmp/certif_worst_filled.png")

def cardSaloperieBestWorst(user, profilePictureLink, serverPictureLink, type):

	profile = Image.open(profilePictureLink).convert("RGBA")
	profile = profile.resize([128, 128])

	server = Image.open(serverPictureLink).convert("RGBA")
	server = server.resize([48, 48])

	fontCardBig = ImageFont.truetype(r'font/Helvetica.ttf', 48)
	fontCardIdentifier = ImageFont.truetype(r'font/Helvetica-Light.ttf', 20) 
	fontCard = ImageFont.truetype(r'font/Helvetica.ttf', 24) 
	fontCardAccent = ImageFont.truetype(r'font/Helvetica-Bold.ttf', 32)

	card = Image.open('img/template/card_master_saloperie_back.png', 'r')
	cardTop = Image.open('img/template/card_master_saloperie_front.png', 'r')

	genRoundImg(profile)
	card.paste(profile, (53, 21, 53 + profile.size[0], 21 + profile.size[1]), profile)

	genRoundImg(server)
	card.paste(server, (133, 101, 133 + server.size[0], 101 + server.size[1]), server)
	
	if (type == BestWorst.best):
		card.paste(cardTop, (0, 0, 0 + cardTop.size[0], 0 + cardTop.size[1]), cardTop)

	draw = ImageDraw.Draw(card)

	textName = ggr_utilities.treedotString(user.name, 12)
	textNameW,textNameH = fontCardBig.getsize(textName)
	draw.text((240, ligneOffset[0]), text=textName, fill=(255,255,255,255), font=fontCardBig, anchor=None, spacing=0, align="left")

	# textIdentifier = " #" + user.discriminator
	# textIdentifierW,textIdentifierH = fontCardIdentifier.getsize(textIdentifier)
	# draw.text((240 + textNameW, ligneOffset[1]), text=textIdentifier, fill=(255,255,255,127), font=fontCardIdentifier, anchor=None, spacing=0, align="left")

	if (type == BestWorst.best):
		l2Text = "est le maître des saloperies"
		l3Text = "avec un score de"
		l4Text = " saloperies invoquées !"


	elif (type == BestWorst.worst):
		l2Text = "est le jean-foutre"
		l3Text = "avec un score minable de"
		l4Text = " saloperies invoquées ..."


	l2TextW, l2TextH = fontCard.getsize(l2Text)
	draw.text((240, ligneOffset[2]), text=l2Text, fill=(255,255,255,255), font=fontCard, anchor=None, spacing=0, align="left")

	l3TextW, l3TextH = fontCard.getsize(l3Text)
	draw.text((240, ligneOffset[3]), text=l3Text, fill=(255,255,255,255), font=fontCard, anchor=None, spacing=0, align="left")

	l4Nbr = str(user.balance) #nombre de salopries mais flem de refaire une struct
	l4NbrW, l4NbrH = fontCardBig.getsize(l4Nbr)
	draw.text((240, ligneOffset[4]), text=l4Nbr, fill=(255,255,255,255), font=fontCardBig, anchor=None, spacing=0, align="left")

	l4TextW, l4TextH = fontCard.getsize(l4Text)
	draw.text((240 + l4NbrW, ligneOffset[5]), text=l4Text, fill=(255,255,255,255), font=fontCard, anchor=None, spacing=0, align="left")
	
	folderMaker()
	return card.save("tmp/card_filled.png")

def generateMoneyPodium(user1, user2, user3, serverPictureLink, serverName):
	profile1 = Image.open(user1.icon).convert("RGBA")
	profile1 = profile1.resize([128, 128])

	profile2 = Image.open(user2.icon).convert("RGBA")
	profile2 = profile2.resize([128, 128])

	profile3 = Image.open(user3.icon).convert("RGBA")
	profile3 = profile3.resize([128, 128])

	server = Image.open(serverPictureLink).convert("RGBA")
	server = server.resize([48, 48])

	#setup des font, on va bouger tout ca apres
	fontCardBig = ImageFont.truetype(r'font/Helvetica.ttf', 48)
	fontCardIdentifier = ImageFont.truetype(r'font/Helvetica-Light.ttf', 20) 
	fontCard = ImageFont.truetype(r'font/Helvetica.ttf', 24) 
	fontCardAccent = ImageFont.truetype(r'font/Helvetica-Bold.ttf', 32) 

	card = Image.open('img/template/top_wad_card_podium.png', 'r')

	genRoundImg(profile1)
	card.paste(profile1, (225, 21, 225 + profile1.size[0], 21 + profile1.size[1]), profile1)

	genRoundImg(profile2)
	card.paste(profile2, (21, 131, 21 + profile2.size[0], 131 + profile2.size[1]), profile2)

	genRoundImg(profile3)
	card.paste(profile3, (431, 151, 431 + profile3.size[0], 151 + profile3.size[1]), profile3)

	genRoundImg(server)
	card.paste(server, (21, 521, 21 + server.size[0], 521 + server.size[1]), server)

	draw = ImageDraw.Draw(card)

	serverNameText = serverName
	serverNameTextW,serverNameTextH = fontCard.getsize(serverNameText)
	draw.text((80, 535), text=serverNameText, fill=(255,255,255,127), font=fontCard, anchor=None, spacing=0, align="left")
	#----------------------------------------------------------------
	UserName1Text = ggr_utilities.treedotString(user1.name, 12)
	UserName1TextW,UserName1TextH = fontCard.getsize(UserName1Text)
	draw.text((290 - (UserName1TextW/2), 280), text=UserName1Text, fill=(255,255,255,127), font=fontCard, anchor=None, spacing=0, align="center")

	UserName2Text = ggr_utilities.treedotString(user2.name, 12)
	UserName2TextW,UserName2TextH = fontCard.getsize(UserName2Text)
	draw.text((85 - (UserName2TextW/2), 370), text=UserName2Text, fill=(255,255,255,127), font=fontCard, anchor=None, spacing=0, align="center")

	UserName3Text = ggr_utilities.treedotString(user3.name, 12)
	UserName3TextW,UserName3TextH = fontCard.getsize(UserName3Text)
	draw.text((495 - (UserName3TextW/2), 390), text=UserName3Text, fill=(255,255,255,127), font=fontCard, anchor=None, spacing=0, align="center")
	#----------------------------------------------------------------
	UserDiscriminator1Text = "#" + user1.discriminator
	UserDiscriminator1TextW,UserDiscriminator1TextH = fontCardIdentifier.getsize(UserDiscriminator1Text)
	draw.text((290 - (UserDiscriminator1TextW/2), 307), text=UserDiscriminator1Text, fill=(255,255,255,127), font=fontCardIdentifier, anchor=None, spacing=0, align="center")

	UserDiscriminator2Text = "#" + user2.discriminator
	UserDiscriminator2TextW,UserDiscriminator2TextH = fontCardIdentifier.getsize(UserDiscriminator2Text)
	draw.text((85 - (UserDiscriminator2TextW/2), 397), text=UserDiscriminator2Text, fill=(255,255,255,127), font=fontCardIdentifier, anchor=None, spacing=0, align="center")

	UserDiscriminator3Text = "#" + user3.discriminator
	UserDiscriminator3TextW,UserDiscriminator1TextH = fontCardIdentifier.getsize(UserDiscriminator3Text)
	draw.text((495 - (UserDiscriminator3TextW/2), 417), text=UserDiscriminator3Text, fill=(255,255,255,127), font=fontCardIdentifier, anchor=None, spacing=0, align="center")
	#----------------------------------------------------------------

	UserMoney1Text = str(user1.balance)
	UserMoney1TextW, UserMoney1TextH = fontCardBig.getsize(UserMoney1Text)
	draw.text((290 - (UserMoney1TextW/2), 450), text=UserMoney1Text, fill=(255,255,255,127), font=fontCardBig, anchor=None, spacing=0, align="center")

	UserMoney2Text = str(user2.balance)
	UserMoney2TextW, UserMoney2TextH = fontCardBig.getsize(UserMoney2Text)
	draw.text((85 - (UserMoney2TextW/2), 450), text=UserMoney2Text, fill=(255,255,255,127), font=fontCardBig, anchor=None, spacing=0, align="center")

	UserMoney3Text = str(user3.balance)
	UserMoney3TextW, UserMoney3TextH = fontCardBig.getsize(UserMoney3Text)
	draw.text((495 - (UserMoney3TextW/2), 450), text=UserMoney3Text, fill=(255,255,255,127), font=fontCardBig, anchor=None, spacing=0, align="center")

	wadsText = " " + Eco.moneyName(user1.balance)
	wadsTextW, wadsTextH = fontCardIdentifier.getsize(wadsText)
	draw.text((290 - (wadsTextW/2), 495), text=wadsText, fill=(255,255,255,127), font=fontCardIdentifier, anchor=None, spacing=0, align="center")
	draw.text((85 - (wadsTextW/2), 495), text=wadsText, fill=(255,255,255,127), font=fontCardIdentifier, anchor=None, spacing=0, align="center")
	draw.text((495 - (wadsTextW/2), 495), text=wadsText, fill=(255,255,255,127), font=fontCardIdentifier, anchor=None, spacing=0, align="center")

	folderMaker()
	return card.save("tmp/card_podium_filled.png")

def generateMoneyCard(user, serverPictureLink):
	ownSynonyms = ["possède", "cache au Fisc", "a", "détient", "dispose de", "garde", "conserve"]
	bankSynonyms = ["en banque.", "dans son portefeuille.", "dans son porte-monnaie."]
	
	profile = Image.open(user.icon).convert("RGBA")
	profile = profile.resize([128, 128])

	server = Image.open(serverPictureLink).convert("RGBA")
	server = server.resize([48, 48])

	fontCardBig = ImageFont.truetype(r'font/Helvetica.ttf', 48)
	fontCardIdentifier = ImageFont.truetype(r'font/Helvetica-Light.ttf', 20) 
	fontCard = ImageFont.truetype(r'font/Helvetica.ttf', 24) 
	fontCardAccent = ImageFont.truetype(r'font/Helvetica-Bold.ttf', 32) 

	card = Image.open('img/template/card.png', 'r')
	
	genRoundImg(profile)
	card.paste(profile, (20, 20, 20 + profile.size[0], 20 + profile.size[1]), profile)
	genRoundImg(server)
	card.paste(server, (100, 100, 100 + server.size[0], 100 + server.size[1]), server)

	draw = ImageDraw.Draw(card)

	textName = user.name + " "
	textNameW,textNameH = fontCardBig.getsize(textName)
	draw.text((188, ligneOffset[0]), text=textName, fill=(255,255,255,255), font=fontCardBig, anchor=None, spacing=0, align="left")

	# textIdentifier = "#" + user.discriminator
	# textIdentifierW,textIdentifierH = fontCardIdentifier.getsize(textIdentifier)
	# draw.text((188 + textNameW, ligneOffset[1]), text=textIdentifier, fill=(255,255,255,127), font=fontCardIdentifier, anchor=None, spacing=0, align="left")

	textOwn = secure_random.choice(ownSynonyms) + " "
	textOwnW,textOwnH = fontCard.getsize(textOwn)
	draw.text((188, ligneOffset[2]), text=textOwn, fill=(255,255,255,255), font=fontCard, anchor=None, spacing=0, align="left")

	textNumber = str(user.balance)
	textNumberW,textNumberH = fontCardAccent.getsize(textNumber)
	draw.text((188 + textOwnW, ligneOffset[2] - 5), text=textNumber, fill=(255,255,255,255), font=fontCardAccent, anchor=None, spacing=0, align="left")

	textMoneyName = " " + Eco.moneyName(user.balance)
	textMoneyNameW,textMoneyNameH = fontCard.getsize(textMoneyName)
	draw.text((188 + textOwnW + textNumberW, ligneOffset[2]), text=textMoneyName, fill=(255,255,255,255), font=fontCard, anchor=None, spacing=0, align="left")

	textInBank = secure_random.choice(bankSynonyms)
	textInBankW,textInBankH = fontCard.getsize(textInBank)
	draw.text((188, ligneOffset[3]), text=textInBank, fill=(255,255,255,255), font=fontCard, anchor=None, spacing=0, align="left")

	#card.show()
	folderMaker()
	return card.save("tmp/card_filled.png")

#generateMoneyCard("img/debug/avatar.png", "img/debug/server.png", "guigur", 200)