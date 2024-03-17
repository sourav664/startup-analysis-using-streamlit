import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='Startup Analysis')
df = pd.read_csv('startup_v1.csv', index_col=False).drop(columns=['Unnamed: 0'])
df['month'] = pd.to_datetime(df['date']).dt.month

def load_overall_analysis():
    st.title('Overall Analysis')
    
    # total invested amount
    total = round(df['amount'].sum())
    
    # max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    
    # avg ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    
    #Total Funded Startup
    startup = df['startup'].nunique()
    
    col1,col2,col3,col4 = st.columns(4)
    with col1:
       st.metric('Total',str(total) + ' Cr')
    with col2:
        st.metric('Max',str(round(max_funding)) + ' Cr')
    with col3:
        st.metric('Avg',str(round(avg_funding)) + ' Cr') 
        
    with col4:
        st.metric('StartUp',str(startup))  
    
    st.header('MoM graph')    
    selected_option = st.selectbox('Select Type',['Total','Count'])
    
    if selected_option == 'Total': 
        temp_df = df.groupby(['year','month'], as_index=False)['amount'].sum() 
        
    else:
        temp_df = df.groupby(['year','month'], as_index=False)['amount'].count() 
    
    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig, ax = plt.subplots()
    ax.plot(temp_df['x_axis'], temp_df['amount'])

    st.pyplot(fig)
        
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
        
    with col2:
        vertical5_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values(ascending=False).head(10)
        st.subheader('Top 10 Sectors Invested in')
        fig, ax = plt.subplots()
        ax.pie(vertical5_series,labels=vertical5_series.index, autopct='%.2f%%')
        st.pyplot(fig)
        
    
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('YoY Investments')
    fig, ax = plt.subplots()
    ax.plot(year_series)
    ax.set_xlim(2014,2020)
    st.pyplot(fig)
    
    
st.sidebar.title('Startup Funding Analyis')
option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor'])

if option == 'Overall Analysis':
    # btn0 = st.sidebar.button('Show Overall Analysis')
    # if btn0:
        load_overall_analysis()

elif option == 'StartUp':
    st.sidebar.selectbox('Select StartUp',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    st.title('StartUp Analysis')
else:
     selected_investors = st.sidebar.selectbox('Select StartUp',sorted(set(df['investors'].str.split(',').sum())))
     btn2 = st.sidebar.button('Find investors Details')
     if btn2:
         load_investor_details(selected_investors)
    
    