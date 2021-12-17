# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


import pygame, sys
import os
import random
import time
import RPi.GPIO as GPIO

global game_running
game_running = True
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN,pull_up_down=GPIO.PUD_UP)

# def main(pos):
def main():
    os.putenv('SDL_VIDEODRIVER','fbcon')
    os.putenv('SDL_FBDEV','/dev/fb1')
    os.putenv('SDL_MOUSEDRV','TSLIB')
    os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')
    # set the window size
    WIDTH = 320
    HEIGHT = 240
    FPS = 30  # gameDisplay的帧率，1/12秒刷新一次
    pygame.init()
    #pygame.mouse.set_visible(True)
    pygame.display.set_caption('Fruit Ninja')  # title
    gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))  # set the size of window
    clock = pygame.time.Clock()
    global no_boom
    no_boom = False
    
    # colour may be used
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    background = pygame.image.load('images/background.jpg')  # background
    font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 21)  # 字体



    # generate the position of the fruits randomly
    def generate_random_fruits(fruit):
        fruit_path = "images/fruit_images/" + fruit + ".png"
        data[fruit] = {
            'img': pygame.image.load(fruit_path),
            'x': random.randint(50, 250),
            'y': 240,
            'speed_x': random.randint(-3, 3),
            'speed_y': random.randint(-15, -10),
            'throw': False,
            't': 0,
            'hit': False,
        }

        if random.random() >= 0.75:
            data[fruit]['throw'] = True
        else:
            data[fruit]['throw'] = False


    data = {}
    ring={'new_game':0,'quit':0,'dojo':0}
    fruits = {'apple', 'banana', 'basaha', 'peach', 'sandia', 'boom'}
    for fruit in fruits:
        generate_random_fruits(fruit)



    # draw the font
    font_name = pygame.font.match_font('comic.ttf')


    def draw_text(display, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        gameDisplay.blit(text_surface, text_rect)


    # 绘制玩家的生命
    def draw_lives(display, x, y, lives, image):
        for i in range(lives):
            img = pygame.image.load(image)
            img_rect = img.get_rect()
            img_rect.x = int(x + 35 * i)
            img_rect.y = y
            display.blit(img, img_rect)


    def hide_cross_lives(x, y):
        gameDisplay.blit(pygame.image.load("images/score.png"), (x, y))


    def show_gameover_screen():
        gameDisplay.blit(background, (0, 0))
        draw_text(gameDisplay, "FRUIT NINJA!", 50, WIDTH / 2, HEIGHT / 4)
        if not game_over:
            draw_text(gameDisplay, "Score : " + str(score), 30, WIDTH / 2, HEIGHT / 2)

        draw_text(gameDisplay, "Press a key to begin!", 32, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        waiting = True
        while waiting:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    waiting = False
    
    def blitRotate(image, topleft, angle):

        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
        gameDisplay.blit(rotated_image, new_rect.topleft)
        

    def show_gamestart_screen():
        
        logo1 = pygame.image.load('images/logo.png')  # background
        logo2 = pygame.image.load('images/ninja.png')
        logo1 = pygame.transform.scale(logo1, (160,90))
        logo2 = pygame.transform.scale(logo2, (130,60))
        
        ring_new_game = pygame.image.load('images/new-game.png')
        ring_quit = pygame.image.load('images/quit.png')
        ring_dojo = pygame.image.load('images/dojo.png')
        ring_new_game = pygame.transform.scale(ring_new_game, (90,90))
        ring_quit = pygame.transform.scale(ring_quit, (90,90))
        ring_dojo = pygame.transform.scale(ring_dojo, (90,90))
        
        gameDisplay.blit(background, (0, 0))
        gameDisplay.blit(logo1, (5, 5))
        gameDisplay.blit(logo2, (170, 30))
        
        data['boom']['img'] = pygame.transform.scale(data['boom']['img'], (40,40))
        data['sandia']['img'] = pygame.transform.scale(data['sandia']['img'], (40,40))
        data['peach']['img'] = pygame.transform.scale(data['peach']['img'], (40,40))
        
        gameDisplay.blit(data['boom']['img'], (244, 113))
        gameDisplay.blit(data['sandia']['img'], (144, 144))
        gameDisplay.blit(data['peach']['img'], (45, 145))
        
        #draw_text(gameDisplay, "Press a key to begin!", 32, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()

        waiting = True
        angle=0
        while waiting:
            
            angle += 2
            if angle>360:
                angle=angle//360
            blitRotate(ring_dojo,(20,120),angle)
            blitRotate(ring_new_game,(120,120),angle)
            blitRotate(ring_quit,(220,90),angle)
            
            pygame.display.flip()
            clock.tick(FPS)
            current_position = pygame.mouse.get_pos()
            if 10 < current_position[0] < 65 and 120 < current_position[1] < 165:
                no_boom = True
                waiting = False
            if 75 < current_position[0] < 165 and 120 < current_position[1] < 165:
                waiting = False
            if 200 < current_position[0] < 265 and 90 < current_position[1] < 135:
                pygame.quit()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    waiting = False
                    
    first_round = True
    game_over = True
    global game_running
    if no_boom == True:
        del data['boom']
    while game_running:
        # pygame.mouse.set_pos(pos[0][0],pos[0][1])
        if game_over:
            if first_round:
                show_gamestart_screen()
                first_round = False
            game_over = False
            player_lives = 3
            draw_lives(gameDisplay, 300, 3, player_lives, 'images/score.png')
            score = 0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_running = False

        gameDisplay.blit(background, (0, 0))
        gameDisplay.blit(font.render('Score : ' + str(score), True, (255, 255, 255)), (0, 0))
        draw_lives(gameDisplay, 195, 3, player_lives, 'images/score.png')

        for key, value in data.items():
            if value['throw']:
                value['x'] += value['speed_x']
                value['y'] += value['speed_y']
                value['speed_y'] += (0.05 * value['t'])
                value['t'] += 1

                if value['y'] <= 480:
                    gameDisplay.blit(value['img'], (value['x'], value['y']))
                else:
                    generate_random_fruits(key)

                current_position = pygame.mouse.get_pos()

                if not value['hit'] and value['x'] < current_position[0] < value['x'] + 60 \
                        and value['y'] < current_position[1] < value['y'] + 60:
                    if key == 'boom':
                        player_lives -= 1
                        if player_lives == 0:
                            hide_cross_lives(195, 9)
                        elif player_lives == 1:
                            hide_cross_lives(145, 9)
                        elif player_lives == 2:
                            hide_cross_lives(95, 9)

                        if player_lives < 0:
                            show_gameover_screen()
                            game_over = True

                        half_fruit_path = "images/fruit_images/xxxf.png"
                    else:
                        half_fruit_path = "images/fruit_images/" + key + "-1" + ".png"

                    value['img'] = pygame.image.load(half_fruit_path)
                    value['speed_x'] += 10
                    if key != 'boom':
                        score += 1
                    score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
                    value['hit'] = True
            else:
                generate_random_fruits(key)

        pygame.display.update()
        clock.tick(FPS)
        if (not GPIO.input(27)):
            pygame.quit()
            return()

    pygame.quit()

if __name__ == '__main__':
    main()
