from AI_analytics import SupplierRanker
import numpy as np
import pandas as pd
import json

def train_AI():
    with open('project\\backend\\testdata.json', 'r') as f:
        loaded_data = json.load(f)

    #создаём экземпляр нейросети
    ranker = SupplierRanker()

    #готвим данные
    df = ranker.preprocess_data(loaded_data)

    #датафрейм для промпта ИИшке
    supplier_data = pd.DataFrame(loaded_data)

    # После препроцессинга данных
    X_demo = df[[
        'years_active',
        'return_rate',
        'order_count',
        'customer_count', 
        'composite_rating'
    ]]

    y_demo = np.array([0.5, 0.5, 0.8])  # Пример целевых значений

    ranker.train_ranking_model(X_demo, y_demo)

    # Обучение модели
    ranker.train_ranking_model(X_demo, y_demo)

    # Получение итоговых оценок
    supplier_scores = ranker.calculate_supplier_score(X_demo)
    print('\nРейтинги поставщиков:')
    for idx, score in enumerate(supplier_scores):
        print(f'Поставщик #{idx+1}: {score:.2f}')

