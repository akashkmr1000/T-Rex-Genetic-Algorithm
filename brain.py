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
ACCLR = 5e-5
GRAVITY = 0.0125
JUMP_Y = 9.687499999999707
CLOUD_SPEED = 0.125
MAX_SPEED = 1.5
FRAME_RATE = 5000000
JUMP_SPEED = 1.55
POP_SIZE=6*10
graph=[]

prev=-1


def jump(y, speed_Y):
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
	global score, score2, landx, land2x, speed_X, cactii, cactii_y,\
	 cact_types, cact_big, cact_small, cluster, removed,	cloud_info, ctr
	removed=0
	ctr=0

	score=score2=landx=0
	land2x=-SCREEN_WIDTH
	speed_X=0.75
	#Heights of Cactus
	cactii_y=[SCREEN_HEIGHT-cact_small[0].get_height()+2, \
	2+SCREEN_HEIGHT-cact_big[0].get_height(),\
	 2+SCREEN_HEIGHT-cluster.get_height()]

	#Types of cactus
	cact_types=[cact_small, cact_big, cluster]

	#List of cactii
	cactii=[[cact_types[1][0], random.randint(SCREEN_WIDTH, 1000), cactii_y[1], ctr]]
	ctr+=1
	makeCactii()

	'''#List of ptero positions
				pteroPos = [(random.randint(10000, 20000), random)]
			'''

	#Clouds
	cloud_info = [[SCREEN_WIDTH, random.randint(5, TREX_Y-5-cloud.get_height())]]
	for i in range(3):
		cloud_info.append([cloud_info[-1][0]+random.randint(50, SCREEN_WIDTH), \
			random.randint(5, TREX_Y-5-cloud.get_height())])

def makeCactii():
	global cactii, cactii_y, cact_types, ctr
	for i in range(3):
		no_of_cactii=random.randint(1,4)
		if no_of_cactii != 4:
			cact_=random.randint(0,1)
			select_cact=random.sample(range(len(cact_types[cact_])), no_of_cactii)
			for j in range(len(select_cact)):
				if j==0:
					cactii.append([cact_types[cact_][select_cact[j]], \
						cactii[-1][1]+random.randint(300, 1000), cactii_y[cact_], ctr])
				else:
					cactii.append([cact_types[cact_][select_cact[j]], \
						cactii[-1][1]+cactii[-1][0].get_width(), cactii_y[cact_], ctr])
		else:
			cact_= 2
			cactii.append([cact_types[cact_], cactii[-1][1]+random.randint(300, 1000), cactii_y[cact_], ctr])
		ctr+=1


def environment():
		global landx, speed_X, land2x, cactii, cact_types, cactii_y, removed, prev
		screen.fill((247, 247, 247))

		if(cloud_info[0][0]+cloud.get_width()<0):
			cloud_info.pop(0)
			cloud_info.append([cloud_info[-1][0]+random.randint(50, SCREEN_WIDTH),\
			 random.randint(5, TREX_Y-5-cloud.get_height())])

		for i in range(len(cloud_info)):
			screen.blit(cloud, (cloud_info[i][0], cloud_info[i][1]))
			cloud_info[i][0]-=CLOUD_SPEED
		#Removing the cactii passed out of screen and adding new one
		if cactii[0][1]+cactii[0][0].get_width()<0:
			if prev!=cactii[0][3]:
				prev=cactii[0][3]
				removed+=1
			cactii.pop(0)
		while(len(cactii)<30):
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
		if(x+4*trex['jump'].get_width()/5<cactii[i][1] or cactii[i][1]+cactii[i][0].get_width()<\
			x+trex['jump'].get_width()/5):
			continue
		elif (y+4*(trex['jump'].get_height())/5<cactii[i][2]):
			continue
		else:
			return True
	return False


def game():
	global score2, speed_X, removed

	weights=[[np.array([np.array([random.uniform(-1, 1) for i in range(5)]) for j in range(4)]),\
	 np.array([np.array([random.uniform(-1, 1) for i in range(5)]) for j in range(6)]),\
	 np.array([random.uniform(-1, 1) for k in range(6)])]
	  for l in range(POP_SIZE)]

	max_score=0
	plt.ion()
	plt.show()
	for _ in range(1000):
		#State of each genotype in population, whether alove or dead
		popAlive= [1 for i in range(POP_SIZE)]
		#Y coordinate of each genotype, indicates the jump state
		popY= [TREX_Y for i in range(POP_SIZE)]
		#speed in y direction for jumping
		popJumpSpeed = [JUMP_SPEED for i in range (POP_SIZE)]

		noOfJumps=[0 for i in range(POP_SIZE)]

		#When population is dead
		zeroPop=[0 for i in range(POP_SIZE)]	

		fitness=[0 for i in range(POP_SIZE)]

		score=score2=0
		leftLeg=1

		preprocess()

		while popAlive != zeroPop:
			environment()
			for i in range(POP_SIZE):
				if popAlive[i]==1:
					#Check for jumping status
					if popY[i] == TREX_Y: 	#If not in a jump
						input_layer=makeInput()
						input_layer=np.array(input_layer)

						if train_(input_layer, weights[i])>=0.5:
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
							fitness[i]=(removed/noOfJumps[i] + 2*sigmoid(score2/100)-1)/2

			if(speed_X<MAX_SPEED):
				speed_X+=ACCLR

			scorer()
			pygame.display.flip()
			clock.tick(FRAME_RATE)
			leftLeg=int(not leftLeg)
			if score2>5000:
				break

		screen.blit(trex['over'], (TREX_X, 300))
		if(score2>max_score):
			max_score=score2

		print('Generation{_} Fitness {fit:.2f}'.format(_=_+1, \
			fit=round(sum(fitness)/POP_SIZE, 2)))
		plotGraph(fitness)
		if sum(fitness)/POP_SIZE > 0.9:
			break


		weights=UpdateWeights(weights, fitness)

	print('MAX SCORE: ', max_score)
	print(weights)


