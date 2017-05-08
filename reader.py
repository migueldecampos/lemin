import fileinput
import re

import room
import env

def reader():
	Env = env.Env()
	sourcepos_sinkneg = 0

	for line in fileinput.input():
		print(line, end='')

		# activate verbose mode
		if line == "##verbose\n":
			Env.verbose = True

		# recognize number of ants
		if re.match("^[0-9]+$", line):
			Env.n_ants = int(line)
		
		# recognize start room
		elif Env.n_ants != -1 and line == "##start\n":
			sourcepos_sinkneg = 1

		# recognize end room
		elif Env.n_ants != -1 and line == "##end\n":
			sourcepos_sinkneg = -1

		# recognize comments
		elif re.match("^[#]+", line):
			pass

		# recognize a room
		elif Env.n_ants != -1 and re.match("^[a-zA-z0-9_'|]+ [-+]?[0-9]+ [-+]?[0-9]+$", line):
			cur_room = (re.search("^[a-zA-z0-9_'|]+", line)).group()
			if cur_room in Env.rooms:
				print(f"Error - Double definition of room {cur_room}.")
				exit()
			if (len(Env.rooms) == 0):
				Env.Rm = room.Room(cur_room, None, sourcepos_sinkneg)
			else:
				Env.Rm.nxt = room.Room(cur_room, Env.Rm, sourcepos_sinkneg)
				Env.Rm = Env.Rm.nxt
			Env.Rm_dict[cur_room] = Env.Rm
			Env.rooms.append(cur_room)
			if sourcepos_sinkneg == 1:
				Env.source = Env.Rm
				Env.source.dist_to_source = 0
			elif sourcepos_sinkneg == -1:
				Env.sink = Env.Rm
			sourcepos_sinkneg = 0

		# recognize tunnel
		elif Env.n_ants != -1 and re.match("^[a-zA-z0-9_'|]+-[a-zA-z0-9_'|]+$", line):
			room_one = (re.search("^[a-zA-z0-9_'|]+", line)).group()
			room_two = (re.search("[a-zA-z0-9_'|]+$", line)).group()
			if room_one not in Env.rooms or room_two not in Env.rooms:
				print(f"Error - At least one of these rooms does not exist.")
				exit()
			(Env.Rm_dict[room_one]).add_neighbour(Env.Rm_dict[room_two])
			(Env.Rm_dict[room_two]).add_neighbour(Env.Rm_dict[room_one])

		else:
			break

	if Env.source == None or Env.sink == None:
		print("Error - No source and/or sink node.")
		exit()
	
	if Env.verbose:
		Env.show_rooms()
	
	return Env
