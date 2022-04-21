import pygame
import random
import os.path
from time import sleep
import datetime as dt

if not os.path.isfile('high2.txt'):
    with open('high2.txt', 'w') as file:
        file.write('0')

screen_width = 1080
screen_height = 720    
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.font.init()
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (150, 75, 0)
rot = 0.1
phonk = 0
clock =  pygame.time.Clock()
with open('high2.txt', 'r') as file:
        game_high = int(file.read())
FPS = 60
pygame.init()
main_sound = pygame.mixer.Sound('main2.mp3')
jump_sound = pygame.mixer.Sound('jump.wav')
count_sound = pygame.mixer.Sound('countdown.mp3')
start_sound = pygame.mixer.Sound('final.mp3')
q_sound = pygame.mixer.Sound('q_tap.mp3')
fail_sound = pygame.mixer.Sound('fail.mp3')
def restart():
    global chunks, emp, game_speed, game_score, game_hb, in_phonk, bsp, j, did, jr, ball_img, zero_d, sun_color, inv, main_color, colorlist
    jr = False
    game_speed = 4
    game_score = 0
    bsp = 1
    j = False
    did = 0
    game_hb = True
    sun_color = (249, 229, 38)
    inv = False
    in_phonk = False
    main_color = (149, 200, 216)
    colorlist = [GREEN, (173, 255, 47), (52,201,36), (0,69,36), (124,252,0), (0,102,51), (19,136,8), (191,255,0)] 
    chunks = [Chunk(150, 350, GREEN)]
    emp = Empty(170, 330, 20, (255, 0, 0)) 
    pygame.display.update()
    pygame.draw.rect(screen, BLACK, (0, 0, screen_width, screen_height))
    ball_img = pygame.image.load('ball_texture.png')
    tm = dt.datetime.now().time()
    zero_d = dt.timedelta(hours=tm.hour,minutes=tm.minute, seconds=tm.second)
    main_sound.play()


def draw_background():
    pygame.draw.rect(screen, main_color, (0, 0, screen_width, screen_height))
    pygame.draw.circle(screen, sun_color, (screen_width, 0), 100)

def circle_spawn():
    while len(circles) < 10:
        circles.append(Circles())
    for i in range(10):
        if i >= len(circles):
            break
        if circles[i].stade > 25:
            del circles[i]

def rotate(screen, image, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=(emp.x, emp.y))

    screen.blit(rotated_image, new_rect)

def moving_chunks(chunks):
    for ch in chunks:
        if ch:
            ch.chunk_move()

def pr_text(txt, cord=(320, 240), n=20, color=(255, 255, 255)):
    font = pygame.font.SysFont('arial', n)
    text = font.render(txt, True, color)
    screen.blit(text, cord)


def punch(emp, chunk):
    if chunk.sp and chunk.block_spawn + chunk.sp_x - emp.rad <= emp.x <= chunk.block_spawn + 20 + chunk.sp_x + emp.rad - 2 and emp.y > 290:
        return game_hb
    return False 

def chunk_generated():
    while chunks[-1].sp_x < screen_width:

        chunks.append(Chunk(chunks[-1].sp_x + chunks[-1].ch_width, 350, random.choice(colorlist)))
    for i in range(len(chunks)):
        if chunks[i] and chunks[i].sp_x <= 0 - chunks[i].ch_width:
            chunks[i] = None

def switch_hb():
    global game_hb
    game_hb = not game_hb

def phonk():
    global in_phonk, colorlist, sun_color, chunks, inv, main_color, circles
    in_phonk = True
    colorlist = [(128,0,128), (89,0,128), (140,0,128), (50,0,128), (113,0,128), (36,0,128), (61,0,128)]
    sun_color = (77,0,128)
    main_color = (23,18,48)
    pygame.draw.rect(screen, BLACK, (0, 0, screen_width, screen_height))
    pygame.display.update()
    chunks.clear()
    chunks = [Chunk(0, 350, (128,0,128))]
    circles = []
    while emp.njump > 30:
        emp.jump_reset()
    inv = True
    chunk_generated()
    inv = False
    sleep(2.3)


class Empty():
    def __init__(self, x, y, rad, col) -> None:
        self.x = x
        self.y = y
        self.rad = rad
        self.col = col
        self.njump = 45
        self.jumpstade = 1
        self.last = game_speed
        pygame.draw.circle(screen, self.col, (self.x, self.y), self.rad)

    def jump_reset(self):
        if self.njump > 9:
            self.njump -= 2

    def jump(self):
        if self.jumpstade == 1:
            jump_sound.play()
        if self.jumpstade <= ((self.njump - 5) / 2):
            self.y -= 85 / ((self.njump - 5) / 2)
        elif self.jumpstade > ((self.njump - 5) / 2) + 5:
            self.y += 85 / ((self.njump - 5) / 2)   

        if self.jumpstade >= self.njump:
            self.jumpstade = 1
            self.y = 330
        else:
            self.jumpstade += 1
        
    def is_score(self, chunk):
        global game_score, did
        if chunk and chunk.sp_x <= self.x <= chunk.sp_x + chunk.ch_width and chunk.sp:
            if chunk.block_spawn + chunk.sp_x - self.rad <= self.x <= chunk.block_spawn + 20 + chunk.sp_x + self.rad and chunks.index(chunk) != did:
                game_score += 1
                did = chunks.index(chunk)


