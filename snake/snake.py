'''
目标：
一、绘制窗口，画布
二、添加静态下的蛇头、蛇身、食物等对象
三、让蛇头先运动起来，蛇身跟随蛇头运动
四、让键盘控制折的移动方向（监听事件）
五、死亡判断
六、吃到食物之后，生成新的食物
七、分数统计

实现功能：
一、目标功能
二、插入背景
三、相撞判断（双人版）
四、tkinter模块实现提取player输入调速值，并修改（可调速版）
五、蛇坐标超过窗口后重回窗口（无敌版）


按钮说明：
1、正常版
2、双人版
3、可调速版
4、无敌版
5、退出

操作说明：
1、双人版：（player1：WSAD（上下左右），player2：上下左右方向键）
2、其他版：上下左右方向键
3、退出游戏：死亡或关闭窗口
'''

import sys
import time
import pygame
import random
from random import *
from tkinter import *

# 定义窗口分辨率
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
# 定义画布宽高
DRAW_X = 600
DRAW_Y = 600
# 定义画布颜色
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 128, 0)
brightred = (255, 0, 0)
brightgreen = (0, 255, 0)
pink = (255, 153, 200)
black = (0, 0, 0)
grey = (150, 150, 150)
# 定义分数
score = 0
# 定义速度
space = 0

# 设计窗口
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("贪吃蛇")
background = pygame.image.load("image/bgimg.jpg")
# pygame.mixer.music.load("snake.mp3")
clock = pygame.time.Clock()
pygame.init()


