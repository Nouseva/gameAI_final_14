
import pygame.sprite
import operator

from . import utils

def calculateValue(object, depth, discount):
    discountMultiplier = discount**depth
    if (object == 'E'):
        value = 60
    elif (object == '.'):
        value = 10
    elif (object == ','):
        value = 20
    elif (object == '-'):
        value == 30
    elif (object == 'G'):
        value == 0
    elif (object == 'P'):
        value = 0

    finalValue = discountMultiplier * value
    return finalValue
#return values are best move, which would be 0 = N, 1 = E, 2 = S, 3 = W.
#The second return value is heuristic score for computation of best move associated with that step.
def calculateBestMove(mapArr, currentX, currentY, historyList, valuesDict, visionScore, depth, discount):
    #if reached peak of depth then end the recursion
    if (visionScore == depth):
        return 0, 0


    #4 possible moves, North, East, South, West. They all start with a heuristical value of 0, and the final return value will be a value which will correspond with the direction to take. 1 for north 2 for east 3 for south 4 for west.
    nObj = mapArr[currentX][currentY+1]
    eObj = mapArr[currentX+1][currentY]
    sObj = mapArr[currentX][currentY-1]
    wObj = mapArr[currentX-1][currentY]
    valuesArr= [0] * 4 #this is used in the future to find max index and value.
    historyList.append((currentX, currentY))

    #if moving in that direction is a wall, or a place we have been before, we do no calculations and never go in that direction. Calculate values for all four directions.
    if (nObj == '%' or (currentX, currentY) in historyList):
        nValue = -1000
    else:
        _, nFutureValue = calculateBestMove(mapArr, currentX, currentY+1, historyList, valuesDict, visionScore, depth+1, discount)
        nValue = calculateValue(nObj, depth, discount) + nFutureValue # + hueristic()
        valuesArr[0] = nValue

    if (eObj == '%' or (currentX, currentY) in historyList):
        eValue = -1000
    else:
        _, eFutureValue = calculateBestMove(mapArr, currentX+1, currentY, historyList, valuesDict, visionScore, depth+1, discount)
        eValue = calculateValue(eObj, depth, discount) + eFutureValue # + hueristic()
        valuesArr[1] = eValue

    if (sObj == '%' or (currentX, currentY) in historyList):
        sValue = -1000
    else:
        _, sFutureValue = calculateBestMove(mapArr, currentX, currentY-1, historyList, valuesDict, visionScore, depth+1, discount)
        sValue = calculateValue(sObj, depth, discount) + sFutureValue # + hueristic()
        valuesArr[2] = sValue

    if (wObj == '%' or (currentX, currentY) in historyList):
        wValue = -1000
    else:
        _, wFutureValue = calculateBestMove(mapArr, currentX-1, currentY, historyList, valuesDict, visionScore, depth+1, discount)
        wValue = calculateValue(wObj, depth, discount) + wFutureValue # + hueristic()
        valuesArr[3] = wValue

    #out of all the options presented, return the move, which should be max index, and the heuristical value which is needed for any recursive calculations.
    max_index, max_value = max(enumerate(valuesArr), key=operator.itemgetter(1))
    return max_index, max_value





class Agent(pygame.sprite.Sprite):
    """
    An agent is something in the world that does something
    Enemy, game/player character

    Agents must define Agent.getAction method,
    but can otherwise overwrite any other methods.

    Methods must assume that they are working with shalow copies of data
    Deep copies must be made of anything they want to keep


    """

    def __init__(self, image, heurstic = None, pos = None, index = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image(image, -1)
        if pos:
            self.rect = self.rect.move(pos)
        self.index = index
        # self.bump  = utils.load_sound('collision.ogg')

    def update(self, action, list_of_components, walls):
        """Move based on the action that was given

        Args:
            action (tuple): a direction normalized to a maze step
            walls (list): Rects which are the maze walls

        Returns:
            : False if action will cause agent to collide with walls, True otherwise

        """

        self.rect = self.rect.move(action)
        collision = self.rect.collidelist(walls)
        if collision == -1:
            pass
            # TODO: behavior when agent collides with wall
            # maybe never executed since ai controlled but w/e
            # self.bump.play() # Hit wall
        return collision

    def getRect(self):
        return self.rect

    def heuristic(self, equiped_list, adj_value):
        heur = 100
        #if enemey

        #if no enemy, but treasure

        #if no enemy and no treasure


        return heur

