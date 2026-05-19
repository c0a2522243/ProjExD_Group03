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

        img = pg.image.load(f"fig/{num}.png")
        self.image = pg.transform.rotozoom(img, 0, 2.0)
        self.rect = self.image.get_rect()
        self.rect.center = xy

        # 正誤判定用ID
        self.bird_id = num

        # 移動速度
        self.vx = random.choice([-3, -2, 2, 3])
        self.vy = random.choice([-3, -2, 2, 3])

    def update(self):
        """
        こうかとんを移動させる
        """
        self.rect.move_ip(self.vx, self.vy)

        # 横方向反射
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.vx *= -1

        # 縦方向反射
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.vy *= -1


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

    # 制限時間
    time_limit = 30
    start_time = pg.time.get_ticks()

    # 状態管理
    game_clear = False
    time_up = False

    clock = pg.time.Clock()

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

        # 画面更新
        pg.display.update()

        # 3秒後終了
        if game_clear or time_up:
            pg.time.wait(3000)
            return

        clock.tick(60)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()