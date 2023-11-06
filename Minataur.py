
#Read input

#For loop(s) to create all of the vertices in the graph model.

#For loop over the vertices to create the outgoing edges from each vertex.

#Run BFS (once)

#Process results from BFS (formatting, multiple shortest paths, etc.)

#Output answer

#reading the input 
def read_input_file(file_path):
    with open(file_path, 'r') as file:
        # Read the first line and extract the respective variables
        R, C, T_row, T_col, M_row, M_col, F_row, F_col = map(int, file.readline().split())

        # Initialize the maze grid
        maze_grid = []

        # Read the remaining lines and add them to the maze_grid list
        for line in file:
            maze_grid.append(line.strip().split())

        return {
            "maze_size": (R, C),
            "theseus_start": (T_row, T_col),
            "minotaur_start": (M_row, M_col),
            "finish": (F_row, F_col),
            "maze_grid": maze_grid
        }
#create the graph and begin implimenting the for loops to create the vertices
def create_graph(R, C, maze):
    graph = {(x, y): [] for x in range(R) for y in range(C)}

    directions = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}

    for i in range(R):
        for j in range(C):
            for direction in maze[i][j]:
                
    return graph

# Create the graph
graph = create_graph(R, C, maze)
