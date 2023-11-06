import sys
import networkx as nx
from networkx.drawing.nx_agraph import write_dot

# Function to load grid data from a file
def load_grid_data(file_name):
    with open(file_name, 'r') as f:
        # Reading from the first line of the file
        params = list(map(int, f.readline().split()))
        rows, cols, t_init_x, t_init_y, m_init_x, m_init_y, goal_x, goal_y = params
        
        # Reading the grid info
        grid_info = [f.readline().split() for _ in range(rows)]
    
    # Returning a dictionary
    return {
        'rows': rows, 
        'cols': cols, 
        'theseus_init': (t_init_x - 1, t_init_y - 1), 
        'minotaur_init': (m_init_x - 1, m_init_y - 1), 
        'goal_point': (goal_x - 1, goal_y - 1), 
        'grid_data': grid_info
    }

# Function to construct the initial state graph
def construct_graph(grid_data, rows, cols):
    graph = nx.DiGraph()
    for i in range(rows):
        for j in range(cols):
            for k in range(rows):
                for l in range(cols):
                    # Adding a node for each possible pair of Theseus and Minotaur positions
                    graph.add_node(((i, j), (k, l)))
    return graph

# Function to get the valid moves from a position
def valid_moves(position, grid_data):
    x, y = position
    return grid_data[x][y]

# Function to determine the next position based on the current position and a target position
def determine_next_position(curr_pos, target_pos, grid_data):
    x1, y1 = curr_pos
    x2, y2 = target_pos
    moves = valid_moves(curr_pos, grid_data)
    
    # Checking valid moves and updating the position 
    if y1 < y2 and 'E' in moves: 
        return x1, y1 + 1
    elif y1 > y2 and 'W' in moves: 
        return x1, y1 - 1
    elif x1 < x2 and 'S' in moves: 
        return x1 + 1, y1
    elif x1 > x2 and 'N' in moves: 
        return x1 - 1, y1
    else:
        return curr_pos

# Function to update the graph with edges representing valid moves
def update_graph(graph, goal_point, grid_data):
    new_graph = graph.copy()
    win_state = ((-1, -1), (-1, -1))
    
    for node in graph:
        theseus, minotaur = node
        theseus_moves = valid_moves(theseus, grid_data)
        
        # Adding a winning edge if Theseus reaches the goal point without Minotaur
        if theseus == goal_point and minotaur != goal_point:
            new_graph.add_edge(node, win_state)
            continue
        
        # Identifying possible directions for Theseus
        directions = [
            theseus,
            (theseus[0] - 1, theseus[1]) if 'N' in theseus_moves else theseus,
            (theseus[0], theseus[1] + 1) if 'E' in theseus_moves else theseus,
            (theseus[0] + 1, theseus[1]) if 'S' in theseus_moves else theseus,
            (theseus[0], theseus[1] - 1) if 'W' in theseus_moves else theseus,
        ]
        
        # Updating the graph with edges representing valid moves
        for new_position in directions:
            minotaur_1st_move = determine_next_position(minotaur, new_position, grid_data)
            minotaur_2nd_move = determine_next_position(minotaur_1st_move, new_position, grid_data)
            new_graph.add_edge(node, (new_position, minotaur_2nd_move))
    
    return new_graph

# Function to find and format the shortest path to the winning state
def shortest_path(graph, initial_state, win_state):
    try:
        # Finding all shortest paths
        paths = list(nx.all_shortest_paths(graph, source=initial_state, target=win_state))
        
        # Formatting the paths and returning the first one
        formatted_paths = format_paths(paths)
        formatted_paths.sort()
        return formatted_paths[0]
    except nx.NetworkXNoPath:
        return "NO PATH"

# Function to format the paths into a readable format
def format_paths(paths):
    formatted_paths = []
    for path in paths:
        moves = []
        for i in range(1, len(path) - 1):
            current, _ = path[i]
            previous, _ = path[i-1]
            
            # Identifying the direction of the move
            diff = (current[0] - previous[0], current[1] - previous[1])
            
            if diff == (-1, 0):
                moves.append('N')
            elif diff == (1, 0):
                moves.append('S')
            elif diff == (0, -1):
                moves.append('W')
            elif diff == (0, 1):
                moves.append('E')
            else:
                moves.append('X')
        
        # Adding the formatted path to the list
        formatted_paths.append(' '.join(moves))
    
    return formatted_paths

# Main function to execute the script
def main():
    # Getting the input file name
    file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    
    # Loading the grid data
    data = load_grid_data(file_name)
    
    # Constructing the initial graph
    graph = construct_graph(data['grid_data'], data['rows'], data['cols'])
    
    # Updating the graph with edges
    graph = update_graph(graph, data['goal_point'], data['grid_data'])
    
    # Finding the initial state and the winning state
    initial_state = (data['theseus_init'], data['minotaur_init'])
    win_state = ((-1, -1), (-1, -1))
    
    # Finding and printing the shortest path
    path_result = shortest_path(graph, initial_state, win_state)
    print(path_result)
    
    # Writing the graph to a file
   # write_dot(graph, "graph.dot")

# Checking if the script is run directly
if __name__ == "__main__":
    main()
