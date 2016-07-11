



"""provides a simple PyGame sample with video, depth stream, and skeletal tracking"""

import sys

import thread
import itertools
import ctypes

import math

from datetime import datetime

import pykinect
from pykinect import nui
from pykinect.nui import JointId, SkeletonTrackingState

import random

import pygame
from pygame.color import THECOLORS
from pygame.locals import *
from pygame.mixer import music

KINECTEVENT = pygame.USEREVENT
VIDEO_WINSIZE = 640, 480
pygame.init()
index = 1
score = 0
round_score = 0
rand_time = random.randint(3, 6)
num_players = 0
net_score = 0
legs = False
arms = False

skeleton_input = raw_input("Would you like to have a skeleton displayed?\n(y, n)")
while(draw_skeletons == None):
    if skeleton_input == "y":
        draw_skeletons = True
    elif skeleton_input == "n":
        draw_skeletons = False
    else:
        skeleton_input = raw_input("Enter a valid value\n(y, n)")
body_parts = raw_input("Would you like to work your upper body, lower body, or both?\n(u, l, b)")
while not (arms or legs):
    if body_parts == "b":
        arms = True
        legs = True
    elif body_parts == "u":
        arms = True
    elif body_parts == "l":
        legs = True
    else:
        body_parts = raw_input("Please enter a valid response\n(u, l, b)")

max_time = float(raw_input("For how long would you like to play? "))

myfont = pygame.font.SysFont("monospace", 36, bold = True)

SKELETON_COLORS = [THECOLORS["red"],  THECOLORS["green"]]

LEFT_ARM = (JointId.ShoulderCenter, 
            JointId.ShoulderLeft, 
            JointId.ElbowLeft, 
            JointId.WristLeft, 
            JointId.HandLeft)
RIGHT_ARM = (JointId.ShoulderCenter, 
             JointId.ShoulderRight, 
             JointId.ElbowRight, 
             JointId.WristRight, 
             JointId.HandRight)
LEFT_LEG = (JointId.HipCenter, 
            JointId.HipLeft, 
            JointId.KneeLeft, 
            JointId.AnkleLeft, 
            JointId.FootLeft)
RIGHT_LEG = (JointId.HipCenter, 
             JointId.HipRight, 
             JointId.KneeRight, 
             JointId.AnkleRight, 
             JointId.FootRight)
SPINE = (JointId.HipCenter, 
         JointId.Spine, 
         JointId.ShoulderCenter, 
         JointId.Head)                

skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image

time_c = datetime.now()
time_s = datetime.now()
original_time = datetime.now()
time_p = datetime.now()
if arms:
    left_hand_pos = (0.0, 0.0)
    right_hand_pos = (0.0, 0.0)
if legs:
    left_foot_pos = (0.0, 0.0)
    right_foot_pos = (0.0, 0.0)

def draw_skeleton_data(pSkelton, index, positions, width = 4):
    start = pSkelton.SkeletonPositions[positions[0]]
       
    for position in itertools.islice(positions, 1, None):
        next = pSkelton.SkeletonPositions[position.value]
        
        curstart = skeleton_to_depth_image(start, dispInfo.current_w, dispInfo.current_h) 
        curend = skeleton_to_depth_image(next, dispInfo.current_w, dispInfo.current_h)

        pygame.draw.line(screen, SKELETON_COLORS[index], curstart, curend, width)
        
        start = next

# recipe to get address of surface: http://archives.seul.org/pygame/users/Apr-2008/msg00218.html
if hasattr(ctypes.pythonapi, 'Py_InitModule4'):
   Py_ssize_t = ctypes.c_int
elif hasattr(ctypes.pythonapi, 'Py_InitModule4_64'):
   Py_ssize_t = ctypes.c_int64
else:
   raise TypeError("Cannot determine type of Py_ssize_t")

_PyObject_AsWriteBuffer = ctypes.pythonapi.PyObject_AsWriteBuffer
_PyObject_AsWriteBuffer.restype = ctypes.c_int
_PyObject_AsWriteBuffer.argtypes = [ctypes.py_object,
                                  ctypes.POINTER(ctypes.c_void_p),
                                  ctypes.POINTER(Py_ssize_t)]

