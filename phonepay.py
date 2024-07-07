import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json

#dataframe_creation

#sql connection
mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepay_data",
                      password="root")
cursor= mydb.cursor()

#aggre_insurance_df
cursor.execute("SELECT * FROM aggregrated_insurance")
mydb.commit()
table1= cursor.fetchall()

Aggre_insurance=pd.DataFrame(table1,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#aggre_transaction_df
cursor.execute("SELECT * FROM aggregrated_transaction")
mydb.commit()
table2= cursor.fetchall()

Aggre_transaction=pd.DataFrame(table2,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#aggre_user_df
cursor.execute("SELECT * FROM aggregrated_user")
mydb.commit()
table3= cursor.fetchall()

Aggre_user=pd.DataFrame(table3,columns=("States","Years","Quarter","Brands","Transaction_count","percentage"))

#map_insurance
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4= cursor.fetchall()

map_insurance=pd.DataFrame(table4,columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

#map_transaction
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5= cursor.fetchall()

map_transaction=pd.DataFrame(table5,columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

#map_user
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6= cursor.fetchall()

map_user=pd.DataFrame(table6,columns=("States","Years","Quarter","Districts","RegisteredUsers","AppOpens"))

#top_insurance
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7= cursor.fetchall()

top_insurance=pd.DataFrame(table7,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))

#top_transaction
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8= cursor.fetchall()

top_transaction=pd.DataFrame(table8,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))

#top_user
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9= cursor.fetchall()

top_user=pd.DataFrame(table9,columns=("States","Years","Quarter","Pincodes","RegisteredUsers"))


def transaction_amount_count_y(df, year):

    tacy = df[df["Years"] == year]
    tacy.reset_index(drop = True, inplace=True)

    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2 = st.columns(2)
    with col1:

        fig_amount= px.bar(tacyg, x="States", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT", height= 650, width= 600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count= px.bar(tacyg, x="States", y="Transaction_count", title=f"{year} TRANSACTION COUNT", height=650, width= 600)
        st.plotly_chart(fig_count)  

    col1,col2= st.columns(2)
    with col1:    
        url ="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1= json.loads(response.content)
        states_names= []
        for feature in data1["features"]:
            states_names.append(feature["properties"]["ST_NM"])

        states_names.sort()

        fig_india_1= px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM", 
                                color= "Transaction_amount", color_continuous_scale= "tealrose",
                                range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name= "States", title= f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                height= 600, width= 600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)
    with col2:

            
        fig_india_2= px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM", 
                                color= "Transaction_count", color_continuous_scale= "tealrose",
                                range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "States", title= f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                height= 600, width= 600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tacy

def transaction_amount_count_y_Q(df, quarter):

    tacy = df[df["Quarter"] == quarter]
    tacy.reset_index(drop = True, inplace=True)

    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(tacyg, x="States", y="Transaction_amount", title=f"{tacy['Years'].min()} year {quarter} TRANSACTION AMOUNT", height= 650, width= 600)
        st.plotly_chart(fig_amount)

    with col2:

        fig_count= px.bar(tacyg, x="States", y="Transaction_count", title=f"{tacy['Years'].min()} year {quarter} TRANSACTION COUNT", height= 650, width= 600)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1: 
        url ="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1= json.loads(response.content)
        states_names= []
        for feature in data1["features"]:
            states_names.append(feature["properties"]["ST_NM"])

        states_names.sort()

        fig_india_1= px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM", 
                                color= "Transaction_amount", color_continuous_scale= "tealrose",
                                range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name= "States", title= f"{tacy['Years'].min()} year {quarter} TRANSACTION AMOUNT", fitbounds= "locations",
                                height= 600, width= 600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2= px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM", 
                                color= "Transaction_count", color_continuous_scale= "tealrose",
                                range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "States", title= f"{tacy['Years'].min()} year {quarter} TRANSACTION COUNT", fitbounds= "locations",
                                height= 600, width= 600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tacy


def Aggre_Tran_Transaction_type(df, state):

    tacy= df[df["States"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_pie_1= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_amount",
                        width= 600, title= f"{state} transaction amount", hole= 0.5)
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_count",
                        width= 600, title= f"{state} transaction count", hole= 0.5)
        st.plotly_chart(fig_pie_2)


#aggre_user_analysis
def Aggre_user_plot_1(df, year):
    aguy= df[df["Years"]== year]
    aguy.reset_index(drop= True, inplace= True)
    aguyg=pd.DataFrame( aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyg, x="Brands", y= "Transaction_count", title= "brands and transaction count", 
                    width= 800, color_discrete_sequence= px.colors.sequential.Greens_r)

    st.plotly_chart(fig_bar_1)

    return aguy


#Aggre_user_analysis_1
def Aggre_user_plot_2(df, quarter):
    aguyq= df[df["Quarter"]== quarter]
    aguyq.reset_index(drop= True, inplace= True)

    aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace= True)


    fig_bar_1= px.bar(aguyqg, x="Brands", y= "Transaction_count", title= f"{quarter} quarter brands and transaction count", 
                    width= 800, color_discrete_sequence= px.colors.sequential.Greens_r)

    st.plotly_chart(fig_bar_1)

    return aguyq

#aggre_user_analysis_3
def Aggre_user_plot_3(df, state):
    auyqs= df[df["States"] == state]
    auyqs.reset_index(drop= True, inplace= True)

    fig_line_1= px.line(auyqs, x= "Brands", y="Transaction_count", hover_data="percentage",
                        title= "brands, transaction count , percentage",width=600)
    st.plotly_chart(fig_line_1)


#map_insurance_district
def map_insur_District(df, state):

    tacy= df[df["States"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)
    col1, col2= st.columns(2)
    with col1:
        fig_bar_1= px.bar(tacyg, x= "Transaction_amount", y= "Districts", orientation= "h",
                        title= f"{state} district and transaction amount", color_discrete_sequence= px.colors.sequential.Greens_r)
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2= px.bar(tacyg, x= "Transaction_count", y= "Districts", orientation= "h",
                        title= f"{state} district and transaction count", color_discrete_sequence= px.colors.sequential.Greens_r)
        st.plotly_chart(fig_bar_2)



#map_user_plot_1
def map_user_plot_1(df, year):
    muy= df[df["Years"]== year]
    muy.reset_index(drop= True, inplace= True)


    muyg=muy.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, x= "States", y=["RegisteredUsers", "AppOpens"],
                        title= "registeruser appopens",width=600, height= 800, markers= True)
    st.plotly_chart(fig_line_1)

    return muy


#map_user_plot_2
def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"]== quarter]
    muyq.reset_index(drop= True, inplace= True)


    muyqg=muyq.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_line_1= px.line(muyqg, x= "States", y=["RegisteredUsers", "AppOpens"],
                        title= "quarter registeruser appopens",width=600, height= 800, markers= True)
    st.plotly_chart(fig_line_1)

    return muyq


#map_user_plot_3
def map_user_plot_3(df, states):
    muyqs= df[df["States"]== states]
    muyqs.reset_index(drop= True, inplace= True)

    fig_map_user_bar_1= px.bar(muyqs, x= "RegisteredUsers", y="Districts", orientation= "h",
                            title= "registered user", height= 800, color_discrete_sequence= px.colors.sequential.Greens_r)
    st.plotly_chart(fig_map_user_bar_1)

    fig_map_user_bar_2= px.bar(muyqs, x= "AppOpens", y="Districts", orientation= "h",
                            title= "appopens", height= 800, color_discrete_sequence= px.colors.sequential.Greens_r)
    st.plotly_chart(fig_map_user_bar_2)

#top_insurance_plot_1
def top_insurance_plot_1(df, state):
    tiy= df[df["States"]== state]
    tiy.reset_index(drop= True, inplace= True)

    col1,col2 = st.columns(2)
    with col1:
        fig_top_insur_bar_1= px.bar(tiy, x= "Quarter", y="Transaction_amount", hover_data= "Pincodes",
                                title= "transaction amount", height= 600,width= 600, color_discrete_sequence= px.colors.sequential.Greens_r)
        st.plotly_chart(fig_top_insur_bar_1)

    with col2:
        fig_top_insur_bar_2= px.bar(tiy, x= "Quarter", y="Transaction_count", hover_data= "Pincodes",
                                title= "transaction count", height= 600,width=600, color_discrete_sequence= px.colors.sequential.Greens_r)
        st.plotly_chart(fig_top_insur_bar_2)


def top_user_plot_1(df, year):
    tuy= df[df["Years"]== year]
    tuy.reset_index(drop= True, inplace= True)


    tuyg= pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUsers", color= "Quarter", width= 1000, height=800,
                        color_discrete_sequence= px.colors.sequential.Greens_r, title= "registerd users")
    st.plotly_chart(fig_top_plot_1)

    return tuy


