'''
Pong Version 3.0 supports online 
How to Use:
1) Put networking.py, SERVER.py,PONG.py in the same folder
2) Execute SERVER.py
3) Open client.py for the game to start

'''
import pygame
import sys
import threading
import socket
from networking import Network
class ball():
	def __init__(self):
		self.ball_speed_x = 6
		self.ball_speed_y = 6
		self.player = Player(335,475,1510,335)
		self.opponent = Player(335,475,10,335)
		self.screen_width = 1530
		self.screen_height = 810
		
		#self.rect = pygame.Rect(self.x,self.y,self.height,self.width)
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
		pygame.display.set_caption("P0NG")
	
		self.ball = pygame.Rect(765,405, 30, 30)

		self.bg_color = (0, 0, 0)
		self.white = (255, 255, 255)
	
		self.player_speed = 0
	def ball_animation(self):
			global ball_speed_x, ball_speed_y, player_score, opponent_score
			# increments the position of the ball with +ve and -ve values
			self.ball.x += self.ball_speed_x
			self.ball.y += self.ball_speed_y
			# -ve speed induces backwards movement
			if self.ball.top <= 0 or self.ball.bottom >= self.screen_height:
				self.ball_speed_y *= -1
			if self.ball.left <= 0:
				self.ball_speed_x *= -1
			if self.ball.right >= self.screen_width:
				self.ball_speed_x *= -1
			
			if self.ball.colliderect(self.player.player1) and self.ball_speed_x > 0:
				self.ball_speed_x *= -1
			if self.ball.colliderect(self.opponent.player1) and self.ball_speed_x < 0:
				self.ball_speed_x *= -1	
		
			#if self.ball.colliderect(self.player.player1) and self.ball_speed_x > 0:
			#	self.ball_speed_x *= -1
			#if self.ball.colliderect(self.opponent.player1) and self.ball_speed_x < 0:
			#	self.ball_speed_x *= -1	
			#print(self.ball.top,self.ball.bottom)
		#	print(self.ball.x,self.ball.y)
			
			return(self.ball.x,self.ball.y)
	
	def draw2(self):
		
		pygame.draw.ellipse(self.screen,self.white,self.ball)

class Player():
	def __init__(self,x,y,width,height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height 
		self.screen_width = 1530
		self.screen_height = 810
	
		
		#self.rect = pygame.Rect(self.x,self.y,self.height,self.width)
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
		pygame.display.set_caption("P0NG")
		#self.ball = pygame.Rect(765,405, 30, 30)
		self.player1 = pygame.Rect(self.width, self.height, 10, 140)

		self.bg_color = (0, 0, 0)
		self.white = (255, 255, 255)
	
		self.player_speed = 0
		
		
	def player_animation(self,player_speed):
		self.player1.y += player_speed
		if self.player1.top <= 0:
			self.player1.top = 0
		if self.player1.bottom >= self.screen_height:
			self.player1.bottom = self.screen_height
		return(self.player1.top,self.player1.bottom)
	
	def draw1(self):
		#self.screen.fill(self.bg_color)
		#self.opponent.screen.fill(self.player.bg_color)
		pygame.draw.rect(self.screen, self.white,self.player1)
	

class pong:
	def __init__(self):
		pygame.init()
		self.y = 0
		self.top = 0
		self.bottom = 0
		
		self.screen_width = 1530
		self.screen_height = 810
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
		self.player = Player(335,475,1510,335)
		self.opponent = Player(335,475,10,335)
		self.pb = ball()
		self.op = ball()
		self.screen_width = 1530
		self.screen_height = 810
		self.bg_color = (0, 0, 0)
		self.white = (255, 255, 255)
	
		#self.ball  = Player(30, 30,750, 390)
		#return (self.player.top,self.player.bottom)
		self.opponent_speed = 0
		self.player_speed = 0
		#self.ball = pygame.Rect(self.screen_width/2 - 15, self.screen_height/2 - 15, 30, 30)
		self.opp()
	
	
	def opp(self):
		clock = pygame.time.Clock()
		self.net = Network()
		while True:
			clock.tick(65)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit() 	
					sys.exit()	
				if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_DOWN:
								self.player_speed += 7
						if event.key == pygame.K_UP:
								self.player_speed -= 7
				if event.type == pygame.KEYUP:
						if event.key == pygame.K_DOWN:
							self.player_speed -= 7
						if event.key == pygame.K_UP:
							self.player_speed += 7  
			self.x,self.y = self.player.player_animation(self.player_speed)
			self.b_x,self.b_y = self.pb.ball_animation()
			data = self.net.send(self.make_pos(self.x,self.y))
			datab =  self.net.send(self.make_pos1(self.b_x,self.b_y))
			
			
			
			#print(self.opponent.player1.top,self.opponent.player1.bottom)
				#print(n,e)
			n,e = self.read_pos(data)
			self.opponent.player1.top = int(n)
			self.opponent.player1.bottom = int(e)
			#self.opponent.player_animation(self.player_speed)
			#self.x,self.y = self.player.player_animation(self.player_speed,self.y,self.top,self.bottom)
			self.player.screen.fill(self.player.bg_color)
			self.opponent.screen.fill(self.opponent.bg_color)
			
			if datab[0] == '1':
				x,y = self.read_pos(datab[1:])
				self.op.ball.x = int(x)
				self.op.ball.y = int(y)
				self.screen.fill(self.op.bg_color)
				self.op.draw2()
			else:
				self.screen.fill(self.pb.bg_color)
				self.pb.draw2()
			
			self.player.draw1()
			self.opponent.draw1()
			
			#self.draw2()
			
			pygame.display.flip()
			#self.opponent = Player(n,e)
			#client.sendall(str.encode("\n".join([str(player.top), str(player.bottom)])))
			#n, e = [int(i) for i in client.recv(2048).decode('utf-8').split('\n')]
			
	
	def make_pos(self,x,y):
		#data = str(self.net.pos) + ":" + str(x) + "," + str(y)
		reply = str.encode(",".join(["P",str(self.x),str(self.y)]))
		return reply
	def make_pos1(self,x,y):
		reply = str.encode(",".join(["B",str(x),str(y)]))
		return reply

	def read_pos(self,data):
		data = str(data)
		n,e = data.split(",")
		return n,e
		
	#updates the game window
			
if __name__ == '__main__':
	pong()
