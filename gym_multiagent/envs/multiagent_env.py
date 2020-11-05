import gym
import numpy as np

from gym_multiagent.action import NoOp, POSSIBLE_ACTIONS
from gym_multiagent.world import World


ACTION_LOOKUP = dict(enumerate(POSSIBLE_ACTIONS))


class MultiAgentEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self, level=None):
        self.world = World(level)
        self.action_space = gym.spaces.Discrete(len(ACTION_LOOKUP))
        self.observation_space = gym.spaces.Tuple(
            [gym.spaces.Discrete(x) for x in self.world.level.shape + (self.world.numAgents + self.world.numBoxes,)]
        )
        self.goalsSolved = 0

    def step(self, actions):
        changes = []
        success = np.full(len(self.world.agents), True)

        for i, action in enumerate(map(ACTION_LOOKUP.get, actions)):
            if action == NoOp:
                continue

            agentLocation = self.world.agents[i]

            (moveLocation, boxLocation, newAgentLocation, newBoxLocation) = action(agentLocation)

            # Check box first to avoid index out of bounds error
            allowed = (boxLocation is None or self.world.hasBox(boxLocation)) and self.world.isFree(moveLocation)

            if allowed:
                changes.append((agentLocation, newAgentLocation))

                if boxLocation is not None:
                    changes.append((boxLocation, newBoxLocation))
            else:
                success[i] = False

        if changes:
            self.world.update(changes)

        goalsSolved = self.world.numGoalsSolved()

        observation = success
        reward = -0.1 + (self.goalsSolved - goalsSolved) * 10
        done = goalsSolved == self.world.numGoals

        self.goalsSolved = goalsSolved

        return observation, reward, done, {}

    def reset(self):
        self.world.reset()

    def render(self, mode="human"):
        state_xy = np.where(self.world.state != " ")
        level = self.world.fixed.copy()
        level[state_xy] = self.world.state[state_xy]
        print("\n".join("".join(row) for row in level))

    def close(self):
        pass
