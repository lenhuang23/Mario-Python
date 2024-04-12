import pygame
from pygame.locals import*
from time import sleep

class Sprite():
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def isBrick(self):
		return False

	def isCoinBrick(self):
		return False


class Mario(Sprite):
	def __init__(self, x, y):
		super(Mario, self).__init__(x, y)
		self.preX = x
		self.preY = y
		self.h = 95
		self.w = 60
		self.imgNum = 0
		self.vert_vel = 0
		self.Air = 0
		self.marioOffset = 150
		self.onGround = False

		self.mario_images = []
		self.mario_images.append(pygame.image.load("mario1.png"))
		self.mario_images.append(pygame.image.load("mario2.png"))
		self.mario_images.append(pygame.image.load("mario3.png"))
		self.mario_images.append(pygame.image.load("mario4.png"))
		self.mario_images.append(pygame.image.load("mario5.png"))

	def draw(self, screen):
		screen.blit(self.mario_images[self.imgNum], (self.marioOffset, self.y))

	def update(self):
		self.vert_vel += 4.9
		self.y += self.vert_vel
		self.Air += 1

		# Mario ground
		if self.y > 465:
			self.vert_vel = 0
			self.y = 465
			self.Air = 0
			self.onGround = True

		# Mario ceiling
		if self.y < 0:
			self.y = 0

		# Mario image cycle
		if self.imgNum > 4:
			self.imgNum = 0;

	def jump(self):
		if self.Air < 7:
			self.vert_vel -= 12

	def previous(self):
		self.preX = self.x
		self.preY = self.y

	def collison(self, brick):
		if self.preX + self.w <= brick.x:
			self.x = brick.x - self.w 
			
		if self.preX >= brick.x + self.w:
			self.x = brick.x + brick.w
			
		if self.preY >= brick.y + brick.h:
			self.y = brick.y + brick.h
			
		if self.preY + self.h <= brick.y:
			self.y = brick.y - self.h 
			self.vert_vel = 0
			self.Air = 0
			self.onGround = True


class Brick (Sprite):
	def __init__(self, x, y, model):
		super(Brick, self).__init__(x, y)
		self.model = model
		self.w = 60
		self.h = 60
		self.brick = pygame.image.load("Brick.png")

	def update(self):
		return

	def draw(self, screen):
		screen.blit(self.brick, (self.x - self.model.mario.x + self.model.mario.marioOffset, self.y))

	def isBrick(self):
		return True

class CoinBrick (Sprite):
		def __init__(self, x, y, model):
			super(CoinBrick, self).__init__(x, y)
			self.model = model
			self.w = 60
			self.h = 60
			self.x = x
			self.y = y
			self.hitLeft = False
			self.hitRight = False
			self.coinBrick = pygame.image.load("CoinBrick.png")

		def update(self):
			return

		def isCoinBrick(self):
			return True

		def draw(self, screen):
				screen.blit(self.coinBrick, (self.x - self.model.mario.x + self.model.mario.marioOffset, self.y))

class Model():
	def __init__(self):
		self.mario = Mario(100, 305)
		self.sprites = []
		self.sprites.append(self.mario)
		self.brick = Brick(721, 236, self)
		self.sprites.append(self.brick)
		self.brick = Brick(111, 136, self)
		self.sprites.append(self.brick)
		self.brick = Brick(921, 100, self)
		self.sprites.append(self.brick)
		self.brick = Brick(301, 336, self)
		self.sprites.append(self.brick)
		self.coinbrick = CoinBrick(411, 136, self)
		self.sprites.append(self.coinbrick)



	def update(self):
		for i in range(len(self.sprites)):
			self.sprites[i].update()
			if self.sprites[i].isBrick():
				self.t = self.sprites[i]
				if self.spriteCollision(self.mario, self.t):
					self.mario.collison(self.t)
				for j in range(len(self.sprites)):
					self.t = self.sprites[j]
					if self.t.isCoinBrick():
						if self.spriteCollision(self.mario, self.t):
							self.mario.collison(self.t)


	def spriteCollision(self, a, b):
		self.a = a;
		self.b = b;

		if self.a.x + self.a.w <= self.b.x:#right of mario
			return False
		if self.a.x >= self.b.x + self.b.w:#left of mario
			return False
		if self.a.y + self.a.h <= self.b.y:#bottom of mario
			return False
		if self.a.y >= self.b.y + self.b.h:#top of mario
			return False
		else:
			return True


class View():
	def __init__(self, model):
		self.model = model
		screen_size = (1000, 600)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.background = pygame.image.load("Background.png")
		self.background = pygame.transform.scale(self.background, (1200, 800))#scales the background image 

	def update(self):
		self.screen.blit(self.background, (0, -120))
		for i in range(len(self.model.sprites)):
			self.model.sprites[i].draw(self.screen)
		pygame.display.flip()

class Controller():
	def __init__(self, model, view):
		self.model = model
		self.view = view
		self.keep_running = True

	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_running = False

			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_running = False

		key = pygame.key.get_pressed()
		self.model.mario.previous()

		if key[K_SPACE]:
			if self.model.mario.onGround == True:
				self.model.mario.jump()
			if self.model.mario.onGround == False:
				return

		if key[K_LEFT]:
			self.model.mario.x -= 10
			self.model.mario.imgNum += 1

		if key[K_RIGHT]:
			self.model.mario.x += 10
			self.model.mario.imgNum += 1


pygame.display.set_caption("Mario!")
print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m, v)

# Main game loop
while c.keep_running	:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")
