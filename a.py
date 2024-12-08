import sys
import pygame as pg
from pygame.locals import *
import pygame.mixer
import time
import random
from collections import Counter

# 画面サイズとフォント設定
WIDTH, HEIGHT = 1080, 760
FONT = "font/JF-Dot-MPlusS10.ttf"
FONT_B = "font/JF-Dot-MPlusS10B.ttf"

# 色の設定
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0,85,46)

#音楽
class MusicManager:
    def __init__(self):
        """
        音楽管理クラスの初期化
        """
        pg.mixer.init()  # ミキサーを初期化
        self.current_music = None  # 現在再生中の音楽ファイル

    def play(self, file, loop=-1):
        """
        音楽を再生する関数
        引数
        file: 再生する音楽ファイルのパス
        loop: ループ回数 (-1で無限ループ)
        """
        if self.current_music != file:  # 違う音楽が再生されている場合のみ切り替える
            pg.mixer.music.stop()
            try:
                pg.mixer.music.load(file)
                pg.mixer.music.play(loop)
                self.current_music = file
                print(f"Playing: {file}")
            except pg.error as e:
                print(f"再生エラーが発生しました {file}: {e}")

    def stop(self):
        """
        音楽を停止する関数
        """
        pg.mixer.music.stop()
        self.current_music = None
        print(f"{self.current_music} is Stopped")

