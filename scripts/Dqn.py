import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense
from collections import deque
import random
from keras.optimizers import Adam
import h5py


class Learner:
    def __init__(self, state_space_size, action_space_size, exploration):
        self.state_size = state_space_size
        self.action_size = action_space_size
        self.learning_rate = 0.001
        self.firstHidden = 604
        self.secondHidden = 1166
        self.regressor = self._build_model()
        self.exploration = exploration
        self.exploration_decay = 0.995
        self.min_exploration = 0.01
        self.memory = deque(maxlen=2000)
        self.batch_size = 200
        self.gamma = 0.95

    def _build_model(self):
        regressor = Sequential()
        regressor.add(Dense(output_dim=self.firstHidden, input_dim=self.state_size, activation='relu'))
        regressor.add(Dense(output_dim=self.secondHidden, activation='relu'))
        regressor.add(Dense(output_dim=self.action_size, activation='linear'))
        regressor.compile(optimizer=Adam(lr=self.learning_rate), loss='mse')
        return regressor

    def act(self, state):
        if np.random.rand() <= self.exploration:
            action = np.random.choice(range(self.action_size))
        else:
            action = np.argmax(self.regressor.predict(state), axis=1)[0]
        return action

    def remember(self, state, action, reward, next_state):
        self.memory.append((state, action, reward, next_state))

    def replay(self):
        minibatch = random.sample(list(self.memory), self.batch_size)
        for state, action, reward, next_state in minibatch:
            # print "Reward: {}".format(type(reward))
            target = reward + self.gamma*np.max(self.regressor.predict(next_state)[0])
            target_f = self.regressor.predict(state)
            # print target_f
            # print target
            target_f[0][action] = target
            self.regressor.fit(state, target_f, epochs=1, verbose=0)
        if self.exploration > self.min_exploration:
            self.exploration *= self.exploration_decay

    def load(self, name):
        self.regressor.load_weights(name)

    def save(self, name):
        self.regressor.save_weights(name)