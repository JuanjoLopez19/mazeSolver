from queue import PriorityQueue

# Variable initialization that represents the maze walls and its dimensions
walls = [
            (1,1,3),(1,1,1),(1,2,1),(1,3,1),(1,4,1),(1,4,0),(1,5,1),(1,5,3),(1,6,1),(1,7,1),(1,7,0),
            (2,1,3),(2,1,0),(2,2,2),(2,2,3),(2,3,0),(2,3,2),(2,4,0),(2,4,3),(2,5,3),(2,5,0),(2,6,3),(2,6,0),(2,7,3),(2,7,0),
            (3,1,3),(3,1,2),(3,2,0),(3,2,1),(3,3,1),(3,3,3),(3,4,0),(3,4,2),(3,5,0),(3,5,2),(3,5,3),(3,6,0),(3,6,3),(3,7,0),(3,7,3),
            (4,1,1),(4,1,3),(4,2,0),(4,2,2),(4,3,0),(4,3,4),(4,4,3),(4,4,1),(4,4,2),(4,5,1),(4,5,2),(4,6,0),(4,7,3),
            (5,1,0),(5,1,3),(5,2,1),(5,2,3),(5,4,1),(5,5,1),(5,6,0),(5,7,0),(5,7,3),
            (6,1,2),(6,1,3),(6,2,2),(6,3,2),(6,4,2),(6,5,2),(6,6,2),(6,7,2),(6,7,0)
]

rows = 7
cols = 8

# Class that represents the maze cells
class complex_maze_cell:
    def __init__(self,x,y,g):

        """
            @param x: x coordinate of the cell
            @param y: y coordinate of the cell
            @param g: direction of the movement 
        """
        self.x=x
        self.y=y
        self.g=g

    def position(self):

        """
            @return: the position of the cell without the direction of the movement
        """
        return (self.x,self.y)

    def complex_position(self):

        """
            @return: the position of the cell with the direction of the movement
        """
        return (self.x,self.y,self.g)

# Heuristic function
def h(cell1,cell2):

    """
        @param cell1: start cell
        @param cell2: objective cell
        @return: the manhattan distance between the two cells
    """
    x1,y1=cell1
    x2,y2=cell2

    return abs(x1-x2) + abs(y1-y2)

def aStar(start, goal, walls, maze):

    """
        @param start: start cell
        @param goal: goal cell
        @param walls: list of maze's walls
        @param maze: each cell of the maze defined by its coordinates and its direction of movement
        @return: the path from the start cell to the objective cell using the A* algorithm with the manhattan distance as heuristic function
    """

    # First, make the heuristics for each cell and initialize the initial cell
    g_score={cell.complex_position():float('inf') for cell in maze}
    g_score[start.complex_position()]=0
    
    f_score={cell.complex_position():float('inf') for cell in maze}
    f_score[start.complex_position()]=h(start.position(),goal.position())
    

    # Initialize the open sets
    open_set = PriorityQueue() # The open set is a priority queue that will be ordered by the f_score first, then the g_score and finally the position of the cell
    open_set.put((h(start.position(),goal.position()),h(start.position(),goal.position()),start.complex_position()))

    # Initialize the closed set
    aPath = {}  
    while not open_set.empty(): # While the open set is not empty, pop the cell with the lowest f_score
        current = open_set.get()[2]
        if (current[0], current[1]) == goal.position(): # If the current cell is the goal cell, exit the loop 
            break

        for i in range(4): 
            temp_cell = complex_maze_cell(current[0], current[1], i) # For each direction of movement, create a temporary cell to check if it is a valid cell to move
            if temp_cell.complex_position() in walls: # If the temporary cell is a wall, continue to the next direction of movement
                continue
            else: # Create a new cel with the new position and the new direction of movement
                if i == 0:
                    new_cell = complex_maze_cell(current[0], current[1] + 1, i) 
                elif i == 1:
                    new_cell = complex_maze_cell(current[0] - 1, current[1], i)
                elif i == 2:
                    new_cell = complex_maze_cell(current[0] + 1, current[1], i)
                elif i == 3:
                    new_cell = complex_maze_cell(current[0], current[1] - 1, i)

                temp_g_score=g_score[current]+1 # Calculate the new g_score by adding 1 to the previous g_score
                temp_f_score=temp_g_score+h(new_cell.position(),goal.position()) # Calculate the new f_score by adding the new g_score to the manhattan distance between the new cell and the goal cell
                
                if temp_f_score < f_score[new_cell.complex_position()]: # If the new f_score is lower than the previous f_score, update the f_score and the g_score
                    g_score[new_cell.complex_position()]=temp_g_score
                    f_score[new_cell.complex_position()]=temp_f_score
                    open_set.put((temp_f_score,h(new_cell.position(),goal.position()),new_cell.complex_position()))
                    aPath[new_cell.complex_position()]=current # Update the path

    fwdPath={}

    for i in range (4):
        temp = (goal.position()[0], goal.position()[1],i)
        try:
            aPath[temp]
            cell = temp
            break
        except KeyError:
            pass

    # Create the path from the goal cell to the start cell
    while cell!=start.complex_position():
        fwdPath[aPath[cell]]=cell
        cell=aPath[cell]

    # return the path from the start cell to the goal cell, and the g and f scores
    return fwdPath, g_score, f_score


# Main program
if __name__=='__main__':
    
    # Create the maze, defining each cell by its coordinates and its direction of movement
    maze = []
    for i in range(rows):
        for j in range(cols):
            for k in range(4):
                maze.append(complex_maze_cell(i,j,k))

    # Call the A* algorithm
    path, g, f = aStar(complex_maze_cell(4,1,0), complex_maze_cell(4,7,0), walls, maze)

    # Print the path from the start cell to the goal cell, and its values
    for key, value in path.items().__reversed__():
        print("Initial cell: {} (g value:{} --- f value: {}) --> goes to: {} (g value:{} --- f value: {}) ".format(key,g[key], f[key],value ,g[value], f[value]))

    print("The number of rules are: {}".format(len(path)))





