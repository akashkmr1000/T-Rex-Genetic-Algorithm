# INTIALISATION
import pygame, math, sys, random
import numpy as np
from pygame.locals import *
import time
from math import sqrt, exp, atan, pi

screen = pygame.display.set_mode((600, 150), DOUBLEBUF)

land = pygame.image.load('assets/landx.png')
cloud = pygame.image.load('assets/cloud.png')

start = pygame.image.load('assets/start.png')
trex_jump=pygame.image.load('assets/trex-jump.png')
trex_run1=pygame.image.load('assets/trex-run1.png')
trex_run2=pygame.image.load('assets/trex-run2.png')
over = pygame.image.load('assets/over.png')

cactus_big_1=pygame.image.load('assets/cact1.png')
cactus_small_1=pygame.image.load('assets/cact2.png')

game_over = pygame.image.load('assets/game_over.png')

numbers=[]
for i in range(10):
	numbers.append(pygame.image.load('assets/numbers/'+str(i)+'.png'))

clock = pygame.time.Clock()

SCREEN_HEIGHT=screen.get_height()
SCREEN_WIDTH=screen.get_width()
GROUND=SCREEN_HEIGHT-land.get_height()
HEAD=GROUND-33
XSHIFT=land.get_width()-SCREEN_WIDTH-4
ACCLR=0.0001
GRAVITY=0.0125
JUMP_HEIGHT=62.168
TREX_X=19
CLOUD_SPEED=0.125
MAX_SPEED=1.5
FRAME_RATE=55000
JUMP_SPEED=1.55
#TIME_TAKEN in one iter = 0.000002 + 0.001

cloud_info=[[SCREEN_WIDTH, random.randint(5, HEAD-5-cloud.get_height())]]
for i in range(3):
	cloud_info.append([cloud_info[-1][0]+random.randint(50, SCREEN_WIDTH), random.randint(5, HEAD-5-cloud.get_height())])


class t_rex():
	def __init__(self):
		self.x=TREX_X
		self.y=HEAD

	def jump(self):
		global score
		height=HEAD
		s=JUMP_SPEED
		while s>0:
			score+=1
			environment()
			s-=GRAVITY
			height-=s
			self.y=height
			screen.blit(trex_jump, (self.x, self.y))
			scorer()
			if (isCollision(self.x, self.y)):
				return True
			pygame.display.flip()
			clock.tick(FRAME_RATE)

		scorer()

		while s<JUMP_SPEED:
			score+=1
			environment()
			s+=GRAVITY
			height+=s
			self.y=height
			screen.blit(trex_jump, (self.x, self.y))
			scorer()
			if isCollision(self.x, self.y):
				return True
			pygame.display.flip()
			clock.tick(FRAME_RATE)



	def run(self):
		global score
		score+=1
		environment()
		screen.blit(trex_run1, (self.x, self.y))
		pygame.display.flip()
		clock.tick(FRAME_RATE)

		environment()
		screen.blit(trex_run2, (self.x, self.y))
		scorer()
		pygame.display.flip()
		clock.tick(FRAME_RATE)
		if isCollision(self.x, self.y):
			return True


def preprocess():
	global score, score2, landx, land2x, speed, cactii, cact_info, removed

	score=score2=landx=removed=0
	land2x=-SCREEN_WIDTH
	speed=0.5
	#Types of Cactus
	cactii=([HEAD+12, cactus_small_1], [HEAD-2, cactus_big_1])
	#List of cactii
	cact_info=[]
	cact_info.append([SCREEN_WIDTH-landx,  cactii[random.randint(0, 1)]])
	for i in range(5):
		k=random.randint(1,4)
		for j in range(k):
			if j == 0:
				cact_info.append([cact_info[-1][0]+cact_info[-1][1][1].get_width()+random.randint(150+int(100*speed), SCREEN_WIDTH),\
				 cactii[random.randint(0, 1)]])
			else:
				cact_info.append([cact_info[-1][0]+cact_info[-1][1][1].get_width(),  cactii[random.randint(0, 1)]])


