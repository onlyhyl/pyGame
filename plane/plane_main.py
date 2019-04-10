import pygame
from plane_sprites import *


class PlaneGame(object):
    """飞机大战游戏"""
    def __init__(self):
        # 1、设置游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2、设置时钟
        self.clock = pygame.time.Clock()
        # 3、设置精灵和精灵组
        self.__creat_sprites()
        # 4、设置定时器事件
        pygame.time.set_timer(CREAT_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __creat_sprites(self):
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)
        self.enemy_group = pygame.sprite.Group()
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):

        while True:
            # 1、设置刷新频率
            self.clock.tick(FRAME_PER_SEC)
            # 2、事件监听
            self.__event_handler()
            # 3、刷新/绘制精灵
            self.__update_sprites()
            # 4、检测碰撞
            self.__check_collide()
            # 5、刷新
            pygame.display.update()

    def __event_handler(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_over()
            elif event.type == CREAT_ENEMY_EVENT:
                enemy = Enemy()
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

        keys_press = pygame.key.get_pressed()
        if keys_press[pygame.K_RIGHT]:
            self.hero.speed = 2
        elif keys_press[pygame.K_LEFT]:
            self.hero.speed = -2
        else:
            self.hero.speed = 0


    def __check_collide(self):
        pygame.sprite.groupcollide(self.hero.bullets,self.enemy_group,True,True)
        enemies = pygame.sprite.spritecollide(self.hero,self.enemy_group,True)
        if len(enemies) > 0:
            self.hero.kill()
            self.__game_over()

    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    @staticmethod
    def __game_over():
        print("退出游戏")
        pygame.quit()
        exit()


if __name__ == '__main__':
    game = PlaneGame()
    while True:
        game.start_game()