import numpy as np
import random
import math

def get_user_input():
    while True:
        try:
            grid_size = int(input("Enter the grid size: "))
            start_x = int(input("Enter the start position X: "))
            start_y = int(input("Enter the start position Y: "))
            goal_x = int(input("Enter the goal position X: "))
            goal_y = int(input("Enter the goal position Y: "))
            obstacle_ratio = float(input("Enter obstacle ratio (0.0 to 0.99): "))
            
            start = (start_x, start_y)
            goal = (goal_x, goal_y)
            
            if not (0 <= start[0] < grid_size and 0 <= start[1] < grid_size):
                print("Invalid start coordinates, try again.")
            elif not (0 <= goal[0] < grid_size and 0 <= goal[1] < grid_size):
                print("Invalid goal coordinates, try again.")
            elif not (0.0 <= obstacle_ratio <= 0.99):
                print("Invalid obstacle ratio, try again.")
            else:
                return start, goal, grid_size, obstacle_ratio
        except ValueError:
            print("Invalid input type, please enter integers for positions and a float for the ratio.")

start, goal, grid_size, obstacle_ratio = get_user_input()

def get_fitness(individual):
    return individual.fitness

def selection(population):
    def condition(individual):
        return individual.fitness
    sorted_population = sorted(population, key=condition, reverse=True)
    return sorted_population[:len(sorted_population) // 2]

def generate_grid(grid_size,obstacle_ratio):
    grid=np.zeros((grid_size,grid_size),dtype=int)
    obstacles_number=int(grid_size**2*obstacle_ratio)
    obstacles = random.sample([(i, j) for i in range(grid_size) for j in range(grid_size) if (i, j) != start and (i, j) != goal], obstacles_number)    
    for i,j in obstacles:
        grid[i,j]=1
    return grid

grid=generate_grid(grid_size,obstacle_ratio)
moves=[(0,1),(0,-1),(1,0),(-1,0)] #up,Down,right,left Starting from (0,0).
population_size=100
generations=150
mutation_rate=0.4

class Chromosome:
    def __init__(self,path=None):
        if(path is None):
            path=[random.choice(moves) for _ in range (50)]
            self.path=path
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
                break
            if (x,y)==goal:
                self.fitness=1/(1+penalty)
                return
        distance=abs(goal[0]-x)+abs(goal[1]-y)
        self.fitness=1/(1+math.exp(distance)+penalty)
        
    @staticmethod
    def crossover(parent1,parent2):
        crossover_point=random.randint(1,len(parent1.path)-1)
        child1=Chromosome(path=parent1.path[:crossover_point] +parent2.path[crossover_point:])
        child2=Chromosome(path=parent2.path[:crossover_point] +parent1.path[crossover_point:])
        return child1,child2

    def mutate(self):
        if random.random() < mutation_rate:
            segment_length = random.randint(1, 5)
            start_index = random.randint(0, len(self.path) - segment_length)
            end_index = start_index + segment_length
            self.path[start_index:end_index] = [random.choice(moves) for _ in range(segment_length)]

def genetic_algorithm():
    population = [Chromosome() for _ in range(population_size)]
    for generation in range(generations):
        for individual in population:
            individual.evaluate_fitness()

        population = selection(population)
        offspring = []
        for _ in range(len(population) // 2):
            parent1, parent2 = random.sample(population, 2)
            child1, child2 = Chromosome.crossover(parent1, parent2)
            child1.mutate()
            child2.mutate()
            offspring.extend([child1, child2])
                
        population = population + offspring
        best_individual = max(population, key=get_fitness)
        if best_individual.fitness >= 1:
            print(f"Goal reached in generation {generation}!")
            return best_individual.path
            
        print(f"Generation {generation}: Best fitness = {best_individual.fitness}")
    return max(population, key=get_fitness).path

best_path = genetic_algorithm()
print("Best path found:", best_path)
