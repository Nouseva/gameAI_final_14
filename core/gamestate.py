import copy

from .agentstate import AgentState
from .directions import Directions
from . import utils

class GameState(object):
    """
    A game state specifies the status of a game, including the food, agents, and score.

    GameStates can be used by agents to reason about the game.

    Only use the accessor methods to get data about the game state.
    """

    def __init__(self, layout):
        self._lastAgentMoved = None
        self._gameover = False
        self._win = False

        self._layout = layout
        # Keep a copy of the hash, since it is expensive to compute.
        # Any children should be sure to clear the hash when modifications are made.
        self._hash = None

        # For food, we will only copy on write (if we eat one of them).
        # This avoid additional copies on successors that don't eat.

        self._foodCopied = False
        self._food = layout.food.copy()
        self._lastFoodEaten = None

        # An ordered list of locations that this state considers special.
        # A view may choose to specially represent these locations.
        self._highlightLocations = []

        self._agentStates = []
        for (isPlayer, position) in layout.agentPositions:
            self._agentStates.append(AgentState(position, Directions.STOP, isPlayer))

        self._score = 0


    def generateSuccessor(self, agentIndex, action):
        pass

    def getLegalActions(self, agentIndex = 0):
        pass

    def addScore(self, score):
        self._hash = None
        self._score += score

    def collectTreasure(self, x, y):
        """
        Mark treasure as collected
        """
    pass
