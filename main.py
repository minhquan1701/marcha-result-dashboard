import pandas as pd
import plotly.express as px
import streamlit as st



# --- Read Datasource ---
df = pd.read_excel(
    io='data.xlsx',
    engine='openpyxl',
    sheet_name='Dataset',
    skiprows=0,
    nrows=700,
    usecols='A:J'
)


# Initialize Streamlit app
st.set_page_config(page_title="Campaign Dashboard",
                   page_icon=":bar_chart:",
                   
                   layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.header("Add your filter: ")
schools = st.sidebar.multiselect(
    "Select schools: ",
    options=df["University - Name Cleaned"].unique(),
    default=df["University - Name Cleaned"].unique()
)

majors = st.sidebar.multiselect(
    "Select majors: ",
    options=df["Major - Cleaned"].unique(),
    default=df["Major - Cleaned"].unique()
)


df_selection = df.query(
    "University == @schools & Major == @majors"
)

# --- Main Page ---

st.title(":bar_chart: Competition Metric Dashboard")
st.markdown("##")

avg_score = round(df["Result"].mean(), 2)
avg_time_completed = round(df["Time Completed"].mean(), 2)
total_contestants = df["Result"].count()


left_col, middle_col, right_col = st.columns(3)

with left_col:
    # st.subheader("Average Scores: ")
    # st.subheader(f"{avg_score} / 100")
    st.metric(label="Average Score", value=f"{avg_score} / 100")


with middle_col:
    # st.subheader("Average Time Completed: ")
    # st.subheader(
    #     f"{round(avg_time_completed // 60)} min {round(avg_time_completed % 60)}s")
    st.metric(label="Average Time Completion", value=f"{round(avg_time_completed // 60)} min {round(avg_time_completed % 60)}s")

with right_col:
    # st.subheader("Total Contestants: ")
    # st.subheader(f"{total_contestants}")
    st.metric(label="Total Contestants", value=f"{total_contestants}")


st.markdown("---")  # section break


# --- Chart Visualization

# Average scores by schools
avg_scr_by_schools = df_selection.groupby(
    by=["University - Name Cleaned"]).mean()[["Result"]].sort_values(by="Result")


fig_avg_scr_by_schools = px.bar(
    avg_scr_by_schools,
    x="Result",
    y=avg_scr_by_schools.index,
    labels={
        "Result": "Average Score",
        "University - Name Cleaned": "University",

    },
    orientation="h",
    title="<b>Average Score by University</b>",
    color_discrete_sequence=["#0083B8"] *
    len(avg_scr_by_schools),  # set color to the bar
    template="plotly_white",
    width=800, height=1200

)


# st.plotly_chart(fig_avg_scr_by_schools)

# Major Distribution

majors_dist = df.groupby(by=["Major - Cleaned"])[
    'Major - Cleaned'].count().reset_index(name="Quant")

fig_major_dist = px.pie(
    majors_dist,
    values="Quant",
    names="Major - Cleaned",
    labels={
        "Major - Cleaned": "Major",
        "Quant" : "Quantity"

    },

    title="<b>Major Distribution</b>",
    width=800, height=800

)
fig_major_dist.update_traces(textposition='inside')
fig_major_dist.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

left_col, right_col = st.columns(2)
left_col.plotly_chart(fig_avg_scr_by_schools, use_container_width=True)
right_col.plotly_chart(fig_major_dist, use_container_width=True)
