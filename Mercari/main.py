from utils import load_image, image_2_price
import pandas as pd


def main():

    # ここらへんは、ベタ打ちから修正すること
    fpath = "gdrive/My Drive/IMG-PRICE/IMG-PRICE/"
    fname = "orutyan.csv"

    # -------- ハイパーパラメータ --------------------------
    # 外部ファイルから読み込めるようにすること

    # 画像サイズ
    x = 150  # 296
    y = 150  # 296
    Z = x*y  # 入力層のノード数
    # エポック数
    E = 100
    # バッチサイズ
    BATCH_SIZE = 32
    # 学習率
    LR = 0.01
    # 使う枚数
    num_image = 100

    # ------- 価格の読み込み、前処理 ---------------------
    df = pd.read_csv(fpath+fname)
    price = df["price"].apply(lambda x: float(str(x).replace(",", "")))
    price = price.fillna(0)

    print("mean_price: ", price.mean())

    # -------- 画像読み込み ---------------
    image_list = load_image(x, y, num_image, fpath)

    # -------- 学習 -----------------------
    image_2_price(price, image_list, x=x, y=y, Z=Z, E=E, BATCH_SIZE=BATCH_SIZE,
                  LR=LR, num_image=num_image)


if __name__ == "__main__":
    main()
