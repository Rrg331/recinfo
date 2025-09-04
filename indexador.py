import os
import re
import pickle
import math
import time
from collections import defaultdict, Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

class Indexador:
    def __init__(self):
        nltk.data.path.append("nltk_data") #hack para funcionar 100% offline, pois o streamlit na nuvem não consegue baixar os dados remotamente
        self.indice_invertido = defaultdict(dict)
        self.documentos = {}
        self.tamanhos_docs = {}
        self.stemmer = PorterStemmer()
        self.stop_words = set()

    def preprocessar(self, texto):
        texto = texto.lower()
        texto = re.sub(r'[^\w\s]', ' ', texto) #remove caracteres especiais
        tokens = word_tokenize(texto)
        tokens = [self.stemmer.stem(token) for token in tokens 
                 if token not in self.stop_words and len(token) > 1]
        return tokens
    
    def indexar(self, pasta):
        inicio = time.time()
        self.stop_words = set(stopwords.words('portuguese'))
        

        for filename in os.listdir(pasta):
            if filename.endswith('.txt'):
                print(f"Indexando o arquivo {filename}")
                filepath = os.path.join(pasta, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    texto = f.read()
                
                doc_id = filename
                self.documentos[doc_id] = texto
                
                tokens = self.preprocessar(texto) 
                freq = Counter(tokens)
                self.tamanhos_docs[doc_id] = len(tokens)

                for term, freq in freq.items():
                    self.indice_invertido[term][doc_id] = freq
        
        fim = time.time()
        tempo_total = fim - inicio
        print(f"Indexação concluída em {tempo_total:.2f} segundos")


    #calcula o TF-IDF de acordo com o slide 18 da aula 8
    #(1 + log fi,j) * (1 + log N/df)
    def calcular_tfidf(self):

        
        N = len(self.documentos) #qtd total de documentos 

        print(f"calculando o TF-IDF para {N} documentos")
        matriz = {}
        
        for termo in self.indice_invertido:
            
            df = len(self.indice_invertido[termo])
            idf = math.log(N / df)
            
            matriz[termo] = {}
            for doc_id, tf in self.indice_invertido[termo].items():
                tfidf = tf * idf
                matriz[termo][doc_id] = tfidf    

        return matriz
    

    #serializa o dicionario para um arquivo
    def salvar(self):
        m = self.calcular_tfidf()
        index_data = {
            'indice_invertido': dict(self.indice_invertido),
            'tfidf': m,
            'documentos': self.documentos,
            'tamanhos_docs': self.tamanhos_docs
        }
        with open('index.pkl', 'wb') as f:
            pickle.dump(index_data, f)
        print(f"Índice salvo em index.pkl")


    def gerarIndice(self) :
        ini = time.time()
        self.indexar('docs')
        self.salvar()
        print(f"Indexados {len(self.documentos)} documentos em {time.time() - ini:.2f} segundos")


#se chamado direto 
if __name__ == "__main__":    
    indexador = Indexador()
    indexador.gerarIndice()
   

