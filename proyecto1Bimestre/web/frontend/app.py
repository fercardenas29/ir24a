from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
from sklearn.metrics import jaccard_score
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__, static_folder='static', template_folder='templates')

# Función para cargar los datos precomputados
def load_precomputed_data(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data

# Ruta del archivo de datos precomputados
precomputed_data_path = r'C:\Users\usuario\Fer-Pc\Escritorio\EPN\2024-A\SEPTIMO_SEMESTRE\RECUPERACION_DE_INFORMACION\ir24a\proyecto1Bimestre\data\preprocessd_data.pkl'

# Cargar los datos precomputados al iniciar la aplicación Flask
precomputed_data = load_precomputed_data(precomputed_data_path)
filenames = precomputed_data['filenames']
documents = precomputed_data['documents']  # Cargar el contenido original de los documentos
bow_vectors = precomputed_data['bow_vectors']
tfidf_vectors = precomputed_data['tfidf_vectors']
bow_vectorizer = precomputed_data['bow_vectorizer']
tfidf_vectorizer = precomputed_data['tfidf_vectorizer']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    method = request.args.get('method')
    threshold = float(request.args.get('threshold'))
    
    bow_query_vector = bow_vectorizer.transform([query])
    tfidf_query_vector = tfidf_vectorizer.transform([query])
    
    bow_query_array = bow_query_vector.toarray()[0]
    bow_vectors_array = bow_vectors.toarray()
    
    if method == 'BoW':
        similarities = [
            jaccard_score(bow_query_array, bow_vector, average='binary') for bow_vector in bow_vectors_array
        ]
    elif method == 'TF-IDF':
        similarities = cosine_similarity(tfidf_query_vector, tfidf_vectors).flatten()
    
    results_df = pd.DataFrame({
        'id': filenames,
        'similarity': similarities
    })
    
    filtered_results = results_df[results_df['similarity'] >= threshold]
    top_results = filtered_results.nlargest(50, 'similarity')
    
    results = [
        {'filename': row['id'], 'content': documents[filenames.index(row['id'])]}
        for _, row in top_results.iterrows()
    ]
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
