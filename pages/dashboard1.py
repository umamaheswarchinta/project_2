import streamlit as st
import polars as pl
from streamlit_echarts import st_echarts, JsCode
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np



# Page Configuration
st.set_page_config(
    page_title="",
    page_icon=":material/bar_chart:",
    layout="wide",
    
)


# --- DATA LOADING ---
@st.cache_data
def get_dataset():
    df = pl.read_csv("data/European_Bank.csv", encoding="latin1")
    return df


df = get_dataset()

st.title(":material/bar_chart: Churn Analytics")




# --- SIDEBAR: Filters + Info ---
with st.sidebar:
    
    selected_geography = st.selectbox(
        "Geography", options=["Spain","Germany","France"]
    )
    selected_age = st.selectbox(
        "Age", options=
    ["<30", "30-45", "46-60", "60+"]
    )

    selected_credit_score = st.selectbox(
        "CreditScore", options=
    ["Low", "Medium", "High"]
    )

    selected_tenure = st.selectbox(
        "Tenure", options=
        ["New", "Mid-Term", "Long-Term"]
    )

    selected_balance = st.selectbox(
        "Balance", options=
        ["Zero", "Low", "High"]
    )


# --- FILTER LOGIC ---


# 2. Categorical Filtering
def apply_categorical_filters(base_df,geography, age, credit_score, tenure, balance):
    filtered = base_df
    if geography:
        if (geography == "Spain"):
            filtered = filtered.filter(pl.col("Geography") == "Spain")
        elif (geography == "Germany"):
            filtered = filtered.filter(pl.col("Geography") == "Germany")
        elif (geography == "France"):
            filtered = filtered.filter(pl.col("Geography") == "France")
    if age:
        if (age == "<30"):
            filtered = filtered.filter(pl.col("Age") < 30)
        elif (age == "30-45"):
            filtered = filtered.filter(pl.col("Age").is_between(30,45))
        elif (age == "46-60"):
            filtered = filtered.filter(pl.col("Age").is_between(45,60))
        elif (age == "60+"):
            filtered = filtered.filter(pl.col("Age") > 60)
    if credit_score:
        if (credit_score == "Low"):
            filtered = filtered.filter(pl.col("CreditScore").is_between(300,600))
        elif (credit_score == "Medium"):
            filtered = filtered.filter(pl.col("CreditScore").is_between(600,700))
        elif (credit_score == "High"):
            filtered = filtered.filter(pl.col("CreditScore").is_between(750,900))


    if tenure:
        if (tenure == "New"):
            filtered = filtered.filter(pl.col("Tenure").is_between(1,2))
        elif (tenure == "Mid-Term"):
            filtered = filtered.filter(pl.col("Tenure").is_between(2,5))
        elif (tenure == "Long-Term"):
            filtered = filtered.filter(pl.col("Tenure") > 5)

    if balance:
        if (balance == "Zero"):
            filtered = filtered.filter(pl.col("Balance") == 0)
        elif (balance == "Low"):
            filtered = filtered.filter(pl.col("Balance").is_between(500,5000))
        elif (balance == "High"):
            filtered = filtered.filter(pl.col("Balance") > 5000)
    return filtered


current_df = apply_categorical_filters(
    df,
    selected_geography,
    selected_age,
    selected_credit_score,
    selected_tenure,
    selected_balance

)






# ==========================================
# ROW 1: KPIs (4 metrics)
# ==========================================
def get_kpis(data):
    if data is None or data.is_empty():
        return pl.DataFrame(
            {
                "overallchurn_rate": 0,
                
            }
        )
    overall_churn = data.filter(pl.col("Exited") == 1).height
    Total = data.height
    Final = (overall_churn/Total)
    return pl.DataFrame(
        {
            "overallchurn_rate": Final
            
        }
    )


current_kpis = get_kpis(current_df)
over_all_churn_rate = get_kpis(df)


result = df.group_by("Geography").len()

Germany_count = result[0][0].row()[1]
France_count = result[1][0].row()[1]
Spain_count = result[2][0].row()[1]


high_value = (df["EstimatedSalary"] > 100000).len()

churn_1 = (df["Exited"] == 1).len()

