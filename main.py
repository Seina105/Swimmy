import sys
import pygame as pg
from pygame.locals import *
import pygame.mixer

# 画面サイズとフォント設定
WIDTH, HEIGHT = 1080, 760
FONT = "font/JF-Dot-MPlusS10.ttf"
FONT_B = "font/JF-Dot-MPlusS10B.ttf"

# 色の設定
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0,85,46)


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
    

def main():
    #初期化・基本設定
    pg.init()
    pg.display.set_caption("タイトル画面")
    pg.mixer.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    #画像・サウンド定義
    bg_img = pg.image.load("images/title.png") #背景
    sign = pg.image.load(f"images/sign.png") #看板
    sign = pg.transform.rotozoom(sign, 0, 1.15)
    mini_bird = pg.image.load(f"images/baby_bird.png") #にわとり
    mini_bird = pg.transform.rotozoom(mini_bird, -2, 1)
    steve = pg.image.load(f"images/steve.png") #スティーブ
    steve = pg.transform.rotozoom(steve, 0, 1.3)

    #musicインスタンス生成
    music_manager = MusicManager() 
    select_sound = load_sound("sound/select_sound.mp3") # 選択音
    done = load_sound("sound/done.mp3") # 決定音


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
                            print("そうさせつめいを選択")
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
        if game_mode == 1:
            print("導入画面に遷移しました。")
        
        # game_mode = 2()
        pg.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()