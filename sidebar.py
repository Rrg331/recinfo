import streamlit as st
import os
import zipfile
import io
import time
from indexador import Indexador

def render_sidebar():
    st.sidebar.header("Menu")
    
    # Verificar se índice existe
    indexado = os.path.exists('index.pkl')
    st.sidebar.write(f"Status do índice: {'✅' if indexado else '❌'}")
    
    # Botão para reindexar
    if st.sidebar.button("Reindexar Documentos"):
        inicio = time.time()
        with st.spinner("Indexando documentos..."):
            indexador = Indexador()
            indexador.gerarIndice()
        fim = time.time()
        tempo = fim - inicio
        st.sidebar.success(f"Índice atualizado em {tempo:.2f}s!")
        st.rerun()
    
    # Botão para exibir índice
    if st.sidebar.button("Ver Índice"):
        if indexado:
            st.session_state.indice_visivel = True
        else:
            st.sidebar.warning("Índice não encontrado.")
    
   

        



    return indexado