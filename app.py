import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='Startup Analysis')
df = pd.read_csv('startup_v1.csv', index_col=False).drop(columns=['Unnamed: 0'])

def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investments of the investor
    last5_df = df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)
    
    col1, col2 = st.columns(2)
    with col1:
        big5_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big5_series.index, big5_series.values)
        st.pyplot(fig)
        

st.sidebar.title('Startup Funding Analyis')
option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor'])

if option == 'Overall Analysis':
    pass

elif option == 'StartUp':
    st.sidebar.selectbox('Select StartUp',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    st.title('StartUp Analysis')
else:
     selected_investors = st.sidebar.selectbox('Select StartUp',sorted(set(df['investors'].str.split(',').sum())))
     btn2 = st.sidebar.button('Find investors Details')
     if btn2:
         load_investor_details(selected_investors)
    
    