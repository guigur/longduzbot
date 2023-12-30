from PIL import Image, ImageDraw 

images = [] 

width = 480
height = 720
centerW = width // 2
centerH = height // 2
color_1 = (0,255, 0) 
color_2 = (255, 0, 0) 
max_radius = int(centerH * 1.5) 
step = 60

for i in range(0, max_radius, step): 
    im = Image.new('RGB', (width, height), color_2) 
    draw = ImageDraw.Draw(im) 
    draw.ellipse((centerW - i, centerH - i, centerW + i, centerH + i), fill = color_1) 
    images.append(im) 

images[0].save('pillow_imagedraw.gif', 
               save_all = True, append_images = images[1:],  
               optimize = True, duration = 60)