def surface_to_array(surface):
   buffer_interface = surface.get_buffer()
   address = ctypes.c_void_p()
   size = Py_ssize_t()
   _PyObject_AsWriteBuffer(buffer_interface,
                          ctypes.byref(address), ctypes.byref(size))
   bytes = (ctypes.c_byte * size.value).from_address(address.value)
   bytes.object = buffer_interface
   return bytes

def center(font, string, w, x, y, z):
    dim = font.size(string)
    width = w + (y - w - dim[0]) / 2
    height = x + (z - x - dim[1]) / 2
    return (width, height)

def draw_skeletons(skeletons):
    for x, data in enumerate(skeletons):
        # draw the Head
        HeadPos = skeleton_to_depth_image(data.SkeletonPositions[JointId.Head], dispInfo.current_w, dispInfo.current_h) 
        draw_skeleton_data(data, index, SPINE, 10)
        pygame.draw.circle(screen, SKELETON_COLORS[index], (int(HeadPos[0]), int(HeadPos[1])), 20, 0)
    
        # drawing the limbs
        draw_skeleton_data(data, index, LEFT_ARM)
        draw_skeleton_data(data, index, RIGHT_ARM)
        draw_skeleton_data(data, index, LEFT_LEG)
        draw_skeleton_data(data, index, RIGHT_LEG)

def video_frame_ready(frame):
    with screen_lock:
        address = surface_to_array(screen)
        frame.image.copy_bits(address)
        del address
        if skeletons is not None and draw_skeleton:
            draw_skeletons(skeletons)

