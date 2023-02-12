#################################################################################################################
#                                                   SUDOKU GAME
#                                             By : Ashritha Parupati
#
#    The main aim is to create a puzzle game where number flies into proper cell. 
#    The goal of sudoku game is to fill numbers 1-9 exactly once in every row, column and 3x3 region. 
#    Install pygame module and initialize it. Set up screen size and title along with dimensions for puzzle grid. 
#    Use functions to calculate, when number is entered in a cell.
#
#################################################################################################################

import pygame
from copy import deepcopy
import random
# Initialize Pygame
pygame.init()

width=800
height=600
# Set up the screen size and title
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sudoku Game")
x = 0
y = 0
val = 0

grid_array=[
[[1,9,0,3,4,2,6,8,0],
[2,0,7,5,0,0,9,1,3],
[8,0,0,0,0,0,2,0,0],
[0,0,0,0,0,0,4,7,9],
[9,0,0,7,3,0,0,6,0],
[0,0,0,2,0,0,5,0,8],
[0,8,1,0,0,0,0,4,5],
[5,0,0,4,7,0,8,9,0],
[0,0,0,8,5,1,7,0,0]],

[[7,0,0,4,5,0,3,8,0],
[5,0,0,0,0,6,0,0,0],
[0,1,0,0,9,8,0,0,5],
[8,0,0,0,0,0,0,3,1],
[0,0,0,0,6,3,2,0,8],
[3,9,0,8,0,2,0,0,0],
[0,0,0,0,0,0,5,0,0],
[0,0,0,1,7,5,8,2,9],
[0,5,7,0,0,0,1,0,0]],

[[5,3,0,0,7,0,0,0,0],
[6,0,0,1,9,5,0,0,0],
[0,9,8,0,0,0,0,6,0],
[8,0,0,0,6,0,0,0,3],
[4,0,0,8,0,3,0,0,1],
[7,0,0,0,2,0,0,0,6],
[0,6,0,0,0,0,2,8,0],
[0,0,0,4,1,9,0,0,5],
[0,0,0,0,8,0,0,7,9]],

[[0,0,0,2,6,0,7,0,1],
[6,8,0,0,7,0,0,9,0],
[1,9,0,0,0,4,5,0,0],
[8,2,0,1,0,0,0,4,0],
[0,0,4,6,0,2,9,0,0],
[0,5,0,0,0,3,0,2,8],
[0,0,9,3,0,0,0,7,4],
[0,4,0,0,5,0,0,3,6],
[7,0,3,0,1,8,0,0,0]],

[[4,7,0,1,0,0,0,0,3],
[6,0,0,5,0,3,0,0,0],
[0,0,5,0,7,9,0,2,0],
[0,1,0,7,0,6,2,0,0],
[0,5,0,0,0,8,9,4,0],
[0,0,0,0,0,0,0,3,6],
[0,0,0,0,0,0,0,8,0],
[7,0,3,0,0,5,0,0,1],
[2,4,8,0,9,0,6,0,0]]

]

n= random.randint(0, 4)
# The puzzle grid
grid = deepcopy(grid_array[n])
grid2=deepcopy(grid)
# The size of each cell in the puzzle
cell_size = 60

# The width and height of the puzzle
puzzle_width = cell_size * 9
puzzle_height = cell_size * 9

# The starting x and y coordinates for the puzzle
start_x = (width - puzzle_width) // 2
start_y = (height - puzzle_height) // 2

font = pygame.font.Font(None, 36)  
font1 = pygame.font.SysFont('Segeo UI', 36) 
font2 = pygame.font.SysFont('Segeo UI', 80) 


def find_empty (board):
    '''Finds an empty cell and returns its position as a tuple'''
    for i in range (9):
        for j in range (9):
            if board[i][j] == 0:
                return i,j

def valid(board, pos, num):
    '''Whether a number is valid in that cell, returns a bool'''
    for i in range(9):
	    #make sure it isn't the same number we're checking for, by comparing coordinates
        if board[i][pos[1]] == num and (i, pos[1]) != pos:  
            return False

    for j in range(9):
	    #Same row but not same number
        if board[pos[0]][j] == num and (pos[0], j) != pos:  
            return False
    
	#ex. 5-5%3 = 3 and thats where the grid starts
    start_i = pos[0] - pos[0] % 3 
    start_j = pos[1] - pos[1] % 3
    for i in range(3):
	    #adds i and j as needed to go from start of grid to where we need to be
        for j in range(3):  
            if board[start_i + i][start_j + j] == num and (start_i + i, start_j + j) != pos:
                return False
    return True

