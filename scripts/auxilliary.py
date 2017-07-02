import os
import sys

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")
sumoBinary = "/usr/bin/sumo"
parent_dir = os.path.dirname(os.path.dirname(__file__))
sumoConfig = os.path.join(parent_dir, "data/bangalore.sumo.cfg")

import traci


def makeDetectors(lanes):
    with open(os.path.join(parent_dir, 'data/bangalore.det.xml'), 'w') as f:
        f.write("<additional>\n")
        for lane in lanes:
            if traci.lane.getLength(lane) > 20.0:
                f.write("\t<inductionLoop id='{}' lane='{}' pos='{}' freq='100' "
                        "file='{}'/>\n".format(lane + "loop", lane, -10, os.path.join(parent_dir, "data/resultsOfDetectors.xml")))
        f.write("</additional>")


def list_of_n_phases(TLIds):
    n_phases = []
    for light in TLIds:
        n_phases.append(int((len(traci.trafficlights.getRedYellowGreenState(light)) ** 0.5) * 2))
    return n_phases


def makemap(TLIds):
    maptlactions = []
    n_phases = list_of_n_phases(TLIds)
    for n_phase in n_phases:
        mapTemp = []
        if len(maptlactions) == 0:
            for i in range(n_phase):
                if i%2 == 0:
                    maptlactions.append([i])
        else:
            for state in maptlactions:
                for i in range(n_phase):
                    if i%2 == 0:
                        mapTemp.append(state+[i])
            maptlactions = mapTemp
    return maptlactions


if __name__ == "__main__":
    sumoCmd = [sumoBinary, "-c", sumoConfig, "--start"]
    traci.start(sumoCmd)
    lanes = traci.lane.getIDList()
    makeDetectors(lanes)
    # TLIds = traci.trafficlights.getIDList()
    # print makemap(TLIds)
    traci.close()