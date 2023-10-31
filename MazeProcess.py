from PIL import Image, ImageDraw

def process_image_to_uniform_pixel_size(image_path, pixel_size = 200):
    try:
        # Open the image
        img = Image.open(image_path)

        # Create a new image with uniform pixel size
        uniform_img = img.resize((pixel_size, pixel_size))

        # Save or display the image with uniform pixel size
        #uniform_img.show()
        
        # Optionally, save the processed image
        uniform_img.save('processed.png')

    except Exception as e:
        print(str(e))

def process_and_simplify_maze(image_path, threshold, scale_factor):
    try:
        # Open the image
        img = Image.open(image_path)

        # Convert the image to grayscale
        img = img.convert('L')

        # Create a new simplified image
        simplified_img = Image.new('1', img.size, 255)  # '1' mode for 1-bit pixel (white)

        # Create a drawing object for the simplified image
        draw = ImageDraw.Draw(simplified_img)

        # Initialize variables to track adjacent pixels
        current_value = None
        current_count = 0

        # Iterate through the pixels of the grayscale image
        for y in range(img.height):
            for x in range(img.width):
                pixel_value = img.getpixel((x, y))

                # Check if the pixel is similar to the current group
                if current_value is None or abs(pixel_value - current_value) < threshold:
                    current_value = pixel_value
                    current_count += 1
                else:
                    # Draw the current group on the simplified image
                    if current_value < 128:  # Adjust threshold as needed
                        draw.rectangle((x - current_count, y, x, y + 1), fill=0)

                    # Reset the tracking variables for the new group
                    current_value = pixel_value
                    current_count = 1

        # Save or display the simplified image
        simplified_img = simplified_img.resize((img.width // scale_factor, img.height // scale_factor))
        simplified_img.save("simple.png")

    except Exception as e:
        print(str(e))
        return None

def crop_maze(image_path):
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Convert the image to grayscale
        img = img.convert('L')
        
        # Define a threshold value to convert pixels to 0 or 255 (white)
        threshold = 128
        
        # Create a bounding box around the maze
        left, top, right, bottom = img.width, img.height, 0, 0
        
        for y in range(img.height):
            for x in range(img.width):
                pixel_value = img.getpixel((x, y))
                if pixel_value < threshold:
                    # Update the bounding box coordinates
                    left = min(left, x)
                    top = min(top, y)
                    right = max(right, x)
                    bottom = max(bottom, y)
        
        # Crop the image to the bounding box
        cropped_img = img.crop((left, top, right, bottom))
        
        # Save or display the cropped image
        cropped_img.save("cropped.png")
        return cropped_img
    except Exception as e:
        print(str(e))

def draw_maze_from_string(maze_string):
    try:
        # Split the maze string into rows
        maze_rows = maze_string.strip().split('\n')
        
        # Calculate the dimensions of the maze
        num_rows = len(maze_rows)
        num_cols = len(maze_rows[0].split('\t'))
        
        # Create a blank image with white background
        img_width = num_cols * 20   # You can adjust the cell size as needed
        img_height = num_rows * 20  # You can adjust the cell size as needed
        img = Image.new('RGB', (img_width, img_height), 'white')
        draw = ImageDraw.Draw(img)
        pixelSize = 20
        
        for y, row in enumerate(maze_rows):
            cell_values = row.split('\t')
            for x, value in enumerate(cell_values):
                if value == '1':
                    # Draw a black square for walls
                    draw.rectangle([x * 20, y * 20, (x + 1) * 20, (y + 1) * 20], fill='black')
                elif value == 'S':
                    # Draw a green square for the start point
                    draw.rectangle([x * 20, y * 20, (x + 1) * 20, (y + 1) * 20], fill='green')
                elif value == 'E':
                    # Draw a red square for the end point
                    draw.rectangle([x * 20, y * 20, (x + 1) * 20, (y + 1) * 20], fill='blue')
                elif value == 'x':
                    # Draw a red square for the end point
                    draw.rectangle([x * pixelSize, y * pixelSize, (x + 1) * pixelSize, (y + 1) * pixelSize], fill='red')
        
        # Save or display the image
        img.show()
        img.save("output.png")
    except Exception as e:
        print(str(e))

def image_to_maze_string(image_path):
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Convert the image to grayscale
        img = img.convert('L')
        
        # Define a threshold value to convert pixels to 0 or 1
        threshold = 128
        
        maze_data = []
        
        # Process each pixel in the image
        for y in range(img.height):
            row = []
            for x in range(img.width):
                pixel_value = img.getpixel((x, y))
                if pixel_value < threshold:
                    row.append('1')  # Empty space
                else:
                    row.append('0')  # Wall
            maze_data.append(row)
        
        # Convert the maze data into a string
        maze_string = '\n'.join(['\t'.join(row) for row in maze_data])

        dimensions = (len(maze_data), len(maze_data[0]))
        
        return dimensions, maze_string
    except Exception as e:
        return str(e)

def main():
    # Provide the path to your maze image
    image_path = 'maze.jpg'  # main image
    cropped = 'cropped.png' # cropped image
    simple = 'simple.png' # scaled down image
    scale = 'processed.png'
    
    threshold = 24  # Adjust this threshold to control pixel similarity
    scale_factor = 4  # Adjust this factor to control the size reduction

    # 1. Scale down the image
    process_and_simplify_maze(image_path, threshold, scale_factor)
    # 2. Crop the iameg
    crop_maze(simple)
    # 3. Make it the same pixel size
    process_image_to_uniform_pixel_size(cropped)
    # 4. Convert image into string
    dimensions, maze_string = image_to_maze_string(scale)

    if maze_string:
        with open("output.txt", "w") as file:
            file.write(str(dimensions[0]) + " " + str(dimensions[1]) + "\n")
            file.write(maze_string)
    else:
        print("Failed to process the image.")

if __name__ == "__main__":
    main()