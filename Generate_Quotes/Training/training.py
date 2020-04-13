from utils import extract_texts_from_db, get_sequence_of_tokens, generate_padded_sequences, create_model
import dataset
import argparse
import pandas as pd
import pandas as pd
import numpy as np
import string, os
import datetime
from keras.preprocessing.text import Tokenizer

if __name__ == "__main__":
    ps = argparse.ArgumentParser(description='文章生成モデルの学習プログラム')
    ps.add_argument("--db_path", "-p", help="path for database")
    ps.add_argument("--epochs", "-e", default=10, help="num of epochs")
    args = ps.parse_args()

    db_path    = args.db_path
    all_quotes = extract_texts_from_db(db_path)
    corpus = [x for x in all_quotes]

    t = Tokenizer(num_words=None, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
                  lower=True, split=' ', char_level=False, oov_token=None,
                  document_count=0)

    input_sequences, num_unique_words = get_sequence_of_tokens(t, corpus)

    predictors, label, max_sequence_len = generate_padded_sequences(input_sequences,
                                                                    num_unique_words)

    model = create_model(max_sequence_len, num_unique_words)
    model.fit(predictors, label, epochs=int(args.epochs), verbose=5)

    dt_now = datetime.datetime.now()
    model.save("generate_text_{time}.h5".format(time=dt_now.isoformat()))
