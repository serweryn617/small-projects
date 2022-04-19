# A* algorithm
import numpy as np
from settings import *

def distance(a, b):
    # return abs(a[0] - b[0]) + abs(a[1] - b[1])
    return np.sum(np.abs(a - b)) * 10

# Node:
# G cost - distance from the start
# H cost - distance from end (heuristic)
# F cost - sum
# 
# Sort by F cost
# Then by H cost
# 
# When node is closed, costs of sorrunding nodes have to be recalculated 
# and updated if they are lowerd

# sorted_by_second = sorted(data, key=lambda tup: tup[1])
# data.sort(key=lambda tup: tup[1])  # sorts in place

# Tile types
T_NONE = 0
T_OPEN = 1
T_CLOS = 2
T_STOP = 3

class astar:
    def __init__(self, w, h):
        # type (none, open, closed, not traversible), G, H, F, parent
        self.board = np.zeros((w, h, 5), dtype=int) + T_NONE

        self.source = 0
        self.target = 0

    def settargets(self, src, dst):
        self.source = np.array(src)
        self.target = np.array(dst)

    
    def block(self, x, y):
        for i in range(len(x)):
            self.board[x[i], y[i], 0] = T_STOP # Not traversible


    def blockl(self, l):
        for i in range(len(l)):
            self.board[l[i][0], l[i][1], 0] = T_STOP # Not traversible


    def clear(self):
        self.board.fill(0)


    def cal(self, rev = False):
        # Source and target need to be accessible
        self.board[self.target[0], self.target[1], 0] = T_NONE

        # Add starting node to open list
        d = distance(self.source, self.target)
        self.board[self.source[0], self.source[1]] = [T_OPEN, 0, d, d, 0]

        # Loop
        while True:
            # Sort by F-cost
            openi = np.argwhere(self.board[:, :, 0] == T_OPEN)
            if openi.size == 0:
                # Path not found
                return False
            
            # Take the smallest, move it to closed
            if not rev:
                minvalarg = np.argmin(self.board[openi[:,0], openi[:,1], 3])
            else:
                minvalarg = np.argmax(self.board[openi[:,0], openi[:,1], 3])

            current = self.board[openi[minvalarg][0], openi[minvalarg][1]]
            current[0] = T_CLOS

            # If it is the target node
            # If the head is close to tail, the snake might get caught in a loop!
            if openi[minvalarg][0] == self.target[0] and openi[minvalarg][1] == self.target[1]:
                return True

            # If not, go through neighbours
            for i, e in enumerate(((1,0), (0,1), (-1,0), (0,-1))):
                neighbour = openi[minvalarg] + e
                # nn = self.board[neighbour[0], neighbour[1]]

                # Out of bounds (has to be first)
                if neighbour[0] < 0 or neighbour[0] >= SIZEX or neighbour[1] < 0 or neighbour[1] >= SIZEY:
                    continue

                # Not traversible
                if self.board[neighbour[0], neighbour[1], 0] == T_CLOS or self.board[neighbour[0], neighbour[1], 0] == T_STOP:
                    continue

                # G cost - to start
                gc = current[1] + 7 # Positions further away (closer to target) are more valuable

                # H cost - to end
                hc = distance(neighbour, self.target)

                # If neighbour is not in open, add it
                if self.board[neighbour[0], neighbour[1], 0] != T_OPEN:
                    self.board[neighbour[0], neighbour[1]] = [T_OPEN, gc, hc, gc + hc, i]

                # Update
                if not rev:
                    if gc < self.board[neighbour[0], neighbour[1], 1]:
                        self.board[neighbour[0], neighbour[1], 1:5] = [gc, hc, gc + hc, i]
                else:
                    if gc + hc > self.board[neighbour[0], neighbour[1], 3]:
                        self.board[neighbour[0], neighbour[1], 1:5] = [gc, hc, gc + hc, i]


    def getpath(self):
        DIRS = ((1,0), (0,1), (-1,0), (0,-1))
        # Follow parents
        out = []
        # pointpos = self.target
        searchpos = self.target.copy()
        # parent = self.board[pointpos[0], pointpos[1], -1]
        parent = self.board[searchpos[0], searchpos[1], -1]

        # for _ in range(2):
        while True:
            out.append(searchpos.copy())
            # print(searchpos)

            searchpos[0] -= DIRS[parent][0]
            searchpos[1] -= DIRS[parent][1]

            if searchpos[0] == self.source[0] and searchpos[1] == self.source[1]:
                break

            c = self.board[searchpos[0], searchpos[1]]
            parent = c[-1]
        
        return out
                
    def getclosed(self):
        return np.argwhere(self.board[:, :, 0] == T_CLOS)

    def getopen(self):
        return np.argwhere(self.board[:, :, 0] == T_OPEN)


