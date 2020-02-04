import os, time, random
from threading import Thread
os.system('clear')
width = int(os.popen('stty size', 'r').read().split()[1]) + 3
height = 8
background = ' '
ground = '━'
gaming = True
jumping = False
listening = True
godmode = False
sleep = 0.05

def message ():
	print ("""

   ┏━┓      \033[33mThere is no internet conection\033[0m
   ┣┳┛      \033[37m    Press Ctrl + Z to exit\033[0m
 ━━┻┻━━━
""")
	pos = 2
	image = ['  ┏━┓  ','  ┣┳┛  ','━━┻┻━━━']
	input ()
	for row in range(height - pos - 3):
		time.sleep(0.03)
		message = '\033[F' * 10
		string = ''
		for newline in range(height):
			string = background * (width - 3)
			if newline >= pos:
				if newline < pos + 3:
					string = string[0] + image[newline - pos] + string[9:]
			message += string + '\n'
		print (message)
		pos += 1
	for colum in range(width - 12):
		time.sleep(0.01)
		message = '\033[F' * 10
		string = ''
		for newline in range(height):
			string = background * (width - 3)
			if newline == height - 1:
				string = ground * (9 + colum)
			if newline >= pos:
				if newline < pos + 3:
 					string = string[0] + image[newline - pos] + string[9:]
			message += string + '\n'
		print (message)

def game ():
	cactus = [['━┻━', '┗╋┛', ' ┃ '], ['━┻━', '┗┫ ', ' ┣┛'], ['━┻━', ' ┣┛', '┗┫ ']]
	dino = ['   ','┣┳┛','┏━┓']
	dino_left = '┻━━'
	dino_right = '━┻━'
	bird = ['┻┳━']
	bird_up = '┻┻━'
	bird_down = '┻┳━'
	jump = [1,2,3,4,4,4,4,3,2,1]
	birds = False
	left = False
	next = 0
	moment = 0
	score = 1
	space = 0
	sprites = []
#	jumps = []
	score_str = '1'

	field = '\033[F' * 10
	sprites.append([dino,width-7,3,0])

	global gaming, jumping, listening, sleep
	while gaming:
		if next == 0:
			if random.randint(0,3) == 0:
				if random.randint(0,1) == 0:
					sprites.append([cactus[1],0,3,0])
					sprites.append([cactus[0],-3,3,0])
				else:
					sprites.append([cactus[0],0,3,0])
					sprites.append([cactus[2],-3,3,0])
#				jumps.append(0)
				next = random.randint(30,60)
			else:
				sprites.append([cactus[random.randint(0,2)],0,3,0])
#				jumps.append(3)
				next = random.randint(12,60)
				if birds == True:
					if next > 20:
						rand = random.randint(0,3)
						if rand < 2:
							if rand == 0:
								sprites.append([bird,-sprites[0][1]-8-random.randint(0,3)*2,1,random.randint(4,5)])
							else:
								sprites.append([bird,-sprites[0][1]+8+random.randint(0,3)*2,1,random.randint(4,5)])
#								jumps[len(jumps)-1] = 0
		else:
			next -= 1
		if jumping:
			dino[0] = '   '
			if moment < len(jump):
				sprites[0][3] = jump[moment]
				moment += 1
			else:
				sprites[0][3] = 0
				moment = 0
				space = 0
				jumping = False
		if space == 0:
			if left == False:
				if jumping == False:
					dino[0] = dino_left
				bird[0] = bird_up
				left = True
			else:
				if jumping == False:
					dino[0] = dino_right
				score += 1
				bird[0] = bird_down
				left = False
			space = 3
		else:
			space -= 1
		for row in range (height):
			line = ''
			objects = []
			if row == 0:
				objects.append([score_str,width-len(score_str),len(score_str)])
			for sprite in sprites:
				if sprite[1] >= width + len(sprite[0]) - 4:
					sprites.remove(sprite)
				if sprite[3] + sprite[2]  >= height - row:
					if sprite[3] <= height - row - 1:
						if sprite != sprites[0]:
							if sprites[0][3] + sprites[0][2]  >= height - row:
								if sprites[0][3] <= height - row - 2:
									if sprite[0][height-row-1-sprite[3]][0] == ' ':
										transl = 1
									else:
										transl = 0
									if sprite[0][height-row-1-sprite[3]][2] == ' ':
										transr = 1
									else:
										transr = 0
#									if jumping == False:
#										if sprites[0][1] > sprite[1]:
#											if sprites[0][1] == sprite[1] + 4 + jumps[0]:
#												jumping = True
#												del jumps[0]
									if sprites[0][1]  < sprite[1] + 3 - transl:
										if sprites[0][1] + 3 - transr > sprite[1]:
											if godmode == False:
												gaming = False
						objects.append([sprite[0][height-row-1-sprite[3]],width-sprite[1]-1,len(sprite[0])])
			for column in range (width):
				if row == height - 1:
					char = ground
				else:
					char = background
				line += char
			for object in objects:
				if object[0][0] == ' ':
					transpl = 1
					object[0] = object[0][1:]
				else:
					transpl = 0
				if object[0][len(object[0]) - 1] == ' ':
	                                transpr = 1
	                                object[0] = object[0][:len(object[0]) - 1]
				else:
	                                transpr = 0
				line = line[:object[1] + transpl] + object[0] + line[object[1] + 3 - transpr:]
			line = line[3:width]
			field += line + '\n'
		if gaming:
			guide = '\033[37mPress Enter to jump\033[0m'
		else:
			guide = '\033[37mYou dead. Press Enter to exit\033[0m'
		field += guide + ' ' * (width - 3 - len(guide))
		print ('\033F' + field)
		if gaming == True:
			for sprite in range(len(sprites)):
				if sprite == 0:
					continue
				sprites[sprite][1] += 1
				if sprites[sprite][0][0] == bird[0]:
					sprites[sprite][1] += 1
			score_str = str(score)
			time.sleep (sleep)
			if sleep > 0.008:
				sleep -= 0.00001
				if sleep < 0.04:
					birds = True
			field = '\033[F' * (height + 1)
		else:
			time.sleep (0.4)
			listening = False

def inp ():
	global jumping, godmode, sleep
	while listening:
		cheat = input ()
		if listening:
			print ('\033[F') #\033[F' + ' ' * (width - 3))
		else:
			print ('\033[F\033[F' + ' ' * (width - 3))
		jumping = True
		if cheat == 'god ':
			godmode = True
		elif cheat == 'hiv ':
			sleep = 0.0000000000001

def threads ():
	inp_thread = Thread(target = inp)
	game_thread = Thread(target = game)

	inp_thread.start ()
	game_thread.start ()

message ()
threads ()