def plotGraph(fitness):
	graph.append(sum(fitness))
	plt.plot(graph)
	plt.xlabel('generation')
	plt.ylabel('fitness')
	plt.pause(0.1)


def UpdateWeights(weights, fitness):
	weights, fitness=sortByFitness(weights, fitness)
	weights=kill(weights, fitness)
	weightLen=len(weights)
	fitness = normalize(fitness)
	weights=crossover(weights, fitness)
	weights=mutate(weights, weightLen)
	return weights


def normalize (fitness):
	fitness=np.array(fitness)
	fitness=-2*(fitness-1)**2
	fitness=np.exp(fitness)
	return list(fitness)


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

	input_vector=[1, (cactii[0][1]-TREX_X+trex['run1'].get_width())/(SCREEN_WIDTH-300),\
	 no_of_cactii/4, speed_X/MAX_SPEED]
	return input_vector


def train_(input_layer, weights):
	hidden_layer1=np.append(1, sigmoid(np.dot(input_layer, weights[0])))
	hidden_layer2=sigmoid(np.dot(hidden_layer1, weights[1]))
	output = sigmoid(np.dot(hidden_layer2, weights[2][1:])+weights[2][0])

	return output


def sortByFitness(weights, fitness):
	for x in range(POP_SIZE-1):
		for y in range(POP_SIZE-1-x):
			if fitness[y]<fitness[y+1]:
				fitness[y], fitness[y+1], weights[y], weights[y+1] =\
				 fitness[y+1], fitness[y], weights[y+1], weights[y]
	return weights, fitness


def kill(weights, fitness):
	#Removing unfit population
	i=len(weights)-1
	while fitness[i] < 0.4 and len(weights) > POP_SIZE//3:
		weights.pop()
	return weights


def crossover(weights, fitness):
	weightsLen=len(weights)
	sumFitness=sum(fitness)
	while len(weights)<POP_SIZE:
		parents=[-1, -1]
		i=0
		while parents[0]==-1 or parents[1]==-1:
			#print(random.uniform(0,1))
			if random.uniform(0, 1) < fitness[i]/sumFitness:
				if parents[0] == -1:
					parents[0]=i
				elif parents[0]!=i:
					parents[1]=i
			i=int((i+1)%(int(POP_SIZE/5)))
			
		if parents[0] != -1 and parents[1] != -1:
			co_weights0=random.sample(range(20), 8)
			co_weights1=random.sample(range(30), 12)
			co_weights2=random.sample(range(6), 2)
			rows0=[k/5 for k in co_weights0]
			cols0=[k%5 for k in co_weights0]
			rows1=[k/5 for k in co_weights1]
			cols1=[k%5 for k in co_weights1]

			temp1 = weights[parents[0]]
			temp1[0][[rows0, cols0]] = weights[parents[1]][0][[rows0, cols0]]
			temp1[1][[rows1, cols1]] = weights[parents[1]][1][[rows1, cols1]]
			temp1[2][co_weights2] = weights[parents[1]][2][co_weights2]

			temp2 = weights[parents[1]]
			temp2[0][[rows0, cols0]] = weights[parents[0]][0][[rows0, cols0]]
			temp2[1][[rows1, cols1]] = weights[parents[0]][1][[rows1, cols1]]
			temp2[2][co_weights2] = weights[parents[0]][2][co_weights2]


			weights.append(temp1)
			if len(weights) < POP_SIZE:
				weights.append(temp2)
			
	return weights


def mutate(weights, weightsLen):
	#MUTATION
	for i in range(weightsLen):
		for x in range(4):
			for y in range(5):
				if random.uniform(0,1)>0.7:
					weights[i][0][x][y]+=random.uniform(-1, 1)

		for x in range(6):
			for y in range(5):
				if random.uniform(0,1)>0.7:
					weights[i][1][x][y]+=random.uniform(-1, 1)


		for l in range(6):
			if random.uniform(0,1)>0.7:
				weights[i][2][l]+=random.uniform(-1, 1)
	return weights

def sigmoid(x):
	return 1/(1+np.exp(-x))

game()
