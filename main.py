from collections import defaultdict
from heapq import *
from utilities import *
from random import random
from reader import load_maze
from probability import DiscreteDistribution
from copy import deepcopy

X_DEST = 0
Y_DEST = 1
PROBABILITY = 2

class Heuristic:
	def __init__(self, portals, target, discrete_distribution):
		self.portals = portals
		self.original_portals = deepcopy(portals)
		self.target = target
		self.discrete_distribution = discrete_distribution

	def restore_data(self):
		self.portals = deepcopy(self.original_portals)

	def manhattan_distance(self, node):
		return abs(node[0] - self.target[0]) + abs(node[1] - self.target[1])

	def get_events(self, events_info):
		events = [(self.manhattan_distance((outcome[0], outcome[1])), outcome[PROBABILITY])\
				 for outcome in events_info]
		return events

	def probabilistic_manhattan(self, node):
		regular_distance = self.manhattan_distance(node)
		if node not in portals:
			return regular_distance

		closer_nodes = list(filter(lambda outcome : self.manhattan_distance((outcome[X_DEST], outcome[Y_DEST])) < regular_distance, portals[node]))
		closer_probability = sum([outcome[PROBABILITY] for outcome in closer_nodes])

		further_probability = 1.0 - closer_probability
		further_nodes = [outcome for outcome in portals[node] if outcome not in closer_nodes]

		heuristic_value = 0.0
		if closer_probability > further_probability:
			closer_events = self.get_events(closer_nodes)
			heuristic_value = discrete_distribution.expected_value(closer_events)

		elif closer_probability < further_probability:
			further_events = self.get_events(further_nodes)
			heuristic_value = discrete_distribution.expected_value(further_events)

		else:
			all_events = self.get_events(portals[node])
			heuristic_value = discrete_distribution.expected_value(all_events)

		return heuristic_value
		

"""
	discovered[node] = (parent, cost)
	frontier[node] = (estimated_cost, node)
"""
class A_Star:
	def __init__(self, universe, portals, start, target, discrete_distribution):
		self.universe = universe
		self.original_universe = deepcopy(universe)
		self.original_portals = deepcopy(portals)
		self.portals = portals

		self.height = len(universe)
		self.width = len(universe[0])

		self.start = start
		self.target = target

		self.discrete_distribution = discrete_distribution

	def print_universe(self):
		for line in self.universe:
			print(line)

	def restore_data(self):
		self.universe = deepcopy(self.original_universe)
		self.portals = deepcopy(self.original_portals)

	def is_good(self, pos):
	    line = pos[0]
	    col = pos[1]
	    
	    return line >= 0 and line < self.height and col >= 0 and col < self.width \
	    				 and self.universe[line][col] != 'X'

	def get_neighbours(self, pos):
		directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
		neighbours = []

		for direction in directions:
			candidate = (pos[0] + direction[0], pos[1] + direction[1])
			if self.is_good(candidate):
				neighbours.append(candidate)
	            
		return neighbours

	def teleport(self, node):
		if node not in portals:
			return node
		return discrete_distribution.sample(node)	

	def explore(self, h, print_path=False, probabilistic=False):
		frontier = []

		heappush(frontier, (0 + h(self.start), self.start))
		discovered = {self.start : (None, 0)}

		while frontier:
			u = heappop(frontier)[1]
			mark_cell(u, start, target, universe)

			if u == self.target:
				break

			cost_till_u = discovered[u][1]
			old_u = u

			if probabilistic:
				u = self.teleport(u)
				discovered[u] = (discovered[old_u][0], cost_till_u)

			#if old_u != u:
			#	print('I jumped from', old_u, 'to', u, '!')

			for v in self.get_neighbours(u):
				if v in discovered:
					continue
				discovered[v] = (u, cost_till_u + 1)
				heappush(frontier, (discovered[v][1] + h(v), v))

		mark_map(self.universe)
	
		if print_path:
			print('Path cost is', discovered[target][1])
			stack = []
			curr = target

			while curr:
				stack.append((curr, self.original_universe[curr[0]][curr[1]]))
				print(curr)
				curr = discovered[curr][0]

			print('Path from start to target:', stack[::-1])

		return discovered[target][1]


if __name__ == '__main__':
	state = load_maze()

	universe = state.universe
	start, target = state.start, state.target
	portals = state.portals

	discrete_distribution = DiscreteDistribution(portals)
	heuristics = Heuristic(portals, target, discrete_distribution)

	solver = A_Star(universe, portals, start, target, discrete_distribution)
	#solver.explore(heuristics.probabilistic_manhattan, probabilistic=True, print_path=True)
	#solver.print_universe()
	
	"""
	for task_index in (1, 2, 3):
		settings = task_requirements(task_index, heuristics, portals, discrete_distribution)
		probabilistic, heuristic, portals = settings[0], settings[1], settings[2]

		heuristics.portals = portals
		solver.portals = portals

		print('Task', task_index, ':')

		val = solver.explore(h=heuristic, probabilistic=probabilistic, print_path=True)
		print(val)
		
		solver.restore_data()
		heuristics.restore_data()

		print('--------------------------------------------------------------------------------')
	"""

	report = make_statistics(solver, heuristics, discrete_distribution)
	print(report)
