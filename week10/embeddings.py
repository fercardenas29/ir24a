import pandas as pd
import numpy as np
import multiprocessing
from gensim.models import KeyedVectors
from transformers import BertTokenizer, TFBertModel


wine_df = pd.read_csv('data/winemag-data_first150k.csv')
corpus = wine_df['description']

model_path = 'data/GoogleNews-vectors-negative300.bin.gz'

#word2vector
word2vec_model = KeyedVectors.load_word2vec_format(model_path, binary=True)

#bert
# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = TFBertModel.from_pretrained('bert-base-uncased')

# Get the embeddings for the corpus using the word2vec model

def generate_word2vec_embeddings(texts):
    embeddings = []
    for text in texts:
        tokens = text.lower().split()
        word_vectors = [word2vec_model[word] for word in tokens if word in word2vec_model]
        if word_vectors:
            embeddings.append(np.mean(word_vectors, axis=0))
        else:
            embeddings.append(np.zeros(word2vec_model.vector_size))
    return np.array(embeddings)


def generate_word2vec_embeddings_parallel(text):
    num_nucleos = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_nucleos)

    embeddings = pool.map(generate_word2vec_embeddings, text)
    pool.close()
    pool.join()
    return np.array(embeddings)

corpus_word2Vec = generate_word2vec_embeddings_parallel(corpus[:10])

#Get the embeddings for the corpus using the bert model