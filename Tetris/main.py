import pygame
from pygame.locals import *
import sys
from random import choice
from collections import Counter
import time
pygame.init()

CELL_SIZE = 40
CELLS_WIDE = 10
assert CELLS_WIDE % 2 == 0
CELLS_HIGH = 24
assert CELLS_HIGH % 2 == 0
SCREEN_WIDTH = CELLS_WIDE * CELL_SIZE
SCREEN_HEIGHT = CELLS_HIGH * CELL_SIZE
FRAMERATE = 5
FRAME_BLOCK = 10
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
ORANGE = (255,65,0)
YELLOW = (255,255,0)
PURPLE = (255,0,255)

MATRIX = []


def eraseRow(row):
    for block in MATRIX:
        if block.y == row:
            MATRIX.remove(block)
def translateRow(row):
    for block in MATRIX:
        if block.y < row:
            block.movefornblocks(1)





class BlockCollapse(Exception):
    pass

class Block:
    def __init__(self,x,y,color,size=CELL_SIZE,blockState=1):
        # x e y son las coordenadas en nuestro grid, siendo el origen la esquina superior izquierda,
        # Por ejemplo el segundo bloque de la segunda fila sería x=1 y =1
        self._x = x
        self._y = y
        self.size = size
        self._blockState = blockState # 0 es ocupado y 1 moviéndose
        self._color = color
    @property
    def blockState(self):
        return self._blockState
    @blockState.setter
    def blockState(self,value):
        if isinstance(value,int):
            if value >= 0 and value < 2:

                self._blockState = value
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self,value):
        if isinstance(value,int):
            if value > 0 and value < CELLS_WIDE:
                self._x = value

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self,v):
        self._color = v
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self,value):
        if isinstance(value,int):
            if value > 0 and value < CELLS_WIDE:
                self._y = value

    def movefornblocks(self,n):
        self._y += n
    def drawBlock(self,surface):
        real_x = self._x * CELL_SIZE
        real_y = self._y * CELL_SIZE
        pygame.draw.rect(surface,self._color,pygame.Rect(real_x,real_y,self.size,self.size))
        pygame.draw.rect(surface,BLACK,pygame.Rect(real_x,real_y,self.size,self.size),width=2)

    def diff_self(self,a):
        return self != a
    def detectDownwardsCollision(self,other):
        return self._y + 1 == other.y and self._x == other.x
    def detectLateralCollision(self,other,dir):
        return self._x + dir == other.x and self._y == other.y
    def moveDownwards(self):
        if self.blockState:
            collision = False
            for block in list(filter(self.diff_self,MATRIX)):
                if block.blockState == 0:
                    if (not self.detectDownwardsCollision(block)) and self._y + 1 < CELLS_HIGH:
                        collision = False
                    else:
                        self.blockState = 0
                        collision = True
                        break
                else:
                    if self._y + 1< CELLS_HIGH:
                        collision = False
                    else:
                        self.blockState = 0
                        collision = True
                        break
            if collision == False:
                self._y += 1
    def moveLaterally(self,dir): # +1 right -1 left
        if self.blockState:

            for block in list(filter(self.diff_self,MATRIX)):
                if block.blockState == 0:
                    if (not self.detectLateralCollision(block,dir)) and self._x + dir < CELLS_WIDE and self._x + dir> -1:
                        collision = False
                    else:
                        collision = True
                        break
                else:
                    if self._x + dir < CELLS_WIDE and self._x + dir> -1:
                        collision = False
                    else:
                        collision = True
                        break
            if collision == False:
                self._x += dir







