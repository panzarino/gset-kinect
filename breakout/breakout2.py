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
balldx = random.choice([0.5, 1, 1.5, 2, -0.5, -1, -1.5, -2])
balldy = random.choice([0.5, 1, 1.5, 2])
speed = math.sqrt(balldx**2 + balldy**2)
paddleCpt = 100
numBalls = 3
lives = Text(Point(170, 90), "Balls: ")
lives.setSize(16)
lives.draw(win)
ball1 = Circle(Point(177, 90), 2)
ball2 = Circle(Point(183, 90), 2)
ball3 = Circle(Point(189, 90), 2)
ball1.draw(win)
ball2.draw(win)
ball3.draw(win)
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
block10.setFill("sky blue")
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
blockArray = Text(Point(100, 35), blockExists)
blockArray.setSize(16)
blockArray.draw(win)
time.sleep(2)
t.setText(3)
time.sleep(1)
t.setText(2)
time.sleep(1)
t.setText(1)
time.sleep(1)
t.setText("Begin!")
while (numBalls > 0 and blockExists != [False, False, False, False, False, False, False, False, False, False]):
	if (abs(paddleCpt - ballCptX) <= 2):
		pass
	elif (paddleCpt < ballCptX and paddleCpt < 184):
		paddle.move(1,0)
		paddleCpt += 1
	elif (paddleCpt > ballCptX and paddleCpt > 16):
		paddle.move(-1,0)
		paddleCpt -= 1

	ball.move(balldx, balldy)
	ballCptX += balldx
	ballCptY += balldy
	if (ballCptX-radius <= -1 or ballCptX+radius >= 201):
		balldx *= -1
		dx.setText("dx = %f" % balldx)
	if (ballCptY+radius >= 101):
		balldy *= -1
		dy.setText("dy = %f" % balldy)
	if (ballCptY <= -3):
		numBalls -= 1
		lives.setText("Balls: ")
		if (numBalls == 2):
			ball3.undraw()
		elif (numBalls == 1):
			ball2.undraw()
		elif (numBalls == 0):
			ball1.undraw()
			break
		time.sleep(2)
		ball.move(paddleCpt-ballCptX, 5-ballCptY)
		ballCptX = paddleCpt
		ballCptY = 5
		win.getMouse()
		balldx = random.choice([0.5, 1, 1.5, 2, -0.5, -1, -1.5, -2])
		dx.setText("dx = %f" % balldx)
		balldy = random.choice([0.5, 1, 1.5, 2])
		dy.setText("dy = %f" % balldy)
		speed = math.sqrt(balldx**2 + balldy**2)
	elif (ballCptY <= 5 and ballCptX >= paddleCpt-15 and ballCptX <= paddleCpt+15):	# paddle collision
		if (ballCptX == paddleCpt):
			angle = 90 + 5 * (paddleCpt - ballCptX) + 0.05
			balldy = math.sin(math.radians(angle)) * speed
			dy.setText("dy = %f" % balldy)
			balldx = math.cos(math.radians(angle)) * speed
			dx.setText("dx = %f" % balldx)
		elif (ballCptX < paddleCpt):
			angle = 90 + 5 * (paddleCpt - ballCptX)
			balldy = math.sin(math.radians(angle)) * speed
			dy.setText("dy = %f" % balldy)
			balldx = math.cos(math.radians(angle)) * speed
			dx.setText("dx = %f" % balldx)
		elif (ballCptX > paddleCpt):
			angle = 90 - 5 * (ballCptX - paddleCpt)
			balldy = math.sin(math.radians(angle)) * speed
			dy.setText("dy = %f" % balldy)
			balldx = math.cos(math.radians(angle)) * speed
			dx.setText("dx = %f" % balldx)
	
	# block collisions
	if (ballCptX+radius >= 80 and ballCptX-radius <= 100):
		if ((ballCptX+radius <= 82 and balldx > 0 or ballCptX-radius >= 98 and balldx < 0) and ballCptY+radius >= 50 and ballCptY-radius <= 60 and blockExists[0]):		# block 1 left/right side
			balldx *= -1
			dx.setText("dx = %f" % balldx)
			block1.undraw()
			blockExists[0] = False
			blockArray.setText(blockExists)
		elif (80 <= ballCptX <= 100 and (50 < ballCptY+radius <= 54 or 56 <= ballCptY-radius < 60) and blockExists[0]):	# block 1 top/bottom side 
			balldy *= -1
			dy.setText("dy = %f" % balldy)
			block1.undraw()
			blockExists[0] = False
			blockArray.setText(blockExists)
		if ((ballCptX+radius <= 82 and balldx > 0 or ballCptX-radius >= 98 and balldx < 0) and ballCptY+radius >= 70 and ballCptY-radius <= 80 and blockExists[8]):		# block 9 left/right side
			balldx *= -1
			dx.setText("dx = %f" % balldx)
			block9.undraw()
			blockExists[8] = False
			blockArray.setText(blockExists)
		elif (80 <= ballCptX <= 100 and (70 < ballCptY+radius <= 74 or 76 <= ballCptY-radius < 80) and blockExists[8]):	# block 9 top/bottom side 
			balldy *= -1
			dy.setText("dy = %f" % balldy)
			block9.undraw()
			blockExists[8] = False
			blockArray.setText(blockExists)

	if (ballCptX+radius >= 60 and ballCptX-radius <= 80):
		if ((ballCptX+radius <= 62 and balldx > 0 or ballCptX-radius >= 78 and balldx < 0) and ballCptY+radius >= 60 and ballCptY-radius <= 70 and blockExists[2]):		# block 3 left/right side
			balldx *= -1
			dx.setText("dx = %f" % balldx)
			block3.undraw()
			blockExists[2] = False
			blockArray.setText(blockExists)
		elif (60 <= ballCptX <= 80 and (60 < ballCptY+radius <= 64 or 66 <= ballCptY-radius < 70) and blockExists[2]):	# block 3 top/bottom side 
			balldy *= -1
			dy.setText("dy = %f" % balldy)
			block3.undraw()
			blockExists[2] = False
			blockArray.setText(blockExists)
		if ((ballCptX+radius <= 62 and balldx > 0 or ballCptX-radius >= 78 and balldx < 0) and ballCptY+radius >= 50 and ballCptY-radius <= 60 and blockExists[1]):		# block 2 left/right side
			balldx *= -1
			dx.setText("dx = %f" % balldx)
			block2.undraw()
			blockExists[1] = False
			blockArray.setText(blockExists)
		elif (60 <= ballCptX <= 80 and (50 < ballCptY+radius <= 54 or 56 <= ballCptY-radius < 60) and blockExists[1]):	# block 2 top/bottom side 
			balldy *= -1
			dy.setText("dy = %f" % balldy)
			block2.undraw()
			blockExists[1] = False
			blockArray.setText(blockExists)
		if ((ballCptX+radius <= 62 and balldx > 0 or ballCptX-radius >= 78 and balldx < 0) and ballCptY+radius >= 70 and ballCptY-radius <= 80 and blockExists[6]):		# block 7 left/right side
			balldx *= -1
			dx.setText("dx = %f" % balldx)
			block7.undraw()
			blockExists[6] = False
			blockArray.setText(blockExists)
		elif (60 <= ballCptX <= 80 and (70 < ballCptY+radius <= 74 or 76 <= ballCptY-radius < 80) and blockExists[6]):	# block 7 top/bottom side 
			balldy *= -1
			dy.setText("dy = %f" % balldy)
			block7.undraw()
			blockExists[6] = False
			blockArray.setText(blockExists)


