import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


import os
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Subash@28',  #your password
    database='practice'    #schema name
)

cur = conn.cursor()

from sqlalchemy import create_engine

engine = create_engine(
    "mysql+mysqlconnector://root:Subash%4028@localhost:3306/practice"
)



b = st.sidebar.selectbox('Select',['Home','Scenario'])
if b == 'Home':  
    data = st.selectbox("EXPLORE DATA",['PAYMENT','INSURANCE'])
    
    if data == 'PAYMENT':
        x = st.selectbox('Select',['transaction','user'])
        
            
        if x == 'transaction':
            
            summary_query = """
                SELECT 
                    SUM(transaction_amount) AS overall_transaction_amount,
                    AVG(transaction_amount) AS avg_transaction_amount
                FROM (
                    SELECT state, SUM(transaction_amount) AS transaction_amount
                    FROM top_transaction
                    GROUP BY state
                ) AS state_summary;
            """
            summary_df = pd.read_sql(summary_query, engine)

            st.subheader("All States Transaction Summary")
            st.write("**Overall Transaction Amount:**", summary_df['overall_transaction_amount'][0])
            st.write("**Average Transaction Amount (per state):**", summary_df['avg_transaction_amount'][0])
                        
            st.title("Top 10 Transactions Insights")

            option = st.selectbox("Select View", ["Districts", "Postal codes", "States"])

            if option == "Districts":
                query = """
                    SELECT state, location AS district, 
                        SUM(transaction_count) AS total_transaction_count,
                        SUM(transaction_amount) AS total_transaction_amount
                    FROM top_transaction
                    WHERE location_type = 'district'
                    GROUP BY state, district
                    ORDER BY total_transaction_amount DESC
                    LIMIT 10;
                """
                df = pd.read_sql(query, engine)
                st.subheader("Top 10 Districts - Transactions")
                st.dataframe(df)

            elif option == "Postal codes":
                query = """
                    SELECT state, location AS pincode, 
                        SUM(transaction_count) AS total_transaction_count,
                        SUM(transaction_amount) AS total_transaction_amount
                    FROM top_transaction
                    WHERE location_type = 'pincode'
                    GROUP BY state, pincode
                    ORDER BY total_transaction_amount DESC
                    LIMIT 10;
                """
                df = pd.read_sql(query, engine)
                st.subheader("Top 10 Pincodes - Transactions")
                st.dataframe(df)

            else:  # State-wise
                query = """
                    SELECT state, 
                        SUM(transaction_count) AS total_transaction_count,
                        SUM(transaction_amount) AS total_transaction_amount
                    FROM top_transaction
                    GROUP BY state
                    ORDER BY total_transaction_amount DESC
                    LIMIT 10;
                """
                df = pd.read_sql(query, engine)
                st.subheader("Top 10 States - Transactions")
                st.dataframe(df)
            
            query_quarter = """
                            SELECT year, quarter, 
                            SUM(transaction_amount) AS total_amount
                            FROM aggregated_transaction
                            GROUP BY year, quarter
                            ORDER BY year, quarter;
                            """

            df_quarter = pd.read_sql(query_quarter, engine)

            df_quarter['Period'] = df_quarter['year'].astype(str) + "-Q" + df_quarter['quarter'].astype(str)

            quarter_list = df_quarter['Period'].tolist()

            selected_quarter = st.selectbox("Select Year and Quarter", quarter_list)

            st.write("You selected:", selected_quarter)

            year_val, q_val = selected_quarter.split("-Q")

            
            query_map = f"""
                        SELECT state, SUM(transaction_amount) AS total_amount
                        FROM aggregated_transaction
                        WHERE year = '{year_val}' AND quarter = '{q_val}'
                        GROUP BY state;
                        """

            df_map = pd.read_sql(query_map, engine)
                
            df_map["state"] = (
                                df_map["state"]
                                .str.replace("-", " ")
                                .str.title()
                            )
                
            import json
            import plotly.express as px

            india_geojson_url = (
                    "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/"
                    "raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                )

            fig = px.choropleth(
                        df_map,
                        geojson=india_geojson_url,
                        featureidkey="properties.ST_NM",
                        locations="state",
                        color="state",   # 🔹 state-wise different colors
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        hover_name="state",
                        hover_data=["total_amount"],
                        title=f"Transaction Amounts - {selected_quarter}"
                    )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)
            
        if x == 'user':
            summary_query = """
                SELECT 
                    SUM(registered_users) AS overall_registered_users
                FROM top_user;
            """
            summary_df = pd.read_sql(summary_query, engine)

            st.subheader("All States Users Summary")
            st.write("**Overall Registered Users:**", summary_df['overall_registered_users'][0])

            st.title("Top 10 Users Insights")

            # Dropdown for selection
            option = st.selectbox("Select View", ["Districts", "Postal code", "States"])

            if option == "Districts":
                query = """
                    SELECT state, location AS district, 
                        SUM(registered_users) AS total_registered_users
                    FROM top_user
                    WHERE location_type = 'district'
                    GROUP BY state, district
                    ORDER BY total_registered_users DESC
                    LIMIT 10;
                """
                df = pd.read_sql(query, engine)
                st.subheader("Top 10 Districts - Registered Users")
                st.dataframe(df)

            elif option == "Postal code":
                query = """
                    SELECT state, location AS pincode, 
                        SUM(registered_users) AS total_registered_users
                    FROM top_user
                    WHERE location_type = 'pincode'
                    GROUP BY state, pincode
                    ORDER BY total_registered_users DESC
                    LIMIT 10;
                """
                df = pd.read_sql(query, engine)
                st.subheader("Top 10 Pincodes - Registered Users")
                st.dataframe(df)

            else:  # State-wise
                query = """
                    SELECT state, 
                        SUM(registered_users) AS total_registered_users
                    FROM top_user
                    GROUP BY state
                    ORDER BY total_registered_users DESC
                    LIMIT 10;
                """
                df = pd.read_sql(query, engine)
                st.subheader("Top 10 States - Registered Users")
                st.dataframe(df)
            
            
            query_quarter = """
                            SELECT year, quarter, state,
                                SUM(`registeredUsers`) AS total_users,
                                SUM(`appOpens`) AS total_appopens
                            FROM map_user
                            GROUP BY year, quarter, state
                            ORDER BY year, quarter, state;
                            """

           
            df_quarter = pd.read_sql(query_quarter, engine)

            df_quarter["Period"] = df_quarter["year"].astype(str) + "-Q" + df_quarter["quarter"].astype(str)

           
            quarter_list = df_quarter['Period'].unique().tolist()
            selected_quarter = st.selectbox("Select Year and Quarter", quarter_list)

            st.write("You selected:", selected_quarter)

            year_val, q_val = selected_quarter.split("-Q")

       
            df_map = df_quarter[
                (df_quarter["year"].astype(str) == year_val) &
                (df_quarter["quarter"].astype(str) == q_val)
            ].copy()

    
            df_map["state"] = (
                df_map["state"]
                .str.replace("-", " ")
                .str.title()
            )

            import plotly.express as px

            india_geojson_url = (
                "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/"
                "raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            )

      
            fig = px.choropleth(
                        df_map,
                        geojson=india_geojson_url,
                        featureidkey="properties.ST_NM",
                        locations="state",
                        color="state",   
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        hover_name="state",
                        hover_data=["total_users", "total_appopens"],
                        title=f"Registered Users & App Opens - {selected_quarter}"
                    )

         
            fig.update_geos(fitbounds="locations", visible=False)

         
            st.plotly_chart(fig, use_container_width=True)

    if data == 'INSURANCE': 
        
        summary_query = """
            SELECT 
                SUM(insurance_amount) AS overall_insurance_amount,
                AVG(insurance_amount) AS avg_insurance_amount
            FROM (
                SELECT state, SUM(insurance_amount) AS insurance_amount
                FROM top_insurance
                GROUP BY state
            ) AS state_summary;
        """
        summary_df = pd.read_sql(summary_query, engine)

        st.subheader("All States Insurance Summary")
        st.write("**Overall Insurance Amount:**", summary_df['overall_insurance_amount'][0])
        st.write("**Average Insurance Amount:**", summary_df['avg_insurance_amount'][0])
        
        st.title("Top 10 Insurance Insights")
        option = st.selectbox("Select View", ["Districts", "Postal code", "States"])

        if option == "Districts":
            query = """
                SELECT state, location AS district, 
                    SUM(insurance_count) AS total_insurance_count,
                    SUM(insurance_amount) AS total_insurance_amount
                FROM top_insurance
                WHERE location_type = 'district'
                GROUP BY state, district
                ORDER BY total_insurance_amount DESC
                LIMIT 10;
            """
            df = pd.read_sql(query, engine)
            st.subheader("Top 10 Districts - Insurance")
            st.dataframe(df)

        elif option == "Postal code":
            query = """
                SELECT state, location AS pincode, 
                    SUM(insurance_count) AS total_insurance_count,
                    SUM(insurance_amount) AS total_insurance_amount
                FROM top_insurance
                WHERE location_type = 'pincode'
                GROUP BY state, pincode
                ORDER BY total_insurance_amount DESC
                LIMIT 10;
            """
            df = pd.read_sql(query, engine)
            st.subheader("Top 10 Pincodes - Insurance")
            st.dataframe(df)

        else:  # State-wise
            query = """
                SELECT state, 
                    SUM(insurance_count) AS total_insurance_count,
                    SUM(insurance_amount) AS total_insurance_amount
                FROM top_insurance
                GROUP BY state
                ORDER BY total_insurance_amount DESC
                LIMIT 10;
            """
            df = pd.read_sql(query, engine)
            st.subheader("Top 10 States - Insurance")
            st.dataframe(df)
        
        query_quarter = """
                        SELECT `year`, `quarter`,
                            SUM(Insurance_amount) AS total_ins_amount,
                            SUM(Insurance_count) AS total_ins_count
                        FROM aggregated_insurance
                        GROUP BY `year`, `quarter`
                        ORDER BY `year`, `quarter`;
                        """
        df_quarter = pd.read_sql(query_quarter, engine)

        
        df_quarter['Period'] = df_quarter['year'].astype(str) + "-Q" + df_quarter['quarter'].astype(str)

     
        quarter_list = df_quarter['Period'].tolist()
        selected_quarter = st.selectbox("Select Year and Quarter", quarter_list)
        st.write("You selected:", selected_quarter)

        
        year_val, q_val = selected_quarter.split("-Q")

  
        query_map = f"""
                    SELECT state,
                        AVG(Insurance_amount) AS avg_ins_amount,
                        SUM(Insurance_amount) AS total_ins_amount,
                        SUM(Insurance_count) AS total_ins_count
                    FROM aggregated_insurance
                    WHERE `year` = {year_val} AND `quarter` = {q_val}
                    GROUP BY state;
                """
        df_map = pd.read_sql(query_map, engine)

   
        df_map["state"] = (
            df_map["state"]
            .str.replace("-", " ")
            .str.title()
        )

        import plotly.express as px

   
        india_geojson_url = (
            "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/"
            "raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        )

    
        fig = px.choropleth(
                df_map,
                geojson=india_geojson_url,
                featureidkey="properties.ST_NM",
                locations="state",
                color="state",   
                color_discrete_sequence=px.colors.qualitative.Set3,
                title=f"Insurance Overview - {selected_quarter}",
                hover_data=["total_ins_amount", "total_ins_count", "avg_ins_amount"],
                scope="asia"
            )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)
        


if b == 'Scenario':
    
    a = st.sidebar.selectbox('Scenario',['Decoding Transaction Dynamics on PhonePe','Device Dominance and User Engagement Analysis','Insurance Transactions Analysis','Transaction Analysis Across States and Districts','User Registration Analysis'])



    if a == 'Decoding Transaction Dynamics on PhonePe':
        c = st.sidebar.selectbox('Select',['Top States by Transaction Amount','Quarterly Transaction Trend (All India)','Transaction Amount Share by Type','State vs Transaction Type'])
        st.title("Decoding Transaction Dynamics on PhonePe")

        
        
        if c == 'Top States by Transaction Amount':
            st.header("Top  States by Transaction Amount")
            query_state = """
                        SELECT state, 
                        SUM(transaction_count) AS total_count, 
                        SUM(transaction_amount) AS total_amount
                        FROM aggregated_transaction
                        GROUP BY state
                        ORDER BY total_amount DESC;
                        """
            df_state = pd.read_sql(query_state, engine)

            fig = px.bar(
                df_state,
                x="state",
                y="total_amount",
                title="Top  States by Transaction Amount",
                labels={"state": "State", "total_amount": "Total Transaction Amount"},
                text="total_amount",
                color="total_amount",
                color_continuous_scale="Blues"
            )
            fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

            st.plotly_chart(fig, use_container_width=True)

            st.markdown("""
            **Insights:**
            1. Telangana, Karnataka, Maharashtra lead.  
            2. High population drives digital adoption.  
            3. Focus offers on lower states.  
            """)
            
            
        if c == 'Quarterly Transaction Trend (All India)' :
            st.header('Quarterly Transaction Trend (All India)')
            query_quarter = """
                            SELECT year, quarter, 
                                SUM(transaction_amount) AS total_amount
                            FROM aggregated_transaction
                            GROUP BY year, quarter
                            ORDER BY year, quarter;
                            """
            df_quarter = pd.read_sql(query_quarter, engine)

            df_quarter['Period'] = df_quarter['year'].astype(str) + "-Q" + df_quarter['quarter'].astype(str)


            fig = px.line(
                df_quarter,
                x="Period",
                y="total_amount",
                title="Quarterly Transaction Trend (All India)",
                labels={"Period": "Year-Quarter", "total_amount": "Total Transaction Amount"},
                markers=True)

            st.plotly_chart(fig, use_container_width=True)


            st.markdown("""
            **Insights:**
            1. Transactions show steady growth each quarter.  
            2. Festival quarters (Q3, Q4) see higher activity.  
            3. Adoption continues to rise across years.  
            """)
            
            
        if c == 'Transaction Amount Share by Type':
            st.header('Transaction Amount Share by Type')
            query_type = """
                        SELECT transaction_type, 
                        SUM(transaction_amount) AS total_amount
                        FROM aggregated_transaction
                        GROUP BY transaction_type
                        ORDER BY total_amount DESC;
                        """

            df_type = pd.read_sql(query_type, engine)
            
            fig = px.pie(df_type,
             values="total_amount",
             names="transaction_type",
             title="Transaction Amount Share by Type",
             hole=0)   
            fig.update_traces(textinfo="percent+label", pull=[0.05]*len(df_type))  
            
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("""
            **Insights:**
                        1. P2P transfers dominate share.
                        2. Merchant payments growing steadily.
                        3. Promote utility and merchant use.
                    """)
            
        if c == 'State vs Transaction Type' :
            st.header('State vs Transaction Type')
            
            query_heatmap = """
                            SELECT state, transaction_type, SUM(transaction_amount) AS total_amount
                            FROM aggregated_transaction
                            GROUP BY state, transaction_type
                            ORDER BY total_amount DESC;
                            """

            df_heatmap = pd.read_sql(query_heatmap, engine)
            
            pivot = df_heatmap.pivot(index="state", columns="transaction_type", values="total_amount")
            
            fig = px.bar(df_heatmap,
                        x="state",
                        y="total_amount",
                        color="transaction_type",
                        title="State vs Transaction Type",
                        labels={"total_amount": "Transaction Amount"},
                        barmode="stack")
            fig.update_layout(xaxis={'categoryorder':'total descending'})
            
            
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("""
            **Insights:**
                        1. Metros prefer merchant payments.
                        2. Smaller states rely on P2P.
                        3. Launch state-specific payment offers.
                    """)
            
        
        
        
    if a == 'Device Dominance and User Engagement Analysis':
        d = st.sidebar.selectbox('Select',['which mobile brand has the most registered users','high registration but low engagement','Which brands are popular in each state','how brand usage changes across years/quarters'])
        st.title("Device Dominance and User Engagement Analysis")
        
        
        if d == 'which mobile brand has the most registered users':
            st.header("which mobile brand has the most registered users")
            
            query_brand_share = """
                                SELECT install_mobile_brand, SUM(reg_user_brand) AS total_users
                                FROM aggregated_user
                                GROUP BY install_mobile_brand
                                ORDER BY total_users DESC;
                                """

            df_brand = pd.read_sql(query_brand_share, engine)
            
            fig = px.pie(df_brand,
                        names="install_mobile_brand",
                        values="total_users",
                        title="Device Brand Share (Registered Users)")
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Insights:**
                    1. Xiaomi and Samsung have highest users.
                    2. These brands are popular in Tier-2 cities.
                    3. Focus ads on lower user brands.
                    """)
            
            
        if d == 'high registration but low engagement':
            st.header('high registration but low engagement')
            
            query_engagement = """
                                SELECT install_mobile_brand, SUM(reg_user_brand) AS reg_users, SUM(appOpens) AS total_app_opens
                                FROM aggregated_user
                                GROUP BY install_mobile_brand
                                ORDER BY reg_users DESC;
                                """

            df_engagement = pd.read_sql(query_engagement, engine)
            
            fig = px.scatter(df_engagement,
                 x="reg_users",
                 y="total_app_opens",
                 size="reg_users",
                 color="install_mobile_brand",
                 text="install_mobile_brand",
                 title="Device Engagement: Registered Users vs App Opens")

            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Insights:**
                    1. Some brands show app opens very low.
                    2. Users register but don’t use regularly.
                    3. Need better app performance for them.
                    
                    """)
            
            
        if d == 'Which brands are popular in each state':
            st.header('Which brands are popular in each state')
            
            query_region = """
                            SELECT state, install_mobile_brand, SUM(reg_user_brand) AS reg_users
                            FROM aggregated_user
                            GROUP BY state, install_mobile_brand
                            ORDER BY state, reg_users DESC;
                            """

            df_region = pd.read_sql(query_region, engine)
            
            fig = px.bar(df_region,
             x="state",
             y="reg_users",
             color="install_mobile_brand",
             title="Region-wise Device Usage",
             labels={"reg_users": "Registered Users"},
             barmode="stack")
            fig.update_layout(xaxis={'categoryorder':'total descending'})
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Insights:**
                        1. iPhone popular in metro states.
                        2. Vivo, Oppo strong in small states.
                        3. Brand choice differs by region.
                    """)
            
        if d == 'how brand usage changes across years/quarters':
            st.header('how brand usage changes across years/quarters')
            
            query_trend = """
                            SELECT year, quarter, install_mobile_brand, SUM(reg_user_brand) AS reg_users
                            FROM aggregated_user
                            GROUP BY year, quarter, install_mobile_brand
                            ORDER BY year, quarter;
                            """

            df_trend = pd.read_sql(query_trend, engine)
            
            df_trend['Period'] = df_trend['year'].astype(str) + "-Q" + df_trend['quarter'].astype(str)
            
            fig = px.line(df_trend,
                            x="Period",
                            y="reg_users",
                            color="install_mobile_brand",
                            title="Device Usage Trend Over Time",
                            markers=True)
            
            fig.update_layout(xaxis_title="Year-Quarter", yaxis_title="Registered Users")

            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Insights:**
                        1. Overall usage grows every year.
                        2. New brands gain share recently.
                        3. Festival quarters show high usage.
                    """)


    if a == 'Insurance Transactions Analysis':
        e = st.sidebar.selectbox('Select',['Top 10 States by Insurance Amount','Top 10 Districts by Insurance Count','Top 10 Pincodes by Insurance Amount','Insurance Amount Growth by Year-Quarter'])
        st.title('Insurance Transactions Analysis')
        
        
        if e == 'Top 10 States by Insurance Amount':
            st.header('Top 10 States by Insurance Amount')
            
            query1 = """
                    SELECT state, SUM(insurance_amount) AS total_amount
                    FROM top_insurance
                    GROUP BY state
                    ORDER BY total_amount DESC
                    LIMIT 10;
                    """
            state_data = pd.read_sql(query1, engine)
            
            fig1 = px.bar(
                        state_data,
                        x="state",
                        y="total_amount",
                        text="total_amount",
                        title="Top 10 States by Insurance Amount",
                        color="total_amount")
            
            st.plotly_chart(fig1, use_container_width=True)
            
            st.markdown("""
            **Insights:**
                    1. Few states contribute the highest share.
                    2. Big states spend more on insurance.
                    3. Small states still have growth chance.
                    """)
            
            
        if e == 'Top 10 Districts by Insurance Count':
            st.header('Top 10 Districts by Insurance Count')
            
            query2 = """
                    SELECT location AS district, SUM(insurance_count) AS total_count
                    FROM top_insurance
                    WHERE location_type = 'district'
                    GROUP BY location
                    ORDER BY total_count DESC
                    LIMIT 10;
                    """
            district_data = pd.read_sql(query2, engine)
            
            fig2 = px.bar(
                        district_data,
                        x="district",
                        y="total_count",
                        text="total_count",
                        title="Top 10 Districts by Insurance Count",
                        color="total_count")
            
            st.plotly_chart(fig2, use_container_width=True)
            
            st.markdown("""
            **Insights:**
                    1. Some districts show very high demand.
                    2. Smaller towns adopt insurance quickly.
                    3. More agents needed in active districts.
                    """)
            
            
        if e == 'Top 10 Pincodes by Insurance Amount':
            st.header('Top 10 Pincodes by Insurance Amount')
            query3 = """
                    SELECT location AS pincode, SUM(insurance_amount) AS total_amount
                    FROM top_insurance
                    WHERE location_type = 'pincode'
                    GROUP BY location
                    ORDER BY total_amount DESC
                    LIMIT 10;
                    """
            pincode_data = pd.read_sql(query3, engine)
            
            fig3 = px.pie(
                        pincode_data,
                        names="pincode",
                        values="total_amount",
                        title="Top 10 Pincodes by Insurance Amount",
                        hole=0.4)
            
            st.plotly_chart(fig3, use_container_width=True)
            
            st.markdown("""
            **Insights:**
                        1. City pincodes lead in insurance spend.
                        2. Wealthy areas buy larger policies.
                        3. Premium plans suit these regions.
                    """)
            
        if e == 'Insurance Amount Growth by Year-Quarter':
            st.header('Insurance Amount Growth by Year-Quarter')
            query4 = """
                    SELECT year, quarter, SUM(insurance_amount) AS total_amount
                    FROM top_insurance
                    GROUP BY year, quarter
                    ORDER BY year, quarter;
                    """
            trend_data = pd.read_sql(query4, engine)
            
            trend_data["year_quarter"] = trend_data["year"].astype(str) + "-Q" + trend_data["quarter"].astype(str)
            
            fig4 = px.line(
                            trend_data,
                            x="year_quarter",
                            y="total_amount",
                            markers=True,
                            title="Insurance Amount Growth by Year-Quarter")
            
            st.plotly_chart(fig4, use_container_width=True)
            
            st.markdown("""
            **Insights:**
                        1. Insurance grows steadily each year.
                        2. Post-pandemic growth is faster.
                        3. Q3, Q4 show seasonal peaks.
                    """)        
        
        
        
    if a == 'Transaction Analysis Across States and Districts':
        f = st.sidebar.selectbox('Select',['where transactions are concentrated (high engagement)','Top States by Transaction amount','Top Districts by Transaction count','Top Pincodes by Transaction amount','District vs Pincode Contribution (count & amout)'])
        st.title('Transaction Analysis Across States and Districts')
        
        
        if f == 'where transactions are concentrated (high engagement)':
            st.header('where transactions are concentrated (high engagement)')
            query = """
                    SELECT state, SUM(transaction_count) AS total_count
                    FROM top_transaction
                    WHERE year='2023' AND quarter=1
                    GROUP BY state
                    ORDER BY total_count DESC
                    LIMIT 10;
                    """
            df_state_count = pd.read_sql(query, engine)
            
            fig = px.bar(df_state_count, x='state', y='total_count',
                        title='Top 10 States by Transaction Volume (2023 Q1)',
                        text_auto=True, color='state')
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Insights:**
                    1. Most transactions happen in few regions.
                    2. Big cities show strong digital activity.
                    3. Smaller areas have less engagement.
                    """)
            
            
        if f == 'Top States by Transaction amount':
            st.header('Top States by Transaction amount')
            query = """
                    SELECT state, SUM(transaction_amount) AS total_amount
                    FROM top_transaction
                    WHERE year='2023' AND quarter=1
                    GROUP BY state
                    ORDER BY total_amount DESC
                    LIMIT 10;
                    """
            df_state_value = pd.read_sql(query, engine)
            
            fig = px.bar(df_state_value, x='state', y='total_amount',
                        title='Top 10 States by Transaction Value (2023 Q1)',
                        text_auto=True, color='state')
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Insights:**
                    1. Few states drive majority of transaction value.
                    2. High population states spend more digitally.
                    3. Other states show scope for growth.
                    """)
            
            
        if f == 'Top Districts by Transaction count':
            st.header('Top Districts by Transaction count')
            
            query = """
                    SELECT state, location AS district, SUM(transaction_count) AS total_count
                    FROM top_transaction
                    WHERE year='2023' AND quarter=1 AND location_type='district'
                    GROUP BY state, district
                    ORDER BY total_count DESC
                    LIMIT 10;
                    """

            df_district_count = pd.read_sql(query, engine)
            
            fig = px.bar(df_district_count, x='district', y='total_count',
                        title='Top 10 Districts by Transaction Volume (2023 Q1)',
                        text_auto=True, color='state')
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Insights:**
                        1. Some districts dominate transaction numbers.
                        2. Semi-urban districts adopting faster.
                        3. Marketing can boost slower districts.
                    """)
            
        if f == 'Top Pincodes by Transaction amount':
            st.header('Top Pincodes by Transaction amount')
            
            query = """
                    SELECT state, location AS pincode, SUM(transaction_amount) AS total_amount
                    FROM top_transaction
                    WHERE year='2023' AND quarter=1 AND location_type='pincode'
                    GROUP BY state, pincode
                    ORDER BY total_amount DESC
                    LIMIT 10;
                    """

            df_pincode_value = pd.read_sql(query, engine)

            fig = px.bar(df_pincode_value, x='pincode', y='total_amount',
                        title='Top 10 Pincodes by Transaction Value (2023 Q1)',
                        text_auto=True, color='state')
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Insights:**
                        1. City pincodes lead in transaction value.
                        2. Rich areas spend higher per transaction.
                        3. Useful for premium offers targeting.
                    """)  
            
        if f == 'District vs Pincode Contribution (count & amout)' :
            st.header('District vs Pincode Contribution (count & amout)' )
            
            query = """
                    SELECT location_type, SUM(transaction_count) AS total_count, SUM(transaction_amount) AS total_amount
                    FROM top_transaction
                    WHERE year='2023' AND quarter=1
                    GROUP BY location_type;
                    """

            df_type = pd.read_sql(query, engine)
            
            fig_count = px.pie(df_type, names='location_type', values='total_count',
                   title='Transaction Volume: District vs Pincode (2023 Q1)')
            
            st.plotly_chart(fig_count, use_container_width=True)
            
            fig_amount = px.pie(df_type, names='location_type', values='total_amount',
                   title='Transaction Value: District vs Pincode (2023 Q1)')
            
            st.plotly_chart(fig_amount, use_container_width=True)
            
            st.markdown("""
            **Insights:**
                        1. Districts show higher transaction counts.
                        2. Pincodes show concentrated high-value spends.
                        3. Both levels give location insights.
                    """)     
            
               
        
        
    if a == 'User Registration Analysis':
        g = st.sidebar.selectbox('Select',['Which states have the most users','Which districts have the most users','Which pincodes have the most users','How registrations change over quarters in a state'])
        st.title('User Registration Analysis')
        
        
        if g == 'Which states have the most users':
            st.header('Which states have the most users')
            query1 = """
                    SELECT state, SUM(registered_users) AS reg_users
                    FROM top_user
                    WHERE year='2023' AND quarter=1
                    GROUP BY state
                    ORDER BY reg_users DESC
                    LIMIT 10;
                    """
            df_states = pd.read_sql(query1, engine)
            fig = px.bar(df_states, x='state', y='reg_users',
                        title='Top 10 States by Registered Users (2023 Q1)',
                        text_auto=True, color='state')
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Insights:**
                    1. Few states contribute the highest registrations.
                    2. High population states bring more users.
                    3. Smaller states show future growth chance.
                                        
                    """)

            
            
        if g == 'Which districts have the most users':
            st.header('Which districts have the most users')
            query2 = """
                    SELECT state, location AS district, SUM(registered_users) AS reg_users
                    FROM top_user
                    WHERE year='2023' AND quarter=1 AND location_type='district'
                    GROUP BY state, district
                    ORDER BY reg_users DESC
                    LIMIT 10;
                    """

            df_districts = pd.read_sql(query2, engine)
            
            fig = px.bar(df_districts, x='district', y='reg_users',
                        title='Top 10 Districts by Registered Users (2023 Q1)',
                        text_auto=True, color='state')
            
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Insights:**
                    1. Certain districts dominate registration counts.
                    2. Semi-urban areas show fast adoption.
                    3. Awareness needed in low-registration districts.
                    """)
            
            
        if g == 'Which pincodes have the most users':
            st.header('Which pincodes have the most users')
            query = """
                    SELECT state, location AS pincode, SUM(transaction_amount) AS total_amount
                    FROM top_transaction
                    WHERE year='2023' AND quarter=1 AND location_type='pincode'
                    GROUP BY state, pincode
                    ORDER BY total_amount DESC
                    LIMIT 10;
                    """

            df_pincode_value = pd.read_sql(query, engine)
            
            fig = px.bar(df_pincode_value, x='pincode', y='total_amount',
                        title='Top 10 Pincodes by Transaction Value (2023 Q1)',
                        text_auto=True, color='state')
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Insights:**
                        1. City pincodes lead in registrations.
                        2. Wealthy areas show more new users.
                        3. Useful for premium service targeting.
                    """)
            
        if g == 'How registrations change over quarters in a state':
            st.header('How registrations change over quarters in a state')
            query4 = """
                    SELECT year, quarter, SUM(registered_users) AS reg_users
                    FROM top_user
                    WHERE state='tamil-nadu'
                    GROUP BY year, quarter
                    ORDER BY year, quarter;
                    """

            df_trend = pd.read_sql(query4, engine)
            
            fig = px.line(df_trend, x='quarter', y='reg_users', color='year',
                            title='Quarterly Registration Trend for tamil-nadu',
                            markers=True)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Insights:**
                        1. Registrations grow steadily each quarter.
                        2. Festival seasons push more sign-ups.
                        3. Some quarters show slower adoption.
                        
                    """)        
        
        
        
       
        
        

    

    