class generalPiece:
    def __init__(self,listOfBlocks):
        self._listOfBlocks = listOfBlocks

    def addToMatrix(self):
        for block in self._listOfBlocks:
            MATRIX.append(block)
    @property
    def listOfBlocks(self):
        return self._listOfBlocks
    def moveDownwards(self):

        simulated_blocks = []
        for block in self._listOfBlocks:
            simulated_blocks.append(Block(block.x,block.y,block.color))
        for block in simulated_blocks:
            block.moveDownwards()
        for block in simulated_blocks:
            if block.blockState == 0:
                for block2 in self._listOfBlocks:
                    block2.blockState = 0
                return
        for block in self._listOfBlocks:
            block.moveDownwards()

    def moveLaterally(self,dir):
        collision = False
        for block in self._listOfBlocks:
            for other in list(filter(block.diff_self,MATRIX)):
                if other.blockState == 0:
                    if block.detectLateralCollision(other,dir) and block.x + dir < CELLS_WIDE and block.x + dir> -1:
                        collision = True
            if block.x + dir > CELLS_WIDE -1 or block.x + dir < 0:
                collision = True
        if collision == False:
            for block in self._listOfBlocks:
                block.moveLaterally(dir)
    def draw(self,screen):
        for block in self._listOfBlocks:
            block.drawBlock(screen)
    def updateBlocks(self,newList):
        for block in self._listOfBlocks:
            MATRIX.remove(block)
        self._listOfBlocks = newList
        for block in self._listOfBlocks:
            MATRIX.append(block)
    def checkIntegrity(self):
        for block in self._listOfBlocks:
            if block.blockState == 0:
                for block2 in self._listOfBlocks:
                    block2.blockState = 0
    def die(self):
        for block in self._listOfBlocks:
            if block.blockState == 1:
                return False
        return True

class IPiece(generalPiece):
    def __init__(self):
        common_x = CELLS_WIDE / 2
        self.block_1 = Block(common_x, 3,BLUE)
        self.block_2 = Block(common_x, 2,BLUE)
        self.block_3 = Block(common_x, 1,BLUE)
        self.block_4 = Block(common_x, 0,BLUE)
        self.rotationState = 0
        super().__init__([self.block_1,self.block_2,self.block_3,self.block_4])
    def checkRotation(self):
        if self.rotationState == 0:
            new_block_1 = self.block_1
            new_block_2 = Block(self.block_1.x - 1, self.block_1.y,BLUE)
            new_block_3 = Block(self.block_1.x - 2, self.block_1.y,BLUE)
            new_block_4 = Block(self.block_1.x - 3, self.block_1.y, BLUE)
            newList = [new_block_1,new_block_2,new_block_3,new_block_4]
            for block in MATRIX:
                for block2 in newList[1:]:
                    if (block.x == block2.x and block.y == block2.y) or block2.x < 0:
                        return False
            return True
        else:
            new_block_1 = self.block_1
            new_block_2 = Block(self.block_1.x, self.block_1.y+1,BLUE)
            new_block_3 = Block(self.block_1.x, self.block_1.y+2,BLUE)
            new_block_4 = Block(self.block_1.x, self.block_1.y+3, BLUE)
            newList = [new_block_1,new_block_2,new_block_3,new_block_4]
            for block in MATRIX:
                for block2 in newList[1:]:
                    if (block.x == block2.x and block.y == block2.y) or block2.y >= CELLS_HIGH:
                        return False
            return True

    def rotate(self):
        if self.rotationState == 0 and self.block_1.blockState == 1 and self.checkRotation():
            self.rotationState = 1
            new_block_1 = self.block_1
            new_block_2 = Block(self.block_1.x - 1, self.block_1.y,BLUE)
            new_block_3 = Block(self.block_1.x - 2, self.block_1.y,BLUE)
            new_block_4 = Block(self.block_1.x - 3, self.block_1.y, BLUE)
            newList = [new_block_1,new_block_2,new_block_3,new_block_4]
            self.updateBlocks(newList)
        elif self.rotationState == 1 and self.block_1.blockState == 1 and self.checkRotation():
            new_block_1 = self.block_1
            new_block_2 = Block(self.block_1.x, self.block_1.y+1,BLUE)
            new_block_3 = Block(self.block_1.x, self.block_1.y+2,BLUE)
            new_block_4 = Block(self.block_1.x, self.block_1.y+3, BLUE)
            newList = [new_block_1,new_block_2,new_block_3,new_block_4]
            self.updateBlocks(newList)


class SquarePiece(generalPiece):
    def __init__(self):
        x_1 = CELLS_WIDE / 2 - 1
        x_2 = CELLS_WIDE / 2
        self.block_3 = Block(x_1,0,YELLOW)
        self.block_4 = Block(x_2,0,YELLOW)
        self.block_1 = Block(x_1,1,YELLOW)
        self.block_2 = Block(x_2,1,YELLOW)
        super().__init__([self.block_1,self.block_2,self.block_3,self.block_4])
    def rotate(self):
        pass
