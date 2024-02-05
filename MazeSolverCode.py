"""
Course: Artificial Intelligence
Code By: Alexander Casada and Kaden Wince

This program is a maze solving implementation using the greedy breadth first search algorithm
with a visual display.

Reference
GPT-4 from phind.com was used to assist with writing this code.
"""

import pygame
from queue import PriorityQueue
import time


# Define the heuristic function
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Define the greedy BFS function
def greedy_bfs(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty():
       _, current = frontier.get()

       if current == goal:
           break
       for next in graph.neighbors(current):
           print(graph.passable(next))
           print("next: ", next)
           if graph.passable(next): # Only proceed if the node is passable
               new_cost = cost_so_far[current] + graph.cost(current, next)
               if next not in cost_so_far or new_cost < cost_so_far[next]:
                   cost_so_far[next] = new_cost
                   priority = new_cost + heuristic(goal, next)
                   frontier.put((priority, next))
                   came_from[next] = current
           else:
               print("Wall")
               continue


    return came_from, cost_so_far


# Define the Maze class
class Maze:
   def __init__(self, width, height):
       self.width = width
       self.height = height
       self.walls = []


   def in_bounds(self, id):
       x, y = id
       return 0 <= x < self.width and 0 <= y < self.height

   def passable(self, id):
       result = id not in self.walls
       return result

   def neighbors(self, id):
       x, y = id
       results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
       results = filter(self.in_bounds, results)
       results = filter(self.passable, results)
       return list(results)


   def cost(self, from_node, to_node):
       return 1


# Initialize pygame
pygame.init()


# Set up some constants
WIDTH = 800
HEIGHT = 800
MARGIN = 0
TILESIZE = 20


# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Create the maze
maze = Maze(WIDTH//TILESIZE, HEIGHT//TILESIZE)
maze.walls = [(0,2), (0,3), (1, 2), (2, 2), (3, 2), (4, 2), (1, 3), (2, 3), (3, 3), (4, 3), (5,2),(6,2), (7,2), (8,2),(8,3), (8,4),(8,5)]
start = (0, 0)
goal = (5, 3)


# Find the path
came_from, cost_so_far = greedy_bfs(maze, start, goal)


# Draw the maze
for i in range(maze.width):
   for j in range(maze.height):
       rect = pygame.Rect((i*TILESIZE)+MARGIN, (j*TILESIZE)+MARGIN, TILESIZE, TILESIZE)
       color = 'black' if (j, i) in maze.walls else 'white'
       pygame.draw.rect(screen, color, rect)

# Highlight the path
current = goal
path = []
while current != start:
   path.append(current)
   current = came_from[current]
path.append(start)
path = path[::-1]

# Animate the search process
for i in range(len(path)-1):
   pygame.draw.circle(screen, 'blue', (path[i+1][1]*TILESIZE+MARGIN, path[i+1][0]*TILESIZE+MARGIN), 10)
   pygame.draw.line(screen, 'red', (path[i][1]*TILESIZE+MARGIN, path[i][0]*TILESIZE+MARGIN), (path[i+1][1]*TILESIZE+MARGIN, path[i+1][0]*TILESIZE+MARGIN), 2)
   pygame.draw.circle(screen, 'green', (goal[1]*TILESIZE+MARGIN, goal[0]*TILESIZE+MARGIN), 10)
   pygame.display.update()
   time.sleep(0.2)


# Quit pygame
pygame.quit()