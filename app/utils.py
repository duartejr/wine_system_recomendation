#%%
import streamlit as st
import numpy as np
import pandas as pd
from joblib import load

clf = load('https://github.com/duartejr/wine_system_recomendation/blob/9e5b2e7cd98b5ede3055bb96ba98b036dd3dd659/app/classifier.joblib') 
vetorizador = load('https://github.com/duartejr/wine_system_recomendation/blob/9e5b2e7cd98b5ede3055bb96ba98b036dd3dd659/app/vectorizer.joblib')
system_data = pd.read_csv('https://raw.githubusercontent.com/duartejr/wine_system_recomendation/main/data/processed/wines_recomendation_system.csv')

@st.cache
def load_data():
    data = pd.read_csv(f'https://raw.githubusercontent.com/duartejr/wine_system_recomendation/main/data/processed/wines_user_consult.csv')
    data = data.drop_duplicates()
    return data

@st.cache
def select_data(data, styles, countries, points, price, sort_by, order):
    data = data[data['style'].isin(styles)]
    data = data[data['country'].isin(countries)]
    data = data[data['points'].between(points[0], points[1])]
    data = data[data['price'].between(price[0], price[1])]
    
    if order == 'ascending':
        order = True
    else:
        order = False
    data = data.sort_values(by=sort_by, ascending=order)
    return data[['title', 'variety', 'style', 'winery', 'province', 'country', 'points', 'price']]

#%%
def recomendation(wine, user_data):
    test = system_data.query(f"title == '{wine}'")
    user_count_vec = vetorizador.transform(test.description)
    NNs_clf = clf.kneighbors(user_count_vec, return_distance=True)
    answer = user_data.loc[NNs_clf[1][0, :]]
    answer['similarity (%)'] = np.round(100 * (1 - NNs_clf[0][0, :]), 2)
    return answer
#%%
