from bisect import bisect_left

X_DEST = 0
Y_DEST = 1
PROBABILITY = 2

def task_requirements(task_index, heuristics, portals, discrete_distribution, steps=1000):
	if task_index == 1:
		return (False, heuristics.manhattan_distance, portals)

	elif task_index == 2:
		return (True, heuristics.probabilistic_manhattan, portals)

	elif task_index == 3:
		return (True, heuristics.probabilistic_manhattan, \
			discrete_distribution.approximated_portals)

	raise ValueError('Invalid task index: ', task_index)


def mark_cell(u, start, target, universe):
	if u == start:
		universe[u[0]][u[1]] = 'S'
	elif u == target:
		universe[u[0]][u[1]] = 'T'
	else:
		universe[u[0]][u[1]] = 'W'


def trials_per_portal(portals, steps):
	trials = {gate : len(portals[gate]) for gate in portals.keys()}
	total_outcomes = sum(trials.values())

	trials = {gate : int(0.5 + steps * (trials[gate] / total_outcomes)) for gate in trials.keys()}
	return trials


def mark_map(universe):
	for line in universe:
		for i in range(len(line)):
			if line[i] != 'W' and line[i] != 'S' and line[i] != 'T':
				line[i] = '.'


def find_ge(a, key):
    '''Find smallest item greater-than or equal to key.
    Raise ValueError if no such item exists.
    If multiple keys are equal, return the leftmost.

    '''
    i = bisect_left(a, key)
    if i == len(a):
        raise ValueError('No item found with key at or above: %r' % (key,))
    return a[i]


def approximation_error(portals, approximated_portals):
	for portal in portals:
		if len(portals[portal]) != len(approximated_portals[portal]):
			print('Mismatch error, some outcomes have not been discovered\
				for portal:', portal)
			break

		portals[portal].sort()
		approximated_portals[portal].sort()

		error = 0.0
		for i in range(len(portals[portal])):
			abs_diff = abs(portals[portal][i][PROBABILITY] - \
							approximated_portals[portal][i][PROBABILITY])

			error += abs_diff ** 2

		print('Approximation L2 error for portal', portal, 'outcomes is', error)
		print(portal)
		print(portals[portal])
		print(approximated_portals[portal])
		print()


def run_task(task_index, solver, heuristics, discrete_distribution):
	settings = task_requirements(task_index, heuristics, solver.portals, discrete_distribution)
	probabilistic, heuristic, portals = settings[0], settings[1], settings[2]

	heuristics.portals = portals
	solver.portals = portals

	solution_cost = solver.explore(h=heuristic, probabilistic=probabilistic)

	solver.restore_data()
	heuristics.restore_data()

	if task_index == 1:
		print('aici', portals)
	return solution_cost

def make_statistics(solver, heuristics, discrete_distribution, runs=1000):
	report = {}

	for task_index in (1, 2, 3):
		if task_index == 1:
			report[task_index] = run_task(task_index, solver, heuristics, discrete_distribution)


		elif task_index == 2:
			avg_best_sol = 0.0
			
			for _ in range(runs):
				avg_best_sol += run_task(task_index, solver, heuristics, discrete_distribution)
			report[task_index] = avg_best_sol / runs

		else:
			report[task_index] = {}
			for steps in [100, 1000, 10000]:

				avg_best_sol = 0.0 
				discrete_distribution.steps = steps

				for _ in range(runs):
					avg_best_sol += run_task(task_index, solver, heuristics, discrete_distribution)
				report[task_index][steps] = avg_best_sol / runs

	return report	