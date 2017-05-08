# lemin
Moving an ant colony - Graphs and maximum flow

This is my OOP implementation in Python3 of a project I did in C for École 42.

The goal is to move ants from the source room in their ant colony to a sink room, and do it in the minimum number of turns possible, knowing that an ant can only move once per turn and that at any given time there can only be one ant per room (except for the source and the sink, where there can be as many ants as needed).

The program takes a map in the following format:

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



In order to find the best solution to any map, I implemented a Ford-Fulkerson-like algorithm. I use consecutive breadth-first searches to find either whole new paths or a way to change the paths already found in order to increse flow, until no new path or augmenting path is found.

usage:
 > python3 lemin.py map.txt
