import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.header("The Intern data analysis of IT NITKKR'24 batch")

# if branch==CS, df = '' elif branch=='IT', df==

df = pd.read_csv("it_intern.csv").set_index("roll_number")
ge = pd.read_csv("it_gender.csv").set_index("roll_number")
df = df.join(ge)
CGPA = "CGPA"
SGPA4 = "SGPA"


def update_gpa(x):
    if x == "RE":
        return 0
    else:
        return round(float(x) / 0.2) * 0.2


dfo = df.copy()
df[SGPA4] = df[SGPA4].map(update_gpa)
df[CGPA] = df[CGPA].map(update_gpa)

st.write(df.median())

st.markdown("## First let's have a overview of general data")
st.markdown(f"* The :blue[median SGPA] of 4th semester is :green[{df.median()[2]}]")
st.markdown(f"* The median CGPA is {round(df.median()[3], 2)}")
st.markdown(f"* The median stipend is {df.median()[5]}")
count = (df["Stipend"] > 0).sum()
st.markdown(
    f"* Count of students with paid Interns are {count}, almost {round((count/df.shape[0])*100, 2)}%"
)

st.markdown(
    " ##### Here Stipend median is 27000, which is good. Also almost 64% students have paid internships which also good. Comparing with CS, these stats seem much better. To be honest rest branches are just terrible. God's grace I don't have their data."
)

st.markdown("### Now let's have a look at mean of data")
general_describe = df[["Stipend", "CGPA", "SGPA"]].describe()
st.markdown("###### All students description: ")
st.write(general_describe[:3])
# fig = px.box(df[df["Stipend"] > 0], x = "Stipend")
# st.plotly_chart(fig)
st.markdown(
    " As shown above, the average stipend is 36600 and average GPA is 7.66. However again, the reason behind this is 0 GPA of failed student. These failed students are pulling average GPA down. That means all the passed students must have high GPA, more than 8. let's check"
)

df_passed = df[df["CGPA"] > 0]
passed_describe = df_passed[["Stipend", "CGPA", "SGPA"]].describe()
st.markdown("###### passed students description: ")
st.write(passed_describe[:3])
st.markdown(
    " Now look, average CGPA for all passed students is 9, awesome. Competitive! Have a look at Stipend now - its 41000. Nice, though this number is also pushed by top high stipend peeps."
)

st.markdown("### Now let's check from where how much stipend came")

fig = px.bar(df, y="Mode")
st.plotly_chart(fig, use_container_width=True)

fig = px.histogram(df, x="Stipend", y="Mode", histfunc="sum")
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    " So frequency wise there is quite big gap here between Oncampus and Offcampus, but Oncampus(4.25 mil, double than CS) just destroyed Offcampus(166l, almost half than CS). Here also the reason for super low stipend by off campus is that a lot of people displaying Offcampus internships are jugaad (in relative's campany or through a relative/friend) which is unpaid."
)

st.markdown("#### Let's have a look at stats with and without these jugaad noise")
df_onCampus = df.loc[df["Mode"] == "T&P"]
st.markdown("###### All OnCampus: ")
st.write(df_onCampus[["Stipend", "CGPA", "SGPA"]].describe()[:3])
st.markdown(
    "Average Oncampus stipend is 64000, incredible, it's pushed though but still it's really good. Credits due here to ICC, TnP and students who kept GPA high"
)

df_offCampus = df.loc[df["Mode"] == "SELF"]
st.markdown("###### All OffCampus: ")
st.write(df_offCampus[["Stipend", "CGPA", "SGPA"]].describe()[:3])
st.markdown(
    "So average stipend of 42 Offcampus students is 4000. But let's check after removing jugaadis"
)

df_offCampus = df_offCampus[df_offCampus["Stipend"] > 0]
st.markdown("###### All paid OffCampus:")
st.write(df_offCampus[["Stipend", "CGPA", "SGPA"]].describe()[:3])
st.markdown(
    "Now have a look, average stipend for Offcampus is now 11000, still shit. and also only 15 students have paid Offcampus interns, so there are 27 jugaadis in IT branch."
)

st.markdown("## Now let's have a look on GPA's relation with Interns")
st.markdown("#### Scatter plot of CGPA vs Stipend, with Mode as color")
fig = px.scatter(df, x="CGPA", y="Stipend", color="Mode", opacity=0.3)
fig.update_traces(marker=dict(size=10, sizemode="diameter", sizeref=0.1))
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """Here also some students with RE have paid interns, but the stipend is peanuts compare to CS students with RE. In my opinion when recruiters don't hire based on GPA, the key thing that matter is skill then(just pointing it out here). The graph clearly shows Oncampus domination here.

Also check its Offcampus stipend are just shit here. But Oncampus is sweet.

And to mention, that horizontal line of 65k is by Byju's and line of 125k is I think of Microsoft."""
)