#タイトル画面
class Title(pg.sprite.Sprite):
    """
    タイトル画面を管理するクラス
    """
    def __init__(self, font, font2, music_manager, select_sound, done):
        """
        コンストラクタ
        引数:
        font: メニューのフォント
        font2: タイトル文字のフォント
        music_manager: 音楽管理クラスのインスタンス
        select_sound: メニュー選択時の音
        done_sound: メニュー決定時の音
        """
        self.font = font
        self.font2 = font2
        self.music_manager = music_manager
        self.select_sound = select_sound
        self.done_sound = done
        self.bg_img = pg.image.load("images/title.png")
        self.sign = pg.transform.rotozoom(pg.image.load(f"images/sign.png"), 0, 1.15)
        self.mini_bird = pg.transform.rotozoom(pg.image.load(f"images/baby_bird.png"), -2, 1)
        self.steve = pg.transform.rotozoom(pg.image.load(f"images/steve.png"), 0, 1.3)
        self.title_select = ["はじめる", "そうさせつめい", "せってい"]
        self.select = 0  # 現在選択中の項目

    def event(self, event):
        """
        イベント処理
        引数:
        event: pygameのイベント
        """
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.select = (self.select - 1) % len(self.title_select)
                self.select_sound.play()
            elif event.key == K_DOWN:
                self.select = (self.select + 1) % len(self.title_select)
                self.select_sound.play()
            elif event.key == K_RETURN:  # Enterキーで決定
                self.done_sound.play()
                return self.select  # 選択された項目のインデックスを返す
        return None

    def update(self, screen):
        """
        タイトル画面の描画を更新
        引数:
        screen: 描画対象のSurface
        """
        screen.blit(self.bg_img, [0, 0])  # 背景
        screen.blit(self.sign, [260, 380])  # 看板
        screen.blit(self.mini_bird, [60, 445])  # にわとり
        screen.blit(self.steve, [690, 250])  # スティーブ

        # タイトル文字
        title_text = self.font2.render("MineCraft", True, BLACK)
        title_text2 = self.font2.render("? RPG ?", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
        screen.blit(title_text2, (WIDTH // 2 - title_text2.get_width() // 2, 200))

        # メニュー選択
        menu_select(screen, self.font, self.title_select, self.select)

#導入画面        
class Introduction(pg.sprite.Sprite):
    """
    タイトル画面を管理するクラス
    """
    def __init__(self, music_manager):
        self.font = pg.font.Font(FONT, 30)  # メニューのフォント
        self.music_manager = music_manager
        self.bg_img = pg.image.load("images/night.png")
        self.story = [
            "とある村で、村人が行方不明になる事件が起きていた。",
            "その噂を聞きつけ、真実を解き明かす旅人が村を訪れた。",
            "旅人が言うには、この村に'魔女'が潜んでいるという。",
            "魔女は動物に化ける不思議な力を持ち、夜になると村人を襲うらしい。",
            "村人たちは旅人の助けを借り、魔女を追い出すために立ち上がることにした。",
            "しかし、誰が本当に味方なのかは誰にも分からない……。"
        ]

        self.story_index = 0
        self.flag = 0

    def key_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                self.story_index += 2
                if self.story_index > len(self.story) - 2:
                    self.flag = 1
        

    def update(self, screen):
        """
        描画処理
        """
        if self.flag == 0:
            # 背景画像を描画
            screen.blit(self.bg_img, [0, 0])

            # 半透明な白い矩形を描画
            bg_surface = pg.Surface((WIDTH, 300), flags=pg.SRCALPHA)  # 透過対応Surface
            bg_surface.fill((255, 255, 255, 150))  # アルファ値200で塗りつぶし（0〜255）
            screen.blit(bg_surface, (0, 500))  # 画面に描画

            # テキストを描画
            story_text = self.font.render(self.story[self.story_index], True, BLACK)
            screen.blit(story_text, (20, 550))  # 中央揃えで描画
            story_text2 = self.font.render(self.story[self.story_index + 1], True, BLACK)
            screen.blit(story_text2, (20, 650))  # 中央揃えで描画

        pg.display.update()  # 画面を更新


#モブ
class Mobs:
    def __init__(self, name):
        self.name = name
        self.role = None
        self.trust = {}
        self.hate = {}
        self.life = 1
        self.target = None
        self.vote = "未投票"

    def set_role(self, role):
        """役職を設定"""
        self.role = role

    def set_trust(self, target, value):
        """信頼度を設定"""
        self.trust[target.name] = value

    def set_hate(self, target, value):
        """敵対度を設定"""
        self.hate[target.name] = value

    def vote(self):
        if self.hate and self.life == 1:
            # 敵対度が最も高い相手を取得
            target = max(self.hate, key=self.hate.get)
            self.target = target
            print(f"{self.name}は{target}に投票しました。")
            self.vote = f"{self.name}は{target}に投票しました。"
        return None

    def __str__(self):
        status = "生存" if self.life == 1 else "死亡"
        return f"{self.name} -> 役職: {self.role}, 状態: {status}, 信頼: {self.trust}, 敵対: {self.hate}"


#討論画面        
class Discussion(pg.sprite.Sprite):
    def __init__(self, music_manager, mobs:Mobs):
        self.bg_img = pg.transform.rotozoom(pg.image.load(f"images/discuss.png"), 0, 0.7)
        self.font = pg.font.Font(FONT_B, 30)
        self.music_manager = music_manager
        self.flag = 0
        self.mobs = mobs


    def key_event(self, event):
        if event.type == KEYDOWN and event.key == K_RETURN:
            self.flag = 1  # フラグを立てて投票処理を呼び出せるようにする

    def update(self, screen):
        screen.blit(self.bg_img, [0, 0])  # 背景
        title_text = self.font.render("議論を開始します。", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 200))

        for i, mob in enumerate(self.mobs):
            text = self.font.render(f"{mob.vote}", True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 300 + 50 * i))
        pg.display.update()


#効果音
def load_sound(file):
    """
    音源を読み込む関数
    引数1 file：音源ファイル
    """
    if not pg.mixer:
        return None
    try:
        sound = pg.mixer.Sound(file) #Soundオブジェクト作成
        return sound
    except pg.error:
        print(f"Warning, unable to load,{file}")
    return None


#メニュー選択
def menu_select(screen, font, selects_item, select):
    """
    メニュー項目を描画する関数
    引数
    screen: 描画対象のSurface
    font: 使用するフォント
    selects_item: メニュー項目のリスト
    select: 現在選択中のインデックス
    """
    arrow = ">"
    for i, item in enumerate(selects_item):
        if i == select:
            font_color = GREEN  # 選択中の項目は緑色
            text = font.render(f"{arrow} {item}", True, font_color)  # 矢印付き
        else:
            font_color = BLACK
            text = font.render(f" {item}", True, font_color)
        
        
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 400 + i * 100))


