# INTIALISATION
import pygame, math, sys, random
from pygame.locals import *
import time

screen = pygame.display.set_mode((600, 150), DOUBLEBUF)

land = pygame.image.load('assets/land.png')
cloud = pygame.image.load('assets/cloud.png')


trex = {
	'start': pygame.image.load('assets/start.png'),
	'jump': pygame.image.load('assets/trex-jump.png'),
	'run1': pygame.image.load('assets/trex-run1.png'),
	'run2': pygame.image.load('assets/trex-run2.png'),
	'duck1': pygame.image.load('assets/trex-duck1.png'),
	'duck2': pygame.image.load('assets/trex-duck2.png'),
	'over': pygame.image.load('assets/over.png')
}

cact_big = [pygame.image.load('assets/cact_big'+str(i)+'.png') for i in range(1, 5, 1)]
cact_small = [pygame.image.load('assets/cact_small'+str(i)+'.png') for i in range(1, 7, 1)]
cluster = pygame.image.load('assets/cluster.png')

game_over = pygame.image.load('assets/game_over.png')

numbers =[pygame.image.load('assets/numbers/'+str(i)+'.png') for i in range(10)]

clock = pygame.time.Clock()

SCREEN_HEIGHT = screen.get_height()
SCREEN_WIDTH = screen.get_width()
GROUND = SCREEN_HEIGHT-land.get_height()
HEAD = SCREEN_HEIGHT-trex['start'].get_height()
XSHIFT = land.get_width()-SCREEN_WIDTH-4
ACCLR = 0.0001
GRAVITY = 0.0125
JUMP_HEIGHT = 62.168
TREX_X = 19
CLOUD_SPEED = 0.125
MAX_SPEED = 1.4
FRAME_RATE = 500
JUMP_SPEED = 1.55
cloud_info=[[SCREEN_WIDTH, random.randint(5, HEAD-5-cloud.get_height())]]
for i in range(3):
	cloud_info.append([cloud_info[-1][0]+random.randint(50, SCREEN_WIDTH), random.randint(5, HEAD-5-cloud.get_height())])


class t_rex():
	def __init__(self):
		self.x=TREX_X
		self.y=HEAD

	def jump(self):
		global score, speed
		height=HEAD
		s=JUMP_SPEED
		while s>0:
			score+=speed
			environment()
			s-=GRAVITY
			height-=s
			self.y=height
			screen.blit(trex['jump'], (self.x, self.y))
			scorer()
			if (isCollision(self.x, self.y)):
				return True
			pygame.display.flip()
			clock.tick(FRAME_RATE)

		scorer()
		print(self.y)

		while s<JUMP_SPEED:
			score+=speed
			environment()
			s+=GRAVITY
			height+=s
			self.y=height
			screen.blit(trex['jump'], (self.x, self.y))
			scorer()
			if isCollision(self.x, self.y):
				return True
			pygame.display.flip()
			clock.tick(FRAME_RATE)



	def run(self):
		global score
		score+=speed
		environment()
		screen.blit(trex['run1'], (self.x, self.y))
		pygame.display.flip()
		clock.tick(FRAME_RATE)

		environment()
		screen.blit(trex['run2'], (self.x, self.y))
		scorer()
		pygame.display.flip()
		clock.tick(FRAME_RATE)
		if isCollision(self.x, self.y):
			return True


	'''def duck(self):
					global score
					score+=speed
					environment()
					screen.blit(trex_duck1, (self.x, DUCK_HEAD))
					pygame.display.flip()
					clock.tick(FRAME_RATE)
			
					environment()
					screen.blit(trex_duck2, (self.x, DUCK_HEAD))
					scorer()
					pygame.display.flip()
					clock.tick(FRAME_RATE)
					if isCollision(self.x, DUCK_HEAD):
						return True
			'''


def preprocess():
	global score, score2, landx, land2x, speed, cactii, cactii_y, cact_types, cact_big, cact_small, cluster

	score=score2=landx=0
	land2x=-SCREEN_WIDTH
	speed=0.75
	#Heights of Cactus
	cactii_y=[SCREEN_HEIGHT-cact_small[0].get_height()+2, SCREEN_HEIGHT-cact_big[0].get_height()+2,\
	 2+SCREEN_HEIGHT-cluster.get_height()]
	#Types of cactus
	cact_types=[cact_small, cact_big, cluster]
	#List of cactii
	cactii=[[cact_types[1][0], random.randint(SCREEN_WIDTH, 1000), cactii_y[1]]]
	make_cactii()

