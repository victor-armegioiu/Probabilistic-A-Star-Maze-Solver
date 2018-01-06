from collections import defaultdict

X_DEST = 0
Y_DEST = 1
PROBABILITY = 2

class MazeState:
	def __init__(self, universe, start, target, portals):
		self.universe = universe
		self.start = start
		self.target = target
		self.portals = portals

def parse_line(input_line, integer=False, floating=False, character=False):
	if floating:
		return list(map(float, input_line.split()))
	if integer:
		return list(map(int, input_line.split()))
	if character:
		return list(map(str, input_line.split()))

def load_maze():
	portals = defaultdict(list)

	first_line = parse_line(input(), integer=True)
	N, M, T = first_line[0], first_line[1], first_line[2]

	second_line = parse_line(input(), integer=True)
	x_i, y_i = second_line[1], second_line[0]

	third_line = parse_line(input(), integer=True)
	x_f, y_f = third_line[1], third_line[0]

	for i in range(int(T)):
		line = parse_line(input(), floating=True)
		x_portal, y_portal, K = int(line[1]), int(line[0]), int(line[2])

		for outcome in range(3, len(line), 3):
			x_dest, y_dest, probability = int(line[outcome + 1]), int(line[outcome]), line[outcome + 2]
			portals[(x_portal, y_portal)].append((x_dest, y_dest, probability))

	universe = [['X'] * M] * N
	for line in range(N):
		current_line = parse_line(input(), character=True)
		universe[line] = [cell for cell in current_line[0]]

	for portal in portals:
		portals[portal].sort(key=lambda outcome : outcome[PROBABILITY])

	start, target = (x_i, y_i), (x_f, y_f)

	return MazeState(universe, start, target, portals)