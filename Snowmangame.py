import pygame
import random

def Snowman_game():
	pygame.init()

	# Initialize window
	wind_width = 500
	wind_height = 700
	win = pygame.display.set_mode((wind_width,wind_height))

	# Initialize window title
	pygame.display.set_caption("First Game")

	# Initialize variables
	stack_min = 5

	#Initialize snowball variables
	radius = 25
	diameter = radius * 2
	x_bottomcircle = wind_width/2
	y_bottomcircle = wind_height - diameter*1.25

	#Movement variables
	vel = 12
	fall_vel = 10
	melt_vel = diameter/10
	delay_vel = diameter/20

	#starting position
	height_ground = diameter*1.1    
	width_ground = wind_width
	
	#Timings
	melting_time = 5000
	#blizzard_time = 100000
	

	#Lists for collision 
	snowball_list = []
	coal_list = []
	add3_list = []
	blizzard_list = []
	snowman_list = [(x_bottomcircle, y_bottomcircle)]
	
	#Starting each action initial condidtions
	run = True
	new_snowball = False 
	new_coal = False
	new_add3 = False
	new_blizzard = False 
	fast = False
	new_coal = False 
	catch_time = pygame.time.get_ticks() + 4500
	melting = False
	winGame = False

	#Images
	bg_image = pygame.image.load('Background.png')
	bg_image_height = bg_image.get_height()
	snowflake_image = pygame.image.load('Snowflake.png')
	snowflake_image = pygame.transform.scale(snowflake_image, (diameter, diameter))
	snowman_image = pygame.image.load('Snowmanbody.png')
	snowman_image = pygame.transform.scale(snowman_image, (diameter, diameter))
	coal_image = pygame.image.load('Coal.png')
	coal_image = pygame.transform.scale(coal_image, (diameter, diameter))
	
	move_increment = 0
	melting_amt = 0
	speed_start = 2500
	speed_end = 6000
	BLUE = (0, 0, 255)

	#Start the game with the background image
	while run: 
		win.blit(bg_image,(0,0), (0, bg_image_height - wind_height - move_increment, wind_width, wind_height))
		pygame.time.delay(50)
		#Set the condition for quitting the game
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		#Set the snowman up
		if len(snowman_list) >= 14:
			x_bottom_idx = len(snowman_list) - 14
		else:
			x_bottom_idx = 0
		x_bottom = snowman_list[x_bottom_idx][0]
		# Generate a new snowball
		catch_time = pygame.time.get_ticks()
		if not new_snowball:
			if fast:
				if pygame.time.get_ticks() - catch_time < melting_time:
					new_snowball_time = random.randint(500,1000) 
				else:
					fast = False
			else:
				new_snowball_time = random.randint(speed_start,speed_end)
			new_snowball_x = random.randint(radius, wind_width - radius)
			new_snowball_y = radius
			start_time = pygame.time.get_ticks()
			new_snowball = True
		else:
			cur_time = pygame.time.get_ticks()
			if cur_time - start_time >= new_snowball_time:
				snowball_list.append((new_snowball_x, new_snowball_y))
				new_snowball = False
		top_snowman_circle = snowman_list[len(snowman_list) - 1]	

		# Generate a new coal
		if not new_coal:
			new_coal_time = random.randint(speed_start,speed_end)
			new_coal_x = random.randint(radius, wind_width - radius)
			new_coal_y = radius
			start_time_coal = pygame.time.get_ticks()
			new_coal = True
		else:
			cur_time = pygame.time.get_ticks()
			if cur_time - start_time_coal >= new_coal_time:
				coal_list.append((new_coal_x, new_coal_y))
				new_coal = False

		# Generate a new add3
		if not new_add3:

			new_add3_time = random.randint(speed_start,speed_end)
			new_add3_x = random.randint(radius, wind_width - radius)
			new_add3_y = radius
			start_time_new_add3 = pygame.time.get_ticks()
			new_add3 = True
		else:
			cur_time = pygame.time.get_ticks()
			if cur_time - start_time_new_add3 >= new_add3_time:
				add3_list.append((new_add3_x, new_add3_y))
				new_add3 = False
		
		# Generate a new blizzard
		if not new_blizzard:
			new_blizzard_time = random.randint(speed_start,speed_end)
			new_blizzard_x = random.randint(radius, wind_width - radius)
			new_blizzard_y = radius
			start_time_blizzard = pygame.time.get_ticks()
			new_blizzard = True
		else:
			cur_time = pygame.time.get_ticks()
			if cur_time - start_time_blizzard >= new_blizzard_time:
				blizzard_list.append((new_blizzard_x, new_blizzard_y))
				new_blizzard = False

		# Iterate through snowball list, update positions, and draw updated snowballs
		for i in range(len(snowball_list) - 1, -1, -1):
			snowball_list[i] = (snowball_list[i][0], snowball_list[i][1] + fall_vel)
			pygame.draw.circle(win,(255,255,255), (snowball_list[i][0], snowball_list[i][1]),radius,0)
			# Remove snowballs from list if snowball is off screen 
			if snowball_list[i][1] < -radius:
				snowball_list.remove(snowball_list[i])
			# If falling snowball collides, add it to the snowman list
			if (abs(snowball_list[i][1] - top_snowman_circle[1]) <= 0.9*diameter) and \
				(abs(snowball_list[i][0] - top_snowman_circle[0]) <= diameter * 0.75):
				catch_time = pygame.time.get_ticks()
				snowman_list.append((top_snowman_circle[0], top_snowman_circle[1]-diameter))
				snowball_list.remove(snowball_list[i])
				if move_increment < bg_image_height - wind_height and len(snowman_list) >= stack_min:
					move_increment += diameter
					for i in range(len(snowman_list)):
						snowman_list[i] = (snowman_list[i][0], snowman_list[i][1] + diameter)
			
				if snowman_list[len(snowman_list) - 1][1] - radius * 3 <= 0:
					run = False
					winGame = True
		for i in range(len(snowman_list)):
			if snowman_list[i][0] < x_bottom:
				new_x = snowman_list[i][0] + vel/3
				if new_x > x_bottom:
					new_x = x_bottom
				snowman_list[i] = (new_x, snowman_list[i][1])
			elif snowman_list[i][0] > x_bottom:
				new_x = snowman_list[i][0] - vel/3
				if new_x < x_bottom:
					new_x = x_bottom
				snowman_list[i] = (new_x, snowman_list[i][1])
		# Iterate through coal list and draw updated snowballs
		for i in range(len(coal_list) - 1, -1, -1):
			coal_list[i] = (coal_list[i][0], coal_list[i][1] + fall_vel)
			win.blit(coal_image,(coal_list[i][0], coal_list[i][1]))
			# Remove coal from list if coal is off screen 
			if coal_list[i][1] < -radius:
				coal_list.remove(coal_list[i])
			# If falling coal collides, melt 3 snowballs
			if(abs(coal_list[i][1] - top_snowman_circle[1]) <= 0.9*diameter) and \
				(abs(coal_list[i][0] - top_snowman_circle[0]) <= diameter * 0.75):
				catch_time = pygame.time.get_ticks()
				coal_list.remove(coal_list[i])
				if move_increment >= diameter:
					new_move_increment = move_increment - 3*diameter
					if new_move_increment < 0:
						move_snowman = move_increment
						move_increment = 0
					else:
						move_increment = new_move_increment
						move_snowman = 3*diameter
					for i in range(len(snowman_list)):
						snowman_list[i] = (snowman_list[i][0], snowman_list[i][1] - move_snowman)
				if len(snowman_list)>3:
					snowman_list.pop() 
					snowman_list.pop()
					snowman_list.pop()
				else:
					run = False
		# Iterate through add3 list, update positions, and draw updated snowballs
		for i in range(len(add3_list) - 1, -1, -1):
			add3_list[i] = (add3_list[i][0], add3_list[i][1] + fall_vel)
			win.blit(snowman_image,(add3_list[i][0], add3_list[i][1]))
			# Remove add3 from list if add3 is off screen 
			if add3_list[i][1] < -radius:
				add3_list.remove(coal_list[i])
			# If falling add3 collides, add 3 snowballs
			if(abs(add3_list[i][1] - top_snowman_circle[1]) <= 0.9*diameter) and \
				(abs(add3_list[i][0] - top_snowman_circle[0]) <= diameter * 0.75):
				catch_time = pygame.time.get_ticks()
				add3_list.remove(add3_list[i])
				snowman_list.append((top_snowman_circle[0], top_snowman_circle[1]-diameter))
				snowman_list.append((top_snowman_circle[0], top_snowman_circle[1]-2*diameter))
				snowman_list.append((top_snowman_circle[0], top_snowman_circle[1]-3*diameter))
				if move_increment < bg_image_height - wind_height and len(snowman_list) > stack_min:
					new_move_increment = move_increment + diameter*3
					if new_move_increment > bg_image_height - wind_height:
						snowman_move = bg_image_height - wind_height - move_increment
						move_increment = bg_image_height - wind_height
					else:
						move_increment = new_move_increment
						snowman_move = 3*diameter
					for i in range(len(snowman_list)):
						snowman_list[i] = (snowman_list[i][0], snowman_list[i][1] + snowman_move)
				if snowman_list[len(snowman_list) - 1][1] - radius * 3 <= 0:
					run = False
					winGame = True
		# Iterate through blizzard list and draw updated snowballs
		for i in range(len(blizzard_list) - 1, -1, -1):
			blizzard_list[i] = (blizzard_list[i][0], blizzard_list[i][1] + fall_vel)
			win.blit(snowflake_image,(blizzard_list[i][0], blizzard_list[i][1]))
			# Remove blizzard from list if snowball is off screen 
			if blizzard_list[i][1] < -radius:
				blizzard_list.remove(coal_list[i])
			# If falling blizzard collides, snowballs will fall faster
			if(abs(blizzard_list[i][1] - top_snowman_circle[1]) <= 0.9*diameter) and \
				(abs(blizzard_list[i][0] - top_snowman_circle[0]) <= diameter * 0.75):
				blizzard_list.remove(blizzard_list[i])
				fast = True
		# Move snowman if left and right keys are pressed and have the stack of snowballs sway
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			if len(snowman_list) >= 14:
				for i in range(len(snowman_list) - 14, len(snowman_list)):
					cur_circle_vel = vel - (2/3) * (i - (len(snowman_list) - 14))
					new_left = snowman_list[i][0] - cur_circle_vel
					if new_left < radius:
						new_left = radius
					snowman_list[i] = (new_left, snowman_list[i][1])
			else:
				for i in range(len(snowman_list)):
					cur_circle_vel = vel - (2/3) * i
					new_left = snowman_list[i][0] - cur_circle_vel
					if new_left < radius:
						new_left = radius
					snowman_list[i] = (new_left, snowman_list[i][1])
				
		if keys[pygame.K_RIGHT]:
			if len(snowman_list) >= 14:
				for i in range(len(snowman_list) - 14, len(snowman_list)):
					cur_circle_vel = vel - (2/3) * (i - (len(snowman_list) - 14))
					new_right = snowman_list[i][0] + cur_circle_vel
					if new_right > wind_width - radius:
						new_right = wind_width - radius
					snowman_list[i] = (new_right, snowman_list[i][1])
			else:
				for i in range(len(snowman_list)):
					cur_circle_vel = vel - (2/3) * i
					new_right = snowman_list[i][0] + cur_circle_vel
					if new_right > wind_width - radius:
						new_right = wind_width - radius
					snowman_list[i] = (new_right, snowman_list[i][1])
		
		for i in range(len(snowman_list)):
			pygame.draw.circle(win,(255,255,255), (snowman_list[i][0], snowman_list[i][1]),radius,0)


		# Melt bottom snowball in snowman
		if melting:
			if melting_amt < diameter:
				melting_amt += melt_vel
				for i in range(len(snowman_list)):
					snowman_list[i] = (snowman_list[i][0], snowman_list[i][1] + melt_vel)
					
			else:
				melting = False
				catch_time = pygame.time.get_ticks()
				snowman_list.pop(0)
				melting_amt = 0
				if move_increment >= diameter:
					move_increment -= diameter
					for i in range(len(snowman_list)):
						snowman_list[i] = (snowman_list[i][0], snowman_list[i][1] - diameter)
				if len(snowman_list) == 0:
					run = False
					winGame = False

		# Check melting time
		if pygame.time.get_ticks() - catch_time > melting_time:
			melting = True

		#Update the pygame window
		pygame.display.update()

	if winGame:
		# Game win screen
		win.fill((0,0,0))
		font = pygame.font.SysFont(None, 24)
		img = font.render('GAME WIN', True, BLUE)
		win.blit(img, (wind_width/2 - 50, wind_height/2))
		pygame.display.update()
		pygame.time.delay(2000)
	else:
		# Game over screen
		win.fill((0,0,0))
		font = pygame.font.SysFont(None, 24)
		img = font.render('GAME OVER', True, BLUE)
		win.blit(img, (wind_width/2 - 50, wind_height/2))
		pygame.display.update()
		pygame.time.delay(2000)
	pygame.quit

Snowman_game()