class Chunk():
    def __init__(self, sp_x, sp_y, c_col):
        global bsp
        self.sp_x = sp_x
        self.sp_y = sp_y
        self.c_col = c_col
        self.ch_width = 150
        self.ch_height = 70
        self.sp = bsp % 2 == 0 if not inv else False
        bsp += 1

        pygame.draw.rect(screen, self.c_col, (sp_x, sp_y, self.ch_width, self.ch_height))
        if self.sp:
            self.block_spawn = random.randint(0, self.ch_width - 20)
            self.img = pygame.image.load('block_texture.png')        

    def chunk_move(self):
        if self.sp_x + self.ch_width >=0:
            self.sp_x -= game_speed
            pygame.draw.rect(screen, self.c_col, (self.sp_x, self.sp_y, self.ch_width, self.ch_height))
            if self.sp:
                self.surf = self.img.get_rect(center = (self.sp_x + self.block_spawn + 10, self.sp_y - 30))
                screen.blit(self.img, self.surf)
    

class Circles:
    def __init__(self):
        self.rad = 0
        self.stade = 1
        self.y = random.randint(0, screen_height)
        while 200 - self.rad < self.y < 550 + self.rad:
            self.y = random.randint(0, screen_height)
        self.x = random.randint(0, screen_width)
        self.color = random.choice(colorlist)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.rad)

    def move(self):
        if self.stade < 11:
            self.rad += 10
        elif self.stade >= 16:
            self.rad -= 10
        self.stade += 1
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.rad)

count_sound.play()
pygame.draw.rect(screen, BLACK, (0, 0, screen_width, screen_height))
pr_text('SPACE to jump', cord=(screen_width // 2 - 50, screen_height // 2 - 50), n=30)
pygame.display.update()
sleep(1)

count_sound.play()
pygame.draw.rect(screen, BLACK, (0, 0, screen_width, screen_height))
pr_text('Q to faster jump', cord=(screen_width // 2 - 50, screen_height // 2 - 50), n=30)
pygame.display.update()
sleep(1)

start_sound.play()
pygame.draw.rect(screen, BLACK, (0, 0, screen_width, screen_height))
pr_text("LET'S GO", cord=(screen_width // 2 - 50, screen_height // 2 - 50), n=35)
pygame.display.update()
sleep(1.5)



restart()
while True:  

    for i in range(len(chunks) - 1, -1, -1):
        if not chunks[i]:
            break 

        if punch(emp, chunks[i]):
            main_sound.stop()
            fail_sound.play()

            if i == did:
                game_score -= 1
            if game_score > game_high:
                game_high = game_score
                with open('high2.txt', 'w') as file:
                    file.write(str(game_high))

            pr_text(f'game over, score - {game_score}  hight - {game_high}', n=36, cord=(250, 130))
            pr_text('SPACE to restart', n=30, cord=(350, 200))

            pygame.display.update()
            events = pygame.event.get()
            f = False

            for e in events:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    f = True

            while not f:
                events = pygame.event.get()
                for e in events:

                    if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                        f = True
                    if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                        exit()
                pass
            fail_sound.stop()
            restart()
            break


    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not j:
            j = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            jr = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_h: 
            switch_hb()

    if j:
        emp.jump()
        if emp.jumpstade == 1:
            j = False
    
    for c in chunks:
        emp.is_score(c)
         
    if jr and emp.jumpstade == 1:
        q_sound.play()
        emp.jump_reset()
        jr = False
    
    chunk_generated()
    draw_background()
    moving_chunks(chunks)
    if game_speed < 6:
        game_speed *= 1.0005
    pr_text(f'this-{game_score} high-{game_high}', cord=(50, 50))
    rotate(screen, ball_img, -rot % 360)
    if not j:
        rot += 5
    else:
        rot += 2
    tm = dt.datetime.now().time()
    now_d = dt.timedelta(hours=tm.hour,minutes=tm.minute, seconds=tm.second)
    if now_d - zero_d == dt.timedelta(seconds=15) and not in_phonk:
        game_speed += 2
        phonk()
    if in_phonk:
        circle_spawn()
        for circle in circles:
            circle.move()
    pygame.display.update()
    
    clock.tick(FPS) 
    