def environment():
		global landx, speed, land2x, cact_info, cactii, removed
		screen.fill((247, 247, 247))

		if(cloud_info[0][0]+cloud.get_width()<0):
			cloud_info.pop(0)
			cloud_info.append([cloud_info[-1][0]+random.randint(50, SCREEN_WIDTH), random.randint(5, HEAD-5-cloud.get_height())])

		for i in range(len(cloud_info)):
			screen.blit(cloud, (cloud_info[i][0], cloud_info[i][1]))
			cloud_info[i][0]-=CLOUD_SPEED
		#Updating list of cactii, removing the cactii passed out of screen and adding new one
		to_be_removed=[]
		for i in range(len(cact_info)):
			if cact_info[i][0]+cact_info[i][1][1].get_width()<0:
				to_be_removed.append(i)

		for i in range(len(to_be_removed)-1, -1, -1):
			cact_info.pop(to_be_removed[i])
			if cact_info[to_be_removed[i]][1][1].get_width()+cact_info[to_be_removed[i]][0]<cact_info[to_be_removed[i]+1][0]:
				removed+=1

		while(len(cact_info)<20):
			k=random.randint(1, 4)
			for j in range(k):
				if k<3:
					if j == 0:
						cact_info.append([cact_info[-1][0]+cact_info[-1][1][1].get_width()+random.randint(150+int(100*speed), SCREEN_WIDTH),\
					 	cactii[random.randint(0, len(cactii)-1)]])
					else:
						cact_info.append([cact_info[-1][0]+cact_info[-1][1][1].get_width(),  cactii[random.randint(0, len(cactii)-1)]])
				else:
					if j == 0:
						cact_info.append([cact_info[-1][0]+cact_info[-1][1][1].get_width()+random.randint(150+int(100*speed), SCREEN_WIDTH),\
					 	cactii[random.randint(0, 2)%2]])
					else:
						cact_info.append([cact_info[-1][0]+cact_info[-1][1][1].get_width(),  cactii[random.randint(0, 2)%2]])

		
		#printing land
		screen.blit(land, (-landx, GROUND))

		#checking if land1 has shifted enough to introduce land2
		if(landx>=XSHIFT):
			screen.blit(land, (-land2x, GROUND))
			land2x+=speed

		#updating position of cactii
		for i in range(len(cact_info)):
			cact_info[i][0]-=speed
			screen.blit(cact_info[i][1][1], (cact_info[i][0], cact_info[i][1][0]))

		#Replacing land by land2 after checking if land has completely gone out of screen
		if(landx>land.get_width()):
			landx=land2x
			land2x=-SCREEN_WIDTH
		#New land position
		landx+=speed

