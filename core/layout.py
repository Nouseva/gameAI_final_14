import os

from core.grid import Grid

# The maze layouts can be found in resources/layouts
DEFAULT_LAYOUT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'layouts')

ENEMY_NUMS = ['1', '2', '3', '4']

class Layout(object):
    """
    A Layout manages the static information about the game board
    """

    def __init__(self, layoutText, maxEnemies = None):
        self.width  = len(layoutText[0])
        self.height = len(layoutText)
        self.walls  = Grid(self.width, self.height, initialValue = False)
        self.food   = Grid(self.width, self.height, initialValue = False)
        self.goal   = None
        
        self.agentPositions = []
        self.numEnemies = 0
        self.layoutText = layoutText

        self.processLayoutText(layoutText, maxEnemies)

    def getNumEnemies(self):
        return self.numEnemies

    def isWall(self, pos):
        x, y = pos
        return self.walls[x][y]
    
    def isGoal(self, pos):
        return self.goal == pos

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def getGoal(self):
        return self.goal

    def __str__(self):
        return '\n'.join(self.layoutText)

    def deepCopy(self):
        return Layout(self.layoutText[:])

    def processLayoutText(self, layoutText, maxEnemies):
        """
        Coordinates are flipped from the input format (layoutText[y][x]) to the
        conventional grid[x][y]
        The shape of the maze.
        Each character represents a different type of object:
        '''
            % - Wall
            G - Goal
            E - Enemy
            P - Player Agent
            o - Food
        '''
        Other characters are ignored
        """
        
        for y in range(self.height):
            for x in range(self.width):
                layoutChar = layoutText[y][x]
                self.processLayoutChar(x, y, layoutChar, maxEnemies)
        self.agentPositions.sort()
        self.agentPositions =[(i == 0, pos) for i, pos in self.agentPositions]

    def processLayoutChar(self, x, y, layoutChar, maxEnemies):
        if   layoutChar == '%':
            self.walls[x][y] = True
        elif layoutChar == 'G':
            self.goal = (x, y)
        elif layoutChar == 'o':
            self.food[x][y] == True
        elif layoutChar == 'P':
            self.agentPositions.append((0, (x, y)))
        elif layoutChar == 'E' and (maxEnemies is None or self.numEnemies < maxEnemies):
            self.agentPositions.append((1, (x, y)))
            self.numEnemies += 1
        # Should different enemies wish to be given different behaviors
        elif layoutChar in ENEMY_NUMS and (maxEnemies is None or self.numEnemies < maxEnemies):
            self.agentPositions.append((int(layoutChar), (x, y)))
            self.numEnemies += 1

def getLayout(name, layout_dir = DEFAULT_LAYOUT_DIR, maxEnemies = None):
    """Converts a given text doc into a Layout object
    """
    if (not name.endswith('.lay')):
        name += '.lay'

    path = os.path.join(layout_dir, name)
    if (not os.path.isfile(path)):
        raise Exception("Could not locate layout file: '%s'." % path)

    rows = []
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if line != '':
                rows.append(line)
    return Layout(rows, maxEnemies)

