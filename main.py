import sys
import pygame as pg
from pygame.locals import *
import pygame.mixer
import time

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
class Title:
    """
    タイトル画面に関するクラス
    """
    def __init__(self, font2):
        """
        引数 font2 : フォント 
        """
        self.bg_img = pg.image.load("images/title.png") #背景
        #にわとり
        self.mini_bird = pg.transform.rotozoom(pg.image.load(f"images/baby_bird.png"), -2, 1)
        #スティーブ
        self.steve = pg.transform.rotozoom(pg.image.load(f"images/steve.png"), 0, 1.3)
        #看板
        self.sign = pg.transform.rotozoom(pg.image.load(f"images/sign.png"), 0, 1.15)
        self.font2 = font2

    def updatea(self, screen:pg.Surface, title_select:int, now_select:int):
        """
        引数 screen : Surface
        引数 title_select : 選択メニュー
        引数 now_select : 現在何を選択しているか
        """
        screen.blit(self.bg_img,[0,0]) #背景
        screen.blit(self.sign,[260,380]) #看板
        screen.blit(self.mini_bird,[60,445]) #にわとり
        screen.blit(self.steve,[690,250]) # スティーブ（立ち絵）
        
        #タイトル文字
        title_text = self.font2.render("MineCraft", True, BLACK)
        title_text2 = self.font2.render("? RPG ?", True, BLACK)
        #描写
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
        screen.blit(title_text2, (WIDTH // 2 - title_text2.get_width() // 2, 200))
        menu_select(screen, self.font2, title_select, now_select) 

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


def main():
    #初期化・基本設定
    pg.init()
    pg.display.set_caption("タイトル画面")
    pg.mixer.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    #画像・サウンド定義
    bg_img = pg.image.load("images/title.png") #背景
    map1_img = pg.image.load("images/map1.png") #マップ背景1
    map1_img = pg.transform.rotozoom(map1_img, 0, 0.7)
    sign = pg.image.load(f"images/sign.png") #看板
    sign = pg.transform.rotozoom(sign, 0, 1.15)
    mini_bird = pg.image.load(f"images/baby_bird.png") #にわとり
    mini_bird = pg.transform.rotozoom(mini_bird, -2, 1)
    steve = pg.image.load(f"images/steve.png") #スティーブ
    steve = pg.transform.rotozoom(steve, 0, 1.3)
    chest = pg.image.load(f"images/chest.png") #チェスト
    e_button = pg.image.load(f"images/e_button.png") #Eボタン
    e_button = pg.transform.rotozoom(e_button, 0, 0.2)
    item_box = pg.image.load(f"images/item_box.png") #チェスト
    item_box = pg.transform.rotozoom(item_box, 0, 0.7)
    beaf = pg.image.load(f"images/meet.webp")# ビーフ
    beaf = pg.transform.rotozoom(beaf, 0, 0.4)

    #musicインスタンス生成
    music_manager = MusicManager() 
    select_sound = load_sound("sound/select_sound.mp3") # 選択音
    done = load_sound("sound/done.mp3") # 決定音

    #インスタンス
    #title = Title(screen, font2)

    items = {
         beaf:("cure",20) #アイテム名:("種類",回復量)
    }

    # フォント設定
    font = pg.font.Font(FONT_B, 40)
    font2 = pg.font.Font(FONT_B, 80)

    # メニュー項目
    title_select = ["はじめる","そうさせつめい","せってい"]
    select = 0
    game_mode = 0

    while True:
        # イベント処理

        # game_mode = 0(タイトル)
        if game_mode == 0:
            music_manager.play("sound/title.mp3")
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        select = (select - 1) % len(title_select) 
                        select_sound.play()
                    elif event.key == K_DOWN:
                        select = (select + 1) % len(title_select) 
                        select_sound.play()
                    elif event.key == K_RETURN:  # Enterキーで選択
                        if select == 0:
                            done.play()
                            print("はじめるを選択")
                            game_mode = 1
                            # はじめるの処理
                        elif select == 1:
                            done.play()
                            loading(screen,font2)
                            pg.display.update()
                            
                            print("そうさせつめいを選択")
                            game_mode = 2
                            # 操作説明の処理をここに記述
                        elif select == 2:
                            done.play()
                            print("せっていを選択")
                            # せっていの処理
            
            screen.blit(bg_img,[0,0]) #背景
            screen.blit(sign,[260,380]) #看板
            screen.blit(mini_bird,[60,445]) #にわとり
            screen.blit(steve,[690,250]) # スティーブ（立ち絵）
            #タイトル文字
            title_text = font2.render("MineCraft", True, BLACK)
            title_text2 = font2.render("? RPG ?", True, BLACK)
            #描写
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
            screen.blit(title_text2, (WIDTH // 2 - title_text2.get_width() // 2, 200))
            menu_select(screen, font, title_select, select) 
        
        # game_mode = 1(導入)
        elif game_mode == 1:
            print("導入画面に遷移しました。")
        
        #game_mode = 2（マップ移動）
        elif game_mode == 2:
            music_manager.play("sound/title.mp3")
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
            
            screen.blit(map1_img, [0,0])
            screen.blit(item_box, [85,470]) # アイテム欄
            screen.blit(chest, [60,580]) #チェスト
            screen.blit(e_button, [90,620]) #背景
            screen.blit(beaf, [180, 610]) #背景
            test = font2.render("Test", True, WHITE)
            #描写
            screen.blit(test, (WIDTH // 2 - test.get_width() // 2, 300))
            print("マップ画面")
        #game_mode = 3（戦闘画面）
        elif game_mode == 3:
            print("戦闘画面に遷移しました。")
        

        # game_mode = 2()
        pg.display.update()
        


if __name__ == "__main__":
    main()