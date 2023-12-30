from PIL import Image, ImageDraw, ImageFont
import textwrap

# Set the tile size
tile_width = 512
tile_height = 512
tile_color = (255, 0, 0, 128)  # Red tile color with 50% transparency
image_width = 480
image_height = 854

image = Image.new("RGBA", (image_width, image_height), tile_color)
draw = ImageDraw.Draw(image)

background_image_path = "../img/wad_texture.png"
tile = Image.open(background_image_path).convert("RGBA")

# Load a font for the text
font_path = "../font/Montserrat-SemiBold.ttf"  # Replace with the path to your TrueType font file
font_size = 20
font = ImageFont.truetype(font_path, font_size)

# List to store each frame of the GIF
frames = []
m = 2

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


	text = "Vous avez invoqué 2000 saloperies cette année !"

	wrapped_text = textwrap.fill(text, width=20)  # Adjust the width as needed
	
	text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)

	text_position = ((image_width - text_bbox[2] - text_bbox[0]) // 2,10)

	draw_text = ImageDraw.Draw(frame)
	draw_text.text(text_position, wrapped_text, font=font, fill=(255, 255, 255, 255))

	frames.append(frame)

# Save the frames as an animated GIF
frames[0].save("animated_tile.gif", save_all=True, append_images=frames[1:], optimize = True, duration=50, loop=0)
