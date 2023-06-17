import mysql.connector 
import pandas as pd
import json
import streamlit as st
import PIL 
from PIL import Image
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import requests
import mysql 
# connect to the database
#establishing the connection
conn = mysql.connector.connect(user='root', password='DevaMEA1833', host='localhost', database="phonepe_pulse", auth_plugin = "mysql_native_password")

# create a cursor object -Allows Py code to execute postgreSQL command in database
cursor = conn.cursor()

#..........TOP BAR.................................#
SELECT = option_menu( 
    menu_title = None,
    options = ["Home","Data Charts","Visual Data"],
    default_index=2,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white","size":"cover", "width": "100%"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "grey"},
        "nav-link-selected": {"background-color": "grey"}})

#...............HOME PAGE...............................#

if SELECT == "Home":
    st.title("Download The App Now!!")
    st.download_button("DOWNLOAD", "https://www.phonepe.com/app-download/")
    st.subheader("PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")

    st.video(r"C:\Users\DRAGSTA\Desktop\phone pe pulse\transactionvideo.mp4")
    st.subheader("PhonePe is a digital wallet and online payment system that allows users to transfer money, pay bills, and recharge mobile phones. It was founded in December 2015 and is headquartered in Bangalore, India. PhonePe is available in 11 Indian languages and is accepted by over 200 million users and 15 million merchants across India. It is owned by Flipkart, one of India's largest e-commerce companies.")
    st.subheader("Phonepe became a leading digital payments company")
    st.image(Image.open(r"C:\Users\DRAGSTA\Desktop\phone pe pulse\leading.png"))
    with open(r"C:\Users\DRAGSTA\Desktop\phone pe pulse\annual report.pdf","rb") as f:
     data = f.read()
     st.title("Click the button to download the Annual Report")
     st.download_button("DOWNLOAD REPORT",data,file_name="annual report.pdf")
    

#..............DATA CHARTS............................#

if SELECT == "Data Charts":
    st.title("DATA CHARTS")
    st.subheader("Here are some of the basic insights of data select and view data with graph")
    options = ["select a list",
               "Top List of states amount of transaction",
               "States based on type and amount of transaction",
               "Top List of Districts Count of transaction",
               "Districts based on states and amount of transaction",
               "Transaction_Count based on Districts and states",
               "Top List RegisteredUsers based on states and District"]
            #Option 1
    select = st.selectbox("Select the option",options)
    if select=="Top List of states amount of transaction":
        cursor.execute("SELECT DISTINCT States, Transaction_Year, SUM(Transaction_Amount) AS Total_Transaction_Amount FROM top_tran GROUP BY States, Transaction_Year ORDER BY Total_Transaction_Amount DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(), columns=['States','Transaction_Year', 'Transaction_Amount'])
        st.write(df)
        st.title("Top 10 states and amount of transaction")
        st.bar_chart(data=df,x="Transaction_Amount",y="States")
         #Option 2        
    elif select=="States based on type and amount of transaction":
        cursor.execute("SELECT DISTINCT States, SUM(Transaction_Count) as Total FROM top_tran GROUP BY States ORDER BY Total ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['States','Total_Transaction'])
        st.write(df)
        st.title("List 10 states based on type and amount of transaction")
        st.bar_chart(data=df,x="Total_Transaction",y="States")
         #Option 3          
    elif select=="Top List of Districts Count of transaction":
        cursor.execute("SELECT DISTINCT State, District, SUM(RegisteredUsers) AS Users FROM top_user GROUP BY State, District ORDER BY Users DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['State','District','RegisteredUsers'])
        st.write(df)
        st.title("Top 10 Registered-users based on States and District")
        st.bar_chart(data=df,x="State",y="RegisteredUsers")   
        #Option 4            
    elif select=="Districts based on states and amount of transaction":
        cursor.execute("SELECT DISTINCT States,Transaction_year,SUM(Transaction_Amount) AS Amount FROM agg_trans GROUP BY States, Transaction_year ORDER BY Amount ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['States','Transaction_year','Transaction_Amount'])
        st.write(df)
        st.title("Least 10 Districts based on states and amount of transaction")
        st.bar_chart(data=df,x="States",y="Transaction_Amount")
            
        #Option 5     
    elif select=="Transaction_Count based on Districts and states":
        cursor.execute("SELECT DISTINCT States, District, SUM(Transaction_Count) AS Counts FROM map_tran GROUP BY States,District ORDER BY Counts ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['States','District','Transaction_Count'])
        st.write(df)
        st.title("List 10 Transaction_Count based on Districts and states")
        st.bar_chart(data=df,x="States",y="Transaction_Count")
            
        #Option 6      
    elif select=="Top List RegisteredUsers based on states and District":
        cursor.execute("SELECT DISTINCT States,District, SUM(RegisteredUsers) AS Users FROM map_user GROUP BY States,District ORDER BY Users DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns = ['States','District','RegisteredUsers'])
        st.write(df)
        st.title("Top 10 RegisteredUsers based on states and District")
        st.bar_chart(data=df,x="States",y="RegisteredUsers")

    

#------vizualization--------#

if SELECT == "Visual Data":
   
 #libre office-ctrl+shift+s(to save file in csv format)
  df = pd.read_csv(r"C:\Users\DRAGSTA\Desktop\dev\phonepe3map.csv",header=0,sep="\t")
  fig = px.choropleth(
    df,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='state',
    color='transactions',
    color_continuous_scale='Reds'
  )

  fig.update_geos(fitbounds="locations", visible=False)
  fig.update_layout(title_text='PhonePe Transactions list in 2022 - Hover on Each State to view the content')
  fig.show()


    
    


    



