import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

# if "selected_model" not in st.session_state:
#     st.session_state.selected_model = None

# if "selected_threadcount" not in st.session_state:
#     st.session_state.selected_threadcount = 1

st.set_page_config(layout='wide', page_title='Startup Analysis')
df = pd.read_csv('startup_v1.csv', index_col=False).drop(columns=['Unnamed: 0'])



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
    
    temp_df['month_wise'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    
    fig = px.line(temp_df, x='month_wise', y='amount', width=900)
    st.plotly_chart(fig, theme=None)
    
    
    
    option = st.selectbox('Sector', ['Amount','Count'])
    
    if option == 'Amount':
        temp_df = df.groupby('vertical', as_index=False)['amount'].sum().sort_values(by='amount', ascending=False).head(20)
        v = 'amount'
    else:
        temp_df = df['vertical'].value_counts().reset_index().head(20)
        v = 'count'
    
    fig = px.pie(temp_df, values=v, names='vertical')
    st.plotly_chart(fig, theme='streamlit')  
    
    select = st.selectbox('Funding',['Type of funding', 'City wise funding'])
    
    if select == 'Type of funding':
        temp_df = df['round'].value_counts().reset_index().head(10)
        b = 'count'
        n = 'round'
    else:
        temp_df = df.groupby('city', as_index=False)['amount'].sum().sort_values(by='amount', ascending=False).head(20)
        b = 'amount'
        n = 'city'
        
    fig = px.pie(temp_df, values=b, names=n)
    st.plotly_chart(fig, theme='streamlit')  
    
    st.header('Top Startups')
    top = st.selectbox('Startup',df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10).index.tolist())
    top_startup = df[df['startup'] == top]
    opt = st.radio('Analysis',["Year wise Investments","Overall"])
    if opt == 'Year wise Investments':
        
        t = top_startup.groupby('year')['amount'].sum()
        fig = plt.figure(figsize=(10,6))
        ax = sns.barplot( x=t.index, y=t.values, estimator='sum', errorbar=None)
        ax.bar_label(ax.containers[0], fontsize=10)
        st.pyplot(fig)
    
    else:
        st.dataframe(top_startup)
        fig = px.bar(top_startup, x='investors', y='amount',  color='round', text_auto=True)
        st.plotly_chart(fig, theme='streamlit') 
     
    st.header('Top Investors')
    top = st.selectbox('Investors',df.groupby('investors')['amount'].sum().sort_values(ascending=False).head(10).index.tolist())
    investors = df[df['investors'] == top]
    fig = px.bar(investors, x='startup', y='amount', color='year', text_auto=True)
    st.plotly_chart(fig, theme='streamlit')    
        
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
   
        fig =px.bar(x=big5_series.index, y=big5_series.values, width=400,height=400)
        st.plotly_chart(fig, theme='streamlit')  
        
    with col2:
        vertical5_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values(ascending=False).head(10)
        st.subheader('Sectors Invested in')
        fig = px.pie(values=vertical5_series.values, names=vertical5_series.index, width=400, height=400)
        st.plotly_chart(fig, theme='streamlit') 
    col3, col4 = st.columns(2)
    
    with col3:
        ro = pd.DataFrame(df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum().sort_values(ascending=False)).reset_index()
        st.subheader('Stages')
        fig = px.pie(ro, values='amount', names='round',width=350, height=350)
        st.plotly_chart(fig, theme=None)
        
    with col4:
        ro = pd.DataFrame(df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum().sort_values(ascending=False)).reset_index()
        st.subheader('City wise Investments')
        fig = px.pie(ro, values='amount', names='city',width=350, height=350)
        st.plotly_chart(fig, theme=None)
            

    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('YoY Investments')
    fig, ax = plt.subplots()
    ax.plot(year_series)
    ax.set_xlim(2014,2020)
    st.pyplot(fig)
    
def startup_analysis(startup):
    st.title(startup)
    startup = df[df['startup'].str.contains(startup)]
    industry = startup['vertical'].values[0]
    sub_industry = startup['subvertical'].values[0] 
    city = startup['city'].values[0]
    
    col1, col2 = st.columns(2)
    col1.metric("Industry", industry ,)
    col2.metric("Sub-Industry", sub_industry)
    st.metric("Location", city)
    
    startup['Date'] = startup['month'].astype('str') + '-' + startup['year'].astype('str')
    fig = px.bar(startup, y='amount',  x='Date', color='investors', text='round', width=1000, height=500)
    st.plotly_chart(fig, theme='streamlit') 
        
st.sidebar.title('Startup Funding Analyis')
option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor'])

if option == 'Overall Analysis':
    btn0 = st.sidebar.button('Show Overall Analysis')
    
    #Initialize sesion state
    if 'load_state' not in st.session_state:
        st.session_state.load_state = False
        
        
    if btn0 or st.session_state.load_state:
        st.session_state.load_state = True
        
        load_overall_analysis()

elif option == 'StartUp':
    selected_startup = st.sidebar.selectbox('Select StartUp',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    
    #Initialize sesion state
    if 'load_state' not in st.session_state:
        st.session_state.load_state = False
        
        
    if btn1 or st.session_state.load_state:
        st.session_state.load_state = True
        
        startup_analysis(selected_startup) 
    
else:
     selected_investors = st.sidebar.selectbox('Select StartUp',sorted(set(df['investors'].str.split(',').sum())))
     btn2 = st.sidebar.button('Find investors Details')
     if btn2:
         load_investor_details(selected_investors)
    
    