import numpy as np
from random import random
from utilities import trials_per_portal, find_ge
from collections import defaultdict

X_DEST = 0
Y_DEST = 1
PROBABILITY = 2

class DiscreteDistribution:
	def __init__(self, portals, steps=1000):
		self.portals = portals
		self.approximated_portals = self.approximate_portals(steps) 

	def expected_value(self, events):
		e_x = 0.0
		e_x = sum([event[0] * event[1] for event in events])
		return e_x

	def sample(self, node):
		cumulative_probabilities = [self.portals[node][0][PROBABILITY]]
		probability_to_outcome = {cumulative_probabilities[0] : 0}
	
		for i in range(1, len(self.portals[node])):
			cumulative_probabilities.append(cumulative_probabilities[i - 1] + self.portals[node][i][PROBABILITY])
			probability_to_outcome[cumulative_probabilities[i]] = i

		random_prob = random()
		outcome_probability = find_ge(cumulative_probabilities, random_prob)
	
		outcome_index = probability_to_outcome[outcome_probability]
		return (self.portals[node][outcome_index][X_DEST], self.portals[node][outcome_index][Y_DEST])

	def numpy_sample(self, node):
		outcomes = []
		probabilities = []

		for entry in self.portals[node]:
			outcomes.append((entry[0], entry[1]))
			probabilities.append(entry[2])

		index = np.random.choice(len(outcomes), 1, probabilities)[0]
		return outcomes[index]

	def approximate_portals(self, steps):
		trials = trials_per_portal(self.portals, steps)
		new_portals = defaultdict(list)

		for portal in self.portals:
			allotted_trials = trials[portal]
			outcomes = {}

			for _ in range(allotted_trials):
				outcome = self.sample(portal)
				if outcome in outcomes:
					outcomes[outcome] += 1
				else:
					outcomes[outcome] = 1

			total_outcomes = allotted_trials
			for destination in outcomes.keys():
				new_portals[portal].append((destination[0], destination[1], outcomes[destination] / total_outcomes))

		for portal in new_portals:
			new_portals[portal].sort(key=lambda outcome : outcome[PROBABILITY])

		return new_portals

