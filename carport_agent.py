import gym

# Create the CartPole environment
env = gym.make("CartPole-v1")

# Reset the environment before starting
state = env.reset()

for _ in range(100):  # Run 100 steps
    env.render()  # Visualize the environment (optional)
    action = env.action_space.sample()  # Select a random action
    state, reward, done, _ = env.step(action)  # Take a step

    if done:
        state = env.reset()  # Restart if the game ends

env.close()
