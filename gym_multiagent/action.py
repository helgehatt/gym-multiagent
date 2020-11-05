from gym_multiagent.point import Point


class Action(tuple):
    """Action base class
    
    Each action is associated with a type, a move direction and optionally a box direction.
    """

    def __new__(cls, moveDirection, boxDirection=None):
        assert moveDirection in LOCATION_CHANGE
        assert boxDirection is None or boxDirection in LOCATION_CHANGE
        return tuple.__new__(cls, (moveDirection, boxDirection))

    @property
    def actionType(self):
        return self.__class__.__name__

    @property
    def moveDirection(self):
        return self.__getitem__(0)

    @property
    def boxDirection(self):
        return self.__getitem__(1)

    def __repr__(self):
        if self.boxDirection is None:
            return f"{self.actionType}({self.moveDirection})"
        return f"{self.actionType}({self.moveDirection},{self.boxDirection})"

    def __call__(self, agentLocation):
        """Returns a tuple (moveLocation, boxLocation, newAgentLocation, newBoxLocation)
        - `moveLocation` indicates which location should be free to perform this action.
        - `boxLocation` indicates which location there should be a box to perform this action.
        - `newAgentLocation` indicates where the agent will move after performing this action.
        - `newBoxLocation` indicates where the box will move after performing this action.
        """
        raise NotImplementedError()


class Move(Action):
    def __new__(cls, moveDirection):
        return Action.__new__(cls, moveDirection)

    def __call__(self, agentLocation):
        """Return a Move tuple (see super class)
        - The agent moves according to `moveDirection`
        """
        newAgentLocation = agentLocation + LOCATION_CHANGE[self.moveDirection]
        moveLocation = newAgentLocation
        return (moveLocation, None, newAgentLocation, None)


class Push(Action):
    def __new__(cls, moveDirection, boxDirection):
        return Action.__new__(cls, moveDirection, boxDirection)

    def __call__(self, agentLocation):
        """Return a Push tuple (see super class)
        - The box is in the `boxDirection` relative to the agent
        - The agent moves to the current box location
        - The box moves according to `moveDirection`
        """
        boxLocation = agentLocation + LOCATION_CHANGE[self.boxDirection]
        newAgentLocation = boxLocation
        newBoxLocation = boxLocation + LOCATION_CHANGE[self.moveDirection]
        moveLocation = newBoxLocation
        return (moveLocation, boxLocation, newAgentLocation, newBoxLocation)


class Pull(Action):
    def __new__(cls, moveDirection, boxDirection):
        return Action.__new__(cls, moveDirection, boxDirection)

    def __call__(self, agentLocation):
        """Return a Pull tuple (see super class)
        - The box is in the `boxDirection` relative to the agent
        - The agent moves according to `moveDirection`
        - The box moves to the current agent location
        """
        boxLocation = agentLocation + LOCATION_CHANGE[self.boxDirection]
        newAgentLocation = agentLocation + LOCATION_CHANGE[self.moveDirection]
        newBoxLocation = agentLocation
        moveLocation = newAgentLocation
        return (moveLocation, boxLocation, newAgentLocation, newBoxLocation)


# fmt: off
N = 'N'; S = 'S'; W = 'W'; E = 'E'; NoOp = 'NoOp'

LOCATION_CHANGE = {
    N: Point(-1,  0),
    S: Point( 1,  0),
    W: Point( 0, -1),
    E: Point( 0,  1),
}

POSSIBLE_ACTIONS = [
    NoOp,
    Move(N)  , Move(S)  , Move(W)  , Move(E)  ,
    Push(N,N), Push(S,S), Push(W,N), Push(E,S),
    Push(N,W), Push(S,W), Push(W,S), Push(E,W),
    Push(N,E), Push(S,E), Push(W,W), Push(E,E),
    Pull(N,S), Pull(S,N), Pull(W,N), Pull(E,N),
    Pull(N,W), Pull(S,W), Pull(W,S), Pull(E,S),
    Pull(N,E), Pull(S,E), Pull(W,E), Pull(E,W),
]
# fmt: on
