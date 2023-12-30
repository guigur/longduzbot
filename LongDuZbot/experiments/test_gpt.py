from PIL import Image, ImageDraw

# Set the tile size
tile_width = 512
tile_height = 512
tile_color = (255, 0, 0, 128)  # Red tile color with 50% transparency


background_image = Image.new("RGBA", (480, 854), tile_color)

background_image_path = "../ps/wad-texture.png"
tile = Image.open(background_image_path).convert("RGBA")


# List to store each frame of the GIF
frames = []
m = 2

# Create frames for the animation
for i in range(tile_width//m):
    # Create a new frame by pasting tiles side by side on the background image
	frame = background_image.copy()
	frame.paste(tile, ((i * m) - tile_width, i * m), mask=tile)
	frame.paste(tile, (i * m, (i * m) - tile_height), mask=tile)
	frame.paste(tile, (i * m, i * m), mask=tile) #down right
	frame.paste(tile, ((i * m) - tile_width, (i * m) - tile_height), mask=tile)
	frame.paste(tile, (i * m, (i * m) + tile_height), mask=tile)
	frame.paste(tile, ((i * m) - tile_width, (i * m) + tile_height), mask=tile)



	frames.append(frame)

# Save the frames as an animated GIF
frames[0].save("animated_tile.gif", save_all=True, append_images=frames[1:], optimize = True, duration=50, loop=0)
