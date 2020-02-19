import pygame
import math
from pygame.locals import *
import random
import time

# Initialize game object and screen
pygame.init()
pygame.mixer.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

# Load Player Sprite
player = pygame.image.load("resources/images/dude.png")

# Load Other Sprites
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
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
    arrow_speed = 10

    badtimer = 200
    badtimer1 = 0
    badguys = [[640, 150]]
    healthvalue = 200

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
                arrow1 = pygame.transform.rotate(arrow, 0)
                screen.blit(arrow1, (projectile[1], projectile[2]))

        # Draw badgers
        if badtimer == 0:
            badguys.append([640, random.choice([player_first_position, player_second_position])])
            badtimer = 200 - (badtimer1 * 2)
            if badtimer1 >= 35:
                badtimer1 = 35
            else:
                badtimer1 += 5

        index = 0
        for index, badguy in enumerate(badguys):
            if badguy[0] < -64:
                badguys.pop(index)
            badguy[0] -= 3

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
            int((90000 - dt) / 60000),
            str(int((90000 - dt) / 1000 % 60)).zfill(2)),
            True, (0, 0, 0))
        textRect = survivedtext.get_rect()
        textRect.topright = [635, 5]
        screen.blit(survivedtext, textRect)

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
            # playerpos[1] -= movement_displacement_value
            playerpos[1] = player_first_position

        if keys[2]:
            # playerpos[1] += movement_displacement_value
            playerpos[1] = player_second_position
        # if keys[1]:
        #     playerpos[0] -= movement_displacement_value
        # if keys[3]:
        #     playerpos[0] += movement_displacement_value

        # Check for win/lose
        if dt >= 90000:
            running = False
            exitcode = True
        elif healthvalue <= 0:
            running = False
            exitcode = False
        
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

        pygame.display.flip()