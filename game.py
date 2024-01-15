import pyxel
import math
import random
from enum import IntEnum, auto

WIDTH = 180
HEIGHT = 200

blocks_arr = []
accelerate = 3
hor_interval = 0


class Difficulty(IntEnum):
    EASY = auto()
    NORMAL = auto()
    HARD = auto()


class Status(IntEnum):
    TITLE = auto()
    PLAYING = auto()
    GAMEOVER = auto()


class Block:
    def __init__(self, hor, ver):
        self.horizontal = hor
        self.vertical = ver
        self.colors = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15]
        self.block_colors = []
        for i in range(ver):
            self.block_colors.append(random.randint(0, len(self.colors)-1))
        self.create()

    def create(self):
        global hor_interval
        # 32*10の長方形を5*4で作る
        hor_interval = (WIDTH-20) / self.horizontal
        global blocks_arr
        blocks_arr = []
        self.x = 10
        self.y = 10
        for i in range(self.vertical):
            self.blocks_sub = []
            for j in range(self.horizontal):
                self.blocks_sub_sub = []
                self.blocks_sub_sub.append(self.x)
                self.blocks_sub_sub.append(self.y)
                self.blocks_sub.append(self.blocks_sub_sub)
                self.x += hor_interval
            blocks_arr.append(self.blocks_sub)
            self.x = 10
            self.y += 10


class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="block KUZUSHI")
        pyxel.mouse(True)  # for debug
        self.game_state = Status.TITLE
        self.padx = 70
        self.ballx = 90
        self.bally = 180
        self.angle = math.radians(random.randint(210, 330))
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if blocks_arr == []:
            Block(5, 4)
        if self.game_state == Status.TITLE:
            self.update_title()
        elif self.game_state == Status.PLAYING:
            self.update_playing()
        elif self.game_state == Status.GAMEOVER:
            self.update_gameover()

    def update_title(self):
        global accelerate
        if pyxel.btnp(pyxel.KEY_E):
            accelerate = 3
            self.game_dif = Difficulty.EASY
            self.game_state = Status.PLAYING
            Block(5, 4)
        if pyxel.btnp(pyxel.KEY_N):
            accelerate = 5
            self.game_dif = Difficulty.NORMAL
            self.game_state = Status.PLAYING
            Block(5, 4)
        if pyxel.btnp(pyxel.KEY_H):
            accelerate = 10
            self.game_dif = Difficulty.HARD
            self.game_state = Status.PLAYING
            Block(8, 5)
        self.vx = math.cos(self.angle) * accelerate
        self.vy = math.sin(self.angle) * accelerate

    def update_playing(self):
        self.update_pad()
        self.update_ball()
        self.update_collision()

    def update_pad(self):
        self.padx = pyxel.mouse_x
        if self.padx < 20:
            self.padx = 20
        elif self.padx > 160:
            self.padx = 160

    def update_ball(self):
        if self.bally > 200:
            self.game_state = Status.GAMEOVER
        if self.bally <= 5:
            self.vy *= -1
        if self.ballx >= 175 or self.ballx <= 5:
            self.vx *= -1
        if self.bally >= 185 and self.padx-20 < self.ballx < self.padx+20:
            self.vy *= -1
        self.ballx += self.vx
        self.bally += self.vy

    def update_collision(self):
        global blocks_arr

        for i in range(len(blocks_arr)):
            for j in range(len(blocks_arr[0])):
                if blocks_arr[i][j] is None:
                    continue
                block_x = blocks_arr[i][j][0]
                block_y = blocks_arr[i][j][1]
                self.w = hor_interval
                if block_x <= self.ballx <= block_x + self.w and math.fabs(block_y - self.bally) < 5:
                    blocks_arr[i][j] = None
                    print("pop")
                    self.vy *= -1
                elif block_y <= self.bally <= block_y + 10 and math.fabs(block_x - self.ballx) < 5:
                    blocks_arr[i][j] = None
                    print("pop")
                    self.vx *= -1

    def update_gameover(self):
        if pyxel.btnp(pyxel.KEY_R):
            self.game_state = Status.TITLE

    def draw(self):
        if self.game_state == Status.TITLE:
            self.draw_title()
        elif self.game_state == Status.PLAYING:
            self.draw_playing()
        elif self.game_state == Status.GAMEOVER:
            self.draw_gameover()

    def draw_title(self):
        pyxel.cls(0)
        pyxel.text(45, 80, "B l o c k  k u z u s h i", 7)
        pyxel.text(60, 120, " Easy : Press 'E'", 10)
        pyxel.text(60, 135, "Normal : Press 'N'", 9)
        pyxel.text(60, 150, " Hard : Press'H'", 8)
        pyxel.text(100, 180, "Press'Q' to quit", 7)
        self.padx = 70
        self.ballx = 90
        self.bally = 180
        self.angle = math.radians(random.randint(210, 330))
        

    def draw_playing(self):
        pyxel.cls(0)
        pyxel.circ(self.ballx, self.bally, 5, 7)
        pyxel.rect(self.padx-20, 190, 40, 5, 7)
        self.draw_block()

    def draw_gameover(self):
        pyxel.cls(0)
        pyxel.text(45, 80, "    G a m e  o v e r    ", 8)
        pyxel.text(60, 130, "Press'R' to retry", 7)

    def draw_block(self):
        for i in range(len(blocks_arr)):
            for j in range(len(blocks_arr[0])):
                if blocks_arr[i][j] is not None:
                    pyxel.rect(
                        blocks_arr[i][j][0], blocks_arr[i][j][1], hor_interval, 10, 7)
                    pyxel.rectb(
                        blocks_arr[i][j][0], blocks_arr[i][j][1], hor_interval, 10, 10)

    # def is_collision(self, ball_center, rect_x, rect_y):


App()