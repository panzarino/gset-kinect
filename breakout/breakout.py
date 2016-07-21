import pygame
from pygame.color import THECOLORS
from pygame.locals import *
from pygame import sprite
from pygame.draw import *
import math
import random
import time
from pykinect import nui
from pykinect.nui import JointId, SkeletonTrackingState
import ctypes
import thread
from numpy import interp


KINECTEVENT = pygame.USEREVENT

video_display = False

kinect = nui.Runtime()
kinect.skeleton_engine.enabled = True

screen_lock = thread.allocate()

def get_screen_size():
	user32 = ctypes.windll.user32
	return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def surface_to_array(surface):
   buffer_interface = surface.get_buffer()
   address = ctypes.c_void_p()
   size = Py_ssize_t()
   _PyObject_AsWriteBuffer(buffer_interface,
                          ctypes.byref(address), ctypes.byref(size))
   bytes = (ctypes.c_byte * size.value).from_address(address.value)
   bytes.object = buffer_interface
   return bytes

def draw_skeletons(skeletons):
    for index, data in enumerate(skeletons):
        # draw the Head
        HeadPos = skeleton_to_depth_image(data.SkeletonPositions[JointId.Head], dispInfo.current_w, dispInfo.current_h) 
        draw_skeleton_data(data, index, SPINE, 10)
        pygame.draw.circle(screen, SKELETON_COLORS[index], (int(HeadPos[0]), int(HeadPos[1])), 20, 0)
        # drawing the limbs
        draw_skeleton_data(data, index, LEFT_ARM)
        draw_skeleton_data(data, index, RIGHT_ARM)
        draw_skeleton_data(data, index, LEFT_LEG)
        draw_skeleton_data(data, index, RIGHT_LEG)


def depth_frame_ready(frame):
    if video_display:
        return
    with screen_lock:
        address = surface_to_array(screen)
        frame.image.copy_bits(address)
        del address
        if skeletons is not None and draw_skeleton:
            draw_skeletons(skeletons)
        pygame.display.update()    


def video_frame_ready(frame):
    if not video_display:
        return
    with screen_lock:
        address = surface_to_array(screen)
        frame.image.copy_bits(address)
        del address
        if skeletons is not None and draw_skeleton:
            draw_skeletons(skeletons)
        pygame.display.update()

def post_frame(frame):
    try:
        pygame.event.post(pygame.event.Event(KINECTEVENT, skeletons = frame.SkeletonData))
    except:
        pass

class Paddle(object):
	def __init__(self, screen, color, x, y, length, width, outline=0):
		self.screen = screen
		self.color = color
		self.rectlist = [x, y, length, width]
		self.outline = outline;
		self.newx = x
		self.diff = 0
		self.center = x + length / 2

	def draw(self):
		self.rect = rect(self.screen, self.color, self.rectlist, self.outline)

	def change(self):
		if (abs(self.newx-self.rectlist[0])>4):
			self.rectlist = [self.rectlist[0] + self.diff, self.rectlist[1], self.rectlist[2], self.rectlist[3]]
			self.center = self.rectlist[0] + self.rectlist[2] / 2
		self.draw()

	def move(self, newx):
		self.newx = newx
		current = self.rectlist[0]
		diff = self.newx - current
		self.diff = diff/4

class Block(object):
	def __init__(self, screen, color, x, y, length, width, exists, outline=0):
		self.screen = screen
		self.color = color
		self.rectlist = [x, y, length, width]
		self.outline = outline
		self.newx = x
		self.diff = 0
		self.exists = exists

	def draw(self):
		if (self.exists):
			self.rect = rect(self.screen, self.color, self.rectlist, self.outline)

	def change(self):
		if (abs(self.newx-self.rectlist[0])>4):
			self.rectlist = [self.rectlist[0] + self.diff, self.rectlist[1], self.rectlist[2], self.rectlist[3]]
		self.draw()

