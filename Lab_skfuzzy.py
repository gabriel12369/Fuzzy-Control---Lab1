import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define the variables
service = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'service')
food = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'food')
tip = ctrl.Consequent(np.arange(0, 30.1, 0.1), 'tip')

# Define input varibles: service and food 
service['poor'] = fuzz.gaussmf(service.universe, 0.0, 1.5)
service['good'] = fuzz.gaussmf(service.universe, 5.0, 1.5)
service['excellent'] = fuzz.gaussmf(service.universe, 10.0, 1.5)

food['rancid'] = fuzz.trapmf(food.universe, [0.0, 0.0, 1.0, 3])
food['delicious'] = fuzz.trapmf(food.universe, [7.0, 9.0, 10.0, 10])

# Define output varible tip 
tip['cheap'] = fuzz.gaussmf(tip.universe, 0.0, 3.0)
tip['average'] = fuzz.gaussmf(tip.universe, 12.5, 3.0)
tip['generous'] = fuzz.gaussmf(tip.universe, 25.0, 3.0)

# Define fuzzy rules

rule1 = ctrl.Rule(service['poor'] | food['rancid'], tip['cheap'])
rule2 = ctrl.Rule(service['good'], tip['average'])
rule3 = ctrl.Rule(service['excellent'] | food['delicious'], tip['generous'])

# Create system control and simulation
tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tipping_sim = ctrl.ControlSystemSimulation(tipping_ctrl)

# Assign input values
tipping_sim.input['service'] = 2.0
tipping_sim.input['food'] = 7.0

# Make a fuzzy inference 
tipping_sim.compute()

# Show the result
print("Propina calculada (y):", tipping_sim.output['tip'])