#top_user_plot_2
def top_user_plot_2(df, state):
    tuys= df[df["States"]== state]
    tuys.reset_index(drop= True, inplace= True)

    fig_top_plot_2= px.bar(tuys, x= "Quarter", y= "RegisteredUsers", title= "registersusers, pincode, quarters",
                        width= 1000, height= 800, color= "RegisteredUsers", hover_data= "Pincodes",
                        color_continuous_scale= px.colors.sequential.Greens_r)
    st.plotly_chart(fig_top_plot_2)

#sql connection
def top_chart_transaction_amount(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepay_data",
                        password="root")
    cursor= mydb.cursor()

    query1=f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns= ("States", "transaction_amount"))

    col1, col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="States", y="transaction_amount", title=f"TRANSACTION AMOUNT", height= 650, width= 600)
        st.plotly_chart(fig_amount)


    query2=f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount 
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns= ("States", "transaction_amount"))
    with col2:

        fig_amount_2= px.bar(df_2, x="States", y="transaction_amount", title=f"TRANSACTION AMOUNT", height= 650, width= 600)
        st.plotly_chart(fig_amount_2)


    query3=f'''SELECT states, AVG(transaction_amount) AS transaction_amount
                    FROM {table_name}
                    GROUP BY states
                    ORDER BY transaction_amount ;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns= ("States", "transaction_amount"))
    fig_amount_3= px.bar(df_3, y="States", x="transaction_amount", title=f"TRANSACTION AMOUNT", height= 650, width= 600,orientation="h",
                        color_discrete_sequence=px.colors.sequential.Redor_r)
    st.plotly_chart(fig_amount_3)

#sql connection
def top_chart_transaction_count(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepay_data",
                        password="root")
    cursor= mydb.cursor()

    query1=f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns= ("States", "transaction_count"))

    col1, col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="States", y="transaction_count", title=f"TRANSACTION COUNT", height= 650, width= 600)
        st.plotly_chart(fig_amount)


    query2=f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count 
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns= ("States", "transaction_count"))

    with col2:
        fig_amount_2= px.bar(df_2, x="States", y="transaction_count", title=f"TRANSACTION COUNT", height= 650, width= 600)
        st.plotly_chart(fig_amount_2)


    query3=f'''SELECT states, AVG(transaction_count) AS transaction_count
                    FROM {table_name}
                    GROUP BY states
                    ORDER BY transaction_count ;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns= ("States", "transaction_count"))
    fig_amount_3= px.bar(df_3, y="States", x="transaction_count", title=f"TRANSACTION COUNT", height= 650, width= 600,orientation="h",
                        color_discrete_sequence=px.colors.sequential.Redor_r)
    st.plotly_chart(fig_amount_3)

