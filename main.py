from Solver import *
from MazeProcess import *

filename = "output.txt"

# show initial maze
with open(filename, "r") as file:
    inputenv = file.readlines()

maze = ""
for line in inputenv[1:]:
    maze += line
#draw_maze_from_string(maze)

input()

filename = "output.txt"

mygrid, width, height, start, end = construct_environment(filename)
result = aStar(mygrid, width, height, start, end)

if result:
    path, cost = result
    output_string = show_movement(mygrid, path, height)

draw_maze_from_string(output_string)


# process the picture to reduce the pixel size and cropped
def process_maze_photo(filename):
    pass
#dimensions, maze_string = image_to_maze_string("processed_image.png")
#draw_maze_from_string(maze_string)
#filename = "output.txt"
#with open(filename, "w") as file:
#    file.write(maze_string)