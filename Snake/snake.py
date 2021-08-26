# coding=utf-8

# Necesitamos os para buscar la localización del icono. Random para la posición de la manzanita.
import sys
import os,pygame
from random import randrange

# Constantes

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
tDelay = 100

# Es importante que tSize % sSize == 0

tSize = 600
sSize = 30

# Clases

# Clase BloqueRed que me sirve para ver mejor la red

class BloqueRed:

	# Constructor

	def __init__(self,x,y,size,width):
		self.x = x
		self.y = y
		self.size = size
		self.width = width
		self.color = WHITE

	# Dibuja los bordes

	def drawBoundaries(self,screen):
		pygame.draw.rect(screen,self.color,(self.x,self.y,self.size,self.size),self.width)

# Clase BloqueSerpiente para los bloques que conforman a la serpiente

class BloqueSerpiente:

	# Constructor

	def __init__(self,posInit,size,color):
		self.posInit = posInit
		self.lastPos = posInit
		self.size = size
		self.color = color

	# Dibuja los bloques rellenos

	def drawBlock(self,screen):
		pygame.draw.rect(screen,self.color,(self.posInit[0],self.posInit[1],self.size,self.size))

	# Teletransporta el bloque.

	def moveBlock(self,posFin):
		self.lastPos = self.posInit
		self.posInit = posFin

	# Sigue a otro bloque.

	def follow(self,otherBlock):
		self.moveBlock(otherBlock.lastPos)

# Clase manzanita que es la que se come la serpiente

class Manzanita:

	# Constructor

	def __init__(self,size,sizeT,color):
		self.numB = round(sizeT / size)
		self.x = randrange(0,self.numB)*size
		self.y = randrange(0,self.numB)*size
		self.size = size
		self.color = color

	# Dibuja la manzana

	def drawManzanita(self,screen):
		pygame.draw.rect(screen,self.color,(self.x,self.y,self.size,self.size))

	# Escoge unas nuevas coordenadas cuando se activa el trigger

	def reEscoger(self):
		self.x = randrange(0,self.numB)*self.size
		self.y = randrange(0,self.numB)*self.size

# Clase serpiente

class Serpiente:

	# Constructor

	def __init__(self,size,cuerpo,sizeT,color):
		self.cuerpo = cuerpo
		self.size = size
		self.dir = "UP"
		self.cabeza = self.cuerpo[0]
		self.sizeT = sizeT
		self.color = color

	# Dibuja a la serpiente

	def drawSerpiente(self,screen):
		for block in self.cuerpo:
			pygame.draw.rect(screen,GREEN,(block.posInit[0],block.posInit[1],self.size,self.size))

	# Primero mueve mediante moverBloqueSerpientePrin() a la cabeza y despues los demás les siguen

	def moverSerpiente(self):
		moverBloqueSerpientePrin(self.cuerpo[0],self.size,self.dir)
		for x in range(1,len(self.cuerpo)):
			self.cuerpo[x].follow(self.cuerpo[x-1])
		self.teleport()

	# Para que no se salga, si lo hace se teletransporta al lado opuesto.

	def teleport(self):
		if self.cabeza.posInit[0] == -self.size:
			self.cabeza.moveBlock([self.sizeT,self.cabeza.posInit[1]])
		elif self.cabeza.posInit[0] == self.sizeT:
			self.cabeza.moveBlock([0,self.cabeza.posInit[1]])
		elif self.cabeza.posInit[1] == -self.size:
			self.cabeza.moveBlock([self.cabeza.posInit[0],self.sizeT])
		elif self.cabeza.posInit[1] == self.sizeT:
			self.cabeza.moveBlock([self.cabeza.posInit[0],0])

	# Chequea las colisiones entre la cabeza y otros bloques del cuerpo

	def collide(self):
		for x in range(1,len(self.cuerpo)):
			if self.cabeza.posInit == self.cuerpo[x].posInit:
				sys.exit()

	# Añade un bloque cuando se come la manzanita.

	def addBlock(self):
		self.cuerpo.append(BloqueSerpiente(self.cuerpo[(len(self.cuerpo)-1)].lastPos,self.size,self.color))

# Funciones

# Mueve la cabeza. Danza kuduro.

def moverBloqueSerpientePrin(bloque,size,direc):
	
	if direc == "UP":
		bloque.moveBlock([bloque.posInit[0],bloque.posInit[1] - size])
	elif direc == "DOWN":
		bloque.moveBlock([bloque.posInit[0],bloque.posInit[1] + size])
	elif direc == "LEFT":
		bloque.moveBlock([bloque.posInit[0] - size,bloque.posInit[1]])
	elif direc == "RIGHT":
		bloque.moveBlock([bloque.posInit[0] + size,bloque.posInit[1]])

# Elemento gráfico del tablero.

def rellenarTablero(sizeT,sizeB,screen,width):
	numB = round(sizeT / sizeB)
	arrayB = []
	for x in range(0,numB):
		for y in range(0,numB):
			arrayB.append(BloqueRed(x*sizeB,y*sizeB,sizeB,width))
	for block in arrayB:
		block.drawBoundaries(screen)

# Abre la ventana principal

def openWindow(size,title,img):
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption(title)
	pygame.display.set_icon(img)
	keep_playing = True
	man = Manzanita(sSize,tSize,RED)
	serpiente = Serpiente(sSize,[BloqueSerpiente([60,60],sSize,GREEN)],tSize,GREEN)

	# Bucle principal de ejecución:


	while keep_playing:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
				keep_playing = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					if serpiente.dir != "DOWN":
						serpiente.dir = "UP"
				elif event.key == pygame.K_DOWN:
					if serpiente.dir != "UP":
						serpiente.dir = "DOWN"
				elif event.key == pygame.K_LEFT:
					if serpiente.dir != "RIGHT":
						serpiente.dir = "LEFT"
				elif event.key == pygame.K_RIGHT:
					if serpiente.dir != "LEFT":
						serpiente.dir = "RIGHT"
					

		screen.fill(BLACK)

		serpiente.moverSerpiente()
		serpiente.drawSerpiente(screen)
		man.drawManzanita(screen)
		rellenarTablero(size[0],sSize,screen,1)

		# chequea la colisión de la manzanita con la serpiente y la aumenta de tamaño, tomando una nueva manzanita en otra localizacíón aleatoria

		if [man.x,man.y] == serpiente.cuerpo[0].posInit:
			serpiente.addBlock()
			man.reEscoger()

		pygame.display.flip()

		pygame.time.delay(tDelay)

		serpiente.collide()



# El bucle main

def main():
	ruta_icono = os.path.join("imagenes","icono.png")
	icono = pygame.image.load(ruta_icono)
	openWindow((tSize,tSize),"Snake",icono)







# Ejecutar cuando se abre el fichero

if __name__ == "__main__":
	main()