#sql connection
def top_chart_registered_user(table_name, state):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepay_data",
                        password="root")
    cursor= mydb.cursor()

    query1=f'''SELECT districts, SUM(registeredusers) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns= ("districts", "registereduser"))
    col1, col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="districts", y="registereduser", title=f"registered user", height= 650, width= 600)
        st.plotly_chart(fig_amount)


    query2=f'''SELECT districts, SUM(registeredusers) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns= ("districts", "registereduser"))

    with col2:

        fig_amount_2= px.bar(df_2, x="districts", y="registereduser", title=f"registered user", height= 650, width= 600)
        st.plotly_chart(fig_amount_2)


    query3=f'''SELECT districts, AVG(registeredusers) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns= ("districts", "registereduser"))
    fig_amount_3= px.bar(df_3, y="districts", x="registereduser", title=f"registered user", height= 650, width= 600,orientation="h",
                        color_discrete_sequence=px.colors.sequential.Redor_r)
    st.plotly_chart(fig_amount_3)



#sql connection
def top_chart_appopens(table_name, state):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepay_data",
                        password="root")
    cursor= mydb.cursor()

    query1=f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns= ("districts", "appopens"))

    col1, col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="districts", y="appopens", title=f"appopens", height= 650, width= 600)
        st.plotly_chart(fig_amount)


    query2=f'''SELECT districts, SUM(registeredusers) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns= ("districts", "appopens"))
    with col2:
        fig_amount_2= px.bar(df_2, x="districts", y="appopens", title=f"appopens", height= 650, width= 600)
        st.plotly_chart(fig_amount_2)


    query3=f'''SELECT districts, AVG(registeredusers) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns= ("districts", "appopens"))
    fig_amount_3= px.bar(df_3, y="districts", x="appopens", title=f"appopens", height= 650, width= 600,orientation="h",
                        color_discrete_sequence=px.colors.sequential.Redor_r)
    st.plotly_chart(fig_amount_3)



#sql connection
def top_chart_registered_users(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepay_data",
                        password="root")
    cursor= mydb.cursor()

    query1=f'''SELECT states, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns= ("states", "registeredusers"))
    col1, col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="states", y="registeredusers", title=f"registered users", height= 650, width= 600)
        st.plotly_chart(fig_amount)


    query2=f'''SELECT states, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers 
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns= ("states", "registeredusers"))
    with col2:
        fig_amount_2= px.bar(df_2, x="states", y="registeredusers", title=f"registered users", height= 650, width= 600)
        st.plotly_chart(fig_amount_2)


    query3=f'''SELECT states, AVG(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers DESC;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns= ("states", "registeredusers"))
    fig_amount_3= px.bar(df_3, y="states", x="registeredusers", title=f"registered users", height= 650, width= 600,orientation="h",
                        color_discrete_sequence=px.colors.sequential.Redor_r)
    st.plotly_chart(fig_amount_3)


