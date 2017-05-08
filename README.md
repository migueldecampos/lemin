# lemin
Moving an ant colony - Graphs and maximum flow

This is my OO implementation in Python3 of a project I did in C for École 42.

This program takes as input a map of an ant colony in the form os a list of rooms and links between those rooms.
The goal is to move ants from the source room to the sink room, and do it in the minimum number of turns possible, knowing that an ant can only move once per turn and that at any given time there can only be one ant per room (except for the source and the sink, where there can be as many ants as needed).

The map must be in the following format:

	# comment   -> comment
	##verbose   -> activate verbose output mode (optional)
	10          -> number of ants
	a 0 0       -> definition of a room, room name followed by the coordinates
	b 0 0
	##start     -> the next room defined will be the source
	start 0 0
	##end       -> the next room defined will be the sink
	end 0 0
	start-a     -> definition of a link between rooms
	a-b
	b-end

(I ignore the coordinates of the rooms)



In order to find the best solution to any map, I implemented a Ford-Fulkerson-like algorithm. I use consecutive breadth-first searches to find either whole new paths or a way to change the paths already found in order to increse flow.

usage:
 > python3 lemin.py map.txt
