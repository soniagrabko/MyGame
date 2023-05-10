import random
import os
import pygame_button
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

SCORE_FONT = pygame.font.SysFont('Verdana', 20)
GAME_OVER_FONT = pygame.font.SysFont('Verdana', 100)


TXT_NEEDABLE_SCORE = "Потрібно бонусів: "
TXT_FINISH_SCORE = "Залишилося бонусів: "
TXT_SCORE = "Твій рахунок: "
TXT_GAME_OVER = "Програш :("
TXT_YOU_WIN = "Перемога!"
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (202, 228, 241)
 
main_display = pygame.display.set_mode((WIDTH,HEIGHT))

bg =pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

print(PLAYER_IMAGES)

#buttons
start_img = pygame.image.load('start_btn.png').convert_alpha()
exit_img = pygame.image.load('exit_btn.png').convert_alpha()


class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):

        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        main_display.blit(self.image, (self.rect.x, self.rect.y))

        return action

start_button = Button(150, 300, start_img, 1) 
exit_button = Button(800, 300, exit_img, 1) 


player_size = (150, 50)
player = pygame.image.load('player.png').convert_alpha() #pygame.Surface(player_size)
player_rect = pygame.Rect(100, 300, *player_size)
player_move_down = [0,4]
player_move_right = [4,0]
player_move_up = [0,-4]
player_move_left = [-4,0]

def create_enemy():
    enemy_size = (180, 30)
    enemy = pygame.image.load('enemy.png').convert_alpha() #pygame.Surface(enemy_size)
    enemy_rect = pygame.Rect(WIDTH, random.randint(200,HEIGHT-200), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus_size = (40, 280)
    bonus = pygame.image.load('bonus.png').convert_alpha() #pygame.Surface(bonus_size)
    bonus_rect = pygame.Rect(random.randint(150,WIDTH-200), -200, *bonus_size)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]  
      

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500 )

enemies = []

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000 )

bonuses = []

CHANGE_IMAGE = pygame.USEREVENT + 3 
pygame.time.set_timer(CHANGE_IMAGE, 200)

score = 0
win_score = 3
needable_score = win_score

image_index = 0


playing = False
gameOver = False
YouWin = False
start_popup_showing = True

while start_popup_showing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            start_popup_showing = False  

    main_display.fill(COLOR_BLUE)

    if start_button.draw():
        playing = True
        start_popup_showing = False
    if exit_button.draw():
        playing = False
        start_popup_showing = False


    pygame.display.flip()


while playing:
    FPS.tick(120)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
           enemies.append(create_enemy()) 

        if event.type == CREATE_BONUS:
           bonuses.append(create_bonus())        

        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join (IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < - bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < - bg.get_width():
        bg_X2 = bg.get_width()    
    
    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))
                     

    keys = pygame.key.get_pressed()   

    if keys [K_DOWN] and player_rect.bottom < HEIGHT-250:
       player_rect = player_rect.move(player_move_down)

    if keys [K_RIGHT] and player_rect.right < WIDTH:
       player_rect = player_rect.move(player_move_right)

    if keys [K_UP] and player_rect.top > 200:
        player_rect = player_rect.move(player_move_up)

    if keys [K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)   

    for enemy in enemies:  
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1]) 

        if player_rect.colliderect(enemy[1]):
            playing = False
            start_popup_showing = True
            gameOver = True
            
            
        if win_score == 0:
            playing = False
            YouWin = True
            
            

    for bonus in bonuses:  
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1]) 

        if player_rect.colliderect(bonus[1]):
            score += 1
            win_score -= 1 
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(SCORE_FONT.render(TXT_NEEDABLE_SCORE + str(needable_score), True, COLOR_BLACK), (WIDTH-250, 20))
    main_display.blit(SCORE_FONT.render(TXT_FINISH_SCORE + str(win_score), True, COLOR_BLACK), (50, 20))
    main_display.blit(player, player_rect)
    
    
    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus)) 

lose_width = GAME_OVER_FONT.render(str(TXT_GAME_OVER), True, COLOR_BLACK).get_width()       
win_width = GAME_OVER_FONT.render(str(TXT_YOU_WIN), True, COLOR_BLACK).get_width()
score_width = GAME_OVER_FONT.render(str(TXT_SCORE)+ str(score), True, COLOR_BLACK).get_width()
finish_score = SCORE_FONT.render(str(TXT_FINISH_SCORE) + str(win_score), True, COLOR_BLACK)

while gameOver:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            gameOver = False            

    main_display.blit(GAME_OVER_FONT.render(str(TXT_GAME_OVER), True, COLOR_BLACK), ((WIDTH - lose_width)/2, 200))
    main_display.blit(GAME_OVER_FONT.render(TXT_SCORE + str(score), True, COLOR_BLACK), ((WIDTH - score_width)/2, 300))
    pygame.display.flip()


while YouWin:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            YouWin = False            

    main_display.blit(GAME_OVER_FONT.render(str(TXT_YOU_WIN), True, COLOR_BLACK), ((WIDTH - win_width)/2, 200))
    main_display.blit(GAME_OVER_FONT.render(TXT_SCORE + str(score), True, COLOR_BLACK), ((WIDTH - score_width)/2, 300))
    pygame.display.flip()
