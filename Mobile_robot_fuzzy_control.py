import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Define the variables
left_sensor = ctrl.Antecedent(np.arange(0, 4.0, 1), 'left_sensor')
front_sensor = ctrl.Antecedent(np.arange(0, 4.0, 1), 'front_sensor')
right_sensor = ctrl.Antecedent(np.arange(0, 4.0, 1), 'right_sensor')

left_motor = ctrl.Consequent(np.arange(0, 2, 1), 'left_motor') # 0 = reverse, 1 = forward
right_motor = ctrl.Consequent(np.arange(0, 2, 1), 'right_motor') # 0 = reverse, 1 = forward

# Define input varibles: left_sensor, front_sensor and  right_sensor
left_sensor['near'] = fuzz.trimf(left_sensor.universe, [2.0, 3.0, 3.0])
left_sensor['far'] = fuzz.trimf(left_sensor.universe, [0.0, 0.0, 3])

front_sensor['near'] = fuzz.trimf(front_sensor.universe, [2.0, 3.0, 3.0])
front_sensor['far'] = fuzz.trimf(front_sensor.universe, [0.0, 0.0, 3])

right_sensor['near'] = fuzz.trimf(right_sensor.universe, [2.0, 3.0, 3.0])
right_sensor['far'] = fuzz.trimf(right_sensor.universe, [0.0, 0.0, 3])

# Define output varibles left_motor and right_motor
left_motor['forward'] = fuzz.trimf(left_motor.universe, [0.0, 0.0, 0.5])
left_motor['reverse'] = fuzz.trimf(left_motor.universe, [0.5, 1.0, 1.0])

right_motor['forward'] = fuzz.trimf(right_motor.universe, [0.0, 0.0, 0.5])
right_motor['reverse'] = fuzz.trimf(right_motor.universe, [0.0, 1.0, 1.0])

# Define fuzzy rules
rule1 = ctrl.Rule(left_sensor['far'] & front_sensor['far'] & right_sensor['far'], (left_motor['forward'], right_motor['forward']))
rule2 = ctrl.Rule(left_sensor['far'] & front_sensor['far'] & right_sensor['near'], (left_motor['reverse'], right_motor['forward']))
rule3 = ctrl.Rule(left_sensor['far'] & front_sensor['near'] & right_sensor['near'], (left_motor['reverse'], right_motor['forward']))
rule4 = ctrl.Rule(left_sensor['far'] & front_sensor['near'] & right_sensor['far'], (left_motor['forward'], right_motor['reverse']))
rule5 = ctrl.Rule(left_sensor['near'] & front_sensor['near'] & right_sensor['far'], (left_motor['forward'], right_motor['reverse']))
rule6 = ctrl.Rule(left_sensor['near'] & front_sensor['near'] & right_sensor['near'], (left_motor['reverse'], right_motor['reverse']))
rule7 = ctrl.Rule(left_sensor['near'] & front_sensor['far'] & right_sensor['near'], (left_motor['forward'], right_motor['reverse']))
rule8 = ctrl.Rule(left_sensor['near'] & front_sensor['far'] & right_sensor['far'], (left_motor['forward'], right_motor['reverse']))

# Create system control and simulation
drive_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8])
drive_sim  = ctrl.ControlSystemSimulation(drive_ctrl)

# Assign input values
drive_sim.input['left_sensor']  = 0
drive_sim.input['front_sensor'] = 0
drive_sim.input['right_sensor'] = 3

# Make a fuzzy inference 
drive_sim.compute()

# Show the result
print("Salida del motor izquierdo:", drive_sim.output['left_motor'])
print("Salida del motor derecho:", drive_sim.output['right_motor'])

left_motor.view(sim=drive_sim)
right_motor.view(sim=drive_sim)
plt.show()