import sys
import pygame
from pygame.locals import *
import os

from bs4 import BeautifulSoup
import urllib
from urllib import request
import json
import time
import random

width = 800
hight = 600
index = 0

fname = list(range(600))
idiom = list(range(600))

next_BTX = 200
next_BTY = 500
next_BTW = 150
next_BTH = 60

ans_BTX = 400
ans_BTY = 500

imgx = width/2 - 140
imgy = hight/2 - 200

def disp_answer():
    font = pygame.font.Font("C:/windows/Fonts/msyh.ttc", 25)
    surf = font.render(idiom[index],False,(255,200,10))
    screen.blit(surf,(300,20))
    pygame.display.flip()

def render_back():
    surf = pygame.Surface((280,280))
    # 设定Surface的颜色，使其和屏幕分离
    surf.fill((255,255,255))
    rect = surf.get_rect()
    screen.blit(surf,(imgx, imgy))
    pygame.display.flip()

def button(name, bx, by, bw, bh):
    ft = pygame.font.Font("C:/windows/Fonts/msyh.ttc", 25)
    pygame.draw.rect(screen, (255, 0, 0), (bx, by, bw, bh), 0)
    text1 = ft.render(name, True, (255, 255, 255))
    tw, th = text1.get_size()
    tx1 = bx + bw/2 - tw/2
    ty1 = by + bh/2 - th/2
    screen.blit(text1, (tx1, ty1))
    pygame.display.update()
 
# 主循环！
def main_loop():
    
    global index, imgx, imgy

    running = True

    while running:

        # for 循环遍历事件队列
        for event in pygame.event.get():
            # 检测 KEYDOWN 事件: KEYDOWN 是 pygame.locals 中定义的常量，pygame.locals文件开始已经导入
            if event.type == KEYDOWN:
                # 如果按下 Esc 那么主循环终止
                if event.key == K_ESCAPE:
                    running = False
            # 检测 QUIT : 如果 QUIT, 终止主循环
            elif event.type == QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse =pygame.mouse.get_pos()
                if next_BTX + next_BTW > mouse[0] > next_BTX and \
                    next_BTY + next_BTH > mouse[1] > next_BTY:
                    #print(" click next detected")
                    screen.fill((40, 40, 40))
                    render_back()
                    index = (index + 1) % 500
                    yippee.stop()
                    yippee.play()
                if ans_BTX + next_BTW > mouse[0] > ans_BTX and \
                    ans_BTY + next_BTH > mouse[1] > ans_BTY:
                    #print(" click answer detected")
                    disp_answer()
                    nono.stop()
                    nono.play()

        button("NEXT", next_BTX, next_BTY, next_BTW, next_BTH)
        button("ANSWER", ans_BTX, ans_BTY, next_BTW, next_BTH)

        img = pygame.image.load(fname[index])
        bigimage = pygame.transform.scale(img, (280, 280))
        screen.blit(bigimage, (imgx, imgy))
        pygame.display.update()
        #yippee.stop()
        #nono.stop()
        clock.tick(15)
 
if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    yippee = pygame.mixer.Sound(r"./yippee.wav")
    nono = pygame.mixer.Sound(r"./no.wav")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, hight))



    i = 0
    for roots, dirs, files in os.walk('./img'):
        for f in files:
            fname[i] = os.path.join(roots, f)
            idiom[i] = fname[i][6:-4]
            #print(fname[i], idiom[i])
            i += 1

    screen.fill((40, 40, 40))
    render_back()


    main_loop()
