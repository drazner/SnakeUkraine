import pygame 
from pygame import mixer 
import time 
import random
from snake import Dot, Snake
import os
#import snake 
#TODO add music and picture effects
#Add Pause menu
#Add start menu
#Add highschores 
#Use Snake class
#Add powerups
#Add different modes
#Add background

pygame.init() 
dis_width = 1300 #700
dis_height = 700 #400
dis = pygame.display.set_mode((dis_width,dis_height))
pygame.display.update() 
pygame.display.set_caption('Snake game by Stone Cold')

white = (255,255,255)
blue = (0,0,255)
red = (255,0,0)
purple = (255,0,255)
black = (0,0,0)
cyan = (0,255,255) 
lime_green = (50,205,50)


snake_block = 70 #10
clock = pygame.time.Clock() 
snake_speed = 10 #30
font_style = pygame.font.SysFont(None, 30) 
flagImg = pygame.image.load('images/ukraineFlag.jpeg')
flagImg = pygame.transform.scale(flagImg, (dis_width, dis_height))
flagImg.set_alpha(200)
bayraktarImg = pygame.image.load('images/bayraktar.png')
bayraktarImg = pygame.transform.scale(bayraktarImg, (snake_block,snake_block))
tankImg = pygame.image.load('images/t80tank.png')
tankImg = pygame.transform.scale(tankImg, (snake_block, snake_block))
bukImg = pygame.image.load('images/BUK.png')
bukImg = pygame.transform.scale(bukImg, (snake_block, snake_block))
scoobyDooTruck = pygame.image.load('images/scoobyDooTruck.png')
scoobyDooTruck = pygame.transform.scale(scoobyDooTruck, (snake_block, snake_block))
explosionImg = pygame.image.load('images/explosion.png')
explosionImg = pygame.transform.scale(explosionImg, (snake_block,snake_block))
widePutin = pygame.image.load('images/widePutinImages/frame00.png')
widePutin = pygame.transform.scale(widePutin, (snake_block,snake_block))
#image0 = pygame.image.load('images/widePutinImages/frame00.png')
    #image0 = pygame.transform.scale(image0, (dis_width, dis_height))
#movie = pygame.movie.Movie('videos/sample.mpg')
#movie_screen = pygame.Surface(movie.get_size()).convert()


def load_images(path):
    images = []
    for i in range(0,76):
        num_suffix = str(i)
        if i<10:
            num_suffix = '0' + num_suffix
        image = pygame.image.load(path + os.sep + 'frame' + num_suffix + '.png').convert()
        image = pygame.transform.scale(image, (dis_width,dis_height))
        images.append(image)
        
    return images

images = load_images('images/widePutinImages')

def message(msg, color, x, y): 
    mesg = font_style.render(msg, True, color) 
    dis.blit(mesg, [x, y])

def spawnFruit(): 
    foodx = round(random.randrange(0, dis_width - snake_block) / float(snake_block)) * float(snake_block)
    foody = round(random.randrange(0, dis_height - snake_block) / float(snake_block)) * float(snake_block)
    foodDot = Dot(foodx,foody,red)
    #print('foodx: ' + str(foodx) + '\nfoody: ' + str(foody))
    curEnemy = chooseEnemy() 
    return foodDot, curEnemy

def initDeltaVector(): 
    x1delta = 0 
    y1delta = 0 
    deltaVector = Dot(x1delta,y1delta,black)
    return deltaVector

def createSnake(): 
    #x1 = ((dis_width / 2) / float(snake_block)) * float(snake_block)
    #y1 = ((dis_height / 2) / float(snake_block)) * float(snake_block)
    x1 = snake_block
    y1 = snake_block
    #print('snakeHeadx: ' + str(x1) + '\snakeHeady: ' + str(y1))
    snakeHead = Dot(x1,y1,cyan)
    snakeList = [snakeHead]
    return snakeList

