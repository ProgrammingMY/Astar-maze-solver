import heapq


def find_size(size):
	#find how many digit for width and height are
	# total length minus 3(\t, \r, \n) then divided by 2(height and width)
	digit = size.split(" ")

	return int(digit[0]), int(digit[1])

def construct_environment(filename):
    with open(filename, 'r') as env:
        inputenv = env.readlines()

    # Get width and height of the environment
    size = inputenv[0]
    width, height = find_size(size)

    grid = [['0' for _ in range(width)] for _ in range(height)]
    start, end = None, None

    # Construct a grid of environment
    for i in range(height):
        line = inputenv[i + 1]
        for j in range(width):
            grid[i][j] = line[j * 2]
            if line[j * 2] == "S":
                start = (i, j)
            if line[j * 2] == "E":
                end = (i, j)

    return grid, width, height, start, end

def show_movement(grid, path, height):
    output_string = ""
    start = path[0]
    grid[start[0]][start[1]] = "S"
    
    for position in path[1:]:
          grid[position[0]][position[1]] = "x"
    
    end = path[-1]
    grid[end[0]][end[1]] = "E"
    
    for i in range(height):
        output_string += "\t".join(grid[i])
        output_string += "\n"
        
    with open("final.txt", "w") as file:
        file.write(output_string)
        
    return output_string

# Define possible movements (up, down, left, right)
movements = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def heuristic(node, goal):
    # Calculate the Manhattan distance as the heuristic
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def aStar(grid, width, height, start, end):
    # Check if start and end are within the grid boundaries
    if not (0 <= start[0] < width) or not (0 <= start[1] < height) or not (0 <= end[0] < width) or not (0 <= end[1] < height):
        return None

    # Initialize data structures
    open_set = []
    heapq.heappush(open_set, (0, start))  # Priority queue with (f, node)
    came_from = {}
    g_score = {node: float('inf') for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float('inf') for row in grid for node in row}
    f_score[start] = heuristic(start, end)

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            # Reconstruct the path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return [path, g_score[end]]

        for dx, dy in movements:
            neighbor = (current[0] + dx, current[1] + dy)

            if 0 <= neighbor[0] < width and 0 <= neighbor[1] < height:
                tentative_g_score = g_score[current] + 1  # Assuming each step has a cost of 1
                print(tentative_g_score)

                # Check if the neighbor is not yet in g_score (initialize it with infinity)
                if neighbor not in g_score:
                    g_score[neighbor] = float('inf')
                    

                if tentative_g_score < g_score[neighbor] and grid[neighbor[0]][neighbor[1]] in ['0', 'E']:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    # No path found
    return None
        
if __name__ == "__main__":
    # construct the environment
    filename = "testgrid_large.txt"
    mygrid, width, height, start, end = construct_environment(filename)
    
    result = aStar(mygrid, width, height, start, end)
    
    if result:
        path, cost = result
        print("Path found.")
    else:
        print("No path found.")
     
	





