import os
import sys
import time
from Dqn import Learner
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

sumoBinary = "/usr/bin/sumo"
sumoConfig = "bangalore.sumo.cfg"
import traci


def makemap(TLIds):
    maptlactions = []
    phasesinfirstlight = (len(traci.trafficlights.getRedYellowGreenState(TLIds[0])) ** 0.5) * 2
    for i in range(int(phasesinfirstlight)):
        maptlactions.append([i])
    for light in TLIds[1:]:
        n_phases = (len(traci.trafficlights.getRedYellowGreenState(light)) ** 0.5) * 2
        temp = maptlactions
        for phase in range(int(n_phases)):
            for state in temp:
                maptlactions.append(state + [phase])
    return maptlactions


def get_state(detectorIDs):
    state = []
    for detector in detectorIDs:
        speed = traci.inductionloop.getLastStepMeanSpeed(detector)
        state.append(speed)
    return state


def calc_reward(state, next_state):
    rew = 0
    for det_old, det_new in zip(state, next_state):
        rew += det_new - det_old
    return rew


def main():
    # Control code here
    sumoCmd = [sumoBinary, "-c", sumoConfig, "--start"]
    traci.start(sumoCmd)
    TLIds = traci.trafficlights.getIDList()
    actionsMap = makemap(TLIds)
    detectorIDs = traci.inductionloop.getIDList()
    traci.close()
    epochs = 1000
    for simulation in range(epochs):
        traci.start(sumoCmd)
        # Get number of induction loops
        state_space_size = traci.inductionloop.IDCount()
        action_space_size = len(actionsMap)
        agent = Learner(state_space_size, action_space_size)
        state = get_state(detectorIDs)
        total_reward = 0
        for simulationSteps in range(10000):
            action = agent.act(state)
            lightsPhase = actionsMap[action]
            for light, index in zip(TLIds, range(len(TLIds))):
                traci.trafficlights.setPhase(light, lightsPhase[index])
            for i in range(10):
                traci.simulationStep()
            simulationSteps += 10
            next_state = get_state(detectorIDs)
            reward = calc_reward(state, next_state)
            total_reward += reward
            agent.remember(state, action, reward, next_state)
            state = next_state
        traci.close()
        print("Simulation {}: {}".format(simulation, total_reward))
        agent.replay()

if __name__ == '__main__':
    main()