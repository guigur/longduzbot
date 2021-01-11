from PIL import Image, ImageOps, ImageDraw, ImageFont
from datetime import datetime
import locale

locale.setlocale(locale.LC_ALL, 'fr_FR') #For the french date

textColor = (0,0,0,255)

def generateCertifMaster(profilePictureLink, pseudo, score):
    profile = Image.open(profilePictureLink) #profileg profile
    profile = profile.resize([512, 512]) #just to be sure

    certif = Image.open('img/certif.png', 'r')
    tampon = Image.open('img/academie.png', 'r')
    signature = Image.open('img/signature.png', 'r')

    profile_w, profile_h  = profile.size
    profileg_w, profileg_h = certif.size
    tampon_w, tampon_h = tampon.size
    signature_w, signature_h = signature.size

    bigsize = (profile.size[0] * 3, profile.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(profile.size, Image.ANTIALIAS)
    profile.putalpha(mask)

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

    return certif.save("tmp/certif_filled.png")

def generateCertifBitch(profilePictureLink, pseudo, score):
    profile = Image.open(profilePictureLink) #profileg profile
    profile = profile.resize([512, 512]) #just to be sure

    certif = Image.open('img/certif_pute.png', 'r')
    tampon = Image.open('img/academie_pute.png', 'r')
    signature = Image.open('img/signature.png', 'r')

    profile_w, profile_h  = profile.size
    profileg_w, profileg_h = certif.size
    tampon_w, tampon_h = tampon.size
    signature_w, signature_h = signature.size

    bigsize = (profile.size[0] * 3, profile.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(profile.size, Image.ANTIALIAS)
    profile.putalpha(mask)

    profile = ImageOps.fit(profile, mask.size, centering=(0.5, 0.5))
    profile.putalpha(mask)

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

    return certif.save("tmp/certif_pute_filled.png")