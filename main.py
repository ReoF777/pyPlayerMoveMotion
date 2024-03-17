import pygame
from pygame.locals import *
import sys
from consts import *

class Back(pygame.sprite.Sprite):
    surface = None
    backGround = None
    images = []
    backWidth = 0
    backHeight = 0
    widthInit = 0
    heightInit = 0

    def __init__(self, surface):
        self.surface = surface
        self.backGround = pygame.image.load(BACKGROUND_IMG).convert_alpha()
        self.backWidth = self.backGround.get_width()
        self.backHeight = self.backGround.get_height()
        self.widthInit = int(self.backWidth / BACK_TILE_WIDTH)
        self.heightInit = int(self.backHeight / BACK_TILE_HEIGHT)

        for i in range(0, self.backHeight, self.heightInit):
            for j in range(0, self.backWidth, self.widthInit):
                cImage = pygame.Surface((self.widthInit, self.heightInit))
                cImage.blit(self.backGround, (0, 0), \
                                (j, i, self.widthInit, self.heightInit)) # テンプレートデータを取得
                cImage = pygame.transform.scale(cImage, \
                            (CHARA_DISP_WIDTH, CHARA_DISP_HEIGHT)) # テンプレートデータのサイズを縮小
                self.images.append(cImage) # 画像データ配列に取得テンプレートデータを設定


    def drawBG(self): # 背景描画
        for i in range(int(WIN_HEIGHT * 0.88), WIN_HEIGHT, int(self.heightInit*0.8)):
            for j in range(0, WIN_WIDTH, int(self.widthInit*0.6)):
                self.surface.blit(self.images[4], (j, i))
        # self.surface.blit(self.images[4], (0, WIN_HEIGHT * 0.8))


class Player(pygame.sprite.Sprite):
    detect = 0
    pos = (0, WIN_HEIGHT * 0.8) # 画像の設置位置における左上の座標
    images = []
    surface = None
    playerData = None

    def __init__(self, winSurface, detect=14):
        pygame.sprite.Sprite.__init__(self)
        self.detect = detect # detectはtomas.pngの画像配列のインデックスに対応する変数(0,2,4,6...)
        self.surface = winSurface # 画像のsurface設定
        self.playerData = pygame.image.load(TOMAS_IMG).convert_alpha() # 画像読み込み
        
        imgWidth = self.playerData.get_width() # 画像の幅取得
        imgHeight = self.playerData.get_height() # 画像の高さ取得

        heightInit = int(imgHeight / CHARA_HEIGHT_BLOCK_NUM) # 画像データ(一つ当たり)のテンプレートの高さ取得
        widthInit = int(imgWidth / CHARA_WIDTH_BLOCK_NUM) # 画像データ(一つ当たり)のテンプレート幅を取得
        for i in range(0, imgHeight, heightInit):
            for j in range(0, imgWidth, widthInit):
                cImage = pygame.Surface((widthInit, heightInit)) # テンプレートを格納する配列を作成
                cImage.blit(self.playerData, (0, 0), (j, i, widthInit, heightInit)) # テンプレートデータを取得
                cImage = pygame.transform.scale(cImage, (CHARA_DISP_WIDTH, CHARA_DISP_HEIGHT)) # テンプレートデータのサイズを縮小
                colorkey = cImage.get_at((0, 0)) # 左上の画素値を取得
                cImage.set_colorkey(colorkey) # 左上の画素値を背景色と一致するとし、左上の画素値を透明色に置換
                self.images.append(cImage) # 画像データ配列に取得テンプレートデータを設定


    def draw(self): # プレイヤ-描画メソッド
        self.surface.blit(self.images[self.detect], self.pos)

    def movePlayer(self, key):      # 移動メソッド
        x,y = self.pos
        if(y < WIN_HEIGHT * 0.8):
            y += 5

        if(key == K_SPACE) and y > 5:
            print("Space button was pushed")
            y -= 50
        elif key == K_a and x >= 10:
            x -= 10
            self.detect = 9
        elif key == K_d and x < WIN_WIDTH:
            x += 10
            self.detect = 13

        self.pos = (x,y)
        self.draw()
    
    def stopPlayer(self):
        if(int(self.detect / 4) == 0 ):
            self.detect = 0
        elif(int(self.detect / 4) == 1 ):
            self.detect = 4
        elif(int(self.detect / 4) == 2 ):
            self.detect = 8
        elif(int(self.detect / 4) == 3 ):
            self.detect = 12
        else:
            pass

        x,y = self.pos
        if(y < WIN_HEIGHT * 0.8):
            y += 2

        self.pos = (x,y)
        self.draw()

    def sountCtrl(self): # 音楽管理メソッド
        pass

def main():
    # 画面初期設定
    pygame.init()
    pygame.key.set_repeat(100, 100)
    surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("pyRpg")
    clock = pygame.time.Clock()

    flag = True # プログラム状態フラグ

    backGround = Back(surface)
    tomas = Player(surface, 14)
    backGround.drawBG()

    while flag:
        clock.tick(FPS)  # fps値設定
        
        getEvent = pygame.event.get()  # 発生イベント取得
        checkEvent(getEvent, tomas)    # 発生イベント処理
        
        surface.fill(WIN_COLOR)
        backGround.drawBG() # 背景設定
        tomas.draw()               # プレイヤー設定
        
        pygame.display.update()    # 画面更新

def checkEvent(getEvent, player):
    for event in getEvent:
        if event.type == QUIT:
            exit()
            return True
        
        elif event.type == KEYDOWN:
            if event.key == K_q:
                exit()

            elif event.key == K_SPACE or \
                    event.key == K_a or event.key == K_d:
                player.movePlayer(event.key)

            else:
                print("Invalid Key was pushed")
        
        else:
            player.stopPlayer()

# プログラム終了関数
def exit():
    pygame.quit()
    sys.exit()

# プログラム開始
if __name__ == "__main__":
    main()