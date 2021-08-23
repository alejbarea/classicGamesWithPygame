import pygame
import sys
from math import floor
import time
pygame.init()


CELL_SIZE = 8
NUMBER_OF_CELLS = 100
MATRIX_SIZE = CELL_SIZE * NUMBER_OF_CELLS

WHITE = (255,255,255)
BLACK = (0,0,0)
FRAMERATE = 20
SIZE = floor(MATRIX_SIZE - 0.2 * NUMBER_OF_CELLS * CELL_SIZE)
SCREEN_SIZE = (SIZE,SIZE)
MATRIX = [[0 for j in range(0,NUMBER_OF_CELLS)] for i in range(0,NUMBER_OF_CELLS)]

AUX_MATRIX = [[0 for j in range(0,NUMBER_OF_CELLS)] for i in range(0,NUMBER_OF_CELLS)]



def main():
    screen = pygame.display.set_mode(SCREEN_SIZE)

    clock = pygame.time.Clock()
    selectorPhase(screen)
    mainPhase(screen,clock)

def getFromMatrix(MATRIX,x,y):
    try:
        return MATRIX[y][x]
    except:
        return 0
def getVecinosVivos(MATRIX,x,y):
    lista_vecinos = [getFromMatrix(MATRIX,x-1,y-1),getFromMatrix(MATRIX,x,y-1),getFromMatrix(MATRIX,x+1,y-1),getFromMatrix(MATRIX,x+1,y),getFromMatrix(MATRIX,x+1,y+1),getFromMatrix(MATRIX,x,y+1),getFromMatrix(MATRIX,x-1,y+1),getFromMatrix(MATRIX,x-1,y)]
    vivos = 0
    for i in lista_vecinos:
        if i == 1:
            vivos +=1
    return vivos
def mainPhase(screen,clock):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        row_count = 0
        column_count = 0

        for row in MATRIX:
            for cell in row:
                if cell == 0:
                    color = BLACK
                else:
                    color = WHITE
                pygame.draw.rect(screen,color,pygame.Rect(column_count*CELL_SIZE,row_count*CELL_SIZE,CELL_SIZE,CELL_SIZE))
                vivos = getVecinosVivos(MATRIX,column_count,row_count)


                if MATRIX[row_count][column_count] == 0:
                    if vivos == 3:
                        AUX_MATRIX[row_count][column_count] = 1
                else:
                    if vivos == 1 or vivos == 0:
                        AUX_MATRIX[row_count][column_count] = 0
                    elif vivos >= 4:
                        AUX_MATRIX[row_count][column_count] = 0
                    else:
                        AUX_MATRIX[row_count][column_count] = 1



                column_count += 1
            column_count = 0
            row_count += 1

        row_count = 0
        column_count = 0
        for row in AUX_MATRIX:
            for cell in row:
                MATRIX[row_count][column_count] = cell
                column_count += 1

            column_count = 0
            row_count += 1


        clock.tick(FRAMERATE)
        pygame.display.flip()
def selectorPhase(screen):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x_scaled = floor(event.pos[0] / CELL_SIZE)
                mouse_y_scaled = floor(event.pos[1] / CELL_SIZE)
                selected_cell = MATRIX[mouse_y_scaled][mouse_x_scaled]

                if selected_cell == 0:
                    MATRIX[mouse_y_scaled][mouse_x_scaled] = 1
                else:
                    MATRIX[mouse_y_scaled][mouse_x_scaled] = 0



            elif event.type == pygame.KEYDOWN:
                return True
        row_count = 0
        column_count = 0
        for row in MATRIX:
            for cell in row:
                if cell == 0:
                    color = BLACK
                else:
                    color = WHITE
                pygame.draw.rect(screen,color,pygame.Rect(column_count*CELL_SIZE,row_count*CELL_SIZE,CELL_SIZE,CELL_SIZE))
                column_count += 1
            column_count = 0
            row_count += 1

        pygame.display.flip()

if __name__ == "__main__":
    main()
