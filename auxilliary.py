def makeDetectors(lanes):
    with open('bangalore.det.xml', 'w') as f:
        for lane in lanes:
            if traci.lane.getLength(lane) > 5.0:
                f.write("<inductionLoop id='{}' lane='{}' pos='{}' freq='100' "
                        "file='resultsOfDetectors.xml'/>\n".format(lane + "loop", lane, float(traci.lane.getLength(lane)) / 2))


def makemap(TLIds):
    maptlactions = []
    phasesinfirstlight = (len(traci.trafficlights.getRedYellowGreenState(TLIds[0])) ** 0.5) * 2
    for i in range(int(phasesinfirstlight)):
        maptlactions.append(i)
    for light in TLIds[1:]:
        n_phases = (len(traci.trafficlights.getRedYellowGreenState(light)) ** 0.5) * 2
        temp = maptlactions
        for phase in range(int(n_phases)):
            for state in temp:
                maptlactions.append(state + [phase])
    return maptlactions


if __name__ == "__main__":
    import os
    import sys

    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("Please declare the environment variable 'SUMO_HOME'")

    sumoBinary = "/usr/bin/sumo"
    sumoConfig = "bangalore.sumo.cfg"

    import traci

    sumoCmd = [sumoBinary, "-c", sumoConfig, "--start"]
    traci.start(sumoCmd)
    lanes = traci.lane.getIDList()
    makeDetectors(lanes)
    traci.close()