st.markdown("#### Bar plot of CGPA vs Stipend, with Mode as color")
fig = px.bar(df, x="CGPA", y="Stipend", color="Mode")
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    "Don't get confused, the fracrion of a bar indicated a single stipend value. A Whole bar represnts sum of all stipends for that CGPA. We don't see any bloodbath here, even tiniest rectangle of Oncampus is of 27k here. Cheers to IT peeps"
)

st.markdown(
    "#### Lineplot of CGPA vs Stipend with Mode as color and in CGPA range [8-10]"
)
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(7, 10)
ax.set_xticks(range(7, 10))
sns.set_style("darkgrid")
sns.set_palette("deep")
ax = sns.lineplot(data=df, x="CGPA", y="Stipend", hue="Mode")
st.pyplot(fig)
st.markdown(
    "Above graph is quite generalized, but still gives a lot of insight. look at uptrend,the clear rise of Stipend with GPA. Common observation says more GPA => more Stipend. So study and get GPA pal, kuchh na rakha dancing, drawing ya gaming me."
)
st.markdown(
    """Also you can use last sem GPA and analyze as it was only offlien exam, but for me personally I think people with highest GPA will have highest GPA irrespective of exam mode. And people with low GPA in online will have even worse in offline.

Also note that Offcampus has highest Stipend in range of 8.4 - 8.7, again same reason as CS. But highest Offcampus stipend here is shit compare to Oncampus donuts"""
)


st.markdown("#### Linear regression Stipend estimation")
st.markdown(
    "##### (just to understand relationship of GPA with Stipend, not for prediction)"
)
df_7to10 = df[df["CGPA"] > 7]
fig = px.scatter(df_7to10, x="CGPA", y="Stipend", trendline="ols")
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)


st.markdown("## Now let's do controversial genderwise analysis")

st.markdown(
    "One thing to keep in mind is that ratio of male to female is nearly 4:1, analysis without knowing this can be misleading"
)

df_male = df[df["gender"] == "M"]
df_female = df[df["gender"] == "F"]

st.markdown(
    f"total males with stipend > 0 are {df_male[df_male['Stipend'] > 0].count()[0]} and {100*(63/101)}% of all males"
)
st.markdown(
    f"total females with stipend > 0 are {df_female[df_female['Stipend'] > 0].count()[0]} and {100*(20/27)}% of all females"
)

st.markdown("###### All boys: ")
st.write(df_male[["Stipend", "CGPA", "SGPA"]].describe()[:3])
st.markdown("###### All girls: ")
st.write(df_female[["Stipend", "CGPA", "SGPA"]].describe()[:3])

st.markdown(
    """Here average female CGPA is better than male counterpart, so higher average stipend is seen. But compare to gap in CGPA(0.5), the gap in stipend(21k gap) is just huge. so if there is no gender bias then every 0.1 GPA = 4k. Doesn't seem very true. Let's check for only passed students"""
)

df_male_passed = df_passed[df_passed["gender"] == "M"]
df_female_passed = df_passed[df_passed["gender"] == "F"]

st.markdown("###### All passed boys: ")
st.write(df_male_passed[["Stipend", "CGPA", "SGPA"]].describe()[:3])
st.markdown("###### All passed girls: ")
st.write(df_female_passed[["Stipend", "CGPA", "SGPA"]].describe()[:3])

st.markdown(
    """Now GPA gap is only 0.2 but CGPA gap is 24,000. Interesting....

Also this mean the people who got RE in IT are mostly boys(ratio wise as well)."""
)

st.markdown("#### CGPA vs Stipend but now with gender as colors")
fig = px.bar(
    df,
    x="CGPA",
    y="Stipend",
    color="gender",
    color_discrete_sequence=px.colors.qualitative.Plotly,
)
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    "Again similar to CS. Females generally have high stipend interns. A lot of males with low stipend brought the average down. One thing I relly like about IT is that everyone has good intern, some has great, some has awesome, but everyone has good intern."
)

