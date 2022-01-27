# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 14:25:29 2021

@author: David Goñi Burgos
@Module: Módulo de conocimiento del profesor y de entrenamiento
"""

import json

def extraer_kb (file):   
    kb_file = json.loads(open(file,encoding="utf-8").read())
    return kb_file


def extraer_contexto(json):
    
    contexts_ = []
    historys_ = []
    questions_ = []
    answers_ = []
    historys_id_ = []
    id_ =0
    for paragraph in json['data']:
        for passage in paragraph['paragraphs']:
            context = passage['context']
            for qa in passage['qas']:
                history = qa['history']
                question = qa['question']
                for answer in qa['answers']:
                    contexts_.append(context)
                    historys_.append(history)
                    historys_id_.append(id_)
                    questions_.append(question)
                    answers_.append(answer)
                id_ += 1
                                    
    return contexts_, historys_, historys_id_, questions_, answers_
