import multiprocessing 
import pandas as pd
import numpy as np
from multiprocessing import Pool
from random import randrange
import time
from gensim.models import KeyedVectors
def f(x):
    time.sleep(randrange(0,1))
    return x*x


def generate_embbedings (text):
    embeddings = []
    tokens = text.lower().split()
    word_vectors = [word2vec_model[word] for word in tokens if word in word2vec_model]
    if word_vectors:
        embeddings.append(np.mean(word_vectors, axis=0))
    else:
        embeddings.append(np.zeros(word2vec_model.vector_size))
    return np.array(embeddings)


def mq(x):
    for i in range(1, len(x)):
        if x[i] < x[i-1]:
            print('False')

def print10(x):
    print(x[:100])

    

if __name__ == '__main__':
    # Ruta al archivo descargado
    
    model_path = 'data/GoogleNews-vectors-negative300.bin.gz'
    # Cargar el modelo Word2Vec preentrenado
    word2vec_model = KeyedVectors.load_word2vec_format(model_path, binary=True)

    df = pd.read_csv('/data/podcastdata_dataset.csv')
    corpus = df['text']
    pool = Pool(processes=4)
    embddings = pool.map(generate_embbedings, corpus[:10])
    print(embddings)
    df['embeddings'] = embddings



    #x = range(1000)
    #pool = Pool(4)
    #ans = pool.map(f, x)
    #print(ans)