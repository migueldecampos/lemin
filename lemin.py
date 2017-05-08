import sys
import os.path

import env


def main():

	if len(sys.argv) > 2:
		print("Too many maps.")
		exit()
	if len(sys.argv) == 2:
		if not os.path.isfile(sys.argv[1]):
			print("Map does not exist.")
			exit()
	envr = env.Env()
	envr.reader()
	
	if envr.verbose:
		print("\n#########################################################")
		print("####################      PATHS      ####################")
		print("#########################################################")
	envr.check_direct_connection()
	i = 1
	while not envr.direct and envr.source.bfs(i, envr.sink, envr.n_ants, envr.verbose) == 1:
		if envr.verbose:
			for n in envr.source.neighbours:
				if n.receives_from != None:
					print("   * " + envr.source.name, end=' -> ')
					tmp = n
					while tmp != None:
						print(tmp.name, end='')
						if tmp != envr.sink:
							print(" -> ", end='')
						tmp = tmp.sends_to
					print()
			print()
		i = i + 1
	if envr.verbose:
		print("#########################################################")
	
	envr.output()

if __name__ == '__main__':
	main()