if (ballCptX+radius >= 100 and ballCptX-radius <= 120):
		if ((ballCptX+radius <= 102 and balldx > 0  or ballCptX-radius >= 118 and balldx < 0) and ballCptY+radius >= 50 and ballCptY-radius <= 60 and blockExists[3]):		# block 4 left/right side
			balldx *= -1
			dx.setText("dx = %f" % balldx)
			block4.undraw()
			blockExists[3] = False
			blockArray.setText(blockExists)
		elif (100 <= ballCptX <= 120 and (50 < ballCptY+radius <= 54 or 56 <= ballCptY-radius < 60) and blockExists[3]):	# block 4 top/bottom side 
			balldy *= -1
			dy.setText("dy = %f" % balldy)
			block4.undraw()
			blockExists[3] = False
			blockArray.setText(blockExists)
		if ((ballCptX+radius <= 102 and balldx > 0 or ballCptX-radius >= 118 and balldx < 0) and ballCptY+radius >= 70 and ballCptY-radius <= 80 and blockExists[7]):		# block 8 left/right side
			balldx *= -1
			dx.setText("dx = %f" % balldx)
			block8.undraw()
			blockExists[7] = False
			blockArray.setText(blockExists)
		elif (100 <= ballCptX <= 120 and (70 < ballCptY+radius <= 74 or 76 <= ballCptY-radius < 80) and blockExists[7]):	# block 8 top/bottom side 
			balldy *= -1
			dy.setText("dy = %f" % balldy)
			block8.undraw()
			blockExists[7] = False
			blockArray.setText(blockExists)