class TPiece(generalPiece):
    def __init__(self):
        x_1 = CELLS_WIDE / 2 - 1
        x_2 = CELLS_WIDE / 2
        x_3 = CELLS_WIDE / 2 + 1
        self.block_1 = Block(x_2,1,PURPLE)
        self.block_2 = Block(x_2,0,PURPLE)
        self.block_3 = Block(x_3,0,PURPLE)
        self.block_4 = Block(x_1,0,PURPLE)
        self.rotationState = 0
        super().__init__([self.block_1,self.block_2,self.block_3,self.block_4])
    def checkRotation(self):
        if self.rotationState == 0:
            new_block_1 = Block(self.block_2.x,self.block_2.y+1,PURPLE)
            new_block_2 = self.block_2
            new_block_3 = Block(self.block_2.x-1, self.block_2.y,PURPLE)
            new_block_4 = Block(self.block_2.x, self.block_2.y-1, PURPLE)
        elif self.rotationState == 1:
            new_block_1 = Block(self.block_2.x-1,self.block_2.y,PURPLE)
            new_block_2 = self.block_2
            new_block_3 = Block(self.block_2.x+1, self.block_2.y,PURPLE)
            new_block_4 = Block(self.block_2.x, self.block_2.y-1, PURPLE)
        elif self.rotationState == 2:
            new_block_1 = Block(self.block_2.x,self.block_2.y+1,PURPLE)
            new_block_2 = self.block_2
            new_block_3 = Block(self.block_2.x+1, self.block_1.y,PURPLE)
            new_block_4 = Block(self.block_2.x, self.block_2.y-1, PURPLE)
        else:
            new_block_1 = Block(self.block_2.x-1,self.block_2.y,PURPLE)
            new_block_2 = self.block_2
            new_block_3 = Block(self.block_2.x+1, self.block_1.y,PURPLE)
            new_block_4 = Block(self.block_2.x, self.block_2.y+1, PURPLE)
        checkList = [new_block_1,new_block_2,new_block_3,new_block_4]
        my_matrix = []
        for block in MATRIX:
            if not block in self.listOfBlocks:
                my_matrix.append(block)
                print(block)
        for block in my_matrix:
            for block2 in checkList:
                if (block.x == block2.x and block.y == block2.y):
                    return False
        return True

    def rotate(self):
        if self.block_1.blockState == 1 and self.checkRotation():
            if self.rotationState == 0:
                self.rotationState = 1
                new_block_1 = Block(self.block_2.x,self.block_2.y+1,PURPLE)
                new_block_2 = self.block_2
                new_block_3 = Block(self.block_2.x-1, self.block_2.y,PURPLE)
                new_block_4 = Block(self.block_2.x, self.block_2.y-1, PURPLE)

            elif self.rotationState == 1:
                self.rotationState = 2
                new_block_1 = Block(self.block_2.x-1,self.block_2.y,PURPLE)
                new_block_2 = self.block_2
                new_block_3 = Block(self.block_2.x+1, self.block_2.y,PURPLE)
                new_block_4 = Block(self.block_2.x, self.block_2.y-1, PURPLE)

            elif self.rotationState == 2:
                self.rotationState = 3
                new_block_1 = Block(self.block_2.x,self.block_2.y+1,PURPLE)
                new_block_2 = self.block_2
                new_block_3 = Block(self.block_2.x+1, self.block_2.y,PURPLE)
                new_block_4 = Block(self.block_2.x, self.block_2.y-1, PURPLE)

            else:
                self.rotationState = 0
                new_block_1 = Block(self.block_2.x-1,self.block_2.y,PURPLE)
                new_block_2 = self.block_2
                new_block_3 = Block(self.block_2.x+1, self.block_2.y,PURPLE)
                new_block_4 = Block(self.block_2.x, self.block_2.y+1, PURPLE)
            self.block_1 = new_block_1
            self.block_2 = new_block_2
            self.block_3 = new_block_3
            self.block_4 = new_block_4
            newList = [new_block_1,new_block_2,new_block_3,new_block_4]
            self.updateBlocks(newList)