class Circle(object):
	def __init__(self, screen, color, pos, radius, outline=0):
		self.screen = screen
		self.color = color
		self.pos = pos
		self.radius = radius
		self.outline = outline
		self.balldx = 2
		self.balldy = -1
		self.speed = math.sqrt(self.balldx**2 + self.balldy**2)

	def draw(self):
		self.setPos(int(self.pos[0]), int(self.pos[1]))
		self.rect = circle(self.screen, self.color, self.pos, self.radius, self.outline)

	def setPos(self, xpos, ypos):
		self.pos = (xpos, ypos)

class Ball(Circle):
	def change(self):
		newx = int(self.pos[0])+self.balldx
		newy = int(self.pos[1])+self.balldy
		self.pos = (newx, newy)
		self.draw()

clock = pygame.time.Clock() 

class Game(object):
	def __init__(self):
		kinect.camera.elevation_angle = 4
		kinect.skeleton_engine.enabled = True
		kinect.skeleton_frame_ready += post_frame
		kinect.video_frame_ready += video_frame_ready    
		kinect.video_stream.open(nui.ImageStreamType.Video, 2, 
                                      nui.ImageResolution.Resolution640x480, 
                                      nui.ImageType.Color)
		self.screensize = get_screen_size()
		self.screen = pygame.display.set_mode(self.screensize, pygame.FULLSCREEN)
		pygame.mouse.set_visible(False)
		
		self.width = 1200
		self.height = 600

		self.numBalls = 3

		self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
		self.screen.convert()
		self.screen.fill(THECOLORS["black"])

		self.background = pygame.Surface((self.width, self.height), 0, 32)
		self.background.fill(THECOLORS["black"])
		self.background.convert()

		block1 = Block(self.screen, THECOLORS["white"], 10, 50, 10, 10, True)
		block2 = Block(self.screen, THECOLORS["white"], 20, 50, 10, 10, True)
		block3 = Block(self.screen, THECOLORS["white"], 30, 50, 10, 10, True)
		block4 = Block(self.screen, THECOLORS["white"], 40, 50, 10, 10, True)
		block5 = Block(self.screen, THECOLORS["white"], 10, 50, 10, 10, True)
		block6 = Block(self.screen, THECOLORS["white"], 10, 40, 10, 10, True)
		block7 = Block(self.screen, THECOLORS["white"], 10, 30, 10, 10, True)
		block8 = Block(self.screen, THECOLORS["white"], 10, 20, 10, 10, True)
		block9 = Block(self.screen, THECOLORS["white"], 20, 20, 10, 10, True)
		block10 = Block(self.screen, THECOLORS["white"], 30, 20, 10, 10, True)
		block11 = Block(self.screen, THECOLORS["white"], 40, 20, 10, 10, True)
		block12 = Block(self.screen, THECOLORS["white"], 40, 30, 10, 10, True)	# reverse to match pygame library
		block13 = Block(self.screen, THECOLORS["white"], 40, 40, 10, 10, True)
		block14 = Block(self.screen, THECOLORS["white"], 30, 40, 10, 10, True)

		block15 = Block(self.screen, THECOLORS["white"], 60, 50, 10, 10, True)
		block16 = Block(self.screen, THECOLORS["white"], 70, 50, 10, 10, True)
		block17 = Block(self.screen, THECOLORS["white"], 80, 50, 10, 10, True)
		block18 = Block(self.screen, THECOLORS["white"], 60, 40, 10, 10, True)	# reverse to match pygame library
		block19 = Block(self.screen, THECOLORS["white"], 60, 30, 10, 10, True)
		block20 = Block(self.screen, THECOLORS["white"], 70, 30, 10, 10, True)
		block21 = Block(self.screen, THECOLORS["white"], 80, 30, 10, 10, True)
		block22 = Block(self.screen, THECOLORS["white"], 80, 20, 10, 10, True)	# reverse to match pygame library
		block23 = Block(self.screen, THECOLORS["white"], 80, 10, 10, 10, True)
		block24 = Block(self.screen, THECOLORS["white"], 70, 10, 10, 10, True)
		block25 = Block(self.screen, THECOLORS["white"], 60, 10, 10, 10, True)

		block26 = Block(self.screen, THECOLORS["white"], 100, 50, 10, 10, True)
		block27 = Block(self.screen, THECOLORS["white"], 110, 50, 10, 10, True)
		block28 = Block(self.screen, THECOLORS["white"], 120, 50, 10, 10, True)
		block29 = Block(self.screen, THECOLORS["white"], 100, 40, 10, 10, True)
		block30 = Block(self.screen, THECOLORS["white"], 100, 30, 10, 10, True)
		block31 = Block(self.screen, THECOLORS["white"], 110, 30, 10, 10, True)
		block32 = Block(self.screen, THECOLORS["white"], 120, 30, 10, 10, True)
		block33 = Block(self.screen, THECOLORS["white"], 100, 20, 10, 10, True)
		block34 = Block(self.screen, THECOLORS["white"], 100, 10, 10, 10, True)
		block35 = Block(self.screen, THECOLORS["white"], 110, 10, 10, 10, True)
		block36 = Block(self.screen, THECOLORS["white"], 120, 10, 10, 10, True)

		block37 = Block(self.screen, THECOLORS["white"], 140, 50, 10, 10, True)	# reverse to match pygame library
		block38 = Block(self.screen, THECOLORS["white"], 150, 50, 10, 10, True)	# reverse to match pygame library
		block39 = Block(self.screen, THECOLORS["white"], 160, 50, 10, 10, True)
		block40 = Block(self.screen, THECOLORS["white"], 170, 50, 10, 10, True)	# reverse to match pygame library
		block41 = Block(self.screen, THECOLORS["white"], 180, 50, 10, 10, True)	# reverse to match pygame library
		block42 = Block(self.screen, THECOLORS["white"], 160, 40, 10, 10, True)
		block43 = Block(self.screen, THECOLORS["white"], 160, 30, 10, 10, True)
		block44 = Block(self.screen, THECOLORS["white"], 160, 20, 10, 10, True)
		block45 = Block(self.screen, THECOLORS["white"], 160, 10, 10, 10, True)

		self.pieces_group = (block1, block2, block3, block4, block5, block6, block7, block8, block9, block10, block11, block12, block13, block14, block15, block16, block17, block18, block19, block20, block21, block22, block23, block24, block25, block26, block27, block28, block29, block30, block31, block32, block33, block34, block35, block36, block37, block38, block39, block40, block41, block42, block43, block44, block45)

		self.image1 = pygame.SurfaceType((15, 40))
		pygame.draw.rect(self.image1, THECOLORS["red"], pygame.Rect(0, 0, 90, 6))

		self.ball = Ball(self.screen, THECOLORS["white"], (650, 560), 12)
		self.paddle = Paddle(self.screen, THECOLORS["red"], 550, 580, 200, 10)

		self.isCollided = False

	def quit(self):
		pygame.quit()
		sys.exit()

	def go(self):
		# move paddles to kinect locations
		events = pygame.event.get()
		for e in events:
			if e.type == KINECTEVENT:
				for skeleton in e.skeletons:
					head = skeleton.SkeletonPositions[JointId.Head]
					if (not head.x==0):
						xval = interp(head.x, [-1, 1], [0,1])
						xpos = (xval) * self.width
						self.paddle.move(xpos)
			elif e.type == KEYDOWN:
				if e.key == K_ESCAPE:
					self.quit()

	def doUpdate(self):
		pygame.display.set_caption('Python Kinect Game %d fps' % clock.get_fps())
		self.screen.fill(THECOLORS["black"])
		self.ball.change()
		self.paddle.change()
		for m in self.pieces_group:
			m.change()

		pygame.display.update()

	def play(self):
		while (self.numBalls > 0):

			if (self.ball.pos[0] - self.ball.radius <= 0):
				if (self.isCollided == False):
					self.ball.balldx = abs(self.ball.balldx)
					self.isCollided = True
			elif (self.ball.pos[0] + self.ball.radius >= self.width):
				if (self.isCollided == False):
					self.ball.balldx = -abs(self.ball.balldx)
					self.isCollided = True
			else:
				self.isCollided = False

			if (self.ball.pos[1] - self.ball.radius <= 0):
				if (self.isCollided == False):
					self.ball.balldy = abs(self.ball.balldy)
					self.isCollided = True
			else:
				self.isCollided = False

			if (self.ball.pos[1] >= 610):
				self.numBalls -= 1
				self.ball.setPos(self.paddle.center, 550)
				self.ball.balldy = random.choice([-1, -2])

			if (self.ball.pos[1] + self.ball.radius >= 580 and self.ball.pos[0] >= self.paddle.rectlist[0] and self.ball.pos[0] <= self.paddle.rectlist[0] + self.paddle.rectlist[2]):
				if (self.isCollided == False):
					self.isCollided = True
					if (self.ball.pos[0] == self.paddle.center):
						self.angle = 90 + 5 * (self.paddle.center - self.ball.pos[0])
						self.ball.balldy = -abs(math.sin(math.radians(self.angle)) * self.ball.speed)
						self.ball.balldx = -math.cos(math.radians(self.angle)) * self.ball.speed

					elif (self.ball.pos[0] < self.paddle.center):
						self.angle = 90 + 5 * (self.paddle.center - self.ball.pos[0])
						self.ball.balldy = -abs(math.sin(math.radians(self.angle)) * self.ball.speed)
						self.ball.balldx = -math.cos(math.radians(self.angle)) * self.ball.speed

					elif (self.ball.pos[0] > self.paddle.center):
						self.angle = 90 - 5 * (self.ball.pos[0] - self.paddle.center)
						self.ball.balldy = -abs(math.sin(math.radians(self.angle)) * self.ball.speed)
						self.ball.balldx = -math.cos(math.radians(self.angle)) * self.ball.speed
			else:
				self.isCollided = False

			check = False

			if (self.isCollided == False):
				for m in self.pieces_group:
					if (self.ball.pos[0] + self.ball.radius >= m.rectlist[0] and self.ball.pos[0] - self.ball.radius <= m.rectlist[0] + m.rectlist[2]):
						if (m.rectlist[1] <= self.ball.pos[1] <= m.rectlist[1] + m.rectlist[3] and (m.rectlist[0] < self.ball.pos[0] <= m.rectlist[0] + 5 or m.rectlist[0] + m.rectlist[2] - 5 <= self.ball.pos[0] < m.rectlist[0] + m.rectlist[2]) and m.exists):		# block 1 left/right side
							self.ball.balldx = -self.ball.balldx
							check = True
							self.isCollided = True

						if (m.rectlist[0] <= self.ball.pos[0] <= m.rectlist[0] + m.rectlist[2] and (m.rectlist[1] < self.ball.pos[1] <= m.rectlist[1] + 5 or m.rectlist[1] + m.rectlist[3] - 5 <= self.ball.pos[1] < m.rectlist[1] + m.rectlist[3]) and m.exists):	# block 1 top/bottom side 
							self.ball.balldy = -self.ball.balldy
							self.isCollided = True
							check = True

					else:
						self.isCollided = False
					
					if (check):
						m.exists = False
						check = False

			print(self.ball.balldx)
			print(self.ball.balldy)
			if (abs(self.ball.balldy) < 1):
				if (self.ball.balldy < 0):
					self.ball.balldy = -1
				else:
					self.ball.balldy = 1
			if (abs(self.ball.balldx) < 1):
				if (self.ball.balldx < 0):
					self.ball.balldx = -1
				else:
					self.ball.balldx = 1
			self.totalx = self.ball.pos[0] + self.ball.balldx
			self.totaly = self.ball.pos[1] + self.ball.balldy
			self.ball.setPos(int(self.totalx), int(self.totaly))

			self.go()

			self.doUpdate()

			pygame.display.flip()
			clock.tick(80)

if __name__ == '__main__':
	# Initialize PyGame
	pygame.init()
	pygame.font.init()

	game = Game()
	game.play()