def gameLoop(): 
    is_running = True
    game_close = False 
    score = 0 #0 
    snake = createSnake() 
    snakeHead = snake[0]
    deltaDot = initDeltaVector() 
    foodDot, curEnemy = spawnFruit()
    frame_num = 0

    while is_running: 
        frame_num+=1
        while game_close == True: 
            frame_num+=1
            # dis.fill(white)
            dis.blit(images[(int(frame_num/4))%76], (0,0))
            print(frame_num)
            message("You Lost! Press [Q]uit or [C]ontinue", red, 10, 10)
            rubUSD = 1/(100*(1+(0.05))**score)
            rubUSD = str(round(rubUSD, 7))
            crashPercent = (1 - ((1-0.05)**score))*100
            crashPercent = str(round(crashPercent,2))
            message("You crashed the ruble " + crashPercent + "% One Ruble is now worth $:  " + rubUSD, lime_green, 100, 100)
            #movie.set_display(movie_screen)
            #movie.play()
            pygame.display.update() 

            for event in pygame.event.get(): 
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_q: 
                        print("Goodbye have a nice day :)")
                        is_running = False 
                        game_close = False 
                    if event.key == pygame.K_c: 
                        print('Play another round :), YOU CAN DO IT')
                        mixer.Channel(2).pause()
                        mixer.Channel(0).unpause() 
                        gameLoop() 

        for event in pygame.event.get(): 
            if event.type==pygame.QUIT: 
                is_running = False 
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT: 
                    deltaDot.x = -snake_block 
                    deltaDot.y = 0
                elif event.key == pygame.K_RIGHT: 
                    deltaDot.x = snake_block
                    deltaDot.y = 0 
                elif event.key == pygame.K_UP: 
                    deltaDot.x = 0
                    deltaDot.y = -snake_block
                elif event.key == pygame.K_DOWN: 
                    deltaDot.x = 0 
                    deltaDot.y = snake_block
                elif event.key == pygame.K_p:
                    paused() 

        if snakeHead.x >= dis_width or snakeHead.x < 0 or snakeHead.y >= dis_height or snakeHead.y<0: 
            mixer.Channel(0).pause()
            mixer.Channel(2).play(pygame.mixer.Sound('music/widePutin.wav'))
            pygame.mixer.Channel(0).set_volume(0.4)
            game_close = True 

        newHead = Dot(0,0,cyan)
        oldHead = snake[-1]
        newHead.x = oldHead.x + deltaDot.x
        newHead.y = oldHead.y + deltaDot.y
        snake.append(newHead)
        snakeHead = snake[-1]

        dis.fill(black) 
        dis.blit(flagImg, (0,0))
        if snakeHead.x == foodDot.x and snakeHead.y == foodDot.y: 
            print('Yummy!\nScore: ' + str(score))
            mixer.Channel(1).play(pygame.mixer.Sound('music/explosion1.wav'))
            dis.blit(explosionImg, (foodDot.x, foodDot.y))
            score += 1 
            foodDot, curEnemy = spawnFruit() 
        else: 
            snake.pop(0)
 
        #draw segments
        for snakeSegment in snake[:-1]: 
            #pygame.draw.rect(dis,snakeSegment.color,[snakeSegment.x,snakeSegment.y,snake_block,snake_block])
            dis.blit(bayraktarImg, (snakeSegment.x, snakeSegment.y))
            if snakeSegment.x == snakeHead.x and snakeSegment.y == snakeHead.y:
                mixer.Channel(0).pause()
                mixer.Channel(2).play(pygame.mixer.Sound('music/widePutin.wav')) 
                pygame.mixer.Channel(0).set_volume(0.4)
                game_close = True 
        #draw head
        #pygame.draw.rect(dis,snakeHead.color,[snakeHead.x, snakeHead.y,snake_block,snake_block])
        dis.blit(bayraktarImg, (snakeHead.x, snakeHead.y))
        #draw food
        #pygame.draw.rect(dis, foodDot.color, [foodDot.x,foodDot.y, snake_block, snake_block])
        
        dis.blit(curEnemy, (foodDot.x, foodDot.y))
        rubUSD =  100*(1+(0.05))**score #
        rubUSD = str(round(rubUSD, 2))
        message("You crashed the Ruble to RUB/USD:  " + rubUSD, lime_green, 10, 10)
        pygame.display.update()

        clock.tick(snake_speed)

    dis.fill(black) 
    message("You Lost", red, 10, 10) 
    pygame.display.update()
    time.sleep(0.5) 
    pygame.quit() 
    quit() 

def paused(): 
    pause = True
    while pause: 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit() 
                quit() 
            elif event.key == pygame.K_p:
                pause = False 

def chooseMusic(): 
    musicList = ['bayraktar.wav','lastDance.wav','coolEdgeDay.wav','rooftopRunDay.wav','escapeFromCity.wav']
    randomSong = 'music/' + random.choice(musicList)
    #return randomSong
    return 'music/bayraktar.wav'

def chooseEnemy(): 
    # random integer from 0 to 9
    ranNum = random.randint(0, 99)
    if 0<=ranNum<=2: 
        randomEnemy = scoobyDooTruck
    elif 3<=ranNum<=55: 
        randomEnemy = tankImg 
    else: 
        randomEnemy = bukImg 
    return randomEnemy 

if __name__ == "__main__": 
    print(images)
    song = chooseMusic() 
    #mixer.init()
    #mixer.music.load(song)
    #mixer.music.play(-1)
    mixer.Channel(0).play(pygame.mixer.Sound(song))
    pygame.mixer.Channel(0).set_volume(0.1)
    gameLoop() 