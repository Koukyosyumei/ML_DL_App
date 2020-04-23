import pandas as pd
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
from keras.callbacks import CSVLogger
import numpy as np
from PIL import Image
from keras.models import Model
from keras.layers import Input
from keras.applications.vgg16 import VGG16
import matplotlib.pyplot as plt


# ------- 画像の読み込み --------------------
def load_image(x, y, num_image, fpath):

    image_list = []
    print("画像の読み込み　開始")
    for i in range(0, num_image):
        # im = cv2.imread(fpath+"img/"+str(i)+".jpg".format(i), 1)

        if i % 100 == 0:
            print(i)
        image = np.array(Image.open(fpath+"img/"+str(i)+".jpg").resize((x, y)))
        image_list.append(image / 296.)
    print("画像の読み込み　終了")

    # kerasに渡すためにnumpy配列に変換。
    image_list = np.array(image_list)
    image_list[np.isnan(image_list)] = 0
    print("変換終了")

    return image_list


def image_2_price(price, image_list, x=150, y=150, Z=150**2, E=100,
                  BATCH_SIZE=32, LR=0.01, num_image=100):

    # ------ モデルの定義 --------------------

    vgg16_model = VGG16(weights='imagenet', include_top=False,
                        input_tensor=Input(shape=(x, y, 3)))

    for layer in vgg16_model.layers[:15]:
        layer.trainable = False

    inputs = vgg16_model.output
    x = Flatten()(inputs)
    x = Dense(1024, activation='relu')(x)
    prediction = Dense(1)(x)

    model = Model(inputs=vgg16_model.input, outputs=prediction)

    print("model_summary")
    print(model.summary())

    opt = Adam(lr=0.01)

    model.compile(loss='mean_squared_error',
                  optimizer=opt,
                  metrics=['mean_absolute_error', 'mean_squared_error'])

    csv_logger = CSVLogger('training_process.csv')

    # ------------------- training -----------------------------

    _ = model.fit(image_list[:num_image], price[:num_image],
                  epochs=E, verbose=1, callbacks=[csv_logger],
                  batch_size=BATCH_SIZE, validation_split=0.2)

    # ------------------- save result --------------------------

    model.save('img2price.h5')

    process = pd.read_csv("training_process.csv")

    plt.plot(process.loss[1:], c="b", label="train_loss")
    plt.plot(process.val_loss[1:], c="g", label="val_loss")
    plt.legend()
    plt.savefig("output/loss.png")

    plt.plot(process.mean_absolute_error[1:], c="b",
             label="train_absolute_error")
    plt.plot(process.val_mean_absolute_error[1:], c="g",
             label="val_absolute_error")
    plt.legend()
    plt.savefig("output/absolute_error.png")
