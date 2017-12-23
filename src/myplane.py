# ===============================================================================
# 主要功能：定义我方飞机类，设置我方飞机的相关属性
# 算法流程：1）加载飞机图片，定义飞机出现位置
#           2）定义飞机上下左右四个方向移动的控制函数
# 注意事项：
# ===============================================================================
# 导入相关模块
# coding: utf-8
import pygame


class MyPlane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load("image/hero1.png")  # 加载飞机图片1
        self.image2 = pygame.image.load("image/hero2.png")  # 加载飞机图片2
        self.mask = pygame.mask.from_surface(self.image1)  # 获取飞机图像的掩膜用以更加精确的碰撞检测
        self.destroy_images = []  # 加载飞机损毁图片
        self.destroy_images.extend([pygame.image.load("image/hero_blowup_n1.png"),
                                    pygame.image.load("image/hero_blowup_n2.png"),
                                    pygame.image.load("image/hero_blowup_n3.png"),
                                    pygame.image.load("image/hero_blowup_n4.png")])
        self.rect = self.image1.get_rect()  # 得到当前我方飞机的位置
        self.width, self.height = bg_size[0], bg_size[1]  # 本地化背景图片的尺寸
        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2, (self.height - self.rect.height - 60)  # 定义飞机初始化位置，底部预留60像素
        self.speed = 10  # 设置飞机移动速度
        self.active = True  # 设置飞机当前的存在属性，True表示飞机正常飞行，False表示飞机已损毁
        self.invincible = False  # 飞机初始化时有三秒的无敌时间

    # ====================定义四个方向的移动函数====================
    def move_up(self):  # 飞机向上移动的操作函数，其余移动函数方法类似
        if self.rect.top > 0:  # 如果飞机尚未移动出背景区域
            self.rect.top -= self.speed
        else:  # 若即将移动出背景区域，则及时纠正为背景边缘位置
            self.rect.top = 0

    def move_down(self):
        if self.rect.bottom < self.height - 60:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height - 60

    def move_left(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def move_right(self):
        if self.rect.right < self.width:
            self.rect.right += self.speed
        else:
            self.rect.right = self.width

    def reset(self):
        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2, (self.height - self.rect.height - 60)
        self.active = True
        self.invincible = True






