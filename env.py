import fileinput
import re

import room

class Env(object):

	def __init__(self):
		self.verbose = False
		self.rooms = []
		self.n_ants = -1
		self.Rm = None
		self.Rm_dict = {}
		self.source = None
		self.sink = None
		self.direct = False


	def reader(self):
		sourcepos_sinkneg = 0

		for line in fileinput.input():
			print(line, end='')
			
			# activate verbose mode
			if line == "##verbose\n":
				self.verbose = True
			
			# recognize number of ants
			elif re.match("^[0-9]+$", line):
				self.n_ants = int(line)
			
			# recognize start room
			elif self.n_ants != -1 and line == "##start\n":
				sourcepos_sinkneg = 1
			
			# recognize end room
			elif self.n_ants != -1 and line == "##end\n":
				sourcepos_sinkneg = -1

			# recognize comments
			elif re.match("^[#]+", line):
				pass

			# recognize a room
			elif self.n_ants != -1 and re.match("^[a-zA-z0-9_'|]+ [-+]?[0-9]+ [-+]?[0-9]+$", line):
				cur_room = (re.search("^[a-zA-z0-9_'|]+", line)).group()
				if cur_room in self.rooms:
					print(f"Error - Double definition of room {cur_room}.")
					exit()
				if (len(self.rooms) == 0):
					self.Rm = room.Room(cur_room, None, sourcepos_sinkneg)
				else:
					self.Rm.nxt = room.Room(cur_room, self.Rm, sourcepos_sinkneg)
					self.Rm = self.Rm.nxt
				self.Rm_dict[cur_room] = self.Rm
				self.rooms.append(cur_room)
				if sourcepos_sinkneg == 1:
					self.source = self.Rm
					self.source.dist_to_source = 0
				elif sourcepos_sinkneg == -1:
					self.sink = self.Rm
					sourcepos_sinkneg = 0

			# recognize tunnel
			elif self.n_ants != -1 and re.match("^[a-zA-z0-9_'|]+-[a-zA-z0-9_'|]+$", line):
				room_one = (re.search("^[a-zA-z0-9_'|]+", line)).group()
				room_two = (re.search("[a-zA-z0-9_'|]+$", line)).group()
				if room_one not in self.rooms or room_two not in self.rooms:
					print(f"Error - At least one of these rooms does not exist.")
					exit()
				(self.Rm_dict[room_one]).add_neighbour(self.Rm_dict[room_two])
				(self.Rm_dict[room_two]).add_neighbour(self.Rm_dict[room_one])
			
			else:
				break
		
		if self.source == None or self.sink == None:
			print("Error - No source and/or sink node.")
			exit()
		
		if self.verbose:
			self.show_rooms()


	def show_rooms(self):
		print("\n#########################################################")
		print("####################      ROOMS      ####################")
		print("#########################################################")
		self.source.show_room()
		self.sink.show_room()
		tmp = self.Rm
		while tmp != None:
			if tmp != self.source and tmp != self.sink:
				tmp.show_room()
			tmp = tmp.prev
		print("#########################################################")

	def check_direct_connection(self):
		for n in self.source.neighbours:
			if n == self.sink:
				self.direct = True
				if self.verbose:
					print(f"   * {self.source.name} -> {self.sink.name}")

	def send_direct_connection(self):
		if self.direct:
			ant = 1
			if self.n_ants != 0 and self.verbose:
				print(f"   (1)   ", end='')
			while ant <= self.n_ants:
				print(f"L{ant}-{self.sink.name} ", end='')
				ant = ant + 1
			print()

	def output(self):
		if self.verbose:
			print("\n#########################################################")
			print("####################      OUTPUT     ####################")
			print("#########################################################")
		else:
			print()
		
		self.send_direct_connection()

		path_starts = []
		path_lens = []
		for n in self.sink.neighbours:
			n.tmp_dist_source = -1
		out = 0
		while out == 0:
			out = 1
			min_dist = 9999999999
			min_room = None
			for n in self.sink.neighbours:
				if n.receives_from != None and n.dist_source < min_dist and n.tmp_dist_source == -1:
					min_dist = n.dist_source
					min_room = n
					out = 0
			if min_room == None:
				break
			min_room.tmp_dist_source = 0
			while min_room.receives_from != self.source:
				min_room = min_room.receives_from
			path_lens.append(min_dist + 1)
			path_starts.append(min_room)
		
		ant = 1
		counter = 1
		moves = 1
		while moves != 0:
			moves = 0
			for x in self.sink.neighbours:
				if x.receives_from != None:
					tmp = x
					while tmp != self.source:
						if tmp.ant != 0	:
							if self.verbose and moves == 0:
								print(f"   ({counter})   ", end='')
							print(f"L{tmp.ant}-{tmp.sends_to.name} ", end='')
							tmp.sends_to.ant = tmp.ant
							tmp.ant = 0
							moves = moves + 1
						tmp = tmp.receives_from
			i = 0
			while i < len(path_starts):
				if ant <= self.n_ants:
					if i == 0 or (path_lens[i] <= self.source.count_turns(path_lens, i, self.n_ants - ant + 1)):
						if self.verbose and moves == 0:
							print(f"   ({counter})   ", end='')
						print(f"L{ant}-{path_starts[i].name} ", end='')
						path_starts[i].ant = ant
						ant = ant + 1
						moves = moves + 1
				i = i + 1
			if moves != 0:
				print()
			counter = counter + 1

		if self.verbose:
			print("#########################################################")