def make_cactii():
	global cactii, cactii_y, cact_types
	for i in range(5):
		no_of_cactii=random.randint(1,4)
		if no_of_cactii<=3:
			cact_=random.randint(0,1)
			select_cact=random.sample(range(len(cact_types[cact_])), no_of_cactii)
			for j in range(len(select_cact)):
				if j==0:
					cactii.append([cact_types[cact_][select_cact[j]], cactii[-1][1]+random.randint(300, 1000), cactii_y[cact_]])
				else:
					cactii.append([cact_types[cact_][select_cact[j]], cactii[-1][1]+cactii[-1][0].get_width(), cactii_y[cact_]])
		else:
			cact_=2
			cactii.append([cact_types[cact_], cactii[-1][1]+random.randint(300, 1000), cactii_y[cact_]])

def environment():
		global landx, speed, land2x, cactii, cact_types, cactii_y
		screen.fill((247, 247, 247))

		if(cloud_info[0][0]+cloud.get_width()<0):
			cloud_info.pop(0)
			cloud_info.append([cloud_info[-1][0]+random.randint(50, SCREEN_WIDTH), random.randint(5, HEAD-5-cloud.get_height())])

		for i in range(len(cloud_info)):
			screen.blit(cloud, (cloud_info[i][0], cloud_info[i][1]))
			cloud_info[i][0]-=CLOUD_SPEED
		#Updating list of cactii, removing the cactii passed out of screen and adding new one
		if cactii[0][1]+cactii[0][0].get_width()<0:
			cactii.pop(0)
		while(len(cactii)<10):
			make_cactii()
		
		#printing land
		screen.blit(land, (-landx, GROUND))

		#checking if land1 has shifted enough to introduce land2
		if(landx>=XSHIFT):
			screen.blit(land, (-land2x, GROUND))
			land2x+=speed

		#updating position of cactii
		for i in range(len(cactii)):
			cactii[i][1]-=speed
			screen.blit(cactii[i][0], (cactii[i][1], cactii[i][2]))

		#Replacing land by land2 after checking if land has completely gone out of screen
		if(landx>land.get_width()):
			landx=land2x
			land2x=-SCREEN_WIDTH
		#New land position
		landx+=speed

def scorer():
	global score,score2
	score2=int(score//25)
	score_str=str(score2)
	digits=[int(i) for i in score_str]
	pos=SCREEN_WIDTH
	for i in range(len(digits)-1, -1, -1):
		screen.blit(numbers[digits[i]], (pos-numbers[digits[i]].get_width()-5, 10))
		pos-=numbers[digits[i]].get_width()+5


def isCollision(x, y):
	global cactii
	for i in range(len(cactii)):
		if(x+4*trex['jump'].get_width()/5<cactii[i][1] or cactii[i][1]+cactii[i][0].get_width()<x+trex['jump'].get_width()/5):
			continue
		elif (y+4*(trex['jump'].get_height())/5<cactii[i][2]):
			continue
		else:
			return True
	return False



def game():
	preprocess()
	environment()
	global landx
	trex=t_rex()
	global score, score2, speed
	score=score2=0
	while not isCollision(trex.x, trex.y):
		for event in pygame.event.get():
			if event.type==KEYDOWN:
				if event.key==K_SPACE or event.key==K_UP:
					trex.jump()
		trex.run()
		if(speed<MAX_SPEED):
			speed+=ACCLR

	environment()
	screen.blit(trex['over'], (trex.x, trex.y+2))
	game_over_screen()
	

def start_game():
	global score
	screen.fill((247, 247, 247))
	screen.blit(trex['start'], (TREX_X, HEAD))
	pygame.display.flip()
	t=True
	while t:
		for event in pygame.event.get():
			if(event.type == KEYDOWN):
				if  event.key==K_SPACE:
					t=False

	height=HEAD
	s=JUMP_SPEED
	while s>0:
		s-=GRAVITY
		height-=s
		screen.blit(land, (0, GROUND))
		screen.blit(trex['jump'], (TREX_X, height))
		pygame.display.flip()
		clock.tick(FRAME_RATE)
	while s<JUMP_SPEED:
		s+=GRAVITY
		screen.blit(land, (0, GROUND))
		height+=s
		screen.blit(trex['jump'], (TREX_X, height))
		pygame.display.flip()
		clock.tick(FRAME_RATE)
	game()

def game_over_screen():
	scorer()
	screen.blit(game_over, (SCREEN_WIDTH/2-game_over.get_width()/2, 50))
	screen.blit(restart, (SCREEN_WIDTH/2-restart.get_width()/2, 75))
	pygame.display.flip()
	t=True
	while t:
		for event in pygame.event.get():
			if(event.type == KEYDOWN):
				if  event.key==K_SPACE:
					t=False
					game()
				elif event.key==K_ESCAPE:
					t=False
		

start_game()
