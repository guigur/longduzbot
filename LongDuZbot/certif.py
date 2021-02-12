from PIL import Image, ImageOps, ImageDraw, ImageFont
from datetime import datetime
import locale
import random

secure_random = random.SystemRandom()

locale.setlocale(locale.LC_ALL, 'fr_FR') #For the french date

textColor = (0,0,0,255)

def genRoundImg(source):
	bigsize = (source.size[0] * 3, source.size[1] * 3)
	mask = Image.new('L', bigsize, 0)
	draw = ImageDraw.Draw(mask) 
	draw.ellipse((0, 0) + bigsize, fill=255)
	mask = mask.resize(source.size, Image.ANTIALIAS)
	source.putalpha(mask)

def generateCertifMaster(profilePictureLink, pseudo, score):
	profile = Image.open(profilePictureLink) #profileg profile
	profile = profile.resize([512, 512]) #just to be sure

	certif = Image.open('img/template/certif_best.png', 'r')
	tampon = Image.open('img/academie_best.png', 'r')
	signature = Image.open('img/signature.png', 'r')

	profile_w, profile_h  = profile.size
	profileg_w, profileg_h = certif.size
	tampon_w, tampon_h = tampon.size
	signature_w, signature_h = signature.size
	
	genRoundImg(profile)

	profile = ImageOps.fit(profile, mask.size, centering=(0.5, 0.5))
	profile.putalpha(mask)

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

	text = "Maître des Saloperies avec un score de " + str(score) + " sur un maximum de 800 Saloperies"
	w,h = font.getsize(text)
	draw.text(((W-w)/2, 1150), text=text, fill=textColor, font=font, anchor=None, spacing=0, align="left")

	certif.paste(tampon, (1700, 750, 1700 + tampon_w, 750 + tampon_h), tampon)
	certif.paste(signature, (1400, 750, 1400 + signature_w, 750 + signature_h), signature)

	return certif.save("tmp/certif_best_filled.png")

def generateCertifBitch(profilePictureLink, pseudo, score):
	profile = Image.open(profilePictureLink) #profileg profile
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
	draw.text(((W-w)/2, 1000), text=text, fill=textColor, font=font, anchor=None, spacing=0, align="left")

	text = "C'est avec déception que le bot LongDuZbot décerne à cette merde de " + pseudo + " le certificat de"
	w,h = font.getsize(text)
	draw.text(((W-w)/2, 1050), text=text, fill=textColor, font=font, anchor=None, spacing=0, align="left")

	text = "la Pute des Saloperies avec un score de " + str(score) + " sur un maximum de 800 Saloperies"
	w,h = font.getsize(text)
	draw.text(((W-w)/2, 1100), text=text, fill=textColor, font=font, anchor=None, spacing=0, align="left")

	text = "Maintenant au travail la pute !"
	w,h = font.getsize(text)
	draw.text(((W-w)/2, 1150), text=text, fill=textColor, font=font, anchor=None, spacing=0, align="middle")

	certif.paste(tampon, (1700, 750, 1700 + tampon_w, 750 + tampon_h), tampon)
	certif.paste(signature, (1400, 750, 1400 + signature_w, 750 + signature_h), signature)

	return certif.save("tmp/certif_worst_filled.png")

def generateMoneyCard(profilePictureLink, serverPictureLink, ctx, money):
	ownSynonyms = ["possède", "cache au Fisc", "a", "détient", "dispose de", "garde", "conserve"]
	bankSynonyms = ["en banque.", "dans son portefeuille.", "dans son porte-monnaie."]
	profile = Image.open(profilePictureLink).convert("RGBA")
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
	ligneOffset = [20, 40, 85, 110]

	draw = ImageDraw.Draw(card)

	textName = ctx.author.name + " "
	textNameW,textNameH = fontCardBig.getsize(textName)
	draw.text((188, ligneOffset[0]), text=textName, fill=(255,255,255,255), font=fontCardBig, anchor=None, spacing=0, align="left")

	textIdentifier = "#" + ctx.author.discriminator
	textIdentifierW,textIdentifierH = fontCardIdentifier.getsize(textIdentifier)
	draw.text((188 + textNameW, ligneOffset[1]), text=textIdentifier, fill=(255,255,255,127), font=fontCardIdentifier, anchor=None, spacing=0, align="left")

	textOwn = secure_random.choice(ownSynonyms) + " "
	textOwnW,textOwnH = fontCard.getsize(textOwn)
	draw.text((188, ligneOffset[2]), text=textOwn, fill=(255,255,255,255), font=fontCard, anchor=None, spacing=0, align="left")

	textNumber = str(money)
	textNumberW,textNumberH = fontCardAccent.getsize(textNumber)
	draw.text((188 + textOwnW, ligneOffset[2] - 5), text=textNumber, fill=(255,255,255,255), font=fontCardAccent, anchor=None, spacing=0, align="left")

	textMoneyName = " WADs"
	textMoneyNameW,textMoneyNameH = fontCard.getsize(textMoneyName)
	draw.text((188 + textOwnW + textNumberW, ligneOffset[2]), text=textMoneyName, fill=(255,255,255,255), font=fontCard, anchor=None, spacing=0, align="left")

	textInBank = secure_random.choice(bankSynonyms)
	textInBankW,textInBankH = fontCard.getsize(textInBank)
	draw.text((188, ligneOffset[3]), text=textInBank, fill=(255,255,255,255), font=fontCard, anchor=None, spacing=0, align="left")

	#card.show()
	return card.save("tmp/card_filled.png")

#generateMoneyCard("img/debug/avatar.png", "img/debug/server.png", "guigur", 200)