def get_change(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def draw_score():
    p = center(myfont, str(int(round_score)), 0, 0, 160, 120)
    p1 = center(myfont, str(num_players) + "-P", 480, 0, 640, 120)
    screen.unlock()
    try:
        screen.blit(myfont.render(str(int(round_score)), True, (0, 0, 0)), p)
        screen.blit(myfont.render(str(num_players) + "-P", True, (0, 0, 0)), p1)
        pygame.display.update()
    except pygame.error:
        screen.unlock()

def display_box():
    rect = Rect(0, 0, 160, 120)
    rect2 = Rect(480, 0, 640, 120)
    if index == 1:
        pygame.Surface.fill(screen, (0, 255, 0), rect)
        pygame.Surface.fill(screen, (0, 255, 0), rect2)
    else :
        pygame.Surface.fill(screen, (255, 0, 0), rect)
        pygame.Surface.fill(screen, (255, 0, 0), rect2)
    draw_score()

def score_update(e, t):
    global left_hand_pos
    global right_hand_pos
    global left_foot_pos
    global right_foot_pos
    global num_players
    global legs
    global arms
    difference_p = datetime.now() - t
    score_change = 0
    num_players = 0
    for skeletons in e.skeletons:
        if skeletons.eTrackingState == SkeletonTrackingState.TRACKED:
            num_players += 1            

            if arms:
                left_hand = skeletons.SkeletonPositions[JointId.HandLeft]
                right_hand = skeletons.SkeletonPositions[JointId.HandRight]
                first_time = left_hand_pos == (0,0)
            if legs:
                left_foot = skeletons.SkeletonPositions[JointId.FootLeft]
                right_foot = skeletons.SkeletonPositions[JointId.FootRight]
                first_time = left_foot_pos == (0,0)
            
            
            
            if difference_p.seconds >= 0.01:
                if arms:
                    left_hand_pos_now = left_hand.x, left_hand.y
                    score_change += get_change(100 * left_hand_pos[0], 100 * left_hand_pos[1], 100 * left_hand_pos_now[0], 100 *left_hand_pos_now[1])
                    left_hand_pos = left_hand_pos_now
                    
                    right_hand_pos_now = right_hand.x, right_hand.y
                    score_change += get_change(100 * right_hand_pos[0], 100 * right_hand_pos[1], 100 * right_hand_pos_now[0], 100 * right_hand_pos_now[1])
                    right_hand_pos = right_hand_pos_now
                if legs:
                    left_foot_pos_now = left_foot.x, left_foot.y
                    score_change = get_change(100 * left_foot_pos[0], 100 * left_foot_pos[1], 100 * left_foot_pos_now[0], 100 *left_foot_pos_now[1])
                    left_foot_pos = left_foot_pos_now
                    
                    right_foot_pos_now = right_foot.x, right_foot.y
                    score_change += get_change(100 * right_foot_pos[0], 100 * right_foot_pos[1], 100 * right_foot_pos_now[0], 100 * right_foot_pos_now[1])
                    right_foot_pos = right_foot_pos_now
                
                time_p = datetime.now()

                if first_time:
                    return 0
    if index == 0:
        if num_players == 2:
            return -1 * int(score_change / 4)
        return -1 * score_change
    else:
        return score_change


if __name__ == '__main__':
    full_screen = False

    pygame.mixer.music.load("Maple Leaf Rag.wav")
    

    first = True

    screen_lock = thread.allocate()

    screen = pygame.display.set_mode(VIDEO_WINSIZE,0,32)
    screen.unlock()
    pygame.display.set_caption('Red-Light, Green-Light, 1, 2, 3!')
    skeletons = None
    screen.fill(THECOLORS["black"])

    kinect = nui.Runtime()
    kinect.camera.elevation_angle = 2
    kinect.skeleton_engine.enabled = True
    def post_frame(frame):
        try:
            pygame.event.post(pygame.event.Event(KINECTEVENT, skeletons = frame.SkeletonData))
        except:
            # event queue full
            pass

    kinect.skeleton_frame_ready += post_frame
    
    kinect.video_frame_ready += video_frame_ready    
    
    kinect.video_stream.open(nui.ImageStreamType.Video, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Color)
    
    # main game loop
    done = False
    while(pygame.event.wait().type != KINECTEVENT)
        pass
    while not done:
        e = pygame.event.wait()
        if first:
            time_m = datetime.now()
            first = False
        difference_c = datetime.now() - time_c
        difference_s = datetime.now() - time_s
        difference_m = datetime.now() - time_m
        if difference_m.seconds > max_time:
            done = True
            break
        if difference_s.seconds >= 0.5:
            round_score = score
            time_s = datetime.now()
        if difference_c.seconds >= rand_time:
            time_c = datetime.now()
            rand_time = random.randint(3, 6)
            index += 1
            if index == 2:
                index = 0
                pygame.mixer.music.load("Tick-Tock.wav")
            else:
                pygame.mixer.music.load("Maple Leaf Rag.wav")
            pygame.mixer.music.play(0)
        dispInfo = pygame.display.Info()
        if e.type == pygame.QUIT:
            done = True
            break
        elif e.type == KINECTEVENT:
            skeletons = e.skeletons
            dif = score_update(e, time_p)
            if dif != None and dif != 0:
                time_p = datetime.now()
                score += dif
                net_score += abs(dif)
            if draw_skeleton:
                draw_skeletons(skeletons)
            display_box()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                done = True
                break
            elif e.key == K_s:
                draw_skeleton = not draw_skeleton
            elif e.key == K_u:
                kinect.camera.elevation_angle = kinect.camera.elevation_angle + 2
            elif e.key == K_j:
                kinect.camera.elevation_angle = kinect.camera.elevation_angle - 2
            elif e.key == K_x:
                kinect.camera.elevation_angle = 2

t = datetime.now()

myfont2 = pygame.font.SysFont("monospace", 80, bold = True)

pos = center(myfont2, "SCORE: " + str(int(score)), 0, 0, 640, 480)
pos2 = center(myfont2, "NET SCORE: " + str(int(net_score)), 0, 0, 640, 480)

pygame.mixer.music.load("Maple Leaf Rag.wav")
pygame.mixer.music.play(0)

while((datetime.now() - t).seconds <= 5):
    rect3 = (0, 0, 640, 480)
    screen.unlock()
    pygame.Surface.fill(screen, (0, 0, 0), rect3)
    try:
        screen.blit(myfont2.render("SCORE: " + str(int(score)), True, (255, 255, 255)), pos)
        pygame.display.update()
    except pygame.error:
        screen.unlock()
while((datetime.now() - t).seconds <= 10):
    rect3 = (0, 0, 640, 480)
    screen.unlock()
    pygame.Surface.fill(screen, (0, 0, 0), rect3)
    try:
        screen.blit(myfont2.render("NET SCORE: " + str(int(net_score)), True, (255, 255, 255)), pos2)
        pygame.display.update()
    except pygame.error:
        screen.unlock()
sys.exit()

#Testing GitHub