#streamlit_part


st.set_page_config(layout="wide")
st.title("project2")

with st.sidebar:
    select=option_menu("menu",["data exploration","top charts"])

if select == "data exploration":
    tab1, tab2, tab3 = st.tabs(["aggregrated analysis","map analysis","top analysis"])


    with tab1:
        method = st.radio("select the method",["insurance analysis","transaction analysis","user analysis"])

        if method == "insurance analysis":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("slect years",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())
            tac_y= transaction_amount_count_y(Aggre_insurance, years)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("slect quarter",tac_y["Quarter"].min(),tac_y["Quarter"].max(),tac_y["Quarter"].min())

            transaction_amount_count_y_Q(tac_y, quarters)

        elif method == "transaction analysis":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("slect years",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
            Aggre_tran_tac_y= transaction_amount_count_y(Aggre_transaction, years)


            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("select the state", Aggre_tran_tac_y["States"].unique())

            Aggre_Tran_Transaction_type(Aggre_tran_tac_y, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("slect quarter",Aggre_tran_tac_y["Quarter"].min(),Aggre_tran_tac_y["Quarter"].max(),Aggre_tran_tac_y["Quarter"].min())

            aggre_tran_tac_y_Q= transaction_amount_count_y_Q(Aggre_tran_tac_y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("select the state", aggre_tran_tac_y_Q["States"].unique())

            Aggre_Tran_Transaction_type(aggre_tran_tac_y_Q, states)

        elif method == "user analysis":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("slect years",Aggre_user["Years"].min(),Aggre_user["Years"].max(),Aggre_user["Years"].min())
            Aggre_user_Y= Aggre_user_plot_1(Aggre_user, years)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("slect quarter",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())

            Aggre_user_Y_Q= Aggre_user_plot_2(Aggre_user_Y, quarters)


            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("select the state", Aggre_user_Y_Q["States"].unique())

            Aggre_user_plot_3(Aggre_user_Y_Q, states)            

    with tab2:
        method_2 = st.radio("select the method",["map insurance","map transaction","map user"])
        
        if method_2 == "map insurance":

            col1,col2= st.columns(2)
            with col1:

                years = st.slider("Select years", map_insurance["Years"].min(), map_insurance["Years"].max(), map_insurance["Years"].min(), key="years_slider")

            map_insur_tac_y= transaction_amount_count_y(map_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("select the state", map_insur_tac_y["States"].unique())

            map_insur_District(map_insur_tac_y, states)

            col1,col2= st.columns(2)
            with col1:



                # Assuming map_insur_tac_y is already defined and loaded with data
                quarters = st.slider(
                    "Select quarter", 
                    min_value=map_insur_tac_y["Quarter"].min(), 
                    max_value=map_insur_tac_y["Quarter"].max(), 
                    value=map_insur_tac_y["Quarter"].min(),
                    key="unique_key_for_slider"
                )



            map_insur_tac_y_Q= transaction_amount_count_y_Q(map_insur_tac_y, quarters)


            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("select the state", map_insur_tac_y_Q["States"].unique())

            map_insur_District(map_insur_tac_y_Q, states)

        elif method_2 == "map transaction":
            
            col1,col2= st.columns(2)
            with col1:

                years = st.slider("Select years", map_transaction["Years"].min(), map_transaction["Years"].max(), map_transaction["Years"].min(), key="years_slider")

            map_tran_tac_y= transaction_amount_count_y(map_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("select the state", map_tran_tac_y["States"].unique())

            map_insur_District(map_tran_tac_y, states)

            col1,col2= st.columns(2)
            with col1:



                # Assuming map_insur_tac_y is already defined and loaded with data
                quarters = st.slider(
                    "Select quarter", 
                    min_value=map_tran_tac_y["Quarter"].min(), 
                    max_value=map_tran_tac_y["Quarter"].max(), 
                    value=map_tran_tac_y["Quarter"].min(),
                    key="unique_key_for_slider"
                )



            map_tran_tac_y_Q= transaction_amount_count_y_Q(map_tran_tac_y, quarters)


            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("select the state", map_tran_tac_y_Q["States"].unique())

            map_insur_District(map_tran_tac_y_Q, states)

        elif method_2 == "map user":

            col1,col2= st.columns(2)
            with col1:

                years = st.slider("Select years", map_user["Years"].min(), map_user["Years"].max(), map_user["Years"].min(), key="years_slider")

            map_user_Y= map_user_plot_1(map_user, years)

            
            col1,col2= st.columns(2)
            with col1:



                # Assuming map_insur_tac_y is already defined and loaded with data
                quarters = st.slider(
                    "Select quarter", 
                    min_value=map_user_Y["Quarter"].min(), 
                    max_value=map_user_Y["Quarter"].max(), 
                    value=map_user_Y["Quarter"].min(),
                    key="unique_key_for_slider"
                )



            map_user_Y_Q= map_user_plot_2(map_user_Y, quarters)


            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("select the state", map_user_Y_Q["States"].unique())

            map_user_plot_3(map_user_Y_Q, states) 

    with tab3:
        method_3 = st.radio("select the emthod",["top insurance","top transaction","top user"])
        
        if method_3 == "top insurance":
            
            col1,col2= st.columns(2)
            with col1:

                years = st.slider("Select years", top_insurance["Years"].min(), top_insurance["Years"].max(), top_insurance["Years"].min(), key="years_slider_ti")

            top_insur_tac_y= transaction_amount_count_y(top_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("select the state_ti", top_insur_tac_y["States"].unique())

            top_insurance_plot_1(top_insur_tac_y, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("slect quarter_tiq",top_insur_tac_y["Quarter"].min(),top_insur_tac_y["Quarter"].max(),top_insur_tac_y["Quarter"].min())

            top_insur_tac_y_Q= transaction_amount_count_y_Q(top_insur_tac_y, quarters)

        elif method_3== "top transaction":
            

            col1,col2= st.columns(2)
            with col1:

                years = st.slider("Select the years", top_transaction["Years"].min(), top_transaction["Years"].max(), top_transaction["Years"].min(), key="years_slider_ti")

            top_tran_tac_y= transaction_amount_count_y(top_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("select the state_tt", top_tran_tac_y["States"].unique())

            top_insurance_plot_1(top_tran_tac_y, states)

            col1,col2= st.columns(2)
            with col1:


                quarters= st.slider("slect the quarter",top_tran_tac_y["Quarter"].min(),top_tran_tac_y["Quarter"].max(),top_tran_tac_y["Quarter"].min())

            top_tran_tac_y_Q= transaction_amount_count_y_Q(top_tran_tac_y, quarters)

        elif method_3 == "top user":
            
            col1,col2= st.columns(2)
            with col1:

                years = st.slider("Select the years_tu", top_user["Years"].min(), top_user["Years"].max(), top_user["Years"].min(), key="years_slider_ti")

            top_user_y= top_user_plot_1(top_user, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("select the state_tu", top_user_y["States"].unique())

            top_user_plot_2(top_user_y, states)


elif select == "top charts":
    
    question= st.selectbox("select the question",["1.Transaction Amount and Count of Aggregated Insurance",
                                                    "2.Transaction Amount and Count of Map Insurance",
                                                    "3.Transaction Amount and Count of Top Insurance",
                                                   "4.Transaction Amount and Count of Aggregated Transaction",
                                                    "5.Transaction Amount and Count of Map Transaction",
                                                    "6.Transaction Amount and Count of Top Transaction",
                                                    "7.Transaction Count of Aggregated User",
                                                    "8.Registered users of Map User",
                                                    "9.App opens of Map User",
                                                    "10.Registered users of Top User",
                                                    ])
    if question == "1.Transaction Amount and Count of Aggregated Insurance":

        st.subheader("transaction amount")
        top_chart_transaction_amount("aggregrated_insurance")

        st.subheader("transaction count")
        top_chart_transaction_count("aggregrated_insurance")

    elif question == "2.Transaction Amount and Count of Map Insurance":

        st.subheader("transaction amount")
        top_chart_transaction_amount("map_insurance")

        st.subheader("transaction count")
        top_chart_transaction_count("map_insurance")


    elif question == "3.Transaction Amount and Count of Top Insurance":

        st.subheader("transaction amount")
        top_chart_transaction_amount("top_insurance")

        st.subheader("transaction count")
        top_chart_transaction_count("top_insurance")

    elif question == "4.Transaction Amount and Count of Aggregated Transaction":

        st.subheader("transaction amount")
        top_chart_transaction_amount("aggregrated_transaction")

        st.subheader("transaction count")
        top_chart_transaction_count("aggregrated_transaction")

    elif question == "5.Transaction Amount and Count of Map Transaction":

        st.subheader("transaction amount")
        top_chart_transaction_amount("map_transaction")

        st.subheader("transaction count")
        top_chart_transaction_count("map_transaction")

    elif question == "6.Transaction Amount and Count of Top Transaction":

        st.subheader("transaction amount")
        top_chart_transaction_amount("top_transaction")

        st.subheader("transaction count")
        top_chart_transaction_count("top_transaction")

    elif question == "7.Transaction Count of Aggregated User":

        st.subheader("transaction count")
        top_chart_transaction_count("aggregrated_user")

    elif question == "8.Registered users of Map User":

        states= st.selectbox("states", map_user["States"].unique())
        st.subheader("register user")
        top_chart_registered_user("map_user", states) 

    elif question == "9.App opens of Map User":

        states= st.selectbox("states", map_user["States"].unique())
        st.subheader("appopens")
        top_chart_appopens("map_user", states)

    elif question == "10.Registered users of Top User":

        st.subheader("registeredusers")
        top_chart_registered_users("top_user")
