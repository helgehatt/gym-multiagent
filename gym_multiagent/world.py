from typing import Iterable, Tuple

import numpy as np

from gym_multiagent.point import Point

DEFAULT_LEVEL = """
++++++++
+0+  cb+
+ A+ ad+
+ +B+  +
+  DC+ +
+ ++++ +
+      +
++++++++
"""


class World(object):
    def __init__(self, level: str = None):
        if level is None:
            level = DEFAULT_LEVEL

        self.level = np.array([[c for c in line] for line in level.split("\n") if line])
        self.state = np.full_like(self.level, " ")
        self.fixed = np.full_like(self.level, " ")

        agents_xy = np.where(np.char.isdigit(self.level))
        boxes_xy = np.where(np.char.isupper(self.level))
        goals_xy = np.where(np.char.islower(self.level))
        walls_xy = np.where(self.level == "+")

        self.state[agents_xy] = self.level[agents_xy]
        self.state[boxes_xy] = self.level[boxes_xy]

        self.fixed[goals_xy] = self.level[goals_xy]
        self.fixed[walls_xy] = "+"

        self.agents = {int(c): Point(x, y) for c, x, y in zip(self.level[agents_xy], *agents_xy)}
        self.goals = {Point(x, y): c.upper() for c, x, y in zip(self.level[goals_xy], *goals_xy)}

        self.numAgents = len(agents_xy[0])
        self.numBoxes = len(boxes_xy[0])
        self.numGoals = len(goals_xy[0])

        self.initialAgents = self.agents.copy()
        self.initialState = self.state.copy()

    def reset(self):
        self.agents = self.initialAgents.copy()
        self.state = self.initialState.copy()

    def update(self, changes: Iterable[Tuple[Point, Point]]):
        fromLocations, toLocations = zip(*changes)
        freedLocations = set(fromLocations) - set(toLocations)

        from_xy = list(zip(*fromLocations))
        to_xy = list(zip(*toLocations))
        freed_xy = list(zip(*freedLocations))

        agents_idx = np.where(np.char.isdigit(self.state[from_xy]))[0]

        for agent_idx in agents_idx:
            agentLocation = fromLocations[agent_idx]
            newAgentLocation = toLocations[agent_idx]
            self.agents[int(self.state[agentLocation])] = newAgentLocation

        self.state[to_xy] = self.state[from_xy]
        self.state[freed_xy] = " "

    def numGoalsSolved(self):
        return sum(self.state[location] == c for location, c in self.goals.items())

    def isFree(self, location: Point):
        return self.fixed[location] != "+" and self.state[location] == " "

    def hasBox(self, location: Point):
        return self.state[location].isalpha()


if __name__ == "__main__":
    world = World()
