from PIL import Image, ImageDraw, ImageFilter

# Set the image size and tile size
image_width = 128
image_height = 128

# Create a new image with a white background
image = Image.new("RGB", (image_width, image_height), "white")
draw = ImageDraw.Draw(image)

# Open an image to be placed within the popping circle
circle_image_path = "../img/default/blue.png"
circle_image = Image.open(circle_image_path).resize((128, 128))  # Adjust the size as needed

# Ensure that the image has an alpha channel
circle_image = circle_image.convert("RGBA")

# List to store each frame of the GIF
frames = []

# Set the diameter of the circle
circle_diameter = 128

# Calculate the position for the center of the circle
center_x = image_width // 2
center_y = image_height // 2

# Create frames for the animation
for i in range(30):  # Adjust the number of frames as needed
    # Create a new frame
    frame = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
    
    # Calculate the radius of the circle based on the animation frame
    radius = i * (circle_diameter / 30)

    # Create a mask for the circle
    mask = Image.new("L", frame.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse(
        (
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius
        ),
        fill=255
    )

    # Create a copy of the circle image and apply blur to the RGB part
    blurred_circle = circle_image.copy()
    blurred_circle.paste(blurred_circle.filter(ImageFilter.GaussianBlur(radius=i)), (0, 0), blurred_circle.split()[-1])

    # Paste the blurred circle onto the frame using the mask
    frame.paste(blurred_circle, (center_x - circle_image.width // 2, center_y - circle_image.height // 2), mask=mask)

    frames.append(frame)

# Reverse the frames to create the popping out effect
frames += frames[::-1]

# Save the frames as an animated GIF
frames[0].save("popping_circle_with_blur.gif", save_all=True, append_images=frames[1:], duration=100, loop=0)
