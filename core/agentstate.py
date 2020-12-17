from .actions import Actions
from .directions import Directions
from . import util

class AgentState:
    """
    This class hold the state of an agent (position, direction, scared, etc).

    The convention for positions, like a graph, is that (0, 0) is the upper right,
    x increases horizontally and y decreases vertically.
    Therefore, north is the direction of decreasing y, or (0, -1).
    """

    def __init__(self, position, direction, isPlayer):
        # Save the starting information for later use.
        self._startPosition = position
        self._startDirection = direction
        self._startIsPlayer = isPlayer

        self._position = position
        self._direction = direction

        self._isPlayer = isPlayer
        self._scaredTimer = 0

    def copy(self):
        state = AgentState(self._startPosition, self._startDirection, self._startIsPacman)

        state._isPlayer = self._isPlayer
        state._position = self._position
        state._direction = self._direction
        state._scaredTimer = self._scaredTimer

        return state
    """    
    def decrementScaredTimer(self):
        self._scaredTimer = max(0, self._scaredTimer - 1)

        
    def setScaredTimer(self, timer):
        self._scaredTimer = timer

    def getScaredTimer(self):
        return self._scaredTimer
        
    def isBraveGhost(self):
        """
        # A ghost that is not scared.
        """

        return (self.isGhost() and not self.isScared())
        
    def isScaredGhost(self):
        return (self.isGhost() and self.isScared())

    def isScared(self):
        return (self._scaredTimer > 0)
    """

    def getDirection(self):
        return self._direction

    def getPosition(self):
        return self._position

    def getNearestPosition(self):
        return util.nearestPoint(self._position)

    def isEnemy(self):
        return not self.isPlayer()

    def isPlayer(self):
        return self._isPlayer

    def setIsPlayer(self, isPlayer):
        self._isPlayer = isPlayer

    def snapToNearestPoint(self):
        """
        Move the agent to the nearest point to its current location.
        """

        self._position = util.nearestPoint(self._position)

    def respawn(self):
        """
        This agent was killed, respawn it at the start as a pacman.
        """

        self._position = self._startPosition
        self._direction = self._startDirection
        self._isPlayer = self._startIsPlayer
        self._scaredTimer = 0

    def updatePosition(self, vector):
        """
        Update the position and direction with the given movement vector.
        """

        x, y = self._position
        dx, dy = vector

        self._position = (x + dx, y + dy)

        direction = Actions.vectorToDirection(vector)
        if (direction != Directions.STOP):
            # If this is a zero vector, face the same direction as before.
            self._direction = direction

    def __eq__(self, other):
        if (other is None):
            return False

        return (self._position == other._position
                and self._direction == other._direction
                and self._isPlayer == other._isPlayer
                and self._scaredTimer == other._scaredTimer)

    def __hash__(self):
        return util.buildHash(self._position, self._direction, self._isPlayer, self._scaredTimer)

    def __str__(self):
        typeString = 'Enemy'
        if (self.isPlayer()):
            typeString = 'Player'

        scaredString = ''
        if (self.isScared()):
            scaredString = '!'

        return "%s%s: Position: %s, Direction: %s" % (typeString, scaredString,
                str(self._position), str(self.direction))