def solve(board):
    '''Solves the Sudoku board via the backtracking algorithm'''
    empty = find_empty(board)
    #no empty spots are left so the board is solved
    if not empty: 
        return True

    for nums in range(9):
        if valid(board, empty,nums+1):
            board[empty[0]][empty[1]] = nums+1

            #recursive step
            if solve(board): 
                return True
	        #this number is wrong so we set it back to 0
            board[empty[0]][empty[1]] = 0 
    return False
# The width of the grid lines
grid_width = 2
flag=0
check=0
def get_cord(pos):
	x,y = pos[0],pos[1]
	box_x=x-((x-start_x)%60)
	box_y=y-((y-start_y)%60)
	return box_x,box_y
 
def val_cord(pos):
	x,y=pos[0],pos[1]
	val_x=int((x-((x-start_x)%60)-start_x)//60)
	val_y=int((y-((y-start_y)%60)-start_y)//60)
	return val_y,val_x

def validate(pos):
	if pos[0] in range(start_x,start_x+540) and pos[1] in range(start_y,start_y+540):
		return True

def draw_box(pos):
	if validate(pos):
		box_x,box_y=get_cord(pos)
		rec=pygame.Rect(box_x, box_y, 60, 60)
		pygame.draw.rect(screen,(0,0,128), rec, 7)

# Draw the puzzle grid
def draw_grid(start_x, start_y, cell_size, grid_width):
	for i in range(10):
		if i % 3 == 0:
			thickness = grid_width * 2
		else:
			thickness = grid_width

		# Draw horizontal lines
		y = start_y + i * cell_size
		pygame.draw.line(screen, (0, 0, 0), (start_x, y), (start_x + puzzle_width, y), thickness)

		# Draw vertical lines
		x = start_x + i * cell_size
		pygame.draw.line(screen, (0, 0, 0), (x, start_y), (x, start_y + puzzle_height), thickness)
        

def draw_numbers():
    # display the numbers in the cells
	for row in range(9):
		for col in range(9):
			num = grid[row][col]
			if num!=0:
				if grid2[row][col]==0:
					text = font1.render(str(num), 1, (255,0,0))
					x = start_x + col * cell_size + (cell_size - text.get_width())//2
					y = start_y + row * cell_size + (cell_size - text.get_height())//2
					screen.blit(text, (x, y))
				else:
					text = font.render(str(num), 1, (0, 0, 0))
					x = start_x + col * cell_size + (cell_size - text.get_width())//2
					y = start_y + row * cell_size + (cell_size - text.get_height())//2
					screen.blit(text, (x, y))

# The main game loop
running = True
while running:
	val=0
	screen.fill((152,251,152))
	draw_grid(start_x, start_y, cell_size, grid_width)
	draw_numbers()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button==1:
				pos = pygame.mouse.get_pos()
				flag=1	
		#Get the number to be inserted if key pressed
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_1 or event.key == pygame.K_KP1:
				val = 1
			if event.key == pygame.K_2 or event.key == pygame.K_KP2:
				val = 2
			if event.key == pygame.K_3 or event.key == pygame.K_KP3:
				val = 3
			if event.key == pygame.K_4 or event.key == pygame.K_KP4:
				val = 4
			if event.key == pygame.K_5 or event.key == pygame.K_KP5:
				val = 5
			if event.key == pygame.K_6 or event.key == pygame.K_KP6:
				val = 6
			if event.key == pygame.K_7 or event.key == pygame.K_KP7:
				val = 7
			if event.key == pygame.K_8 or event.key == pygame.K_KP8:
				val = 8
			if event.key == pygame.K_9 or event.key == pygame.K_KP9:
				val = 9
			if event.key==pygame.K_SPACE:
				grid=deepcopy(grid2 )
				solve(grid)
			if event.key==pygame.K_DELETE or event.key==pygame.K_BACKSPACE:
				a,b=val_cord(pos)
				if grid2[a][b]==0:
					grid[a][b]=0
				
			if event.key==pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
				check=1

			if val!=0 and validate(pos):
				v_x,v_y=val_cord(pos)
				if grid2[v_x][v_y]==0:
					grid[v_x][v_y]=val
			
	if flag==1:
		draw_box(pos)
	if check==1:
		solve(grid2)
		if grid2==grid:
			message="YOU WON...!!"
		else:
			message="YOU LOSE...!!"
		text = font2.render(message, 1, (210,105,30))
		text_rect = text.get_rect()
		text_rect.centerx = screen.get_rect().centerx
		text_rect.centery = screen.get_rect().centery
		screen.blit(text, text_rect)

	pygame.display.update()

pygame.quit()
