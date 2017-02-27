# INTIALISATION
import pygame, math, sys, random
import numpy as np
from pygame.locals import *
import time
from math import sqrt, exp, atan, pi
import matplotlib.pyplot as plt
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
start = pygame.image.load('assets/start.png')

cact_big = [pygame.image.load('assets/cact_big'+str(i)+'.png') for i in range(1, 5, 1)]
cact_small = [pygame.image.load('assets/cact_small'+str(i)+'.png') for i in range(1, 7, 1)]
cluster = pygame.image.load('assets/cluster.png')

game_over = pygame.image.load('assets/game_over.png')

numbers =[pygame.image.load('assets/numbers/'+str(i)+'.png') for i in range(10)]

clock = pygame.time.Clock()

SCREEN_HEIGHT = screen.get_height()
SCREEN_WIDTH = screen.get_width()
TREX_X = 19
GROUND = SCREEN_HEIGHT-land.get_height()
TREX_Y = SCREEN_HEIGHT-start.get_height()
XSHIFT = land.get_width()-SCREEN_WIDTH-4
ACCLR = 0.0001
GRAVITY = 0.0125
JUMP_Y = 9.687499999999707
CLOUD_SPEED = 0.125
MAX_SPEED = 1.4
FRAME_RATE = 500
JUMP_SPEED = 1.55

graph=[]
cloud_info = [[SCREEN_WIDTH, random.randint(5, TREX_Y-5-cloud.get_height())]]
for i in range(3):
	cloud_info.append([cloud_info[-1][0]+random.randint(50, SCREEN_WIDTH), random.randint(5, TREX_Y-5-cloud.get_height())])


def jump(y, speed_Y):
	global speed_X
	if speed_Y>-JUMP_SPEED:
		y-=speed_Y
		speed_Y-=GRAVITY
	screen.blit(trex['jump'], (TREX_X, y))
	return y, speed_Y


def run(leftLeg):
	if leftLeg == 1:
		screen.blit(trex['run1'], (TREX_X, TREX_Y))
	else:
		screen.blit(trex['run2'], (TREX_X, TREX_Y))


def preprocess():
	global score, score2, landx, land2x, speed_X, cactii, cactii_y, cact_types, cact_big, cact_small, cluster, removed
	removed=0

	score=score2=landx=0
	land2x=-SCREEN_WIDTH
	speed_X=0.75
	#Heights of Cactus
	cactii_y=[SCREEN_HEIGHT-cact_small[0].get_height()+2, 2+SCREEN_HEIGHT-cact_big[0].get_height(),\
	 2+SCREEN_HEIGHT-cluster.get_height()]
	#Types of cactus
	cact_types=[cact_small, cact_big, cluster]
	#List of cactii
	cactii=[[cact_types[1][0], random.randint(SCREEN_WIDTH, 1000), cactii_y[1]]]
	makeCactii()


def makeCactii():
	global cactii, cactii_y, cact_types
	for i in range(5):
		no_of_cactii=random.randint(1,4)
		if no_of_cactii != 4:
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
		global landx, speed_X, land2x, cactii, cact_types, cactii_y, removed
		screen.fill((247, 247, 247))

		if(cloud_info[0][0]+cloud.get_width()<0):
			cloud_info.pop(0)
			cloud_info.append([cloud_info[-1][0]+random.randint(50, SCREEN_WIDTH), random.randint(5, TREX_Y-5-cloud.get_height())])

		for i in range(len(cloud_info)):
			screen.blit(cloud, (cloud_info[i][0], cloud_info[i][1]))
			cloud_info[i][0]-=CLOUD_SPEED
		#Updating list of cactii, removing the cactii passed out of screen and adding new one
		if cactii[0][1]+cactii[0][0].get_width()<0:
			cactii.pop(0)
			removed+=1
		while(len(cactii)<20):
			makeCactii()
		
		#printing land
		screen.blit(land, (-landx, GROUND))

		#checking if land1 has shifted enough to introduce land2
		if(landx>=XSHIFT):
			screen.blit(land, (-land2x, GROUND))
			land2x+=speed_X

		#updating position of cactii
		for i in range(len(cactii)):
			cactii[i][1]-=speed_X
			screen.blit(cactii[i][0], (cactii[i][1], cactii[i][2]))

		#Replacing land by land2 after checking if land has completely gone out of screen
		if(landx>land.get_width()):
			landx=land2x
			land2x=-SCREEN_WIDTH
		#New land position
		landx+=speed_X


