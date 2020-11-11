from time import sleep

from IPython.display import clear_output
import gym
import gym_multiagent

level = """
+++++++++++
+0      Aa+
+++++++++++
"""

env = gym.make("MultiAgent-v0", level=level)

for _ in range(1000):
    action = max(1, env.action_space.sample())  # 0 is NoOp

    observation, reward, done, info = env.step([action])

    if any(observation):
        clear_output(wait=True)
        env.render(mode="human")
        sleep(0.5)

        if done:
            break

env.close()
