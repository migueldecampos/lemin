
class Room(object):

	def __init__(self, name, prev, sourcepos_sinkneg):
		self.name = name
		self.ant = 0
		self.prev = prev
		self.sourcepos_sinkneg = sourcepos_sinkneg
		self.neighbours = []
		self.nxt = None
		self.receives_from = None
		self.sends_to = None
		self.dist_source = -1
		self.tmp_dist_source = -1
		self.opportunity_cost = 0
		self.added_to_q_by = None
		self.number_of_test = -1

	def add_neighbour(self, neighbour):
		if neighbour not in self.neighbours:
			self.neighbours.append(neighbour)
	
	def show_room(self):
		print(f"   {self.name}", end='')
		if self.sourcepos_sinkneg == 1:
			print("(source)", end='')
		elif self.sourcepos_sinkneg == -1:
			print("(sink)", end='')
		print(":  ", end='')
		i = 0
		total = len(self.neighbours)
		for n in self.neighbours:
			i = i + 1
			print(n.name, end='')
			if i != total:
				print(", ", end='')
		print()

	def add_to_queue(self, queue, added_by, i):
		self.added_to_q_by = added_by
		self.opportunity_cost = added_by.opportunity_cost
		if added_by.tmp_dist_source != -1:
			self.tmp_dist_source = added_by.tmp_dist_source + 1
		else:
			self.tmp_dist_source = added_by.dist_source + 1
		self.number_of_test = i
		j = 0
		added = False
		while j < len(queue):
			if self.tmp_dist_source + self.opportunity_cost < queue[j].tmp_dist_source + queue[j].opportunity_cost:
				queue.insert(j, self)
				added = True
				break
			j = j + 1

		if not added:
			queue.append(self)

	def go_back_path(self, queue, added_by, i):
		self.added_to_q_by = added_by
		self.opportunity_cost = added_by.tmp_dist_source - self.dist_source
		self.number_of_test = i
		self.tmp_dist_source = -1
		tmp = self.receives_from
		while tmp.sourcepos_sinkneg != 1:
			tmp.added_to_q_by = tmp.sends_to
			tmp.opportunity_cost = tmp.added_to_q_by.opportunity_cost
			tmp.number_of_test = i
			tmp.tmp_dist_source = -1
			for n in tmp.neighbours:
				if n.number_of_test != i and n.receives_from == None:
					n.add_to_queue(queue, tmp, i)
			tmp = tmp.receives_from

	def queue_neighbours(self, queue, i):
		for n in self.neighbours:
			if n.number_of_test != i:
				if n.receives_from == None:
					n.add_to_queue(queue, self, i)
				else:
					n.go_back_path(queue, self, i)
	
	def count_turns(self, path_lens, paths, ants):
		turns = 0
		ns = 0
		while ns < ants:
			turns = turns + 1
			i = 0
			while i < paths:
				if path_lens[i] <= turns:
					ns = ns + 1
				i = i + 1
		return turns

	def save_new_path(self):
		for n in self.neighbours:
			if n.tmp_dist_source != -1 and n.receives_from == None:
				nb = n
				break
		nxt = self
		while nb.sourcepos_sinkneg != 1:
			if nb.receives_from == None:
				nb.receives_from = nb.added_to_q_by
				nb.sends_to = nxt
				nb.dist_source = nb.tmp_dist_source
			elif nb.receives_from != None and nxt != nb.receives_from:
				nb.sends_to = nxt
			elif nb.receives_from != None and nb.added_to_q_by.receives_from == None:
				nb.receives_from = nb.added_to_q_by
				tmp = nb
				while tmp.sourcepos_sinkneg != -1:
					tmp.dist_source = tmp.tmp_dist_source
					tmp.tmp_dist_source = -1
					tmp = tmp.sends_to
			else:
				nb.sends_to = None
				nb.receives_from = None
			nb.tmp_dist_source = -1
			nxt = nb
			nb = nb.added_to_q_by
			nxt.added_to_q_by = None

	def compare_sols(self, ants, verbose):
		rec = None
		for n in self.neighbours:
			if n.tmp_dist_source != -1 and (rec == None or n.tmp_dist_source + n.opportunity_cost < rec):
				rec = n.tmp_dist_source + n.opportunity_cost
				nw = n
		for n in self.neighbours:
			if n != nw:
				n.tmp_dist_source = -1
		while nw.sourcepos_sinkneg != 1:
			if nw.receives_from != None and nw.added_to_q_by.receives_from != None:
				tmp = nw
				while tmp.sourcepos_sinkneg != -1:
					if tmp.added_to_q_by == None:
						tmp.tmp_dist_source = tmp.receives_from.tmp_dist_source + 1
					else:
						tmp.tmp_dist_source = tmp.added_to_q_by.tmp_dist_source + 1
					tmp = tmp.sends_to
			nw = nw.added_to_q_by
		old = []
		new = []
		for n in self.neighbours:
			if n.dist_source != -1:
				old.append(n.dist_source + 1)
				if n.tmp_dist_source == -1:
					new.append(n.dist_source + 1)
				else:
					new.append(n.tmp_dist_source + 1)
			elif n.tmp_dist_source != -1:
				new.append(n.tmp_dist_source + 1)
		old.sort()
		if len(old) > 0:
			old_turns = self.count_turns(old, len(old), ants)
		new.sort()
		new_turns = self.count_turns(new, len(new), ants)
		
		if len(old) == 0 or old_turns > new_turns:
			self.save_new_path()
			if verbose:
				print(f"   The paths found in this iteration, {new},\n   can be used to send all {ants} ants in {new_turns} turns.")
			return 1
		if verbose and len(new) > 0:
			print("   No room for improvement.")
		elif verbose:
			print("   No path found.")
		return 0

	def bfs(self, i, sink, ants, verbose):
		if verbose:
			print(f"## Iteration number {i}")
		queue = []
		self.number_of_test = i
		self.tmp_dist_source = 0
		self.queue_neighbours(queue, i)
		found_path = False
		while len(queue) > 0:
			if queue[0].sourcepos_sinkneg == -1:
				found_path = True
				break
			else:
				tmp = queue[0]
				queue.pop(0)
				tmp.queue_neighbours(queue, i)
		if not found_path:
			if verbose:
				print("   No path found.")
			return 0
		return sink.compare_sols(ants, verbose)
