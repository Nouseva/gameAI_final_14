
import pygame.sprite
import operator

# self.equipment = dict()
from random import choice
from . import utils

def calculateValue(pos, layout, depth, discount):
    discountMultiplier = discount**depth
    value = 0
    if layout.isEnemy(pos):
        value = 60
    elif layout.isFood(pos):
        value = 40
    # elif (object == '.'):
    #     value = 10
    elif layout.isRoad(pos):
        value = 20
    elif layout.isBoost(pos):
        value == 30
    elif layout.isGoal(pos):
        value == 5000
    # elif (object == 'P'):
    # assume that only option remaining is plain empty space
    else:
        value = 10

    finalValue = discountMultiplier * value
    return finalValue

def default_heuristic(self, equiped_list, pos, layout):
    # print('adj_val', adj_value)
    heur = 0
    # empty_list = ['.', ',' ,'-']
    #if enemey
    if 'Claws' in equiped_list and layout.isEnemy(pos):
        heur = -60
    #if no enemy, but treasure
    elif 'Backpack' in equiped_list and layout.isFood(pos):
        heur = -40
    #if no enemy and no treasure
    elif 'Wheels' in equiped_list and (layout.isRoad(pos) or layout.isBoost(pos)):
        heur = -10
    else:
        heur = 100
    return heur

class Agent(pygame.sprite.Sprite):
    """
    An agent is something in the world that does something
    Enemy, game/player character

    Agents must define Agent.getAction method,
    but can otherwise overwrite any other methods.

    Methods must assume that they are working with shalow copies of data
    Deep copies must be made of anything they want to keep


    """

    def __init__(self, image, equipment, tile_size, heuristic = default_heuristic, pos = None, index = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image(image, scale = tile_size, colorkey = -1)
        self.tile_size = tile_size
        if pos:
            self.rect = self.rect.move((self.tile_size[0] * pos[0], self.tile_size[1] * pos[1]))
            self.pos  = utils.Point(pos[0], pos[1])
        else:
            x, y  = utils.nearestPoint((self.rect[0] / self.tile_size[0], self.rect[1] / self.tile_size[1]))
            self.pos = utils.Point(x, y)
        # self.rect = utils.nearestPoint(self.rect)
    
        self.index = index
        self.equipment = equipment
        self.heuristic = heuristic
        # self.bump  = utils.load_sound('collision.ogg')

    def update(self, list_of_components, layout):
        """Move based on the action that was given

        Args:
            action (tuple): a direction normalized to a maze step
            walls (list): Rects which are the maze walls

        Returns:
            : False if action will cause agent to collide with walls, True otherwise

        """
        # Agent is enemy
        if self.index > 0:
            move = self.getRandNeighbor(layout)

        # Agent is player
        else:
            move, _ = self.calculateBestMove(layout, self.pos, [], dict(), 0, 10)

        print('best_move', move)
        print('current_pos', self.pos)
        directional_move = (move[0] - self.pos.x, move[1]- self.pos.y)
        pix_move = utils.pos_to_coord(directional_move, self.tile_size)
        print('pix_move', pix_move)

        self.rect = self.rect.move(pix_move)
        self.pos  = move
        # collision = self.rect.collidelist(layout.walls.asList())
        lvl_complete = layout.isGoal(self.pos)
        return lvl_complete

    def getRect(self):
        return self.rect

    def getVision(self):
        if 'Googles' in self.equipment:
            return 8
        else:
            return 5

    def getRandNeighbor(self, layout):
        north = self.pos + utils.Point(0, 1)
        east  = self.pos + utils.Point(1, 0)
        south = self.pos + utils.Point(0, -1)
        west  = self.pos + utils.Point(-1, 0)
        stop  = self.pos

        directions = [north, east, south, west, stop]
        print(directions)
        valid = []
        for d in directions:
            if not layout.isWall(d.tup):
                valid.append(d)
        move = choice(valid)

        return move

    #return values are best move, which would be 0 = N, 1 = E, 2 = S, 3 = W.
    #The second return value is heuristic score for computation of best move associated with that step.
    def calculateBestMove(self, layout, current_pos, historyList, valuesDict, depth, discount):

        #if reached peak of depth then end the recursion
        if (self.getVision() == depth):
            return 0, 0


        #4 possible moves, North, East, South, West. They all start with a heuristical value of 0, and the final return value will be a value which will correspond with the direction to take. 1 for north 2 for east 3 for south 4 for west.
        north = current_pos + utils.Point(0, 1)
        east  = current_pos + utils.Point(1, 0)
        south = current_pos + utils.Point(0, -1)
        west  = current_pos + utils.Point(-1, 0)
        index_to_position = [north, east, south, west]
        # nObj = layout[currentX][currentY+1]
        # eObj = layout[currentX+1][currentY]
        # sObj = layout[currentX][currentY-1]
        # wObj = layout[currentX-1][currentY]
        valuesArr = [0] * 4#this is used in the future to find max index and value.

        #if moving in that direction is a wall, or a place we have been before, we do no calculations and never go in that direction. Calculate values for all four directions.
        if (layout.isWall(north) or current_pos in historyList):
            print(depth, ': invalid north')
            nValue = -1000
        else:
            historyList.append(current_pos)
            _, nFutureValue = self.calculateBestMove(layout, north, historyList, valuesDict, depth+1, discount)
            nValue = calculateValue(north, layout, depth, discount) + nFutureValue + self.heuristic(self, self.equipment, north, layout)
        valuesArr[0] = nValue

        if (layout.isWall(east) or current_pos in historyList):
            print(depth, ': invalid east')
            eValue = -1000
        else:
            historyList.append(current_pos)
            _, eFutureValue = self.calculateBestMove(layout, east, historyList, valuesDict, depth+1, discount)
            eValue = calculateValue(east, layout, depth, discount) + eFutureValue + self.heuristic(self, self.equipment, east, layout)
        valuesArr[1] = eValue

        if (layout.isWall(south) or current_pos in historyList):
            print(depth, ': invalid south')
            sValue = -1000
        else:
            historyList.append(current_pos)
            _, sFutureValue = self.calculateBestMove(layout, south, historyList, valuesDict, depth+1, discount)
            sValue = calculateValue(south, layout, depth, discount) + sFutureValue + self.heuristic(self, self.equipment, south, layout)
        valuesArr[2] = sValue

        if (layout.isWall(west) or current_pos in historyList):
            print(depth, ': invalid west')
            wValue = -1000
        else:
            historyList.append(current_pos)
            _, wFutureValue = self.calculateBestMove(layout, west, historyList, valuesDict, depth+1, discount)
            wValue = calculateValue(west, layout, depth, discount) + wFutureValue  + self.heuristic(self, self.equipment, west, layout)
        valuesArr[3] = wValue

        print(valuesArr)
        #out of all the options presented, return the move, which should be max index, and the heuristical value which is needed for any recursive calculations.
        max_index, max_value = max(enumerate(valuesArr), key=operator.itemgetter(1))
        return index_to_position[max_index], max_value