class LPiece(generalPiece):
    def __init__(self):
        x_1 = CELLS_WIDE / 2
        x_2 = CELLS_WIDE / 2 + 1
        self.block_1 = Block(x_1,2,ORANGE)
        self.block_2 = Block(x_2,2,ORANGE)
        self.block_3 = Block(x_1,1,ORANGE)
        self.block_4 = Block(x_1,0,ORANGE)
        self.rotationState = 0
        super().__init__([self.block_1,self.block_2,self.block_3,self.block_4])
    def rotate(self):
        if self.block_1.blockState == 1 and self.checkRotation():
            if self.rotationState == 0:
                self.rotationState = 1
                new_block_1 = Block(self.block_1.x,self.block_1.y+1,ORANGE)
                new_block_2 = self.block_1
                new_block_3 = Block(self.block_1.x+1, self.block_1.y,ORANGE)
                new_block_4 = Block(self.block_1.x+2, self.block_1.y, ORANGE)
            elif self.rotationState == 1:
                self.rotationState = 2
                new_block_1 = Block(self.block_2.x,self.block_2.y+2,ORANGE)
                new_block_2 = Block(self.block_2.x,self.block_2.y+1,ORANGE)
                new_block_3 = self.block_2
                new_block_4 = Block(self.block_2.x-1,self.block_2.y,ORANGE)
            elif self.rotationState == 2:
                self.rotationState = 3
                new_block_1 = Block(self.block_3.x-2,self.block_3.y,ORANGE)
                new_block_2 = Block(self.block_3.x-1,self.block_3.y,ORANGE)
                new_block_3 = self.block_3
                new_block_4 = Block(self.block_3.x,self.block_3.y-1,ORANGE)
            else:
                self.rotationState = 0
                new_block_1 = self.block_3
                new_block_2 = Block(self.block_3.x+1,self.block_3.y,ORANGE)
                new_block_3 = Block(self.block_3.x,self.block_3.y-1,ORANGE)
                new_block_4 = Block(self.block_3.x,self.block_3.y-2,ORANGE)
            self.block_1 = new_block_1
            self.block_2 = new_block_2
            self.block_3 = new_block_3
            self.block_4 = new_block_4
            newList = [new_block_1,new_block_2,new_block_3,new_block_4]
            self.updateBlocks(newList)
    def checkRotation(self):
        if self.rotationState == 0:
            new_block_1 = Block(self.block_2.x,self.block_2.y+1,PURPLE)
            new_block_2 = self.block_2
            new_block_3 = Block(self.block_2.x-1, self.block_2.y,PURPLE)
            new_block_4 = Block(self.block_2.x, self.block_2.y-1, PURPLE)

        elif self.rotationState == 1:
            new_block_1 = Block(self.block_2.x-1,self.block_2.y,PURPLE)
            new_block_2 = self.block_2
            new_block_3 = Block(self.block_2.x+1, self.block_2.y,PURPLE)
            new_block_4 = Block(self.block_2.x, self.block_2.y-1, PURPLE)

        elif self.rotationState == 2:
            new_block_1 = Block(self.block_2.x,self.block_2.y+1,PURPLE)
            new_block_2 = self.block_2
            new_block_3 = Block(self.block_2.x+1, self.block_2.y,PURPLE)
            new_block_4 = Block(self.block_2.x, self.block_2.y-1, PURPLE)

        else:
            new_block_1 = Block(self.block_2.x-1,self.block_2.y,PURPLE)
            new_block_2 = self.block_2
            new_block_3 = Block(self.block_2.x+1, self.block_2.y,PURPLE)
            new_block_4 = Block(self.block_2.x, self.block_2.y+1, PURPLE)
        checkList = [new_block_1,new_block_2,new_block_3,new_block_4]
        my_matrix = []
        for block in MATRIX:
            if not block in self.listOfBlocks:
                my_matrix.append(block)
                print(block)
        for block in my_matrix:
            for block2 in checkList:
                if (block.x == block2.x and block.y == block2.y):
                    return False
        return True
