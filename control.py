import os
import sys
import time
import subprocess

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

sumoBinary = "/usr/bin/sumo-gui"
sumoConfig = "bangalore.sumo.cfg"

import traci

sumoCmd = [sumoBinary, "-c", sumoConfig, "--start"]
traci.start(sumoCmd)

"""PORT = 8873
if len(sys.argv)>1:
    retcode = subprocess.call("%s -c %s --python-script %s" % (sumoBinary, sumoConfig, __file__),
                              shell=True, stdout=sys.stdout)
    sys.exit(retcode)
else:
    sumoProcess = subprocess.Popen("%s -c %s" % (sumoBinary, sumoConfig),
                                   shell=True, stdout=sys.stdout)"""

# Code to control traffic lights here
# Example code :P
# print traci.inductionloop.getIDList()
# lanes = traci.lane.getIDList()
"""with open('bangalore.det.xml', 'w') as f:
    for lane in lanes:
        f.write("<inductionLoop id='{}' lane='{}' pos='{}' freq='100' "
                "file='bangalore.net.xml'/>\n".format(lane+"loop", lane, float(traci.lane.getLength(lane))/2))"""
traci.inductionloop.getLastStepMeanSpeed()
for step in range(1000):
    traci.simulationStep()
    time.sleep(0.1)

traci.close()
