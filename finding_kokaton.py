import os
import sys
import random
import pygame as pg
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 画面サイズ
WIDTH, HEIGHT = 800, 600


class Bird(pg.sprite.Sprite):
    """
    こうかとんに関するクラス
    """

    def __init__(self, num: int, xy: tuple[int, int]):
        """
        こうかとん画像を初期化する
        引数1 num：画像番号(0-9)
        引数2 xy：配置座標
        """
        super().__init__()
        # figフォルダ内の0.png~9.pngを読み込む
        img = pg.image.load(f"fig/{num}.png")
        self.image = pg.transform.rotozoom(img, 0, 1.0)
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.bird_id = num  # 正誤判定用の画像番号

        # 移動速度
        self.vx = random.choice([-3, -2, 2, 3])
        self.vy = random.choice([-3, -2, 2, 3])

    def update(self):
        """
        こうかとんを移動させる
        """
        self.rect.move_ip(self.vx, self.vy)
        
        # 画面端判定
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.vx *= -1  # 画面の左右の端に触れたら速度を反転
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.vy *= -1  # 画面の上下の端に触れたら速度を反転
            

def reset_stage(birds: pg.sprite.Group):
    """
    担当機能：既存のこうかとんたちを消して、新しい配置とターゲットを生成する
    """
    birds.empty()  # 今いるこうかとんを全消去

    img_nums = [random.randint(0, 9) for _ in range(9)]  # 新しいステージ用の画像番号のリストを作る

    for i in range(9):
        x = random.randint(100, WIDTH - 100)
        y = random.randint(100, HEIGHT - 100)
        bird = Bird(img_nums[i], (x, y))
        birds.add(bird)  # こうかとんをランダムな位置に再配置
    
    return random.choice(birds.sprites())  # 新しいターゲットを決めて返す


def main():
    pg.display.set_caption("正しいこうかとんを探せ！！")

    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")

    # フォント
    font = pg.font.Font(None, 50)
    big_font = pg.font.Font(None, 100)

    # 鳥グループ
    birds = pg.sprite.Group()

    # 画像番号をランダムに9個選択
    img_nums = random.sample(range(10), 9)

    # ランダム座標
    positions = []

    for _ in range(9):
        x = random.randint(100, WIDTH - 100)
        y = random.randint(100, HEIGHT - 100)
        positions.append((x, y))

    # 鳥生成
    for i in range(9):
        bird = Bird(img_nums[i], positions[i])
        birds.add(bird)

    # 正解の鳥をランダム決定
    target_bird = random.choice(birds.sprites())

    # 左上に表示する画像
    target_img = pg.transform.rotozoom(
        pg.image.load(f"fig/{target_bird.bird_id}.png"),
        0,
        1.0
    )
    # 基本機能：9種類の鳥を生成してグループに登録
    birds = pg.sprite.Group()
    target_bird = reset_stage(birds)  # 初回ステージ生成

    img_nums = list(range(10)) 
    random.shuffle(img_nums)  # 画像をランダムに
    mode = "PLAYING"  # 最初はプレイ中モード
    clear_timer = 0  # クリア画面の表示時間
    stage_count = 1   # 何問目かのカウント

    # 基本機能：ターゲット（正解）を1つ決める
    target_bird = random.choice(birds.sprites())
    target_img = pg.transform.rotozoom(pg.image.load(f"fig/{target_bird.bird_id}.png"), 0, 1.0)
    clock = pg.time.Clock()

    # 制限時間
    time_limit = 30
    start_time = pg.time.get_ticks()

    # 状態管理
    game_clear = False
    time_up = False

    # clock = pg.time.Clock()

    while True:

        # イベント処理
        for event in pg.event.get():

            if event.type == pg.QUIT:
                return

            # マウスクリック
            if event.type == pg.MOUSEBUTTONDOWN:

                # クリア後はクリック無効
                if game_clear or time_up:
                    continue

                for bird in birds:

                    if bird.rect.collidepoint(event.pos):

                        # 正解判定
                        if bird.bird_id == target_bird.bird_id:
                            game_clear = True

        # 経過時間
        now = pg.time.get_ticks()
        elapsed = (now - start_time) / 1000

        # 残り時間
        remaining = max(0, int(time_limit - elapsed))

        # 時間切れ
        if remaining <= 0 and not game_clear:
            time_up = True

        # 更新
        if not game_clear and not time_up:
            birds.update()

        # 背景
        screen.blit(bg_img, (0, 0))

        if mode == "PLAYING":  # プレイ中の更新処理
            birds.update()
            birds.draw(screen)  # すべてのこうかとんを描画
            target_img = pg.transform.rotozoom(pg.image.load(f"fig/{target_bird.bird_id}.png"), 10, 1.5)  # ターゲットの見本を左上に表示
            screen.blit(target_img, [10, 10])
            pg.draw.rect(screen, (255, 0, 0), [5, 5, 120, 120], 3) # # 正解のこうかとんを囲む赤い枠線

        elif mode == "CLEAR":  # クリア画面の演出
            txt = font.render(f"STAGE {stage_count} CLEAR!!", True, [255, 0, 0])
            screen.blit(txt, [WIDTH//2 - 250, HEIGHT//2 - 50])  # 画面中央に現在のステージクリアを表示
            
            clear_timer -= 1 # タイマーを減らす
            
            # タイマーが0になったらリセットして次の問題へ
            if clear_timer <= 0:
                stage_count += 1
                target_bird = reset_stage(birds) # ステージ再構築
                mode = "PLAYING" # ゲーム再開
        
        pg.display.update()

        # ターゲット画像
        screen.blit(target_img, (10, 10))

        # 枠線
        pg.draw.rect(screen, (255, 0, 0), (5, 5, 100, 100), 3)

        # タイマー表示
        timer_text = font.render(
            f"TIME : {remaining}",
            True,
            (255, 255, 255)
        )
        screen.blit(timer_text, (580, 20))

        # 鳥描画
        birds.draw(screen)

        # CLEAR表示
        if game_clear:
            clear_text = big_font.render(
                "CLEAR!",
                True,
                (255, 0, 0)
            )
            screen.blit(clear_text, (220, 250))

        # TIME UP表示
        if time_up:
            time_text = big_font.render(
                "TIME UP!",
                True,
                (0, 0, 255)
            )
            screen.blit(time_text, (150, 250))

     


        # # 3秒後終了
        # if game_clear or time_up:
        #     pg.time.wait(3000)
        #     return

        clock.tick(60)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()