#loading画面の処理
def loading(screen,font):
    screen.fill((0, 0, 0))
    chest = pg.image.load(f"images/chest.png") #チェスト

    images = [chest, chest, chest]
    test = font.render("Now Loading...", True, WHITE)
    screen.blit(test, (WIDTH // 2 - test.get_width() // 2, 500))
    # 各画像を描画しながら更新
    for i, img in enumerate(images):
        screen.blit(img, (170 + 260 * i, 300))  # 画像の位置を調整
        pg.display.update()  # 画面を更新
        pg.time.delay(1000)  # 1秒間遅延
    screen.fill((0, 0, 0))  # 再度画面を黒で塗りつぶす
    pg.display.update()  # 画面を更新


def assignment_role(discuss = None):
    # キャラクターのリストを作成
    mobs = [
        Mobs("旅人"),
        Mobs("鶏"),
        Mobs("村人1"),
        Mobs("村人2"),
        Mobs("村人3"),
        Mobs("豚"),
        Mobs("アイアンゴーレム"),
        Mobs("商人"),
    ]

    # 役職を定義
    roles = [
        "魔女",      # 人狼的な役職
        "占い師",    # 特殊能力持ち
        "霊媒師",    # 特殊能力持ち
        "狂人"
    ] + ["村人"] * (len(mobs) - 4)  # 残りはすべて村人

    # 役職をシャッフルして割り振り
    random.shuffle(roles)
    for i, mob in enumerate(mobs):
        mob.set_role(roles[i])
    
    # 信頼度と敵対度をランダムに設定
    for mob in mobs:
        for target in mobs:
            if mob.name != target.name:
                num = random.randint(0, 100)
                mob.set_trust(target, num)
                mob.set_hate(target, 100-num)

    # 割り振り結果を表示
    for mob in mobs:
        print(mob)

    return mobs


#信用度
def trust_status(mobs, me, target, trust_value = 0):
    for mob in mobs:
        if mob["name"] == me:
            mob["trust"][target] = trust_value


#憎み
def hate_status(mobs, me, target, hate_value = 0):
    for mob in mobs:
        if mob["name"] == me:
            mob["hate"][target] = hate_value


def result_voting(mobs):
    votes = {}
    for mob in mobs:
        if mob.name not in votes:
            votes[mob.name] = 0
        if mob.target not in votes:
            votes[mob.target] = 1
            continue
        
        votes[mob.target] += 1


def reset_status(mobs):
    """
    敵対度を再設定する関数
    """
    for mob in mobs:
        if mob.life == 1:  # 生存している場合のみ設定
            for target in mobs:
                if mob.name != target.name:  # 自分以外
                    if target.life == 0:  # 生存中の場合
                        mob.set_hate(target, 0)  # 敵対度を0にリセット

def main():
    #初期化・基本設定
    pg.init()
    pg.display.set_caption("タイトル画面")
    pg.mixer.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    #画像・サウンド定義
    
    font = pg.font.Font(FONT, 40)  # メニューのフォント
    font2 = pg.font.Font(FONT_B, 80)  # タイトル文字のフォント

    #musicインスタンス生成
    music_manager = MusicManager() 
    select_sound = load_sound("sound/select_sound.mp3") # 選択音
    done = load_sound("sound/done.mp3") # 決定音

        #インスタンス
    game_mode = 0
    mobs = assignment_role()
    title_screen = Title(font, font2, music_manager, select_sound, done)
    introduction_story = Introduction(music_manager)
    discuss = Discussion(music_manager,mobs)
    


    # メニュー項目
    
    
    
    while True:
        # イベント処理
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

            if game_mode == 0:  # タイトル画面
                selected = title_screen.event(event)
                if selected is not None:
                    if selected == 0:  # はじめる
                        game_mode = 1
                        loading(screen, font2)

                    elif selected == 1:  # そうさせつめい
                        game_mode = 2

                    elif selected == 2:  # せってい
                        game_mode = 3

            elif game_mode == 1:
                introduction_story.key_event(event)
                if introduction_story.flag == 1:
                    game_mode = 2

            #議論モード
            elif game_mode == 2:
                discuss.key_event(event)
                if discuss.flag == 1:
                    for mob in mobs:
                        mob.vote()

                    most  = result_voting(mobs)
                    
                    
                    if most and most.life == 0:
                        print(f"{most.name} が追放されました！")
                        reset_status(mobs)
                    discuss.flag = 0
    


                

        # ゲーム画面の描画
        if game_mode == 0:
            title_screen.update(screen)
            
        elif game_mode == 1:
            if introduction_story:
                introduction_story.update(screen)


        elif game_mode == 2:
            discuss.update(screen)
        elif game_mode == 3:
            print("設定画面")

        pg.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()