import sys
import os.path

import reader


def main():

	if len(sys.argv) > 2:
		print("Too many maps.")
		exit()
	if len(sys.argv) == 2:
		if not os.path.isfile(sys.argv[1]):
			print("Map does not exist.")
			exit()
	Env = reader.reader()
	
	if Env.verbose:
		print("\n#########################################################")
		print("####################      PATHS      ####################")
		print("#########################################################")
	Env.check_direct_connection()
	i = 1
	while not Env.direct and Env.source.bfs(i, Env.sink, Env.n_ants, Env.verbose) == 1:
		if Env.verbose:
			for n in Env.source.neighbours:
				if n.receives_from != None:
					print("   * " + Env.source.name, end=' -> ')
					tmp = n
					while tmp != None:
						print(tmp.name, end='')
						if tmp != Env.sink:
							print(" -> ", end='')
						tmp = tmp.sends_to
					print()
			print()
		i = i + 1
	if Env.verbose:
		print("#########################################################")
	
	Env.output()

main()
