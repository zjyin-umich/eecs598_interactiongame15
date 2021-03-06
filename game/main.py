import pygame
import math
from pygame.locals import *
import random
import time
import cv2 as cv
import numpy as np
import sys
import datetime
from threading import Thread

FUNCTIONS_INPUT = [False, False, False, False, False]

# Class for OpenCV Stuff
class ProcessImage:

    def __init__(self):
        self.playing_area_x = 300
        self.touch_history_range = 10
        self.two_finger_history_range = 3
        self.touch_history_swipe_area = []
        self.two_finger_history = []
        self.pinch_last_updated = datetime.datetime.now()
        self.two_finger_clear_interval = 10
        self.t0 = time.time()

    def detect_multi_touch(self, touch_play_area):
        if len(touch_play_area) == 1:
            return "single_touch"
        elif len(touch_play_area) > 1:
            return "multi_touch"
        else:
            return "no_touch"

    def detect_swipe_direction(self):
        y_values = [center[1] for center in self.touch_history_swipe_area]
        sorted_y = y_values[:]
        sorted_y.sort()
        reverse_y = sorted_y[:]
        reverse_y.reverse()
        if len(y_values) > 3:
            if y_values == sorted_y:
                return "swiped_up"
            elif y_values == reverse_y:
                return "swiped_down"
            self.touch_history_swipe_area = []
        return "no_swipe"

    def detect_pinch(self):
        # print(self.two_finger_history)
        if len(self.two_finger_history) < 3:
            return "no_pinch"
        distances = []
        for first, second in self.two_finger_history:
            current_distance = math.sqrt(((first[0] - second[0]) ** 2) + ((first[1] - second[1]) ** 2))
            distances.append(current_distance)

        self.two_finger_history = []

        sorted_distances = distances[:]
        sorted_distances.sort()
        reverse_distances = sorted_distances[:]
        reverse_distances.reverse()

        if sorted_distances == distances:
            return "reverse_pinch"
        elif reverse_distances == distances:
            return "pinch"
        
        return "no_pinch"

    def DetectObject(self):

        vid = cv.VideoCapture(0)

        if(vid.isOpened() == False):
            print('Cannot open input video')
            return

        width = int(vid.get(3))
        height = int(vid.get(4))
        

        while(vid.isOpened()):
            rc, frame = vid.read()

            if(rc == True):
                    
                #[pinkyX, pinkyY] = self.DetectBall(frame, 0, 154, 83, 19, 239, 115)
                self.DetectBall(frame, 24, 33, 203, 100, 151, 255)

                
                
                #Pinky Actual
                #cv.circle(frame, (int(pinkyX), int(pinkyY)), 20, [0,0,255], 2, 8)
                #cv.line(frame,(int(pinkyX), int(pinkyY + 20)), (int(pinkyX + 50), int(pinkyY + 20)), [100,100,255], 2,8)
                #cv.putText(frame, "X = ", (int(pinkyX + 50), int(pinkyY + 20)), cv.FONT_HERSHEY_SIMPLEX,0.5, [50,200,250])
                #cv.putText(frame, str(pinkyX), (int(pinkyX + 65), int(pinkyY + 20)), cv.FONT_HERSHEY_SIMPLEX,0.5, [50,200,250])
                

                #cv.imshow('Input', frame)

                if (cv.waitKey(300) & 0xFF == ord('q')):
                    break

            else:
                break

        vid.release()
        cv.destroyAllWindows()

    # Segment the green ball in a given frame
    def DetectBall(self, frame, loH, loS, loV, hiH, hiS, hiV):

        global FUNCTIONS_INPUT
        
        lower = np.array([loH, loS, loV], dtype = "uint8")
        upper = np.array([hiH, hiS, hiV], dtype = "uint8")
        frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(frame_HSV, lower, upper)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv.dilate(mask, kernel)

        contour_image = np.copy(mask)
        contours, _ = cv.findContours(contour_image, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)


        #greenMask = cv.inRange(frame_HSV,(loH, loS, loV),(hiH, hiS, hiV)) #This is the line being tested
        #output = cv.bitwise_and(frame,frame, mask= mask)


        #contours,  = cv.findContours(canny_output,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

        contours_poly = []
        centers = []
        radius = []
        touch_play_area = []
        
        for i, c in enumerate(contours):
           # calculate moments for each contour
           #contours_poly[i] = cv.approxPolyDP(c, 3, True)
           if cv.contourArea(c)>500:
               center, rad = cv.minEnclosingCircle(c)
               centers.append(center)
               radius.append(rad)

        drawing = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)

        for i in range(len(centers)):
            #color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
            #cv.drawContours(drawing, contours_poly, i, color)
            #cv.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
            #  (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
            if centers[i][0] > self.playing_area_x:
                color = [0, 0, 255]
                touch_play_area.append(centers[i])
            else:
                color = [0, 255, 0]
                self.touch_history_swipe_area.append(center)
                if len(self.touch_history_swipe_area) > self.touch_history_range:
                    self.touch_history_swipe_area = self.touch_history_swipe_area[-1 * self.touch_history_range:]
                # print(self.touch_history_swipe_area)
                
            cv.circle(frame, (int(centers[i][0]), int(centers[i][1])), int(radius[i]), color, -1)
            cv.putText(frame, "x: {}, y: {}".format(int(centers[i][0]), int(centers[i][1]), int(radius[i])), (int(centers[i][0] + radius[i] + 10), int(centers[i][1])), cv.FONT_HERSHEY_SIMPLEX,0.5, [0,0,255])
            cv.putText(frame, "{}".format(int(radius[i])), (int(centers[i][0] + radius[i] + 10), int(centers[i][1] + 20)), cv.FONT_HERSHEY_SIMPLEX,0.5, [0,0,255])
    
        swipe_direction = self.detect_swipe_direction()
        
        if swipe_direction == "swiped_up":
            # print("Swiping up")
            self.touch_history_swipe_area = []
            FUNCTIONS_INPUT[0] = True

        elif swipe_direction == "swiped_down":
            # print("Swiping down")
            self.touch_history_swipe_area = []
            FUNCTIONS_INPUT[1] = True

        touch_type = self.detect_multi_touch(touch_play_area)
        if touch_type == "single_touch":
            # print("Detecting single touch")
            FUNCTIONS_INPUT[2] = True
        if touch_type == "multi_touch":
            # print("Detecting multi touch")
            FUNCTIONS_INPUT[4] = True

        if len(centers) == 2:
            self.two_finger_history.append(centers)
            self.two_finger_history = self.two_finger_history[-1 * self.two_finger_history_range:]
            self.pinch_last_updated = datetime.datetime.now()

        if (datetime.datetime.now() - self.pinch_last_updated).total_seconds() > self.two_finger_clear_interval:
            self.two_finger_history = []

        pinch_event = self.detect_pinch()
        if pinch_event == "pinch":
            # print("Pinch Detected")
            FUNCTIONS_INPUT[3] = True
        # print("detecting pinch")

        cv.imshow('Contours', frame)

