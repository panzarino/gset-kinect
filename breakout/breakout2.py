from graphics import *
import math
import random
import time

win = GraphWin("Breakout", 1200, 600)
win.setCoords(0, 0, 200, 100)
paddle = Polygon(Point(115, 1), Point(85, 1), Point(85, 3), Point(115, 3))
paddle.setFill("blue")
paddle.setOutline("red")
paddle.setWidth(2)
paddle.draw(win)
ball = Circle(Point(100, 5), 2)		# ball starts on paddle
ball.draw(win)						# use leg? to start (kick leg)
ballCptX = 100
ballCptY = 5
radius = 2
balldx = random.choice([2])
balldy = 2#])
speed = math.sqrt(balldx**2 + balldy**2)
paddleCpt = 100
numBalls = 3
lives = Text(Point(190, 90), "Lives: %i" % numBalls)
lives.setSize(16)
lives.draw(win)
block1 = Polygon(Point(100, 50), Point(100, 60), Point(80, 60), Point(80, 50))
block2 = Polygon(Point(80, 50), Point(80, 60), Point(60, 60), Point(60, 50))
block3 = Polygon(Point(80, 70), Point(60, 70), Point(60, 60), Point(80, 60))
block4 = Polygon(Point(120, 50), Point(120, 60), Point(100, 60), Point(100, 50))
block5 = Polygon(Point(140, 50), Point(140, 60), Point(120, 60), Point(120, 50))
block6 = Polygon(Point(140, 70), Point(140, 60), Point(120, 60), Point(120, 70))
block7 = Polygon(Point(80, 80), Point(80, 70), Point(60, 70), Point(60, 80))
block8 = Polygon(Point(100, 70), Point(120, 70), Point(120, 80), Point(100, 80))
block9 = Polygon(Point(100, 70), Point(80, 70), Point(80, 80), Point(100, 80))
block10 = Polygon(Point(120, 70), Point(140, 70), Point(140, 80), Point(120, 80))
block1.setFill("blue")
block2.setFill("green")
block3.setFill("yellow")
block4.setFill("orange")
block5.setFill("red")
block6.setFill("purple")
block7.setFill("pink")
block8.setFill("black")
block9.setFill("tan")
block10.setFill("light blue")
block1.draw(win)
block2.draw(win)
block3.draw(win)
block4.draw(win)
block5.draw(win)
block6.draw(win)
block7.draw(win)
block8.draw(win)
block9.draw(win)
block10.draw(win)
t = Text(Point(100, 65), "Welcome to Breakout!")
t.setSize(16)
t.draw(win)
dx = Text(Point(100, 45), "dx = %f" % balldx)
dy = Text(Point(100, 40), "dy = %f" % balldy)
dx.setSize(16)
dy.setSize(16)
dx.draw(win)
dy.draw(win)
blockExists = [True, True, True, True, True, True, True, True, True, True]
while (numBalls > 0 and blockExists != [False, False, False, False, False, False, False, False, False, False]):
	if (paddleCpt == ballCptX):
		pass
	elif (paddleCpt < ballCptX and paddleCpt < 185):
		paddle.move(2,0)
		paddleCpt += 2
	elif (paddleCpt > ballCptX and paddleCpt > 15):
		paddle.move(-2,0)
		paddleCpt -= 2

	ball.move(balldx, balldy)
	ballCptX += balldx
	ballCptY += balldy
	if (ballCptX-radius <= 0 or ballCptX+radius >= 200):
		balldx *= -1
		dx.setText("dx = %f" % balldx)
	if (ballCptY+radius >= 99):
		balldy *= -1
		dy.setText("dy = %f" % balldy)
	if (ballCptY <= -2):
		numBalls -= 1
		lives.setText("Lives: %i" % numBalls)
		time.sleep(2)
		ball.move(paddleCpt-ballCptX, 5-ballCptY)
		ballCptX = paddleCpt
		ballCptY = 5
		balldx = random.choice([1, 0.5])
		dx.setText("dx = %f" % balldx)
		balldy = random.choice([1, 0.5])
		dy.setText("dy = %f" % balldy)
	elif (ballCptY <= 5 and ballCptX >= paddleCpt-15 and ballCptX <= paddleCpt+15):	# paddle collision
		if (ballCptX == paddleCpt):
			balldx = 0.05
			dx.setText("dx = %f" % balldx)
			balldy *= -1
			dy.setText("dy = %f" % balldy)
		elif (ballCptX < paddleCpt):
			angle = 90 - 6 * (paddleCpt - ballCptX)
			balldy = math.sin(math.radians(angle)) * speed
			dy.setText("dy = %f" % balldy)
			balldx = math.cos(math.radians(angle)) * speed
			dx.setText("dx = %f" % balldx)
		elif (ballCptX > paddleCpt):
			angle = 90 - 6 * (ballCptX - paddleCpt)
			balldy = math.sin(math.radians(angle)) * speed
			dy.setText("dy = %f" % balldy)
			balldx = math.cos(math.radians(angle)) * speed
			dx.setText("dx = %f" % balldx)
	
	# block collisions
	if (ballCptX+radius >= 80 and ballCptX-radius <= 100):
		if ((ballCptX+radius <= 84 or ballCptX-radius >= 96) and (50 <= ballCptY <= 60) and blockExists[0]):		# block 1 left/right side
			balldx *= -1
			dx.setText("dx = %f" % balldx)
			block1.undraw()
			blockExists[0] = False
		elif ((50 <= ballCptY+radius <= 55 or 55 <= ballCptY-radius <= 60) and blockExists[0]):	# block 1 top/bottom side 
			balldy *= -1
			dy.setText("dy = %f" % balldy)
			block1.undraw()
			blockExists[0] = False
		if ((ballCptX+radius <= 84 or ballCptX-radius >= 96) and 70 <= ballCptY <= 80 and blockExists[8]):		# block 9 left/right side
			balldx *= -1
			dx.setText("dx = %f" % balldx)
			block9.undraw()
			blockExists[8] = False
		elif ((70 <= ballCptY+radius <= 75 or 75 <= ballCptY-radius <= 80) and blockExists[8]):	# block 9 top/bottom side 
			balldy *= -1
			dy.setText("dy = %f" % balldy)
			block9.undraw()
			blockExists[8] = False

	elif (ballCptX+radius >= 60 and ballCptX-radius <= 80):
		if ((ballCptX+radius <= 64 or ballCptX-radius >= 76) and 50 <= ballCptY <= 60 and blockExists[1]):		# block 2 left/right side
			balldx *= -1
			dx.setText("dx = %f" % balldx)
			block2.undraw()
			blockExists[1] = False
		elif ((50 <= ballCptY+radius <= 55 or 55 <= ballCptY-radius <= 60) and blockExists[1]):	# block 2 top/bottom side 
			balldy *= -1
			dy.setText("dy = %f" % balldy)
			block2.undraw()
			blockExists[1] = False
		if ((ballCptX+radius <= 64 or ballCptX-radius >= 76) and 60 <= ballCptY <= 70 and blockExists[2]):		# block 3 left/right side
			balldx *= -1
			dx.setText("dx = %f" % balldx)
			block3.undraw()
			blockExists[2] = False
		elif ((60 <= ballCptY+radius <= 65 or 65 <= ballCptY-radius <= 70) and blockExists[2]):	# block 3 top/bottom side 
			balldy *= -1
			dy.setText("dy = %f" % balldy)
			block3.undraw()
			blockExists[2] = False
		if ((ballCptX+radius <= 64 or ballCptX-radius >= 76) and 70 <= ballCptY <= 80 and blockExists[6]):		# block 7 left/right side
			balldx *= -1
			dx.setText("dx = %f" % balldx)
			block7.undraw()
			blockExists[6] = False
		elif ((70 <= ballCptY+radius <= 75 or 75 <= ballCptY-radius <= 80) and blockExists[6]):	# block 7 top/bottom side 
			balldy *= -1
			dy.setText("dy = %f" % balldy)
			block7.undraw()
			blockExists[6] = False

	elif (ballCptX+radius >= 100 and ballCptX-radius <= 120):
		if ((ballCptX+radius <= 104 or ballCptX-radius >= 116) and 50 <= ballCptY <= 60 and blockExists[3]):		# block 4 left/right side
			balldx *= -1
			dx.setText("dx = %f" % balldx)
			block4.undraw()
			blockExists[3] = False
		elif ((50 <= ballCptY+radius <= 55 or 55 <= ballCptY-radius <= 60) and blockExists[3]):	# block 4 top/bottom side 
			balldy *= -1
			dy.setText("dy = %f" % balldy)
			block4.undraw()
			blockExists[3] = False
		if ((ballCptX+radius <= 104 or ballCptX-radius >= 116) and 70 <= ballCptY <= 80 and blockExists[7]):		# block 8 left/right side
			balldx *= -1
			dx.setText("dx = %f" % balldx)
			block8.undraw()
			blockExists[7] = False
		elif ((70 <= ballCptY+radius <= 75 or 75 <= ballCptY-radius <= 80) and blockExists[7]):	# block 8 top/bottom side 
			balldy *= -1
			dy.setText("dy = %f" % balldy)
			block8.undraw()
			blockExists[7] = False

	elif (ballCptX+radius >= 120 and ballCptX-radius <= 140):
		if ((ballCptX+radius <= 124 or ballCptX-radius >= 136) and 50 <= ballCptY <= 60 and blockExists[4]):		# block 5 left/right side
			balldx *= -1
			dx.setText("dx = %f" % balldx)
			block5.undraw()
			blockExists[4] = False
		elif ((50 <= ballCptY+radius <= 55 or 55 <= ballCptY-radius <= 60) and blockExists[4]):	# block 5 top/bottom side 
			balldy *= -1
			dy.setText("dy = %f" % balldy)
			block5.undraw()
			blockExists[4] = False
		if ((ballCptX+radius <= 124 or ballCptX-radius >= 136) and 60 <= ballCptY <= 70 and blockExists[5]):		# block 6 left/right side
			balldx *= -1
			dx.setText("dx = %f" % balldx)
			block6.undraw()
			blockExists[5] = False
		elif ((60 <= ballCptY+radius <= 65 or 65 <= ballCptY-radius <= 70) and blockExists[5]):	# block 6 top/bottom side 
			balldy *= -1
			dy.setText("dy = %f" % balldy)
			block6.undraw()
			blockExists[5] = False
		if ((ballCptX+radius <= 124 or ballCptX-radius >= 136) and 70 <= ballCptY <= 80 and blockExists[9]):		# block 10 left/right side
			balldx *= -1
			dx.setText("dx = %f" % balldx)
			block10.undraw()
			blockExists[9] = False
		elif ((70 <= ballCptY+radius <= 75 or 75 <= ballCptY-radius <= 80) and blockExists[9]):	# block 10 top/bottom side 
			balldy *= -1
			dy.setText("dy = %f" % balldy)
			block10.undraw()
			blockExists[9] = False
if numBalls == 0:
	t.setText("You lost!")
else:
	t.setText("You won!")
win.getMouse()
win.close()