if (ballCptX+radius >= 120 and ballCptX-radius <= 140):
		if ((ballCptX+radius <= 122 and balldx > 0 or ballCptX-radius >= 138 and balldx < 0) and ballCptY+radius >= 60 and ballCptY-radius <= 70 and blockExists[5]):		# block 6 left/right side
			balldx *= -1
			dx.setText("dx = %f" % balldx)
			block6.undraw()
			blockExists[5] = False
			blockArray.setText(blockExists)
		elif (120 <= ballCptX <= 140 and (60 < ballCptY+radius <= 64 or 66 <= ballCptY-radius < 70) and blockExists[5]):	# block 6 top/bottom side 
			balldy *= -1
			dy.setText("dy = %f" % balldy)
			block6.undraw()
			blockExists[5] = False
			blockArray.setText(blockExists)
		if ((ballCptX+radius <= 122 and balldx > 0 or ballCptX-radius >= 138 and balldx < 0) and ballCptY+radius >= 50 and ballCptY-radius <= 60 and blockExists[4]):		# block 5 left/right side
			balldx *= -1
			dx.setText("dx = %f" % balldx)
			block5.undraw()
			blockExists[4] = False
			blockArray.setText(blockExists)
		elif (120 <= ballCptX <= 140 and (50 < ballCptY+radius <= 54 or 56 <= ballCptY-radius < 60) and blockExists[4]):	# block 5 top/bottom side 
			balldy *= -1
			dy.setText("dy = %f" % balldy)
			block5.undraw()
			blockExists[4] = False
			blockArray.setText(blockExists)
		if ((ballCptX+radius <= 122 and balldx > 0 or ballCptX-radius >= 138 and balldx < 0) and ballCptY+radius >= 70 and ballCptY-radius <= 80 and blockExists[9]):		# block 10 left/right side
			balldx *= -1
			dx.setText("dx = %f" % balldx)
			block10.undraw()
			blockExists[9] = False
			blockArray.setText(blockExists)
		elif (120 <= ballCptX <= 140 and (70 < ballCptY+radius <= 74 or 76 <= ballCptY-radius < 80) and blockExists[9]):	# block 10 top/bottom side 
			balldy *= -1
			dy.setText("dy = %f" % balldy)
			block10.undraw()
			blockExists[9] = False
			blockArray.setText(blockExists)
if numBalls == 0:
	t.setText("You lost!")
else:
	t.setText("You won!")
win.getMouse()
win.close()