import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Machine Learning Highlights", page_icon="🤖", layout="wide")
# Add your logo at the top of the page
# st.image("fdLogo.png", width =200)  # Adjust the width as needed

st.image("fdLogo.png")

# Hide the Streamlit header and footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Title of the page
st.title("Machine Learning Highlights")

# Infographic styled highlights
st.header("Key Highlights of fintastic Datas Machine Learning services")

# Display highlights in columns using KPI widgets
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Growth in Data", value="44 Zettabytes", delta="Exponential Growth")
    st.write("Machine learning thrives on data. The volume of data generated is growing exponentially each year.")

with col2:
    st.metric(label="Algorithm Advancements", value="100+ New Algorithms", delta="Yearly")
    st.write("Algorithms are becoming more sophisticated, allowing for better predictions and insights.")

with col3:
    st.metric(label="Computational Power", value="10x Increase", delta="Last 5 Years")
    st.write("With the rise of powerful GPUs and TPUs, machine learning models can be trained faster than ever.")

# Another row of highlights
col4, col5, col6 = st.columns(3)
with col4:
    st.metric(label="Real-World Applications", value="Every Industry")
    st.write("Machine learning is being applied across various industries, from healthcare to finance to retail.")

with col5:
    st.metric(label="Automation and Efficiency", value="70% Tasks Automated", delta="Increasing")
    st.write("ML models automate repetitive tasks, leading to increased efficiency and productivity.")

with col6:
    st.metric(label="AI and Ethics", value="Ongoing Research")
    st.write("As machine learning advances, it is important to consider the ethical implications and ensure fair use.")

# Highlight some stats with charts
st.header("Interesting Statistics")

# Static bar chart example
st.subheader("Investment in AI and ML (in Billion $)")
investment_data = {
    'Year': ['2016', '2017', '2018', '2019', '2020', '2021'],
    'Investment': [12, 15, 20, 24, 30, 35]
}
investment_df = pd.DataFrame(investment_data)

fig = px.bar(investment_df, x='Year', y='Investment', text='Investment', color='Investment', 
             color_continuous_scale=px.colors.sequential.Plasma)

fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# Static pie chart example
st.subheader("Popular ML Algorithms")
algorithm_data = {
    'Algorithm': ['Linear Regression', 'Decision Trees', 'SVM', 'Neural Networks', 'K-Means'],
    'Usage': [25, 20, 15, 30, 10]
}
algorithm_df = pd.DataFrame(algorithm_data)

fig2 = px.pie(algorithm_df, names='Algorithm', values='Usage', title='Usage of ML Algorithms',
              color_discrete_sequence=px.colors.sequential.RdBu)

st.plotly_chart(fig2, use_container_width=True)

# Footer with a call to action
st.write("---")
st.header("Learn More About Machine Learning")
st.write("Machine learning is a rapidly evolving field with countless opportunities. Explore more to stay ahead in this exciting domain.")
st.button("Explore More", on_click=lambda: st.write("Visit [our website](https://yourwebsite.com) for more information."))

# Footer link
st.write("---")
st.write("[Explore More >](https://yourwebsite.com)")
