from time import sleep

import gym
import gym_multiagent

level = """
+++++++++++
+0      Aa+
+++++++++++
"""

env = gym.make("MultiAgent-v0", level=level)
env.render()

for _ in range(1000):
    observation, reward, done, info = env.step([env.action_space.sample()])

    if any(observation):
        env.render()
        sleep(0.5)

        if done:
            break

env.close()
