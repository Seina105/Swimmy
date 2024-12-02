import os
import sys
import pygame as pg
from pygame.locals import *
import pygame.mixer
import cv2
import numpy as np
import time
import random
import math

WIDTH, HEIGHT = 1080, 760 # ディスプレイサイズ
FONT = "font/JF-Dot-MPlusS10.ttf"  # ドット文字細目
FONT_B = "font/JF-Dot-MPlusS10B.ttf"  # ドット文字太目

class Player():
    """
    プレイヤーに関するクラス
    """
    def __init__(self, max_hp: int, max_mp: int, pl_hp:int, pl_mp:int, num:int, name:str):
        """
        プレイヤーのSurfaceを作成
        引数 max_hp：プレイヤーの最大HP
        引数 max_mp：プレイヤーの最大MP
        引数 pl_hp：プレイヤーのHP
        引数 pl_mp：プレイヤーのMP
        引数 num： プレイヤーの画像を番号で指定
        引数 name：プレイヤーの名前
        """

        #ステータス
        self.pl_hp = pl_hp
        self.pl_mp = pl_mp
        self.max_hp = max_hp
        self.max_mp = max_mp

        #画像
        self.image = pg.image.load(f"images/PL{num}.png")
        self.rect = self.image.get_rect()
        self.image = pg.transform.rotozoom(self.image, 0, 0.4)

        self.fonto = pg.font.SysFont(FONT, 20)
        self.black = (0, 0, 0)
        #プレイヤー名
        self.name = name


    def update(self, screen:pg.Surface):
        """
        プレイヤーの画像を表示
        引数 screen：Surface
        """
        #プレイヤーの名前
        self.img = self.fonto.render(str(self.name), 0, (0,0,0))
        screen.blit(self.image, (self.rect.centerx, self.rect.centery-40))


def main():
    pg.display.set_caption("Swimmy")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_title = pg.image.load(f"images/title.png")

    #インスタンス
    pl = None

    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    "モード設定"
    screen_mode = 0 # mode = 0:タイトル 1:スタート 2:マップ 3:バトル 4:エンディング

    while True:
        if screen_mode == 0:
            screen.blit(bg_title, [0, 0]) #背景画像

            


        pg.display.update()
if __name__ == "__main__":
    main()

