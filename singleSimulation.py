import os
import sys
import numpy as np
from scripts.Dqn import Learner
import time

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

sumoBinary = "/usr/bin/sumo-gui"
sumoConfig = "data/bangalore.sumo.cfg"
import traci
from scripts.auxilliary import makemap


def get_state(detectorIDs):
    state = []
    for detector in detectorIDs:
        speed = traci.inductionloop.getLastStepMeanSpeed(detector)
        state.append(speed)
    for detector in detectorIDs:
        veh_num = traci.inductionloop.getLastStepVehicleNumber(detector)
        state.append(veh_num)
    state = np.array(state)
    state = state.reshape((1, state.shape[0]))
    return state


def calc_reward(state, next_state):
    rew = 0
    lstate = list(state)[0]
    lnext_state = list(next_state)[0]
    for ind, (det_old, det_new) in enumerate(zip(lstate, lnext_state)):
        if ind < len(lstate)/2:
            rew += 1000*(det_new - det_old)
        else:
            rew += 1000*(det_old - det_new)

    return rew


def main():
    # Control code here
    sumoCmd = [sumoBinary, "-c", sumoConfig, "--start"]
    traci.start(sumoCmd)
    TLIds = traci.trafficlights.getIDList()
    actionsMap = makemap(TLIds)
    detectorIDs = traci.inductionloop.getIDList()
    state_space_size = traci.inductionloop.getIDCount()*2
    action_space_size = len(actionsMap)
    agent = Learner(state_space_size, action_space_size, 0.0)
    agent.load("./save/traffic.h5")
    # Get number of induction loops
    state = get_state(detectorIDs)
    total_reward = 0
    simulationSteps = 0
    while simulationSteps < 1000:
        action = agent.act(state)
        lightsPhase = actionsMap[action]
        for light, index in zip(TLIds, range(len(TLIds))):
            traci.trafficlights.setPhase(light, lightsPhase[index])
        for i in range(2):
            traci.simulationStep()
            time.sleep(0.4)
        simulationSteps += 2
        next_state = get_state(detectorIDs)
        reward = calc_reward(state, next_state)
        total_reward += reward
        agent.remember(state, action, reward, next_state)
        state = next_state
    traci.close()
    print "Simulation Reward: {}".format(total_reward)

if __name__ == '__main__':
    main()