import streamlit as st
import pickle
import pandas as pd
from pesquisa import Pesquisa
from sidebar import render_sidebar

st.title("Sistema de Recuperação de Informação - UFRJ 2025/2")

indexado = render_sidebar() #desenha a sidebar, e retorna se o indice existe ou não

#Exibir indice ou  pesquisa session do streamlit
if hasattr(st.session_state, 'indice_visivel') and st.session_state.indice_visivel and indexado:
    #deserializa o indice para uso
    with open('index.pkl', 'rb') as f:
        data = pickle.load(f)
    
    st.header("Índice")
    
    # Criar DataFrame para exibição em grid
    rows = []
    for term, docs in data['tfidf'].items():
        for doc_id, tfidf in docs.items():
            tf = data['indice_invertido'][term][doc_id]
            df = len(data['indice_invertido'][term])
            idf = tfidf / tf if tf > 0 else 0
            rows.append({
                'Termo': term,
                'Documento': doc_id,
                'TF': tf,
                'DF': df,
                'IDF': round(idf, 4),
                'TF-IDF': round(tfidf, 4)
            })
    
    df_index = pd.DataFrame(rows)
    st.dataframe(df_index)
    
    if st.button("Fechar"):
        st.session_state.indice_visivel = False
        st.rerun()

# pesquisa
elif indexado:
    motor = Pesquisa()

    #caso existam documentos indexados
    if motor.documentos:
        st.write(f"**{len(motor.documentos)} documentos** indexados")

        # Campo de busca
        query = st.text_input("Pesquisa:", placeholder="Ex: xadrez peão")

        col1, col2 = st.columns([1, 4])
        with col1:
            top_k = st.selectbox("Resultados:", [5, 10, 20], index=1)
        
        if query:
            results = motor.pesquisar(query, top_k)
            
            if results:
                st.write(f"**resultados encontrados: {len(results)}**")

                for i, (doc_id, score, preview) in enumerate(results, 1):
                    with st.expander(f"{i}. {doc_id} (Score: {score:.3f})"):
                        st.write(preview)
                        
                        if st.button(f"Ver documento completo", key=f"view_{doc_id}"):
                            st.text_area("Conteúdo completo:",
                                       motor.documentos[doc_id],
                                       height=300)
            else:
    
                st.warning("Nenhum documento encontrado para esta consulta.")    
    else: #sem documentos indexados
        st.warning("Nenhum documento indexado.")

elif not (hasattr(st.session_state, 'indice_visivel') and st.session_state.indice_visivel): #se não tiver indice, não exibe a tela de pesquisa
    st.error("Índice não encontrado. Clique em 'Reindexar Documentos' para criar o índice.")
