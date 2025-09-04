import pickle
import math
from collections import Counter
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

class Pesquisa:
    def __init__(self):

        nltk.data.path.append("nltk_data") #hack para funcionar 100% offline, pois o streamlit na nuvem não consegue baixar os dados remotamente
        self.carregarIndice("index.pkl")
        self.stemmer = PorterStemmer()        
        self.stop_words = set(stopwords.words('portuguese'))

        #**
        # 
        #   'indice_invertido': dict(self.indice_invertido),
        #    'tfidf': m,
        #    'documentos': self.documentos,
        #    'tamanhos_docs': self.tamanhos_docs
        # *#
    
    def carregarIndice(self, index_file):
        try:
            with open(index_file, 'rb') as f:
                data = pickle.load(f)
            self.indice_invertido = data['indice_invertido']
            self.tfidf = data['tfidf']
            self.documentos = data['documentos']
            self.tamanhos_docs = data['tamanhos_docs']
        except FileNotFoundError:
            self.indice_invertido = {}
            self.tfidf = {}
            self.documentos = {}
            self.tamanhos_docs = {}
    

    def preprocessar(self, texto):
        texto = texto.lower()
        texto = re.sub(r'[^\w\s]', ' ', texto) #remove caracteres especiais
        tokens = word_tokenize(texto)
        tokens = [self.stemmer.stem(token) for token in tokens 
                 if token not in self.stop_words and len(token) > 1]
        return tokens    


    def pesquisar(self, consulta, t=10): #pesquisa paginada
        if not self.documentos:
            return []

        # Preprocessar a consulta e extrair termos
        temos = self.preprocessar(consulta)
        if not temos:
            return []
                
        scores = {}
        freq = Counter(temos)
        
        for documento in self.documentos:
            score = 0
            for termo in temos:  #soma os scores dos termos para o score final
                if termo in self.tfidf and documento in self.tfidf[termo]:
                    score += self.tfidf[termo][documento] * freq[termo]

            if score > 0:  #Trocar aqui caso deseje mudar o thredshold
                scores[documento] = score
        #ordena o resultado do maior para o menor, levando a página em consideração (:t )
        results = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:t]

        return [(documento, score, self.documentos[documento][:200] + "...")
                for documento, score in results]