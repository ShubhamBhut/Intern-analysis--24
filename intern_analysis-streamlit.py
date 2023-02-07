import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns 
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.header("The Intern data analysis of NITKKR'24 batch")

st.selectbox('Please selct the branch: ', ('CSE', 'IT'))

df = pd.read_csv("cs_intern.csv").set_index("roll_number")
ge = pd.read_csv("cs_gender.csv").set_index("roll_number")
df = df.join(ge)
CGPA="CGPA"
SGPA4="SGPA"

def update_gpa(x): 
    if x == "RE":
        return 0
    else:
        return round(float(x) / 0.2) * 0.2

dfo = df.copy()
df[SGPA4] = df[SGPA4].map(update_gpa)
df[CGPA] = df[CGPA].map(update_gpa)

st.markdown(f" ##### The :blue[median SGPA] of 4th semester is :green[{df.median()[1]}]")
st.markdown(f" ##### The median CGPA is {df.median()[2]}")
st.markdown(f" ##### The median stipend is {df.median()[4]}")

st.markdown(" ##### Stipend Median is 0, that means less than 50% students has paid intern. This is horrible. Don't know who to blame here ICC, P&C department, online education or students. I would say all partially, but more goes to ICC and P&C.")

count = (df['Stipend'] > 0).sum()
st.markdown(f" ##### Count of students with paid Interns are {count}, almost {(count/df.shape[0])*100}%")

general_describe = df[['Stipend', 'CGPA', 'SGPA']].describe()
st.write(general_describe)
st.markdown(" ##### As shown above, the average stipend is 21880 and average GPA is 5.18. However the reason behind this is 0 GPA of failed student. These failed students are pulling average GPA down. That means all the passed students must have high GPA, more than 8. let's check")

df_passed = df[df['CGPA'] > 0]
passed_describe = df_passed[['Stipend', 'CGPA', 'SGPA']].describe()
st.write(passed_describe)

st.markdown(' ##### Now look, average CGPA for all passed students is 8.5. A little more competitive. Have a look at Stipend now - its almost 31000. Not bad for 2 years of JEE prep.')

st.markdown("### Now let's check from where how much stipend came")

fig = px.bar(df, y='Mode')
st.plotly_chart(fig, use_container_width=True)

fig = px.histogram(df, x='Stipend', y='Mode', histfunc='sum')
st.plotly_chart(fig, use_container_width=True)






st.markdown("## Now let's have a look on GPA's relation with Interns")
st.markdown('#### Scatter plot of CGPA vs Stipend, with Mode as color')
fig = px.scatter(df, x='CGPA', y='Stipend', color='Mode')
fig.update_traces(marker=dict(size=10, sizemode='diameter', sizeref=0.1))
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

st.markdown("""Surprizing, some students with RE has got paid internships (well I am same as well, but its different), One thing to note is that students with low GPA has higher tandency to go Offcampus, makes sense while high GPA are totally oncampus. Quite some students with good GPA has also failed to get good intern, while our MX Bot is at the top with 160k, so skills also play quite an important role.

Also check its extremely rare to have intern above 50,000 for offcampus

And to mention, that horizontal line of 65k is by Byju's so remove that 1 company and intern stats will be scrap""")

