import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import psycopg2
import json

# ---------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------
st.set_page_config(
    page_title="PhonePe Pulse Dashboard",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Cache the engine itself so a brand-new DB connection isn't opened on every rerun
@st.cache_resource
def get_engine():
    return create_engine(
        "postgresql+psycopg2://phonepe_azst_user:cqDPwTuKyebyTKZsDk2wof1y37ngovSK@dpg-d9bhnm7aqgkc739e2fc0-a.singapore-postgres.render.com/phonepe_azst"
    )

engine = get_engine()

# Cache query results for a few minutes
@st.cache_data(ttl=600, show_spinner="Fetching data...")
def run_query(query):
    return pd.read_sql(query, engine)

# Small helper so every table gets a one-click CSV download button.
@st.cache_data
def to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

st.title("📱 PhonePe Pulse Dashboard")
st.caption("Interactive exploration of PhonePe transaction, insurance and user data")
st.divider()

b = st.sidebar.selectbox('Select', ['Home', 'Scenario'])

if b == 'Home':  
    data = st.selectbox("EXPLORE DATA", ['PAYMENT', 'INSURANCE'])
    
    if data == 'PAYMENT':
        x = st.selectbox('Select', ['transaction', 'user'])
        
        if x == 'transaction':
            # Corrected query logic for standard aggregates
            summary_query = """
                SELECT 
                    SUM(transaction_amount) AS overall_transaction_amount,
                    AVG(transaction_amount) AS avg_transaction_amount
                FROM top_transaction;
            """
            summary_df = run_query(summary_query)

            st.subheader("All States Transactions Summary")
            m1, m2 = st.columns(2)
            
            # Handling potential None values safely
            val1 = summary_df['overall_transaction_amount'][0] if pd.notna(summary_df['overall_transaction_amount'][0]) else 0
            val2 = summary_df['avg_transaction_amount'][0] if pd.notna(summary_df['avg_transaction_amount'][0]) else 0
            
            m1.metric("Overall Transaction Amount", f"₹{val1:,.0f}")
            m2.metric("Average Transaction Amount", f"₹{val2:,.0f}")
                        
            st.title("Top 10 Transactions Insights")
            option = st.selectbox("Select View", ["Districts", "Postal codes", "States"])

            if option == "Districts":
                query = """
                    SELECT state, location AS district, 
                        SUM(transaction_count) AS total_transaction_count,
                        SUM(transaction_amount) AS total_transaction_amount
                    FROM top_transaction
                    WHERE location_type = 'district'
                    GROUP BY state, location
                    ORDER BY total_transaction_amount DESC
                    LIMIT 10;
                """
                df = run_query(query)
                st.subheader("Top 10 Districts - Transactions")
                st.dataframe(df, use_container_width=True)
                st.download_button("⬇️ Download CSV", to_csv(df), file_name="districts_transactions.csv", mime="text/csv", key="dl_districts_transactions")

            elif option == "Postal codes":
                query = """
                    SELECT state, location AS pincode, 
                        SUM(transaction_count) AS total_transaction_count,
                        SUM(transaction_amount) AS total_transaction_amount
                    FROM top_transaction
                    WHERE location_type = 'pincode'
                    GROUP BY state, location
                    ORDER BY total_transaction_amount DESC
                    LIMIT 10;
                """
                df = run_query(query)
                st.subheader("Top 10 Pincodes - Transactions")
                st.dataframe(df, use_container_width=True)
                st.download_button("⬇️ Download CSV", to_csv(df), file_name="pincodes_transactions.csv", mime="text/csv", key="dl_pincodes_transactions")

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
                df = run_query(query)
                st.subheader("Top 10 States - Transactions")
                st.dataframe(df, use_container_width=True)
                st.download_button("⬇️ Download CSV", to_csv(df), file_name="states_transactions.csv", mime="text/csv", key="dl_states_transactions")
            
            query_quarter = """
                            SELECT year, quarter, 
                            SUM(transaction_amount) AS total_amount
                            FROM aggregated_transaction
                            GROUP BY year, quarter
                            ORDER BY year, quarter;
                            """
            df_quarter = run_query(query_quarter)
            df_quarter['Period'] = df_quarter['year'].astype(str) + "-Q" + df_quarter['quarter'].astype(str)

            yc, qc = st.columns(2)
            year_list = sorted(df_quarter['year'].astype(str).unique().tolist())
            selected_year = yc.selectbox("Select Year", year_list, key="txn_map_year")

            quarter_options = sorted(
                df_quarter.loc[df_quarter['year'].astype(str) == selected_year, 'quarter']
                .astype(str).unique().tolist()
            )
            selected_q = qc.selectbox("Select Quarter", quarter_options, key="txn_map_quarter")

            selected_quarter = f"{selected_year}-Q{selected_q}"
            st.write("You selected:", selected_quarter)

            query_map = f"""
                        SELECT state, SUM(transaction_amount) AS total_amount
                        FROM aggregated_transaction
                        WHERE CAST(year AS VARCHAR) = '{selected_year}' AND CAST(quarter AS VARCHAR) = '{selected_q}'
                        GROUP BY state;
                        """
            df_map = run_query(query_map)
            df_map["state"] = df_map["state"].str.replace("-", " ").str.title()
                
            india_geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

            fig = px.choropleth(
                        df_map,
                        geojson=india_geojson_url,
                        featureidkey="properties.ST_NM",
                        locations="state",
                        color="state",
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        hover_name="state",
                        hover_data=["total_amount"],
                        title=f"Transaction Amounts - {selected_quarter}"
                    )
            fig.update_geos(fitbounds="locations", visible=True)
            st.plotly_chart(fig, use_container_width=True)
            
        if x == 'user':
            summary_query = "SELECT SUM(registered_users) AS overall_registered_users FROM top_user;"
            summary_df = run_query(summary_query)

            st.subheader("All States Users Summary")
            val_u = summary_df['overall_registered_users'][0] if pd.notna(summary_df['overall_registered_users'][0]) else 0
            st.metric("Overall Registered Users", f"{val_u:,.0f}")

            st.title("Top 10 Users Insights")
            option = st.selectbox("Select View", ["Districts", "Postal code", "States"])

            if option == "Districts":
                query = """
                    SELECT state, location AS district, SUM(registered_users) AS total_registered_users
                    FROM top_user
                    WHERE location_type = 'district'
                    GROUP BY state, location
                    ORDER BY total_registered_users DESC
                    LIMIT 10;
                """
                df = run_query(query)
                st.subheader("Top 10 Districts - Registered Users")
                st.dataframe(df, use_container_width=True)
                st.download_button("⬇️ Download CSV", to_csv(df), file_name="districts_users.csv", mime="text/csv", key="dl_districts_users")

            elif option == "Postal code":
                query = """
                    SELECT state, location AS pincode, SUM(registered_users) AS total_registered_users
                    FROM top_user
                    WHERE location_type = 'pincode'
                    GROUP BY state, location
                    ORDER BY total_registered_users DESC
                    LIMIT 10;
                """
                df = run_query(query)
                st.subheader("Top 10 Pincodes - Registered Users")
                st.dataframe(df, use_container_width=True)
                st.download_button("⬇️ Download CSV", to_csv(df), file_name="pincodes_users.csv", mime="text/csv", key="dl_pincodes_users")

            else:
                query = """
                    SELECT state, SUM(registered_users) AS total_registered_users
                    FROM top_user
                    GROUP BY state
                    ORDER BY total_registered_users DESC
                    LIMIT 10;
                """
                df = run_query(query)
                st.subheader("Top 10 States - Registered Users")
                st.dataframe(df, use_container_width=True)
                st.download_button("⬇️ Download CSV", to_csv(df), file_name="states_users.csv", mime="text/csv", key="dl_states_users")
            
            # Map fixing for column case sensitivity
            query_quarter = """
                            SELECT year, quarter, state,
                                SUM("registeredUsers") AS total_users,
                                SUM("appOpens") AS total_appopens
                            FROM map_user
                            GROUP BY year, quarter, state
                            ORDER BY year, quarter, state;
                            """
            df_quarter = run_query(query_quarter)
            df_quarter["Period"] = df_quarter["year"].astype(str) + "-Q" + df_quarter["quarter"].astype(str)

            yc, qc = st.columns(2)
            year_list = sorted(df_quarter['year'].astype(str).unique().tolist())
            selected_year = yc.selectbox("Select Year", year_list, key="user_map_year")

            quarter_options = sorted(
                df_quarter.loc[df_quarter['year'].astype(str) == selected_year, 'quarter']
                .astype(str).unique().tolist()
            )
            selected_q = qc.selectbox("Select Quarter", quarter_options, key="user_map_quarter")

            selected_quarter = f"{selected_year}-Q{selected_q}"
            st.write("You selected:", selected_quarter)

            df_map = df_quarter[
                (df_quarter["year"].astype(str) == selected_year) &
                (df_quarter["quarter"].astype(str) == selected_q)
            ].copy()

            df_map["state"] = df_map["state"].str.replace("-", " ").str.title()
            india_geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

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
            fig.update_geos(fitbounds="locations", visible=True)
            st.plotly_chart(fig, use_container_width=True)

    if data == 'INSURANCE': 
        summary_query = """
            SELECT 
                SUM(insurance_amount) AS overall_insurance_amount,
                AVG(insurance_amount) AS avg_insurance_amount
            FROM top_insurance;
        """
        summary_df = run_query(summary_query)

        st.subheader("All States Insurance Summary")
        m1, m2 = st.columns(2)
        val_i1 = summary_df['overall_insurance_amount'][0] if pd.notna(summary_df['overall_insurance_amount'][0]) else 0
        val_i2 = summary_df['avg_insurance_amount'][0] if pd.notna(summary_df['avg_insurance_amount'][0]) else 0
        
        m1.metric("Overall Insurance Amount", f"₹{val_i1:,.0f}")
        m2.metric("Average Insurance Amount", f"₹{val_i2:,.0f}")
        
        st.title("Top 10 Insurance Insights")
        option = st.selectbox("Select View", ["Districts", "Postal code", "States"])

        if option == "Districts":
            query = """
                SELECT state, location AS district, 
                    SUM(insurance_count) AS total_insurance_count,
                    SUM(insurance_amount) AS total_insurance_amount
                FROM top_insurance
                WHERE location_type = 'district'
                GROUP BY state, location
                ORDER BY total_insurance_amount DESC
                LIMIT 10;
            """
            df = run_query(query)
            st.subheader("Top 10 Districts - Insurance")
            st.dataframe(df, use_container_width=True)
            st.download_button("⬇️ Download CSV", to_csv(df), file_name="districts_insurance.csv", mime="text/csv", key="dl_districts_insurance")

        elif option == "Postal code":
            query = """
                SELECT state, location AS pincode, 
                    SUM(insurance_count) AS total_insurance_count,
                    SUM(insurance_amount) AS total_insurance_amount
                FROM top_insurance
                WHERE location_type = 'pincode'
                GROUP BY state, location
                ORDER BY total_insurance_amount DESC
                LIMIT 10;
            """
            df = run_query(query)
            st.subheader("Top 10 Pincodes - Insurance")
            st.dataframe(df, use_container_width=True)
            st.download_button("⬇️ Download CSV", to_csv(df), file_name="pincodes_insurance.csv", mime="text/csv", key="dl_pincodes_insurance")

        else:
            query = """
                SELECT state, 
                    SUM(insurance_count) AS total_insurance_count,
                    SUM(insurance_amount) AS total_insurance_amount
                FROM top_insurance
                GROUP BY state
                ORDER BY total_insurance_amount DESC
                LIMIT 10;
            """
            df = run_query(query)
            st.subheader("Top 10 States - Insurance")
            st.dataframe(df, use_container_width=True)
            st.download_button("⬇️ Download CSV", to_csv(df), file_name="states_insurance.csv", mime="text/csv", key="dl_states_insurance")
        
        query_quarter = """
                        SELECT year, quarter,
                            SUM("Insurance_amount") AS total_ins_amount,
                            SUM("Insurance_count") AS total_ins_count
                        FROM aggregated_insurance
                        GROUP BY year, quarter
                        ORDER BY year, quarter;
                        """
        df_quarter = run_query(query_quarter)
        df_quarter['Period'] = df_quarter['year'].astype(str) + "-Q" + df_quarter['quarter'].astype(str)

        yc, qc = st.columns(2)
        year_list = sorted(df_quarter['year'].astype(str).unique().tolist())
        selected_year = yc.selectbox("Select Year", year_list, key="ins_map_year")

        quarter_options = sorted(
            df_quarter.loc[df_quarter['year'].astype(str) == selected_year, 'quarter']
            .astype(str).unique().tolist()
        )
        selected_q = qc.selectbox("Select Quarter", quarter_options, key="ins_map_quarter")

        selected_quarter = f"{selected_year}-Q{selected_q}"
        st.write("You selected:", selected_quarter)

        query_map = f"""
                    SELECT state,
                        AVG("Insurance_amount") AS avg_ins_amount,
                        SUM("Insurance_amount") AS total_ins_amount,
                        SUM("Insurance_count") AS total_ins_count
                    FROM aggregated_insurance
                    WHERE CAST(year AS VARCHAR) = '{selected_year}' AND CAST(quarter AS VARCHAR) = '{selected_q}'
                    GROUP BY state;
                """
        df_map = run_query(query_map)
        df_map["state"] = df_map["state"].str.replace("-", " ").str.title()

        india_geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

        fig = px.choropleth(
                df_map,
                geojson=india_geojson_url,
                featureidkey="properties.ST_NM",
                locations="state",
                color="state",   
                color_discrete_sequence=px.colors.qualitative.Set3,
                title=f"Insurance Overview - {selected_quarter}",
                hover_data=["total_ins_amount", "total_ins_count", "avg_ins_amount"]
            )
        fig.update_geos(fitbounds="locations", visible=True)
        st.plotly_chart(fig, use_container_width=True)

if b == 'Scenario':
    a = st.sidebar.selectbox('Scenario',['Decoding Transaction Dynamics on PhonePe','Device Dominance and User Engagement Analysis','Insurance Transactions Analysis','Transaction Analysis Across States and Districts','User Registration Analysis'])

    if a == 'Decoding Transaction Dynamics on PhonePe':
        c = st.sidebar.selectbox('Select',['Top States by Transaction Amount','Quarterly Transaction Trend (All India)','Transaction Amount Share by Type','State vs Transaction Type'])
        st.title("Decoding Transaction Dynamics on PhonePe")
        
        if c == 'Top States by Transaction Amount':
            st.header("Top States by Transaction Amount")
            query_state = """
                        SELECT state, 
                        SUM(transaction_count) AS total_count, 
                        SUM(transaction_amount) AS total_amount
                        FROM aggregated_transaction
                        GROUP BY state
                        ORDER BY total_amount DESC;
                        """
            df_state = run_query(query_state)

            fig = px.bar(df_state, x="state", y="total_amount", title="Top States by Transaction Amount", text="total_amount", color="total_amount", color_continuous_scale="Blues")
            fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)

        if c == 'Quarterly Transaction Trend (All India)':
            st.header('Quarterly Transaction Trend (All India)')
            query_quarter = "SELECT year, quarter, SUM(transaction_amount) AS total_amount FROM aggregated_transaction GROUP BY year, quarter ORDER BY year, quarter;"
            df_quarter = run_query(query_quarter)
            df_quarter['Period'] = df_quarter['year'].astype(str) + "-Q" + df_quarter['quarter'].astype(str)

            fig = px.line(df_quarter, x="Period", y="total_amount", title="Quarterly Transaction Trend (All India)", markers=True)
            st.plotly_chart(fig, use_container_width=True)

        if c == 'Transaction Amount Share by Type':
            st.header('Transaction Amount Share by Type')
            query_type = "SELECT transaction_type, SUM(transaction_amount) AS total_amount FROM aggregated_transaction GROUP BY transaction_type ORDER BY total_amount DESC;"
            df_type = run_query(query_type)
            
            fig = px.pie(df_type, values="total_amount", names="transaction_type", title="Transaction Amount Share by Type")   
            st.plotly_chart(fig, use_container_width=True)
            
        if c == 'State vs Transaction Type':
            st.header('State vs Transaction Type')
            query_heatmap = "SELECT state, transaction_type, SUM(transaction_amount) AS total_amount FROM aggregated_transaction GROUP BY state, transaction_type ORDER BY total_amount DESC;"
            df_heatmap = run_query(query_heatmap)
            
            fig = px.bar(df_heatmap, x="state", y="total_amount", color="transaction_type", title="State vs Transaction Type", barmode="stack")
            fig.update_layout(xaxis={'categoryorder':'total descending'})
            st.plotly_chart(fig, use_container_width=True)

    if a == 'Device Dominance and User Engagement Analysis':
        d = st.sidebar.selectbox('Select',['which mobile brand has the most registered users','high registration but low engagement','Which brands are popular in each state','how brand usage changes across years/quarters'])
        st.title("Device Dominance and User Engagement Analysis")
        
        if d == 'which mobile brand has the most registered users':
            st.header("which mobile brand has the most registered users")
            query_brand_share = "SELECT install_mobile_brand, SUM(reg_user_brand) AS total_users FROM aggregated_user GROUP BY install_mobile_brand ORDER BY total_users DESC;"
            df_brand = run_query(query_brand_share)
            fig = px.pie(df_brand, names="install_mobile_brand", values="total_users", title="Device Brand Share (Registered Users)")
            st.plotly_chart(fig, use_container_width=True)
            
        if d == 'high registration but low engagement':
            st.header('high registration but low engagement')
            query_engagement = "SELECT install_mobile_brand, SUM(reg_user_brand) AS reg_users, SUM(\"appOpens\") AS total_app_opens FROM aggregated_user GROUP BY install_mobile_brand ORDER BY reg_users DESC;"
            df_engagement = run_query(query_engagement)
            fig = px.scatter(df_engagement, x="reg_users", y="total_app_opens", size="reg_users", color="install_mobile_brand", text="install_mobile_brand", title="Device Engagement")
            st.plotly_chart(fig, use_container_width=True)

        if d == 'Which brands are popular in each state':
            st.header('Which brands are popular in each state')
            query_region = "SELECT state, install_mobile_brand, SUM(reg_user_brand) AS reg_users FROM aggregated_user GROUP BY state, install_mobile_brand ORDER BY state, reg_users DESC;"
            df_region = run_query(query_region)
            fig = px.bar(df_region, x="state", y="reg_users", color="install_mobile_brand", title="Region-wise Device Usage", barmode="stack")
            fig.update_layout(xaxis={'categoryorder':'total descending'})
            st.plotly_chart(fig, use_container_width=True)
            
        if d == 'how brand usage changes across years/quarters':
            st.header('how brand usage changes across years/quarters')
            query_trend = "SELECT year, quarter, install_mobile_brand, SUM(reg_user_brand) AS reg_users FROM aggregated_user GROUP BY year, quarter, install_mobile_brand ORDER BY year, quarter;"
            df_trend = run_query(query_trend)
            df_trend['Period'] = df_trend['year'].astype(str) + "-Q" + df_trend['quarter'].astype(str)
            fig = px.line(df_trend, x="Period", y="reg_users", color="install_mobile_brand", title="Device Usage Trend Over Time", markers=True)
            st.plotly_chart(fig, use_container_width=True)

    if a == 'Insurance Transactions Analysis':
        e = st.sidebar.selectbox('Select',['Top 10 States by Insurance Amount','Top 10 Districts by Insurance Count','Top 10 Pincodes by Insurance Amount','Insurance Amount Growth by Year-Quarter'])
        st.title('Insurance Transactions Analysis')
        
        if e == 'Top 10 States by Insurance Amount':
            st.header('Top 10 States by Insurance Amount')
            query1 = "SELECT state, SUM(insurance_amount) AS total_amount FROM top_insurance GROUP BY state ORDER BY total_amount DESC LIMIT 10;"
            state_data = run_query(query1)
            fig1 = px.bar(state_data, x="state", y="total_amount", text="total_amount", title="Top 10 States by Insurance Amount", color="total_amount")
            st.plotly_chart(fig1, use_container_width=True)
            
        if e == 'Top 10 Districts by Insurance Count':
            st.header('Top 10 Districts by Insurance Count')
            query2 = "SELECT location AS district, SUM(insurance_count) AS total_count FROM top_insurance WHERE location_type = 'district' GROUP BY location ORDER BY total_count DESC LIMIT 10;"
            district_data = run_query(query2)
            fig2 = px.bar(district_data, x="district", y="total_count", text="total_count", title="Top 10 Districts by Insurance Count", color="total_count")
            st.plotly_chart(fig2, use_container_width=True)
            
        if e == 'Top 10 Pincodes by Insurance Amount':
            st.header('Top 10 Pincodes by Insurance Amount')
            query3 = "SELECT location AS pincode, SUM(insurance_amount) AS total_amount FROM top_insurance WHERE location_type = 'pincode' GROUP BY location ORDER BY total_amount DESC LIMIT 10;"
            pincode_data = run_query(query3)
            fig3 = px.pie(pincode_data, names="pincode", values="total_amount", title="Top 10 Pincodes by Insurance Amount", hole=0.4)
            st.plotly_chart(fig3, use_container_width=True)
            
        if e == 'Insurance Amount Growth by Year-Quarter':
            st.header('Insurance Amount Growth by Year-Quarter')
            query4 = "SELECT year, quarter, SUM(insurance_amount) AS total_amount FROM top_insurance GROUP BY year, quarter ORDER BY year, quarter;"
            trend_data = run_query(query4)
            trend_data["year_quarter"] = trend_data["year"].astype(str) + "-Q" + trend_data["quarter"].astype(str)
            fig4 = px.line(trend_data, x="year_quarter", y="total_amount", markers=True, title="Insurance Amount Growth by Year-Quarter")
            st.plotly_chart(fig4, use_container_width=True)

    if a == 'Transaction Analysis Across States and Districts':
        f = st.sidebar.selectbox('Select',['where transactions are concentrated (high engagement)','Top States by Transaction amount','Top Districts by Transaction count','Top Pincodes by Transaction amount','District vs Pincode Contribution (count & amout)'])
        st.title('Transaction Analysis Across States and Districts')
        
        if f == 'where transactions are concentrated (high engagement)':
            st.header('where transactions are concentrated (high engagement)')
            query = "SELECT state, SUM(transaction_count) AS total_count FROM top_transaction WHERE CAST(year AS VARCHAR)='2023' AND quarter=1 GROUP BY state ORDER BY total_count DESC LIMIT 10;"
            df_state_count = run_query(query)
            fig = px.bar(df_state_count, x='state', y='total_count', title='Top 10 States by Transaction Volume (2023 Q1)', text_auto=True, color='state')
            st.plotly_chart(fig, use_container_width=True)
            
        if f == 'Top States by Transaction amount':
            st.header('Top States by Transaction amount')
            query = "SELECT state, SUM(transaction_amount) AS total_amount FROM top_transaction WHERE CAST(year AS VARCHAR)='2023' AND quarter=1 GROUP BY state ORDER BY total_amount DESC LIMIT 10;"
            df_state_value = run_query(query)
            fig = px.bar(df_state_value, x='state', y='total_amount', title='Top 10 States by Transaction Value (2023 Q1)', text_auto=True, color='state')
            st.plotly_chart(fig, use_container_width=True)
            
        if f == 'Top Districts by Transaction count':
            st.header('Top Districts by Transaction count')
            query = "SELECT state, location AS district, SUM(transaction_count) AS total_count FROM top_transaction WHERE CAST(year AS VARCHAR)='2023' AND quarter=1 AND location_type='district' GROUP BY state, location ORDER BY total_count DESC LIMIT 10;"
            df_district_count = run_query(query)
            fig = px.bar(df_district_count, x='district', y='total_count', title='Top 10 Districts by Transaction Volume (2023 Q1)', text_auto=True, color='state')
            st.plotly_chart(fig, use_container_width=True)
            
        if f == 'Top Pincodes by Transaction amount':
            st.header('Top Pincodes by Transaction amount')
            query = "SELECT state, location AS pincode, SUM(transaction_amount) AS total_amount FROM top_transaction WHERE CAST(year AS VARCHAR)='2023' AND quarter=1 AND location_type='pincode' GROUP BY state, location ORDER BY total_amount DESC LIMIT 10;"
            df_pincode_value = run_query(query)
            fig = px.bar(df_pincode_value, x='pincode', y='total_amount', title='Top 10 Pincodes by Transaction Value (2023 Q1)', text_auto=True, color='state')
            st.plotly_chart(fig, use_container_width=True)
            
        if f == 'District vs Pincode Contribution (count & amout)':
            st.header('District vs Pincode Contribution (count & amout)')
            query = "SELECT location_type, SUM(transaction_count) AS total_count, SUM(transaction_amount) AS total_amount FROM top_transaction WHERE CAST(year AS VARCHAR)='2023' AND quarter=1 GROUP BY location_type;"
            df_type = run_query(query)
            
            fig_count = px.pie(df_type, names='location_type', values='total_count', title='Transaction Volume: District vs Pincode (2023 Q1)')
            st.plotly_chart(fig_count, use_container_width=True)
            
            fig_amount = px.pie(df_type, names='location_type', values='total_amount', title='Transaction Value: District vs Pincode (2023 Q1)')
            st.plotly_chart(fig_amount, use_container_width=True)

    if a == 'User Registration Analysis':
        g = st.sidebar.selectbox('Select',['Which states have the most users','Which districts have the most users','Which pincodes have the most users','How registrations change over quarters in a state'])
        st.title('User Registration Analysis')
        
        if g == 'Which states have the most users':
            st.header('Which states have the most users')
            query1 = "SELECT state, SUM(registered_users) AS reg_users FROM top_user WHERE CAST(year AS VARCHAR)='2023' AND quarter=1 GROUP BY state ORDER BY reg_users DESC LIMIT 10;"
            df_states = run_query(query1)
            fig = px.bar(df_states, x='state', y='reg_users', title='Top 10 States by Registered Users (2023 Q1)', text_auto=True, color='state')
            st.plotly_chart(fig, use_container_width=True)

        if g == 'Which districts have the most users':
            st.header('Which districts have the most users')
            query2 = "SELECT state, location AS district, SUM(registered_users) AS reg_users FROM top_user WHERE CAST(year AS VARCHAR)='2023' AND quarter=1 AND location_type='district' GROUP BY state, location ORDER BY reg_users DESC LIMIT 10;"
            df_districts = run_query(query2)
            fig = px.bar(df_districts, x='district', y='reg_users', title='Top 10 Districts by Registered Users (2023 Q1)', text_auto=True, color='state')
            st.plotly_chart(fig, use_container_width=True)
            
        if g == 'Which pincodes have the most users':
            st.header('Which pincodes have the most users')
            query = "SELECT state, location AS pincode, SUM(transaction_amount) AS total_amount FROM top_transaction WHERE CAST(year AS VARCHAR)='2023' AND quarter=1 AND location_type='pincode' GROUP BY state, location ORDER BY total_amount DESC LIMIT 10;"
            df_pincode_value = run_query(query)
            fig = px.bar(df_pincode_value, x='pincode', y='total_amount', title='Top 10 Pincodes by Transaction Value (2023 Q1)', text_auto=True, color='state')
            st.plotly_chart(fig, use_container_width=True)
            
        if g == 'How registrations change over quarters in a state':
            st.header('How registrations change over quarters in a state')
            query4 = "SELECT year, quarter, SUM(registered_users) AS reg_users FROM top_user WHERE state='tamil-nadu' GROUP BY year, quarter ORDER BY year, quarter;"
            df_trend = run_query(query4)
            fig = px.line(df_trend, x='quarter', y='reg_users', color='year', title='Quarterly Registration Trend for tamil-nadu', markers=True)
            st.plotly_chart(fig, use_container_width=True)