def scorer():
	global score,score2,speed
	score2=int(score//25)
	score_str=str(score2)
	digits=[int(i) for i in score_str]
	pos=SCREEN_WIDTH
	for i in range(len(digits)-1, -1, -1):
		screen.blit(numbers[digits[i]], (pos-numbers[digits[i]].get_width()-5, 10))
		pos-=numbers[digits[i]].get_width()+5


def isCollision(x, y):
	global cact_info
	for i in range(len(cact_info)):
		if(x+3*trex_jump.get_width()/4<cact_info[i][0] or cact_info[i][0]+cact_info[i][1][1].get_width()<x+3*trex_jump.get_width()/4):
			continue
		elif (y+3*(trex_jump.get_height())/4<cact_info[i][1][0]):
			continue
		else:
			return True
	return False



def game():
	global score2, speed, removed
	weights=[[np.array([np.array([random.uniform(-1, 1) for i in range(5)]) for j in range(4)]), np.array([random.uniform(-1, 1) for k in range(6)])] for l in range(10)]
	fitness=[0 for i in range(10)]
	max_score=0
	for _ in range(200):
		nn=[t_rex() for i in range(10)]
		score=score2=0
		for i in range(10):
			preprocess()
			jumps=1
			while not isCollision(nn[i].x, nn[i].y):
				input_layer=make_input()
				input_layer=np.array(input_layer)
				if train_(input_layer, weights[i])>=0:
					nn[i].jump()
					jumps+=1
				nn[i].run()
				if(speed<MAX_SPEED):
					speed+=ACCLR
				if(score2>30000):
					break
				
			fitness[i]=getFitness(score2, removed, jumps)
			print('Epoch {_} Rex {i} Fitness {fit:.2f} cact jumped {cj} score {score2}'.format(_=_, i=i, score2=score2, fit=round(fitness[i], 2), cj=removed))
			environment()
			screen.blit(over, (TREX_X, 300))
			pygame.time.delay(100)
			if(score2>max_score):
				max_score=score2
			if(score2>30000):
				break
		if(score2>30000):
			break
		weights, fitness=sortByFitness(weights,fitness)
		weights=crossoverMutate(weights)
		weights=survive(weights)

	print('MAX SCORE: ', max_score)

def getFitness(score, removed, jumps):
	return exp(-((removed/jumps-1)**2*2))#+atan(score-250)*2/pi

def make_input():
	global cact_info, speed
	#input=[BIAS, DISTANCE, NO_OF_CACTII, SPEED]
	no_of_cactii=1
	for i in range(1, len(cact_info)):
		if cact_info[i][0]-cact_info[i-1][0]<=cact_info[i-1][1][1].get_width():
			no_of_cactii+=1
		else:
			break

	input_vector=[1, (cact_info[0][0]-TREX_X-trex_run1.get_width())/(SCREEN_WIDTH-225), no_of_cactii/4, speed/MAX_SPEED]
	return input_vector

def train_(input_layer, weights):
	hidden_layer=sigmoid(np.dot(input_layer, weights[0]))
	output=np.dot(hidden_layer, weights[1][1:])+weights[1][0]

	return output

def sortByFitness(weights, fitness):
	for x in range(9):
		for y in range(9-x):
			if fitness[y]<fitness[y+1]:
				fitness[y], fitness[y+1], weights[y], weights[y+1] = fitness[y+1], fitness[y], weights[y+1], weights[y]
	return weights, fitness

def crossoverMutate(weights):
	for i in range (3):
		#CROSSOVER
		co_weights0=random.sample(range(20), 8)
		co_weights1=random.sample(range(6), 2)
		rows=[k/5 for k in co_weights0]
		cols=[k%5 for k in co_weights0]

		weights[2*i-1][0][[rows, cols]], weights[2*i-1][1][co_weights1], weights[2*i][0][[rows, cols]], weights[2*i][1][co_weights1] = weights[2*i-1][0][[rows, cols]], weights[2*i-1][1][co_weights1], weights[2*i-1][0][[rows, cols]], weights[2*i-1][1][co_weights1]
		
		#MUTATION
		mt_weights0=random.sample(range(20), 4)
		mt_weights1=random.sample(range(6), 1)
		rows=[k/5 for k in mt_weights0]
		cols=[k%5 for k in mt_weights0]

		weights[2*i-1][0][[rows, cols]]=np.square(weights[2*i-1][0][[rows, cols]])
		weights[2*i][0][[rows, cols]]=np.square(weights[2*i-1][0][[rows, cols]])
		weights[2*i-1][1][mt_weights1]=np.square(weights[2*i-1][1][mt_weights1])
		weights[2*i][1][mt_weights1]=np.square(weights[2*i][1][mt_weights1]) 

	return weights

def survive(weights):
	weights[8:]=[[np.array([np.array([random.uniform(-1, 1) for i in range(5)]) for j in range(4)]), np.array([random.uniform(-1, 1) for k in range(6)])] for l in range(2)]
	return weights

def sigmoid(x):
	return 1/(1+np.exp(-x))

game()