class Position(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


def show_welcome():
    '''
    欢迎界面
    :return: None
    '''
    font = pygame.font.SysFont('comicsansms', 70)
    fontsurf = font.render('Welcome Snaker!', True, white)
    fontrect = fontsurf.get_rect()
    fontrect.center = ((SCREEN_WIDTH / 2), (200))
    surface.blit(fontsurf, fontrect)
    pygame.display.update()


# def music_go():
#     '''
#     调用音乐模块
#     :return: None
#     '''
#     pygame.mixer.music.play(2, 0.0)


def show_end():
    '''
    结束界面
    :return: None
    '''
    font = pygame.font.Font("ziti.ttf", 40)
    fontsurf = font.render('Game Over! Your score: %s' % score, False, black)
    surface.blit(fontsurf, (100, 200))
    pygame.display.update()
    time.sleep(2)


def first_end():
    '''
    双人模式中，player1死亡
    :return: None
    '''
    font = pygame.font.Font("ziti.ttf", 40)
    fontsurf = font.render('Player 2 Win! Your score: %s' % score, False, black)
    surface.blit(fontsurf, (100, 200))
    pygame.display.update()
    time.sleep(2)


def second_end():
    '''
    双人模式中，player2死亡
    :return: None
    '''
    font = pygame.font.Font("ziti.ttf", 40)
    fontsurf = font.render('Player 1 Win! Your score: %s' % score, False, black)
    surface.blit(fontsurf, (100, 200))
    pygame.display.update()
    time.sleep(2)


def button(msg, x, y, w, h, ic, ac, action=None):
    '''
    按钮事件
    :param msg: 按钮信息
    :param x: 按钮的x轴
    :param y: 按钮的y轴
    :param w: 按钮的宽
    :param h: 按钮的高
    :param ic: 按钮初始颜色
    :param ac: 按钮按下颜色
    :param action: 按钮按下的动作
    :return: None
    '''
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(surface, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(surface, ic, (x, y, w, h))
    font = pygame.font.SysFont('comicsansms', 20)
    smallfont = font.render(msg, True, white)
    smallrect = smallfont.get_rect()
    smallrect.center = ((x + (w / 2)), (y + (h / 2)))
    surface.blit(smallfont, smallrect)


def rect(color, position):
    '''
    简化绘制画布
    :param color:画布颜色
    :param position: 画布坐标
    :return: None
    '''
    pygame.draw.rect(surface, color, ((position.x, position.y), (20, 20)))


def drect(color, x, y):
    '''
    简化绘制画布
    :param color: 画布颜色
    :param x: 画布坐标x轴
    :param y: 画布坐标y轴
    :return: None
    '''
    pygame.draw.rect(surface, color, ((x, y), (20, 20)))


def new_food(head):
    """
    创建新树莓
    :return:None
    """
    while True:
        newfood = Position(randint(0, 29) * 20, randint(0, 29) * 20)
        if newfood.x != head.x and newfood.y != head.y:
            break
        else:
            continue
    return newfood


def die_snake(head, snake_body):
    '''
    贪吃蛇死亡事件
    :param head: 蛇头
    :param snake_body:蛇身
    :return: None
    '''
    die_eatmyself = False
    for body in snake_body[1:]:
        if head.x == body.x and head.y == body.y:
            die_eatmyself = True
    if head.x < 0 or head.x > 600 or head.y < 0 or head.y > 600 or die_eatmyself:
        show_end()
        quit_game()


def quit_game():
    '''
    退出游戏
    :return: None
    '''
    pygame.quit()
    quit()


def chang_snake():
    '''
    变速模块
    :return: None
    '''
    def changinto():
        space = xls_text.get()
        root.destroy()
        start_cgame(space)

    root = Tk()
    root.title = "贪吃蛇速度"
    root.geometry('100x100')

    l1 = Label(root, text="速度：")
    l1.pack()
    xls_text = IntVar()
    xls = Entry(root, textvariable=xls_text)
    xls_text.set("")
    xls.pack()
    Button(root, text="开始游戏", command=changinto).pack()
    root.mainloop()


def through_snake(head, snake_body):
    """
    穿墙模块
    :param head:蛇头
    :param snake_body:蛇身
    """
    die_eatmyself = False
    for body in snake_body[1:]:
        if head.x == body.x and head.y == body.y:
            die_eatmyself = True
    if die_eatmyself:
        show_end()
        quit_game()

    else:
        if head.x < 0:
            head.x = 600
        if head.x > 600:
            head.x = 0
        if head.y < 0:
            head.y = 600
        if head.y > 600:
            head.y = 0


def start_game():
    '''
    正常模式
    :return: None
    '''
    global score
    # 定义蛇初始方向
    runtest = "up"
    run = runtest

    # 实例化蛇头、蛇身、食物对象
    head = Position(160, 160)
    snake_body = [Position(head.x, head.y + 20), Position(head.x, head.y + 40), Position(head.x, head.y + 60)]
    food = Position(300, 300)

    while True:
        surface.blit(background, (0,0))
        # 设计画布
        # pygame.draw.rect(surface, white, ((0, 0), (DRAW_X, DRAW_Y)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    runtest = "up"
                elif event.key == pygame.K_RIGHT:
                    runtest = "right"
                elif event.key == pygame.K_LEFT:
                    runtest = "left"
                elif event.key == pygame.K_DOWN:
                    runtest = "down"

        # 食物
        rect(green, food)
        # 蛇头
        rect(red, head)
        # 蛇身
        for pos in snake_body:
            rect(pink, pos)

        if run == "up" and not runtest == "down":
            run = runtest
        elif run == "down" and not runtest == "up":
            run = runtest
        elif run == "left" and not runtest == "right":
            run = runtest
        elif run == "right" and not runtest == "left":
            run = runtest

        snake_body.insert(0, Position(head.x, head.y))

        if run == "up":
            head.y -= 20
        elif run == "down":
            head.y += 20
        elif run == "left":
            head.x -= 20
        elif run == "right":
            head.x += 20

        die_snake(head, snake_body)

        if head.x == food.x and head.y == food.y:
            score += 1
            food = new_food(head)
        else:
            snake_body.pop()

        # 绘制更新
        pygame.display.update()
        clock.tick(8)


def start_cgame(space):
    """
    变速模式
    :param space: 速度
    """
    global score
    # 定义蛇初始方向
    runtest = "up"
    run = runtest

    # 实例化蛇头、蛇身、食物对象
    head = Position(160, 160)
    snake_body = [Position(head.x, head.y + 20), Position(head.x, head.y + 40), Position(head.x, head.y + 60)]
    food = Position(300, 300)

    while True:
        surface.blit(background, (0,0))
        # 设计画布
        # pygame.draw.rect(surface, white, ((0, 0), (DRAW_X, DRAW_Y)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    runtest = "up"
                elif event.key == pygame.K_RIGHT:
                    runtest = "right"
                elif event.key == pygame.K_LEFT:
                    runtest = "left"
                elif event.key == pygame.K_DOWN:
                    runtest = "down"

        # 食物
        rect(green, food)
        # 蛇头
        rect(red, head)
        # 蛇身
        for pos in snake_body:
            rect(pink, pos)

        if run == "up" and not runtest == "down":
            run = runtest
        elif run == "down" and not runtest == "up":
            run = runtest
        elif run == "left" and not runtest == "right":
            run = runtest
        elif run == "right" and not runtest == "left":
            run = runtest

        snake_body.insert(0, Position(head.x, head.y))

        if run == "up":
            head.y -= 20
        elif run == "down":
            head.y += 20
        elif run == "left":
            head.x -= 20
        elif run == "right":
            head.x += 20

        die_snake(head, snake_body)

        if head.x == food.x and head.y == food.y:
            score += 1
            food = new_food(head)
        else:
            snake_body.pop()

        # 绘制更新
        pygame.display.update()
        clock.tick(space)


def start_kgame():
    """
    无敌模式
    """
    global score
    # 定义蛇初始方向
    runtest = "up"
    run = runtest

    # 实例化蛇头、蛇身、食物对象
    head = Position(160, 160)
    snake_body = [Position(head.x, head.y + 20), Position(head.x, head.y + 40), Position(head.x, head.y + 60)]
    food = Position(300, 300)

    while True:
        surface.blit(background, (0,0))
        # 设计画布
        # pygame.draw.rect(surface, white, ((0, 0), (DRAW_X, DRAW_Y)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    runtest = "up"
                elif event.key == pygame.K_RIGHT:
                    runtest = "right"
                elif event.key == pygame.K_LEFT:
                    runtest = "left"
                elif event.key == pygame.K_DOWN:
                    runtest = "down"

        # 食物
        rect(green, food)
        # 蛇头
        rect(red, head)
        # 蛇身
        for pos in snake_body:
            rect(pink, pos)

        if run == "up" and not runtest == "down":
            run = runtest
        elif run == "down" and not runtest == "up":
            run = runtest
        elif run == "left" and not runtest == "right":
            run = runtest
        elif run == "right" and not runtest == "left":
            run = runtest

        snake_body.insert(0, Position(head.x, head.y))

        if run == "up":
            head.y -= 20
        elif run == "down":
            head.y += 20
        elif run == "left":
            head.x -= 20
        elif run == "right":
            head.x += 20

        through_snake(head, snake_body)

        if head.x == food.x and head.y == food.y:
            score += 1
            food = new_food(head)
        else:
            snake_body.pop()

        # 绘制更新
        pygame.display.update()
        clock.tick(8)


def start_dgame():
    """
    双人模式
    """
    # pygame初始化
    pygame.init()
    fpsClock = pygame.time.Clock()
    # 第二条蛇属性
    twice_snake = [460, 200]
    twice_snake_length = [[460, 200], [480, 200], [500, 200]]
    twice_direction = 'left'
    twice_changedirection = twice_direction
    # 定义常量
    snakepostion = [160, 100]
    snakelength = [[160, 100], [140, 100], [120, 100]]
    raspberrypostion = [300, 300]
    raspberry = 1
    direction = 'right'
    changedirection = direction
    pygame.display.set_caption("贪吃蛇")

    while True:
        # 定义画布
        # pygame.draw.rect(surface, white, ((0, 0), (600, 600)))
        surface.blit(background, (0, 0))

        for twice_body in twice_snake_length:
            drect(grey, twice_body[0], twice_body[1])
        for body in snakelength:
            drect(red, body[0], body[1])
            drect(pink, raspberrypostion[0], raspberrypostion[1])
        drect(green, snakepostion[0], snakepostion[1])
        drect(black, twice_snake[0], twice_snake[1])
        if raspberry == 1:
            drect(pink, raspberrypostion[0], raspberrypostion[1])
        # 键盘输入事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == ord('w'):
                    changedirection = 'up'
                if event.key == pygame.K_UP:
                    twice_changedirection = 'up'
                if event.key == ord('s'):
                    changedirection = 'down'
                if event.key == pygame.K_DOWN:
                    twice_changedirection = 'down'
                if event.key == ord('d'):
                    changedirection = 'right'
                if event.key == pygame.K_RIGHT:
                    twice_changedirection = 'right'
                if event.key == ord('a'):
                    changedirection = 'left'
                if event.key == pygame.K_LEFT:
                    twice_changedirection = 'left'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
        # 判断方向是否相反
        if direction == 'up' and not changedirection == 'down':
            direction = changedirection
        if twice_direction == 'up' and not twice_changedirection == 'down':
            twice_direction = twice_changedirection
        if direction == 'down' and not changedirection == 'up':
            direction = changedirection
        if twice_direction == 'down' and not twice_changedirection == 'up':
            twice_direction = twice_changedirection
        if direction == 'left' and not changedirection == 'right':
            direction = changedirection
        if twice_direction == 'left' and not twice_changedirection == 'right':
            twice_direction = twice_changedirection
        if direction == 'right' and not changedirection == 'left':
            direction = changedirection
        if twice_direction == 'right' and not twice_changedirection == 'left':
            twice_direction = twice_changedirection
        # 蛇运动
        if direction == 'right':
            snakepostion[0] += 20
        if twice_direction == 'right':
            twice_snake[0] += 20
        if direction == 'left':
            snakepostion[0] -= 20
        if twice_direction == 'left':
            twice_snake[0] -= 20
        if direction == 'up':
            snakepostion[1] -= 20
        if twice_direction == 'up':
            twice_snake[1] -= 20
        if direction == 'down':
            snakepostion[1] += 20
        if twice_direction == 'down':
            twice_snake[1] += 20
        # 增加蛇的长度
        snakelength.insert(0, list(snakepostion))
        twice_snake_length.insert(0, list(twice_snake))
        # 吃掉树莓
        if snakepostion[0] == raspberrypostion[0] and snakepostion[1] == raspberrypostion[1]:
            raspberry = 0
        else:
            snakelength.pop()
        if twice_snake[0] == raspberrypostion[0] and twice_snake[1] == raspberrypostion[1]:
            raspberry = 0
        else:
            twice_snake_length.pop()
        # 生成树莓
        if raspberry == 0:
            raspberrypostion[0] = random.randint(1, 29) * 20
            raspberrypostion[1] = random.randint(1, 29) * 20
            raspberry = 1
        pygame.display.update()
        # 判断边界死亡
        if snakepostion[0] == -20 or snakepostion[0] > 580:
            first_end()
            quit_game()
        if snakepostion[1] == -20 or snakepostion[1] > 580:
            first_end()
            quit_game()
        # 判断吃到自身死亡
        for snakebody in snakelength[1:]:
            if snakebody[0] == snakepostion[0] and snakebody[1] == snakepostion[1]:
                first_end()
                quit_game()
        # 判断第二条蛇的边界死亡
        if twice_snake[0] == -20 or twice_snake[0] > 580:
            second_end()
            quit_game()
        if twice_snake[1] == -20 or twice_snake[1] > 580:
            second_end()
            quit_game()
        # 判断第二条蛇吃到自身死亡
        for twice_snake_body in twice_snake_length[1:]:
            if twice_snake_body[0] == twice_snake[0] and twice_snake_body[1] == twice_snake[1]:
                second_end()
                quit_game()
        # 判断两条蛇相撞
        for twice_snake_body_l in twice_snake_length[1:]:
            if twice_snake_body_l[0] == snakepostion[0] and twice_snake_body_l[1] == snakepostion[1]:
                first_end()
                quit_game()
        for snakebody_l in snakelength[1:]:
            if snakebody_l[0] == twice_snake[0] and snakebody_l[1] == twice_snake[1]:
                second_end()
                quit_game()
        fpsClock.tick(8)


def into_game():
    """
    开始页面信息
    """
    into = True
    while into:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
        show_welcome()

        button("Normal", 230, 290, 100, 40, green, brightred, start_game)
        button("Double", 230, 340, 100, 40, green, brightred, start_dgame)
        button("Adjust Space", 220, 390, 120, 40, green, brightred, chang_snake)
        button("King", 230, 440, 100, 40, green, brightred, start_kgame)
        button("Quit", 230, 490, 100, 40, red, brightred, quit_game)
        pygame.display.update()
        clock.tick(15)

into_game()
start_game()