def initiateOpenCV():
    processImg = ProcessImage()
    processImg.DetectObject()

camera_thread = Thread(target = initiateOpenCV)
camera_thread.start()

# Initialize game object and screen
pygame.init()
pygame.mixer.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

# Load Player Sprite
player = pygame.image.load("resources/images/BOSS_sample.jpg")
# player = pygame.transform.scale(player, (100, 85))

# Load Other Sprites
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")

quiz = pygame.image.load("resources/images/quiz_bullet.jpg")
quiz = pygame.transform.scale(quiz, (40, 35))

badguyimg = pygame.image.load("resources/images/badguy.png")
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")

# Load audio
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# Outer loop to handle restart
while True:
    
    # Keep track of player position
    keys = [False, False, False, False]
    playerpos = [150, 150]

    t0 = time.time()

    accuracy = [0, 0]
    arrows = []
    movement_displacement_value = 3
    player_first_position = 150
    player_second_position = 350
    arrow_speed = 5
    baddie_speed = 0.5

    badtimer = 200
    badtimer1 = 0
    badguys = [[640, 150]]
    healthvalue = 200

    game_duration = 60000

    running = True
    exitcode = False

    while running:
        # Clear screen for every frame
        screen.fill(255)

        # Draw grass Over entire screen:
        for x in range(int(width/grass.get_width()) + 1):
            for y in range(int(height/grass.get_height()) + 1):
                screen.blit(grass, (x * 100, y * 100))

        # Decrease timer for bad guys
        badtimer -= 1

        # Draw player and rotate according to mouse
        position = pygame.mouse.get_pos()
        angle = math.atan2(position[1] - (playerpos[1] + 32), 
            position[0] - (playerpos[0] + 26))
        # playerrot = pygame.transform.rotate(player, 360 - angle * 57.29)
        playerrot = pygame.transform.rotate(player, 0)
        playerrot_pos = (playerpos[0] - playerrot.get_rect().width / 2, 
            playerpos[1] - playerrot.get_rect().height / 2)
        screen.blit(playerrot, playerrot_pos)

        # Draw arrows
        for bullet in arrows:
            index=0

            velx=math.cos(bullet[0]) * arrow_speed
            vely=math.sin(bullet[0]) * arrow_speed
            
            bullet[1] += velx
            bullet[2] += vely
            
            if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
                arrows.pop(index)

            index += 1

            for projectile in arrows:
                # arrow1 = pygame.transform.rotate(arrow, 360 - projectile[0] * 57.29)
                arrow1 = pygame.transform.rotate(projectile[3], 0)
                screen.blit(arrow1, (projectile[1], projectile[2]))

        # Draw badgers
        if badtimer == 0:
            badguys.append([640, random.choice([player_first_position, player_second_position])])
            badtimer = 200
            # badtimer = 200 - (badtimer1 * 2)
            # if badtimer1 >= 35:
            #     badtimer1 = 35
            # else:
            #     badtimer1 += 5

        index = 0
        for index, badguy in enumerate(badguys):
            if badguy[0] < -64:
                badguys.pop(index)
            badguy[0] -= baddie_speed

            # Detect collision with castle
            badrect = pygame.Rect(badguyimg.get_rect())
            badrect.top = badguy[1]
            badrect.left = badguy[0]
            if badrect.left < 64:
                healthvalue -= random.randint(5, 20)
                badguys.pop(index)
                hit.play()

            # Detect collisions with arrows
            for arrow_index, bullet in enumerate(arrows):
                bullrect = pygame.Rect(arrow.get_rect())
                bullrect.left = bullet[1]
                bullrect.top = bullet[2]
                if badrect.colliderect(bullrect):
                    accuracy[0] += 1
                    try:
                        badguys.pop(index)
                        arrows.pop(arrow_index)
                    except:
                        pass
                    enemy.play()

        for badguy in badguys:
            screen.blit(badguyimg, badguy)

        # Draw castle
        # screen.blit(castle, (0, 30))
        screen.blit(castle, (0, 100))
        screen.blit(castle, (0, 300))
        # screen.blit(castle, (0, 345))

        # Draw clock
        font = pygame.font.Font(None, 24)
        dt = (time.time() - t0) * 1000
        survivedtext = font.render("{}:{}".format(
            int((game_duration - dt) / game_duration),
            str(int((game_duration - dt) / 1000 % 60)).zfill(2)),
            True, (0, 0, 0))
        textRect = survivedtext.get_rect()
        textRect.topright = [635, 5]
        screen.blit(survivedtext, textRect)

        # Draw Instructions
        font = pygame.font.Font(None, 20)
        instructionsText = font.render("1. Swipe to change lanes", True, (0, 0, 0))
        textRect = instructionsText.get_rect()
        textRect.topleft = [15, 30]
        screen.blit(instructionsText, textRect)

        instructionsText = font.render("2. Single tap to shoot arrows", True, (0, 0, 0))
        textRect = instructionsText.get_rect()
        textRect.topleft = [15, 45]
        screen.blit(instructionsText, textRect)

        instructionsText = font.render("3. Double tap to shoot quizzes", True, (0, 0, 0))
        textRect = instructionsText.get_rect()
        textRect.topleft = [15, 60]
        screen.blit(instructionsText, textRect)

        # Draw healthbar
        screen.blit(healthbar, (5, 5))
        for health_val in range(healthvalue):
            screen.blit(health, (health_val + 8, 8))

        # Update screen
        pygame.display.flip()

        # Loop through events
        for event in pygame.event.get():

            # Handle quit
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            # Handle key presses to move character
            if event.type == pygame.KEYDOWN:
                # print("Received Keydown", event)
                if event.key == K_w:
                    keys[0] = True
                # if event.key == K_a:
                #     keys[1] = True
                elif event.key == K_s:
                    keys[2] = True
                # if event.key == K_d:
                #     keys[3] = True
                elif event.key == K_q:
                    pygame.quit()
                    exit(0)
                elif event.key == K_SPACE:
                    # position = pygame.mouse.get_pos()
                    shoot.play()
                    accuracy[1] += 1
                    arrows.append([
                        # math.atan2(position[1] - (playerrot_pos[1] + 32), 
                        # position[0] - (playerrot_pos[0] + 26)),
                        0,
                        playerrot_pos[0] + 32,
                        playerrot_pos[1] + 32
                    ])

            if event.type == pygame.KEYUP:
                if event.key==pygame.K_w:
                    keys[0]=False
                # elif event.key==pygame.K_a:
                #     keys[1]=False
                elif event.key==pygame.K_s:
                    keys[2]=False
                # elif event.key==pygame.K_d:
                #     keys[3]=False

            # # Handle mouse click to shoot arrows
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     # position = pygame.mouse.get_pos()
            #     shoot.play()
            #     accuracy[1] += 1
            #     arrows.append([
            #         # math.atan2(position[1] - (playerrot_pos[1] + 32), 
            #         # position[0] - (playerrot_pos[0] + 26)),
            #         0,
            #         playerrot_pos[0] + 32,
            #         playerrot_pos[1] + 32
            #     ])

        if keys[0]:
            playerpos[1] = player_first_position
        if keys[2]:
            playerpos[1] = player_second_position

        if FUNCTIONS_INPUT[0]:
            # playerpos[1] -= movement_displacement_value
            # print("Handling event up")
            playerpos[1] = player_first_position
            FUNCTIONS_INPUT[0] = False

        if FUNCTIONS_INPUT[1]:
            # playerpos[1] += movement_displacement_value
            # print("Handling event down")
            playerpos[1] = player_second_position
            FUNCTIONS_INPUT[1] = False

        if FUNCTIONS_INPUT[2]:
            shoot.play()
            accuracy[1] += 1
            arrows.append([
                0,
                playerrot_pos[0] + 32,
                playerrot_pos[1] + 32,
                arrow
            ])
            FUNCTIONS_INPUT[2] = False

        if FUNCTIONS_INPUT[4]:
            shoot.play()
            accuracy[1] += 1
            arrows.append([
                0,
                playerrot_pos[0] + 32,
                playerrot_pos[1] + 32,
                quiz
            ])
            FUNCTIONS_INPUT[4] = False

        # if keys[1]:
        #     playerpos[0] -= movement_displacement_value
        # if keys[3]:
        #     playerpos[0] += movement_displacement_value

        # Check for win/lose
        if dt >= game_duration:
            running = False
            exitcode = True
            FUNCTIONS_INPUT[3] = False
        elif healthvalue <= 0:
            running = False
            exitcode = False
            FUNCTIONS_INPUT[3] = False
        
        if accuracy[1] != 0:
            final_accuracy = (accuracy[0] * 1.0 / accuracy[1]) * 100
        else:
            final_accuracy = 0

    # Display Win/lose
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    if not exitcode:
        text = font.render("Accuracy: {}%".format(round(final_accuracy, 2)), True, (0, 255, 0))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery + 24
        screen.blit(gameover, (0, 0))
        screen.blit(text, textRect)
    else:
        text = font.render("Accuracy: {}%".format(round(final_accuracy, 2)), True, (0, 255, 0))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery + 24
        screen.blit(youwin, (0, 0))
        screen.blit(text, textRect)


    # Draw Instructions
    font = pygame.font.Font(None, 20)
    instructionsText = font.render("Pinch to restart game", True, (0, 0, 0))
    textRect = instructionsText.get_rect()
    textRect.topleft = [270, 380]
    screen.blit(instructionsText, textRect)

    restart = False
    
    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            elif event.type == pygame.KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    exit(0)

                elif event.key == K_r:
                    restart = True

        if FUNCTIONS_INPUT[3]:
            restart = True
            FUNCTIONS_INPUT[3] = False

        pygame.display.flip()

