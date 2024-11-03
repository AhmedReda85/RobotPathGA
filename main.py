import numpy as np
import random

start=(0,0)
goal=(8,6)
grid_size=15
obstacle_ratio=(0.2)

def generate_grid(grid_size,obstacle_ratio):
    grid=np.zeros((grid_size,grid_size),dtype=int)
    obstacles_number=int(grid_size**2*obstacle_ratio)
    obstacles = random.sample([(i, j) for i in range(grid_size) for j in range(grid_size) if (i, j) != start and (i, j) != goal], obstacles_number)    
    for i,j in obstacles:
        grid[i,j]=1
        return grid

grid=generate_grid(grid_size,obstacle_ratio)
moves=[(0,1),(0,-1),(1,0),(-1,0)] #up,Down,right,left Starting from (0,0).
population_size=40
generations=100
mutation_rate=0.1

class Chromosome:
    def __init__(self,path=None):
        if(path is None):
            path=[random.choice(moves) for _ in range (20)]
        else:
            self.path=path
        self.fitness=0
    def evaluate_fitness(self):
        x,y=start
        penalty=0
        for move in self.path:
            x,y=x+move[0],y+move[1]
            if not(0<=x<grid_size and 0<=y<grid_size) or grid[x][y]==1:
                penalty+=10
            elif (x,y==goal):
                self.fitness=1/(1+penalty)
                return
            