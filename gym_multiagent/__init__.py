from gym.envs.registration import register

register(
    id='multiagent-v0',
    entry_point='gym_multiagent.envs:MultiagentEnv',
)