engagement_drop = df.filter((df["IsActiveMember"] == 0) & (df["Exited"] == 1)).height
#col1,col2,col3,col4 = st.columns(4)
st.set_page_config(initial_sidebar_state="collapsed")
with st.container(horizontal=True,border=False):
    val = over_all_churn_rate.row(0)[0] * 100
    st.metric(
        "Over All Churn",
        f"{val:,.1f}%",
        border=True,
        height=150,
        width=140
    )
    val1 = current_kpis.row(0)[0] * 100
    st.metric(
        "Current KPI",
        f"{val1:,.1f}%",
        border=True,
        height=150,
        width=140
    )
    st.metric(
        "High Value Churn",
        f"{high_value/churn_1:,.2f}%",
        border=True,
        height=150,
        width=150
    )


    st.markdown("""
    <style>
    [data-testid="stMetricLabel"] {
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)

    
    with st.container(horizontal=True,border=True,width=200,height=150):
        
        st.write(f"Germany Total : {Germany_count}")
    
        st.write(f"France Total : {France_count}")
        
        st.write(f"Spain Total : {Spain_count}")

    st.metric(
        "Engagement Drop",
        f"{engagement_drop/churn_1:,.2f}%",
        border=True,
        height=150,
        width=160
    )


df1 = df
df2 = df

geo_group = df1.select("Geography", "Exited")

geo_gender = df2.select("Geography", "Gender", "Exited")


geo_group1 = geo_group.group_by('Geography').sum()

geo_group2 = geo_gender











#hello = df.group_by("Age").agg(pl.col("Age") < 30).count()




age_1st_group = df.filter(pl.col("Age") < 30).height

age_2nd_group = df.filter(pl.col("Age").is_between(30,46)).height

age_3rd_group = df.filter(pl.col("Age").is_between(46,60)).height

age_4th_group = df.filter(pl.col("Age") > 60).height


Total_age_groups = age_1st_group + age_2nd_group + age_3rd_group + age_4th_group

age_1st_group_perc = (age_1st_group/Total_age_groups)*100
age_2nd_group_perc = (age_2nd_group/Total_age_groups)*100
age_3rd_group_perc = (age_3rd_group/Total_age_groups)*100
age_4th_group_perc = (age_4th_group/Total_age_groups)*100



df_age_perc_label = ["age < 30","age 30-45","age 46-60","age >60"]
df_age_perc_value = [age_1st_group_perc,age_2nd_group_perc,age_3rd_group_perc,age_4th_group_perc]





tab1, tab2, tab3, tab4 = st.tabs(["Geography-wise churn visualization", "Age churn comparison", "Tenure churn comparison","High-value customer churn explorer"])

# 2. Add content to the first tab
with tab1:
    fig = px.bar(geo_group2, x="Geography", y="Exited", title="Churn among Geography")


    fig.update_layout(clickmode="event+select")

    click = st.plotly_chart(fig,on_select="rerun")

    if click and click["selection"]["points"]:
        @st.dialog("Example",width="large")
        def some_function():
            selected_geography = click["selection"]["points"][0]["x"]
            st.subheader(f"some thing: {selected_geography}")
            df_filtered = geo_group2.filter(pl.col("Geography") == selected_geography)
            result = df_filtered.group_by("Gender").agg(
                pl.col("Exited").sum()
            ) 
            #df_filtered1 = df_filtered.groupby("Gender").count()
            #df_filtered2 = df_filtered1["Gender"]
            new_chart = px.bar(

                result,
                x="Gender",
                y="Exited",
                title="some thing",
                text_auto=True


            )

            new_chart.update_traces(width=0.5) 

            st.plotly_chart(new_chart)

        some_function()

# 3. Add content to the second tab
with tab2:
    age_fig = px.pie(labels=df_age_perc_label,values=df_age_perc_value,title='Age wise churn percentage',hover_name=df_age_perc_label)


    st.plotly_chart(age_fig)


# 4. Add content to the third tab
with tab3:
    df_tenure = df.group_by("Tenure").agg(
    pl.col("Exited").filter(pl.col("Exited") == 1).sum().alias("sum_high_values")
    )
    tenure_fig = px.line(df_tenure["sum_high_values"])
    st.plotly_chart(tenure_fig)

    

with tab4:
    df = pd.DataFrame(np.random.random((1000,10)), columns=[f'Col{i}' for i in range(10)])
    fig, ax = plt.subplots()
    sns.heatmap(df.corr(), annot=False)
    
    st.pyplot(fig)

