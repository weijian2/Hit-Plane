# ===============================================================================
# 主要功能：模拟微信打飞机的小游戏
# 算法流程：1）加载相关图片、声音资源
#           2）编写my_plane.py模块，定义我方飞机的所有动作属性函数
#           3）编写enemy.py模块，定义敌方飞机的所有动作属性函数
# 注意事项：1）大型飞机出厂有帧切换和音效特效
#           2）大型中型飞机有血槽属性，血槽低于百分之二十为红色，否则为绿色
# ===============================================================================
# 导入相关模块
# coding: utf-8
import pygame
import sys
import traceback
import myplane
import enemy
import bullet
import supply
from random import *
from pygame.locals import *

# ====================初始化====================
pygame.init()
pygame.mixer.init()  # 混音器初始化
bg_size = width, height = 480, 852  # 设计背景尺寸
screen = pygame.display.set_mode(bg_size)  # 设置背景对话框
pygame.display.set_caption("飞机大战……FishC Demo")
background = pygame.image.load("image/background.png")  # 加载背景图片,并设置为不透明

# ====================载入游戏音乐====================
pygame.mixer.music.load("sound/game_music.wav")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
big_enemy_flying_sound = pygame.mixer.Sound("sound/big_spaceship_flying.wav")
big_enemy_flying_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound("sound/game_over.wav")
me_down_sound.set_volume(0.2)
button_down_sound = pygame.mixer.Sound("sound/button.wav")
button_down_sound.set_volume(0.2)
level_up_sound = pygame.mixer.Sound("sound/achievement.wav")
level_up_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_double_laser.wav")
get_bullet_sound.set_volume(0.2)


# ====================敌方飞机生成控制函数====================
def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)


def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)


# ====================提升敌机速度====================
def inc_speed(target, inc):
    for each in target:
        each.speed += inc