st.markdown("### CGPA box plots with genders as colors")
st.markdown("### All students")
fig = px.box(
    df, color="gender", y="CGPA", color_discrete_sequence=px.colors.qualitative.Plotly
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("### Passed Students")
fig = px.box(
    df_passed,
    color="gender",
    y="CGPA",
    color_discrete_sequence=px.colors.qualitative.Plotly,
)
st.plotly_chart(fig, use_container_width=True)
st.markdown(
    "As we saw previously, females have little edge with CGPA and that really paid off as good stipend"
)

st.markdown(
    "#### Lineplot of CGPA vs Stipend with Gender as color and in CGPA range [8-10]"
)
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(7, 10)
ax.set_xticks(range(7, 10))
sns.set_style("darkgrid")
sns.set_palette("deep")
ax = sns.lineplot(data=df, x="CGPA", y="Stipend", hue="gender")
st.pyplot(fig)

st.markdown(
    """Above chart again gives interesting insights, Females have almost always stayed above males irrespective of GPA except Offcampus range (8.4-8.7, it more like 9.6-8.7 here). Let's confirm these observations with other plots to look in depth"""
)

st.markdown("### Box plot of Stipends in common range of CGPA (7 to 9.2)")
df_7to10 = df[(df["CGPA"] > 7) & (df["CGPA"] < 9.2)]
fig = px.box(
    df_7to10,
    y="Stipend",
    color="gender",
    color_discrete_sequence=px.colors.qualitative.Plotly,
)
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)
st.markdown(
    "Nothing is as happy as it seems, especially for boys. Median stipend is only 5000 while for girls it is 15,000. just a little 3x gap. Also the distribution after median shows insane stipend gap."
)
st.markdown(
    "Also note that you need better GPA in order to get good stipend here as generally everyone has good GPA."
)

fig = px.box(
    df,
    x="Mode",
    y="Stipend",
    color="gender",
    color_discrete_sequence=px.colors.qualitative.Plotly,
)
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """Just like CS, the Offcampus is dominated by males, but in case of IT the vast majority of interns are Oncampus so that matters much more here. And female stipend stats have wrecked male stipend stats. Female stipend median is 75k, just insane and awesome."""
)

st.markdown(
    "We saw even bigger stipend gap here in favour of females. So does being a female helps ? let's make algorithm to decide."
)

st.markdown(
    "### Again linear regression estimation of Stipend, but this time genderwise"
)
df_7to10 = df[df["CGPA"] > 7]
fig = px.scatter(
    df_7to10,
    x="CGPA",
    y="Stipend",
    trendline="ols",
    color="gender",
    color_discrete_sequence=px.colors.qualitative.Plotly,
)
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

st.markdown("### Let's remove extreme data and then check")

df_7to10 = df[(df["CGPA"] > 7) & (df["CGPA"] < 9.6)]
fig = px.scatter(
    df_7to10,
    x="CGPA",
    y="Stipend",
    trendline="ols",
    color="gender",
    color_discrete_sequence=px.colors.qualitative.Plotly,
)
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    "Female regression line has always stayed above male line and also unlike CS, here the stipend gap is increasing with increase in CGPA."
)
st.markdown(
    "Note that it is just a simple ML algo which has worked on given data, its analysis should not be taken that seriously without human and data verification. You can try various models and mess around."
)

st.markdown("## Time for the Conclusion:")
st.markdown(
    """0. IT interns were just dominated by Oncampus and they perfomed much better than CS overall.
1. More than 64% students have paid internships so kudos to everyone ICCs, students and profs (who gave good grades lol). 
2. The students with paid internships have quite good stipend with 36k, average for passed students is 41k, good. Also IT had more average CGPA than CS. That could be a reason.
3. You can have paid internship even if you have RE, but you would have to work on your skills and there are even less chance of high stipend here. 
4. High GPA helps a ton in Oncampus and most interns are Oncampus so CGPA matters by a lot for intern at least.
5. OnCampus is great if get selected for almost all studens, have much higher stipend and Offcampus selection chances are super rare. Plus stipend sucked for IT Offcampus.
6. Generally Offcampus selected peeps are boys and with GPA range of 8.4-8.7 for previously discussed reasons, but less stipend compare to CS Offcampus students. Probably CS students are more favoured for Offcampus, but I am not from CS and still worked for me. There could also be skill issue.
7. Girls group has higher GPA, they are in much better interns with tremendous stipend gap, being a girl helps even more than CS here. A lot varies as per GPA range, here we saw Stipend gap increase in favour of girls with GPA increase.
8. Again highest stipends were secured by peeps with highest GPA, which pushed average Stipend.
9. Girls didn't shine Offcampus again, but Oncampus, they did much better than average boys, just wrecked them to be honest. Girls median stipend was 75k for Oncampus.
10. IT doesn't have anyone like MX who just crushed every other factor with his excellent skills, but if you are skilled enough, probably you can be the one next year."""
)
