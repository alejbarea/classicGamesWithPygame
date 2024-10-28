import pygame
import sys
from random import choice
from math import floor
def get_grid_position(x,y):
	return floor(x // RECT_SIZE), floor(y // RECT_SIZE)


WIDTH = 500
HEIGHT = 500
RECT_SIZE = 10
WHITE = (255,255,255)
BLACK = (0,0,0)
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))

cols = WIDTH // RECT_SIZE
rows = HEIGHT // RECT_SIZE

current_color = 0
grid = []
row = []
for i in range(rows):
	row = []
	for j in range(cols):
		row.append(0)
	grid.append(row)
pressed = False

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			pressed = True
		if event.type == pygame.MOUSEBUTTONUP:
			pressed = False
		
	if pressed:
		m_pos = pygame.mouse.get_pos()
		if m_pos[0] > 0 and m_pos[0] < WIDTH and m_pos[1] > 0 and m_pos[1] < HEIGHT:
			x, y = get_grid_position(m_pos[0],m_pos[1])
			if grid[x][y] == 0:
				grid[x][y] = current_color

	for i in range(rows-1,-1,-1):
		for j in range(cols-1,-1,-1):
			if i < rows-1:
				current_block = grid[j][i]
				block_below = grid[j][i+1]
				if block_below == 0 and current_block:
					grid[j][i] = 0
					grid[j][i+1] = current_block
				else:
					if j == 0:
						current_block = grid[j][i]
						block_below_right = grid[j+1][i+1]
						if block_below_right == 0 and current_block:
							grid[j][i] = 0
							grid[j+1][i+1] = current_block
					elif j == cols-1:
						current_block = grid[j][i]
						block_below_left = grid[j-1][i+1]
						if block_below_left == 0 and current_block:
							grid[j][i] = 0
							grid[j-1][i+1] = current_block
					else:
						direc = choice([-1,1])
						current_block = grid[j][i]
						block_below_direc = grid[j+direc][i+1]
						if block_below_direc == 0 and current_block:
							grid[j][i] = 0
							grid[j+direc][i+1] = current_block
						
	screen.fill(BLACK)
	for i in range(rows):
		for j in range(cols):
			if grid[i][j] > 0:
				pygame.draw.rect(screen,grid[i][j], [i*RECT_SIZE,j*RECT_SIZE,RECT_SIZE,RECT_SIZE])
	current_color += 1
	pygame.time.delay(10)
	pygame.display.update()