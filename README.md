## **Traffic Optimisation**

Traffic Signals optimisation for better road traffic handling using 
Deep Reinforcement Learning.
The software SUMO ( Simulation of Urban MObility )
has been used to simulate traffic. To control the traffic signals system,
the Traci, or Traffic Control Interface has been used which allows to
retrieve values of simulated objects and to manipulate their behaviour "on-line".

### **Setup Instructions**
Install SUMO 0.28.0 using the command - 

`sudo apt-get install sumo sumo-tools sumo-doc`

Create a virtual environment(install if not installed) using the command - 

`virtualenv venv`

Activate the virtual environment -

`source venv/bin/activate`

Install requirements using 
`pip install -r setup/requirements.txt`

Set the SUMO_HOME environment variable equal to the SUMO directory installed in 
your system ( /usr/share/sumo ).

Clone this repository using

`git clone https://github.com/Wert1996/Traffic-Optimisation.git`

To see the simulation in action, run

`python singleSimulation.py`

To see the training of the Deep Q Learner in action, run

`python control.py`

The training can be run in gui mode by changing sumo to sumo-gui in the sumo binary path in control.py. 
The training results are stored in ResultsOfSimulations.txt
