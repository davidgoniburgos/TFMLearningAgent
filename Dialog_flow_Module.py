# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 20:05:37 2022

@author: David Goñi Burgos
@Module: Flujo de diálogo
"""

def siguiente_pregunta(dialogflow_):
    # se recorre el diálogo de atras a adelante buscando el úlitmo id de pregunta contestada correctamente
    for dialog_ in reversed(dialogflow_):
        if dialog_['pregunta']['res_preg'] == 1:
            return dialog_['pregunta']['id']
    return 0

def calcular_acierto_pregunta(respuestas_, historys_id_, id_preg_ ,res_usuario_, res_modelo_):
    
    #https://machinelearninggeek.com/text-similarity-measures/
    score_ = 0.0
    
    # Let's import text feature extraction TfidfVectorizer
    from sklearn.feature_extraction.text import TfidfVectorizer
    
    # Import Cosien Similarity metric
    from sklearn.metrics.pairwise import cosine_similarity
        
    docs_=[res_usuario_, res_modelo_]
    
    # Create TFidfVectorizer 
    tfidf = TfidfVectorizer()
    
    # Fit and transform the documents 
    tfidf_vector = tfidf.fit_transform(docs_)
    
    # Compute cosine similarity
    score_=cosine_similarity(tfidf_vector[0],tfidf_vector[1])
    
    # Print the cosine similarity
    print("Cálculo de acierto coseno: ",score_)
    return res_modelo_, score_

def calcular_acierto_pregunta_fonetica(res_usuario_, res_modelo_):
    #https://pypi.org/project/phonetics/
    import phonetics
    
    score_=0.0
    from sklearn.feature_extraction.text import TfidfVectorizer
    
    # Import Cosien Similarity metric
    from sklearn.metrics.pairwise import cosine_similarity
        
    docs_=[phonetics.dmetaphone(res_usuario_)[0], phonetics.dmetaphone(res_modelo_)[0]]
    
    # Create TFidfVectorizer 
    tfidf = TfidfVectorizer()
    
    # Fit and transform the documents 
    tfidf_vector = tfidf.fit_transform(docs_)
    
    # Compute cosine similarity
    score_=cosine_similarity(tfidf_vector[0],tfidf_vector[1])
    
    # Print the cosine similarity
    print("Cálculo de acierto fonético: ",score_)
    return score_
    
def calcular_tfidf_doc(pregunta_, contextos_, oraculo_):
    #Se pasa la pregunta a minúsculas
    texto_busqueda = pregunta_.lower()
    documentos = contextos_
    #Eliminamos stopwords de pregunta y contexto
    #Eliminamos signos de puntuación de pregunta y contexto    
    import pandas as pd
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize

    nltk.download('punkt')
    nltk.download('stopwords')
    stop_words = set(stopwords.words('spanish'))
    documentos_new = []
    for doc in documentos:
      word_tokens = word_tokenize(doc)
      # Se eliminan las palabras que no contengan caracteres alfanuméricos
      new_words = [word for word in word_tokens if word.isalnum()]
      # Se eliminan las stop words de español
      filtered_sentence = [w for w in new_words if not w.lower() in stop_words]
      
      documentos_new.append(' '.join(map(str, filtered_sentence)))
    
    documentos = documentos_new
    #import the TfidfVectorizer from Scikit-Learn.
    from sklearn.feature_extraction.text import TfidfVectorizer
    all_docs = documentos
    #vectorizer = TfidfVectorizer(max_df=.65, min_df=1, stop_words=None, use_idf=True, norm=None)
    vectorizer = TfidfVectorizer(stop_words=None, use_idf=True, norm=None)
    transformed_documents = vectorizer.fit_transform(all_docs)
    
    transformed_documents_as_array = transformed_documents.toarray()
    # Se genera un tfidf por documento de contexto
    documentos_tfidf =[]
    for counter, doc in enumerate(transformed_documents_as_array):
        # construct a dataframe
        tf_idf_tuples = list(zip(vectorizer.get_feature_names_out(), doc))
        one_doc_as_df = pd.DataFrame.from_records(tf_idf_tuples, columns=['term', 'score']).sort_values(by='score', ascending=False).reset_index(drop=True)
        # se eliminan registros a cero
        one_doc_as_df = one_doc_as_df[one_doc_as_df.score != 0]
        # Se transforma del DataFrame en array
        documentos_tfidf.append(one_doc_as_df.to_numpy())
    
    documentos_limpio = documentos_tfidf
    texto_busqueda_tokens = word_tokenize(texto_busqueda)
    texto_busqueda_tokens_words = [word for word in texto_busqueda_tokens if word.isalnum()]
    texto_busqueda_tokens_words_filtered_sentence = [w for w in texto_busqueda_tokens_words if not w.lower() in stop_words]
      
    calculo_doc = []
    score_per_doc = 1.0
    for i,doc in enumerate(documentos_limpio):
      #Si no hay aciertos devolverá -1
      calculo_doc.append(-1)
      for word in texto_busqueda_tokens_words_filtered_sentence:
        for word_in_doc in doc:
          if word == word_in_doc[0]:
            score_per_doc *= word_in_doc[1]
      calculo_doc[i] = score_per_doc
    
    print("doc a buscar:" ,calculo_doc.index(max(calculo_doc)))
    return calculo_doc.index(max(calculo_doc))