class SPiece(generalPiece):
    def __init__(self):
        x_1 = CELLS_WIDE / 2
        x_2 = CELLS_WIDE / 2 + 1
        self.block_1 = Block(x_2,2,GREEN)
        self.block_2 = Block(x_2,1,GREEN)
        self.block_3 = Block(x_1,1,GREEN)
        self.rotationState = 0
        self.block_4 = Block(x_1,0,GREEN)
        super().__init__([self.block_1,self.block_2,self.block_3,self.block_4])
    def rotate(self):
        if self.block_1.blockState == 1 and self.checkRotation():
            if self.rotationState == 0:
                self.rotationState = 1
                new_block_1 = Block(self.block_3.x-1,self.block_3.y+1,GREEN)
                new_block_2 = Block(self.block_3.x,self.block_3.y+1,GREEN)
                new_block_3 = self.block_3
                new_block_4 = Block(self.block_3.x+1, self.block_3.y, GREEN)
            elif self.rotationState == 1:
                self.rotationState = 0
                new_block_1 = Block(self.block_3.x+1,self.block_3.y+1,GREEN)
                new_block_2 = Block(self.block_3.x+1,self.block_3.y,GREEN)
                new_block_3 = self.block_3
                new_block_4 = Block(self.block_3.x,self.block_3.y-1,GREEN)

            self.block_1 = new_block_1
            self.block_2 = new_block_2
            self.block_3 = new_block_3
            self.block_4 = new_block_4
            newList = [new_block_1,new_block_2,new_block_3,new_block_4]
            self.updateBlocks(newList)
    def checkRotation(self):
        if self.rotationState == 0:
            new_block_1 = Block(self.block_3.x-1,self.block_3.y+1,GREEN)
            new_block_2 = Block(self.block_3.x,self.block_3.y+1,GREEN)
            new_block_3 = self.block_3
            new_block_4 = Block(self.block_3.x+1, self.block_3.y, GREEN)

        elif self.rotationState == 1:
            new_block_1 = Block(self.block_3.x+1,self.block_3.y+1,GREEN)
            new_block_2 = Block(self.block_3.x+1,self.block_3.y,GREEN)
            new_block_3 = self.block_3
            new_block_4 = Block(self.block_3.x,self.block_3.y-1,GREEN)


        checkList = [new_block_1,new_block_2,new_block_3,new_block_4]
        my_matrix = []
        for block in MATRIX:
            if not block in self.listOfBlocks:
                my_matrix.append(block)
                print(block)
        for block in my_matrix:
            for block2 in checkList:
                if (block.x == block2.x and block.y == block2.y):
                    return False
        return True
def main():

    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("")
    clock = pygame.time.Clock()
    background = pygame.Surface(screen.get_size())
    background.fill(WHITE)
    blockMovement = FRAME_BLOCK
    moveablePiece = choice([IPiece(),SquarePiece(),LPiece(),SPiece(),TPiece()])
    moveablePiece.addToMatrix()
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moveablePiece.moveLaterally(-1)

                elif event.key == pygame.K_RIGHT:

                    moveablePiece.moveLaterally(1)

                elif event.key == pygame.K_r:
                    moveablePiece.rotate()
        if moveablePiece.die():
            for block in moveablePiece.listOfBlocks:
                if block.y < 4:
                    sys.exit()

            del moveablePiece
            moveablePiece = choice([IPiece(),SquarePiece(),LPiece(),SPiece(),TPiece()])

            moveablePiece.addToMatrix()



        screen.blit(background,(0,0))




        row_eraser_trigger = []

        for block in MATRIX:
            block.drawBlock(screen)

            if block.blockState == 0:
                row_eraser_trigger.append(block.y)
            elif not block in moveablePiece.listOfBlocks:
                block.moveDownwards()

        row_eraser_counter = Counter(row_eraser_trigger)
        rows_to_erase = []
        for row in reversed(list(row_eraser_counter.keys())):
            if row_eraser_counter[row] == CELLS_WIDE:
                rows_to_erase.append(row)
        for row in rows_to_erase:
            eraseRow(row)
            eraseRow(row)
            eraseRow(row)
            eraseRow(row)
        for row in rows_to_erase:
            translateRow(row)





        moveablePiece.checkIntegrity()
        moveablePiece.moveDownwards()
        moveablePiece

        pygame.display.flip()
        clock.tick(FRAMERATE)




if __name__ == "__main__":
    main()