def main():
    clock = pygame.time.Clock()  # 设置帧率
    switch_image = False  # 控制飞机图片切换的标志位（用以模拟发动机喷火效果）
    delay = 60  # 控制分级图片切换的频率（延时参数）
    running = True
    pygame.mixer.music.play(-1)  # 循环播放背景音乐
    me = myplane.MyPlane(bg_size)  # 生成我方飞机
    score = 0  # 统计用户得分
    paused = False  # 标志是否暂停游戏
    pause_nor_image = pygame.image.load("image/game_pause_nor.png")  # 加载暂停相关按钮
    pause_pressed_image = pygame.image.load("image/game_pause_pressed.png")
    resume_nor_image = pygame.image.load("image/game_resume_nor.png")
    resume_pressed_image = pygame.image.load("image/game_resume_pressed.png")
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10  # 设置暂停按钮位置
    paused_image = pause_nor_image  # 设置默认显示的暂停按钮
    score_font = pygame.font.SysFont("arial", 48)  # 定义分数字体
    color_black = (0, 0, 0)
    color_green = (0, 255, 0)
    color_red = (255, 0, 0)
    color_white = (255, 255, 255)
    bomb_image = pygame.image.load("image/bomb.png")  # 加载全屏炸弹图标
    bomb_rect = bomb_image.get_rect()
    bomb_front = score_font
    bomb_num = 3  # 初始为三个炸弹
    level = 1  # 游戏难度级别
    life_image = pygame.image.load("image/life.png").convert()
    life_rect = life_image.get_rect()
    life_num = 3  # 一共有三条命
    invincible_time = USEREVENT + 2  # 接触我方飞机无敌时间定时器
    flag_recorded = False  # 是否已经打开记录文件标志位
    gameover_image = pygame.image.load("image/game_over.png")  # 游戏结束背景图片
    gameover_rect = gameover_image.get_rect()

    # ====================生成普通子弹====================
    bullet1 = []
    bullet1_index = 0
    bullet1_num = 6  # 定义子弹实例化个数
    for i in range(bullet1_num):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    # ====================生成超级子弹====================
    double_bullet_timer = USEREVENT + 1  # 超级子弹持续时间定时器
    is_double_bullet = False   # 是否使用超级子弹标志位
    bullet2 = []
    bullet2_index = 0
    bullet2_num = 10  # 定义子弹实例化个数
    for i in range(bullet2_num//2):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))

    # ====================实例化敌方飞机====================
    enemies = pygame.sprite.Group()  # 生成敌方飞机组
    small_enemies = pygame.sprite.Group()   # 敌方小型飞机组
    add_small_enemies(small_enemies, enemies, 1)  # 生成若干敌方小型飞机
    mid_enemies = pygame.sprite.Group()   # 敌方小型飞机组
    add_mid_enemies(mid_enemies, enemies, 1)  # 生成若干敌方中型飞机
    big_enemies = pygame.sprite.Group()   # 敌方小型飞机组
    add_big_enemies(big_enemies, enemies, 1)  # 生成若干敌方大型飞机

    # ====================实例化补给包====================
    bullet_supply = supply.BulletSupply(bg_size)
    bomb_supply = supply.BombSupply(bg_size)
    supply_timer = USEREVENT  # 补给包发放定时器
    pygame.time.set_timer(supply_timer, 10 * 1000)  # 定义每30秒发放一次补给包

    # ====================飞机损毁图像索引====================
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    # ===============================================================================
    # 主要功能：主循环，响应用户鼠标按键以及键盘事件
    # 算法流程：
    # 注意事项：
    # ===============================================================================
    while running:
        screen.blit(background, (0, 0))  # 将背景图片打印到内存的屏幕上
        score_text = score_font.render("Score : %s" % str(score), True, color_white)
        screen.blit(score_text, (10, 5))

        # ====================定义难度递进操作====================
        if level == 1 and score > 5000:  # 如果达到第二难度等级，则增加3架小型敌机，2架中型敌机，1架大型敌机,并提升小型敌机速度
            level = 2
            level_up_sound.play()
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            inc_speed(small_enemies, 1)
        elif level == 2 and score > 30000:  # 如果达到第三难度等级
            level = 3
            level_up_sound.play()
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 3 and score > 60000:  # 如果达到第四难度等级
            level = 4
            level_up_sound.play()
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
            inc_speed(big_enemies, 1)

        # ====================检测用户的退出及暂停操作====================
        for event in pygame.event.get():  # 响应用户的偶然操作
            if event.type == QUIT:  # 如果用户按下屏幕上的关闭按钮，触发QUIT事件，程序退出
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                button_down_sound.play()
                if event.button == 1 and paused_rect.collidepoint(event.pos):  # 如果检测到用户在指定按钮区域按下鼠标左键
                    paused = not paused
                    if paused:  # r如果当前的状态是暂停
                        paused_image = resume_pressed_image
                        pygame.time.set_timer(supply_timer, 0)  # 关闭补给机制以及所有音效
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        paused_image = pause_pressed_image
                        pygame.time.set_timer(supply_timer, 30 * 1000)  # 开启补给机制以及所有音效
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):  # 如果鼠标悬停在按钮区域
                    if paused:  # r如果当前的状态是暂停
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:  # 如果检测到用户按下空格键
                    if bomb_num:  # 如果炸弹数量大于零，则引爆一颗超级炸弹
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:  # 屏幕上的所有敌机均销毁
                                each.active = False
            elif event.type == supply_timer:  # 响应补给发放的事件消息
                if choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
            elif event.type == double_bullet_timer:
                is_double_bullet = False
                pygame.time.set_timer(double_bullet_timer, 0)
            elif event.type == invincible_time:  # 如果无敌时间已过
                me.invincible = False
                pygame.time.set_timer(invincible_time, 0)
        screen.blit(paused_image, paused_rect)

        if life_num and (not paused):  # 如果游戏未被暂停，正常运行
            # ====================绘制全屏炸弹数量和剩余生命数量====================
            bomb_text = bomb_front.render("× %d" % bomb_num, True, color_black)
            bomb_text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 10 - bomb_text_rect.height))
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image, (width - 10 - (i + 1) * life_rect.width, height - 10 - life_rect.height))

            # ====================检测用户的键盘操作====================
            key_pressed = pygame.key.get_pressed()  # 获得用户所有的键盘输入序列
            if key_pressed[K_w] or key_pressed[K_UP]:  # 如果用户通过键盘发出“向上”的指令,其他类似
                me.move_up()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.move_down()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.move_left()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.move_right()

            if not (delay % 10):  # 每十帧发射一颗移动的子弹
                bullet_sound.play()
                if not is_double_bullet:  # 如果当前是普通子弹状态
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % bullet1_num
                else:  # 如果当前是超级子弹状态
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
                    bullets[bullet2_index + 1].reset((me.rect.centerx + 30, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % bullet2_num

            # ====================绘制补给并检测玩家是否获得====================
            if bomb_supply.active:  # 如果是超级炸弹补给包
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):  # 如果玩家获得超级炸弹补给包
                    get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False
            if bullet_supply.active:  # 如果是超级子弹补给包
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    is_double_bullet = True
                    pygame.time.set_timer(double_bullet_timer, 18 * 1000)
                    bullet_supply.active = False

            # ====================子弹与敌机的碰撞检测====================
            for b in bullets:
                if b.active:  # 只有激活的子弹才可能击中敌机
                    b.move()  # 子弹移动
                    screen.blit(b.image, b.rect)
                    enemies_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemies_hit:  # 如果子弹击中飞机
                        b.active = False  # 子弹损毁
                        for e in enemies_hit:
                            if e in big_enemies or e in mid_enemies:
                                e.energy -= 1
                                e.hit = True  # 表示飞机已经被击中
                                if e.energy == 0:
                                    e.active = False  # 大中型敌机损毁
                            else:
                                e.active = False  # 小型敌机损毁

            # ====================我方飞机碰撞检测====================
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:  # 如果碰撞检测返回的列表非空，则说明已发生碰撞,若此时我方飞机处于无敌状态
                me.active = False
                for e in enemies_down:
                    e.active = False  # 敌机损毁

            # ====================绘制我方飞机，设置两种飞机交替绘制，以实现动态喷气效果====================
            if delay == 0:
                delay = 60
            delay -= 1
            if not delay % 3:
                switch_image = not switch_image
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)  # 绘制我方飞机的两种不同的形式
                else:
                    screen.blit(me.image2, me.rect)
            else:
                if not (delay % 3):
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)  # 绘制我方飞机损毁画面
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        me_down_sound.play()
                        life_num -= 1
                        me.reset()  # 我方飞机重生并开始无敌时间计时
                        pygame.time.set_timer(invincible_time, 3 * 1000)

            # ====================绘制敌方飞机，由大到小进行绘制，避免速度快的小飞机被覆盖====================
            for each in big_enemies:  # 绘制大型敌机并自动移动
                if each.active:  # 如果飞机正常存在
                    each.move()  # 绘制大型敌机
                    if not each.hit:  # 如果飞机未被击中
                        if switch_image:
                            screen.blit(each.image1, each.rect)  # 绘制大型敌机的两种不同的形式
                        else:
                            screen.blit(each.image2, each.rect)
                    else:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False

                    # ====================绘制血槽====================
                    pygame.draw.line(screen, color_black,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5),
                                     2)
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:  # 如果血量大约百分之二十则为绿色，否则为红色
                        energy_color = color_green
                    else:
                        energy_color = color_red
                    pygame.draw.line(screen, energy_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5),
                                     2)
                    if each.rect.bottom == -50:
                        big_enemy_flying_sound.play(-1)  # 播放大型飞机的音效(循环播放)

                else:  # 如果飞机已撞毁
                    big_enemy_flying_sound.stop()  # 出场音效停止
                    if e3_destroy_index == 0:
                        enemy3_down_sound.play()  # 播放飞机撞毁音效
                    if not (delay % 3):  # 每三帧播放一张损毁图片
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6  # 大型敌机有六张损毁图片
                        if e3_destroy_index == 0:  # 如果损毁图片播放完毕，则重置飞机属性
                            score += 6000  # 击毁一架大型敌机得6000分
                            each.reset()

            for each in mid_enemies:  # 绘制中型敌机并自动移动
                if each.active:
                    each.move()  # 绘制中型敌机
                    if not each.hit:
                        screen.blit(each.image, each.rect)
                    else:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False

                    # ====================绘制血槽====================
                    pygame.draw.line(screen, color_black,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5),
                                     2)
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:  # 如果血量大约百分之二十则为绿色，否则为红色
                        energy_color = color_green
                    else:
                        energy_color = color_red
                    pygame.draw.line(screen, energy_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5),
                                     2)
                else:
                    if e2_destroy_index == 0:
                        enemy2_down_sound.play()  # 播放损毁音效
                    if not (delay % 3):
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)  # 绘制损毁画面
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 2000  # 击毁一架中型飞机得2000分
                            each.reset()

            for each in small_enemies:  # 绘制小型敌机并自动移动
                if each.active:
                    each.move()  # 绘制小型敌机
                    screen.blit(each.image, each.rect)
                else:
                    if e1_destroy_index == 0:
                        enemy1_down_sound.play()  # 敌机损毁音效
                    if not (delay % 3):
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)  # 播放损毁画面
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 500  # 击毁一架小型飞机得500分
                            each.reset()
        elif life_num == 0:  # 生命值为零，绘制游戏结束画面
            screen.blit(gameover_image, gameover_rect)
            pygame.mixer.music.stop()  # 关闭背景音乐
            pygame.mixer.stop()  # 关闭所有音效
            pygame.time.set_timer(supply_timer, 0)  # 关闭补给机制

            if not flag_recorded:  # 读取历史最高分
                flag_recorded = True
                with open("score_record.txt", "r") as f:
                    record_score = int(f.read())
                if score > record_score:  # 如果玩家得分大于历史最高分，则将当前分数存档
                    with open("score_record.txt", "w") as f:
                        f.write(str(score))

            record_score_text = score_font.render("%d" % record_score, True, color_white)
            screen.blit(record_score_text, (150, 25))
            game_over_score_text = score_font.render("%d" % score, True, color_white)
            screen.blit(game_over_score_text, (180, 370))

        pygame.display.flip()  # 将内存中绘制好的屏幕刷新到设备屏幕上
        clock.tick(60)  # 设置帧数为60

# ===============================================================================
# 主要功能：程序入口
# 算法流程：
# 注意事项：
# ===============================================================================
if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()



