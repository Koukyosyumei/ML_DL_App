import pandas as pd
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from keras.callbacks import EarlyStopping
from keras.models import Sequential
import keras.utils as ku
import pandas as pd
import numpy as np
import string
import os
import pickle
import sys
from tqdm import tqdm


def generate_text(seed_text, next_words, max_sequence_len, model_path=None, tokenizer_path=None):
    """ Summary line
        seed_textを基に、それに続く文章をnext_words文だけつくる

    Args
        seed_text  (str)   : もとになる文章
        next_words (int)   : 何文字生成するか
        max_sequence_len (int)
        model_path (str)     : 生成モデルのpath
        tokenizer_path (str) : tokenizerのpath

    Returns :
        result_text  (str) : seed_textに生成された文字列が結合されたもの

    """
    #------------------ 学習済みトークないざーとモデルの読み込み --------
    if tokenizer_path == None:
        tokenizer_path = "models/tokenizer-char.pickle"
    if model_path == None:
        model_path = 'models/generate_quote-char.h5'

    with open(tokenizer_path, 'rb') as handle:
         t = pickle.load(handle)

    model = load_model(model_path)

    #-------------------　生成 ---------------------------------


    for _ in range(next_words):
        #学習時と同様の前処理をする
        token_list = t.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')

        #次の一文字を生成
        predicted = model.predict_classes(token_list, verbose=0)
        #生成されたtokenをもとの文字に戻してseed_textに結合
    	output_word = ""

    	for word, index in t.word_index.items():
    		if index == predicted:
    		   output_word = word
    		   break

    	seed_text += "" + output_word

    result_text = seed_text

    return result_text