def scorer():
	global score,score2
	score+=speed_X
	score2=int(score//25)
	score_str=str(score2)
	digits=[int(i) for i in score_str]
	pos=SCREEN_WIDTH
	for i in range(len(digits)-1, -1, -1):
		screen.blit(numbers[digits[i]], (pos-numbers[digits[i]].get_width()-5, 10))
		pos-=numbers[digits[i]].get_width()+5


def isCollision(y):
	global cactii
	x=TREX_X
	for i in range(len(cactii)):
		if(x+4*trex['jump'].get_width()/5<cactii[i][1] or cactii[i][1]+cactii[i][0].get_width()<x+trex['jump'].get_width()/5):
			continue
		elif (y+4*(trex['jump'].get_height())/5<cactii[i][2]):
			continue
		else:
			return True
	return False


def game():
	global score2, speed_X, removed

	weights=[[np.array([np.array([random.uniform(-1, 1) for i in range(5)]) for j in range(4)]), np.array([random.uniform(-1, 1)\
	 for k in range(6)])] for l in range(50)]

	max_score=0
	plt.ion()
	plt.show()
	for _ in range(1000):
		#State of each genotype in population, whether alove or dead
		popAlive= [1 for i in range(50)]
		#Y coordinate of each genotype, indicates the jump state
		popY= [TREX_Y for i in range(50)]
		#speed in y direction for jumping
		popJumpSpeed = [JUMP_SPEED for i in range (50)]

		noOfJumps=[0 for i in range(50)]

		#When population is dead
		zeroPop=[0 for i in range(50)]	

		fitness=[0 for i in range(50)]

		score=score2=0
		leftLeg=1

		preprocess()

		while popAlive != zeroPop:
			environment()
			for i in range(50):
				if popAlive[i]==1:
					#Check for jumping status
					if popY[i] == TREX_Y: 	#If not in a jump
						input_layer=makeInput()
						input_layer=np.array(input_layer)

						if train_(input_layer, weights[i])>=0:
							popY[i], popJumpSpeed[i]=jump(popY[i], popJumpSpeed[i])
							noOfJumps[i]+=1
						else:
							run(leftLeg)

					else:	#If in a jump
						popY[i], popJumpSpeed[i]=jump(popY[i], popJumpSpeed[i])
						if popJumpSpeed[i]<=-JUMP_SPEED:
							popY[i]=TREX_Y
							popJumpSpeed[i]=JUMP_SPEED

					if isCollision(popY[i]):
						popAlive[i]=0
						if noOfJumps[i]==0:
							fitness[i]=0
						else:
							fitness[i]=removed/noOfJumps[i]

					if(speed_X<MAX_SPEED):
						speed_X+=ACCLR

			scorer()
			pygame.display.flip()
			clock.tick(FRAME_RATE)
			leftLeg=int(not leftLeg)

		screen.blit(trex['over'], (TREX_X, 300))
		if(score2>max_score):
			max_score=score2
			
		print('Generation{_} Fitness {fit:.2f}'.format(_=_+1, fit=round(sum(fitness)/50, 2)))
		graph.append(sum(fitness))
		plt.plot(graph)
		plt.ylabel('generation')
		plt.xlabel('fitness')
		plt.pause(0.1)
		weights, fitness=sortByFitness(weights, fitness)
		weights=crossoverMutate(weights)

	print('MAX SCORE: ', max_score)


def makeInput():
	global cactii, speed_X, cact_types
	#input=[BIAS, DISTANCE, NO_OF_CACTII, SPEED]
	no_of_cactii=1
	for i in range(1, len(cactii)):
		if cactii[0][0].get_width()==cact_types[2].get_width():
			no_of_cactii=4
			break
		elif cactii[i][1]-cactii[i-1][1]<=cactii[i-1][0].get_width():
			no_of_cactii+=1
		else:
			break

	input_vector=[1, (cactii[0][1]-TREX_X+trex['run1'].get_width())/(SCREEN_WIDTH-225), no_of_cactii/4, speed_X/MAX_SPEED]
	return input_vector


def train_(input_layer, weights):
	hidden_layer=sigmoid(np.dot(input_layer, weights[0]))
	output=np.dot(hidden_layer, weights[1][1:])+weights[1][0]

	return output


def sortByFitness(weights, fitness):
	for x in range(49):
		for y in range(49-x):
			if fitness[y]<fitness[y+1]:
				fitness[y], fitness[y+1], weights[y], weights[y+1] = fitness[y+1], fitness[y], weights[y+1], weights[y]
	return weights, fitness


def crossoverMutate(weights):
	for i in range (25):
		#CROSSOVER
		co_weights0=random.sample(range(20), 8)
		co_weights1=random.sample(range(6), 2)
		rows=[k/5 for k in co_weights0]
		cols=[k%5 for k in co_weights0]

		weights[2*i-1][0][[rows, cols]], weights[2*i-1][1][co_weights1], weights[2*i][0][[rows, cols]],\
		 weights[2*i][1][co_weights1] = weights[2*i-1][0][[rows, cols]], weights[2*i-1][1][co_weights1],\
		  weights[2*i-1][0][[rows, cols]], weights[2*i-1][1][co_weights1]
		
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


def sigmoid(x):
	return 1/(1+np.exp(-x))

game()
