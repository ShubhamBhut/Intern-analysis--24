import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns 
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.header("The Intern data analysis of CS NITKKR'24 batch")

#if branch==CS, df = '' elif branch=='IT', df==

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

st.markdown("## First let's have a overview of general data")
st.markdown(f"* The :blue[median SGPA] of 4th semester is :green[{df.median()[1]}]")
st.markdown(f"* The median CGPA is {round(df.median()[2], 2)}")
st.markdown(f"* The median stipend is {df.median()[4]}")
count = (df['Stipend'] > 0).sum()
st.markdown(f"* Count of students with paid Interns are {count}, almost {round((count/df.shape[0])*100, 2)}%")

st.markdown(" ##### Stipend Median is 0, that means less than 50% students has paid intern. This is horrible. Don't know who to blame here ICC, P&C department, online education or students. I would say all partially, but more goes to ICC and P&C.")

st.markdown("### Now let's have a look at mean of data")
general_describe = df[['Stipend', 'CGPA', 'SGPA']].describe()
st.markdown("###### All students description: ")
st.write(general_describe[:3])
#fig = px.box(df[df["Stipend"] > 0], x = "Stipend")
#st.plotly_chart(fig)
st.markdown(" As shown above, the average stipend is 21880 and average GPA is 5.18. However the reason behind this is 0 GPA of failed student. These failed students are pulling average GPA down. That means all the passed students must have high GPA, more than 8. let's check")

df_passed = df[df['CGPA'] > 0]
passed_describe = df_passed[['Stipend', 'CGPA', 'SGPA']].describe()
st.markdown("###### passed students description: ")
st.write(passed_describe[:3])
st.markdown(' Now look, average CGPA for all passed students is 8.5. A little more competitive. Have a look at Stipend now - its almost 31000. Not bad for 2 years of JEE prep.')

st.markdown("### Now let's check from where how much stipend came")

fig = px.bar(df, y='Mode')
st.plotly_chart(fig, use_container_width=True)

fig = px.histogram(df, x='Stipend', y='Mode', histfunc='sum')
st.plotly_chart(fig, use_container_width=True)

st.markdown(" So frequency wise oncampus and offcampus are quite same, but oncampus(22.5 mil) brought a ton of more stipend than offcampus(300k), if you think offcampus is just grabage, let me clear this for you. The reason for super low stipend by off campus is that a lot of people displaying offcampus internships are jugaad (in relative's campany or through a relative/friend) which is unpaid.")

st.markdown("#### Let's have a look at stats with and without these jugaad noise")
df_onCampus = df.loc[df['Mode'] == "T&P"]
st.markdown("###### All OnCampus: ")
st.write(df_onCampus[['Stipend', 'CGPA', 'SGPA']].describe()[:3])
st.markdown(" It seems that Stipend wise oncampus is a much better option with average Stipend around 44000. I will be honest, there are some factors which has pushed this number, but stil oncampus stipend is good.")

df_offCampus = df.loc[df['Mode'] == "SELF"]
st.markdown("###### All OffCampus: ")
st.write(df_offCampus[['Stipend', 'CGPA', 'SGPA']].describe()[:3])
st.markdown("It seems total offcampus internships are 40 with mean Stipend 7500. Total shit, but let's look after removing these jugaadis.")

df_offCampus = df_offCampus[df_offCampus['Stipend'] > 0]
st.markdown("###### All paid OffCampus:")
st.write(df_offCampus[['Stipend', 'CGPA', 'SGPA']].describe()[:3])
st.markdown("Now have a look, average stipend for offcampus is now 37500, not bad. But look at frequency(count), only 8 people have offcampus paid internships, that means around 32 people in CS are jugaadi, shameful. Also it requires skills to get offcampus paid intern.")

st.markdown("## Now let's have a look on GPA's relation with Interns")
st.markdown('#### Scatter plot of CGPA vs Stipend, with Mode as color')
fig = px.scatter(df, x='CGPA', y='Stipend', color='Mode', opacity=0.4)
fig.update_traces(marker=dict(size=10, sizemode='diameter', sizeref=0.1))
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

st.markdown("""Surprizing, some students with RE has got paid internships (well I am same as well, but its different), One thing to note is that students with low GPA has higher tandency to go Offcampus, makes sense while high GPA are totally oncampus. Quite some students with good GPA has also failed to get good intern, while our MX Bot is at the top with 160k, so skills also play quite an important role.

Also check its extremely rare to have intern above 50,000 for offcampus

And to mention, that horizontal line of 65k is by Byju's so remove that 1 company and intern stats will be scrap""")

st.markdown("#### Bar plot of CGPA vs Stipend, with Mode as color")
fig = px.bar(df, x="CGPA", y="Stipend", color="Mode")
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

st.markdown("Don't get confused, the fracrion of a bar indicated a single stipend value. A Whole bar represnts sum of all stipends for that CGPA. Look at range of stipends varying with CGPA, at 9.2 you have mostly good stipends, while RE and 8.4 is bloodbath")

st.markdown("#### Lineplot of CGPA vs Stipend with Mode as color and in CGPA range [8-10]")
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(7,10)
ax.set_xticks(range(7,10))
sns.set_style("darkgrid")
sns.set_palette("deep")
ax = sns.lineplot(data=df, x='CGPA', y='Stipend', hue='Mode')
st.pyplot(fig)
st.markdown("Above graph is quite generalized, but still gives a lot of insight. look at uptrend, rise of Stipend with GPA. Now look at the slope after 9.4. After 9.4, the probability of good intern is excellent. So study and get GPA pal, kuchh na rakha dancing, drawing ya gaming me.")
st.markdown("""Also you can use last sem GPA and analyze as it was only offlien exam, but for me personally I think people with highest GPA will have highest GPA irrespective of exam mode. And people with low GPA in online will have even worse in offline.

Also note that offcampus has highest Stipend in range of 8.4 - 8.7, that means of campus companies don't care that much about GPA compare to skills and mostly skilled pople can have this range of GPA cause they spent more time in coding than mugging, while they are smart, so still GPA stays above 8.4""")

st.markdown("#### Linear regression Stipend estimation")
st.markdown("##### (just to understand relationship of GPA with Stipend, not for prediction)")
df_7to10 = df[df['CGPA'] > 7]
fig = px.scatter(df_7to10, x="CGPA", y="Stipend", trendline="ols")
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)


st.markdown("## Now let's do controversial genderwise analysis")

st.markdown("One thing to keep in mind is that ratio of male to female is nearly 4:1, analysis without knowing this can be misleading")

df_male = df[df['gender'] == 'M']
df_female = df[df['gender'] == 'F']

st.markdown(f"total males with stipend > 0 are {df_male[df_male['Stipend'] > 0].count()[0]} and {100*(41/92)}% of all males")
st.markdown(f"total females with stipend > 0 are {df_female[df_female['Stipend'] > 0].count()[0]} and {100*(16/25)}% of all females")

st.markdown("###### All boys: ")
st.write(df_male[['Stipend', 'CGPA', 'SGPA']].describe()[:3])
st.markdown("###### All girls: ")
st.write(df_female[['Stipend', 'CGPA', 'SGPA']].describe()[:3])
st.markdown("""Surprisingly average CGPA is higher in males still average stipend is higher in females. Also percentage wise stats are a lot better in females. Let's try to find reasons behind this""")

df_male_passed = df_passed[df_passed['gender'] == 'M']
df_female_passed = df_passed[df_passed['gender'] == 'F']

st.markdown("###### All passed boys: ")
st.write(df_male_passed[['Stipend', 'CGPA', 'SGPA']].describe()[:3])
st.markdown("###### All passed girls: ")
st.write(df_female_passed[['Stipend', 'CGPA', 'SGPA']].describe()[:3])
st.markdown("""Still better CGPA in males, also increase in female stipend is more than increase in male stipend.

As we know, mean can pe affected by a couple of extreme inputs. So let's check if there is anything like this hered. Also here our previous insight regarding higher CGPA means higher stipend seems to be wrong, let's study this as well""")

st.markdown("#### CGPA vs Stipend but now with gender as colors")
fig = px.bar(df, x="CGPA", y="Stipend", color="gender", color_discrete_sequence=px.colors.qualitative.Plotly)
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

st.markdown("so a lot of low stipend interns are by males and female intern's are generally with good stipend. So its a general case, there is no push by extreme cases. Even against our thinking, extreme cases of high stipend are pushing male average stipend, otherwise it would be even lower.")
st.markdown("But what could be the reason behind this ? let's see if most females have high GPA and that helped while some females failed and that brought overall GPA down to male average")

st.markdown("### CGPA box plots with genders as colors")
st.markdown("### All students")
fig = px.box(df, color="gender", y='CGPA', color_discrete_sequence=px.colors.qualitative.Plotly)
st.plotly_chart(fig, use_container_width=True)
st.markdown("### Passed Students")
fig = px.box(df_passed, color="gender", y='CGPA', color_discrete_sequence=px.colors.qualitative.Plotly)
st.plotly_chart(fig, use_container_width=True)
st.markdown("Nah, GPA is almost same in case of both genders, sure highest GPA is by a male and lowest by a female; but median and rest student's distribution is almost same")

st.markdown("### Box plot of Stipends in common range of CGPA (7 to 9)")
df_7to10 = df[(df['CGPA'] > 7) & (df['CGPA'] < 9)]
fig = px.box(df_7to10,  y="Stipend", color='gender', color_discrete_sequence=px.colors.qualitative.Plotly)
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)
st.markdown("Nothing is as happy as it seems, especially for boys. Median stipend is 0 while for girls it is 30,000. Also the distribution after median shows insane stipend gap is, boys q3 is same as girls median.")
st.markdown("Also note that you need better GPA in order to get good stipend here as generally everyone has good GPA.")

st.markdown("#### Lineplot of CGPA vs Stipend with Gender as color and in CGPA range [8-10]")
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(7,10)
ax.set_xticks(range(7,10))
sns.set_style("darkgrid")
sns.set_palette("deep")
ax = sns.lineplot(data=df, x='CGPA', y='Stipend', hue='gender')
st.pyplot(fig)

st.markdown("""Above chart again made a lot of things clear. Look the range of off campus (8.4-8.7), there males have lot higher Stipend compare to females and also females with GPA range of 9-9.4 has same stipend as males with above 9.6. Interesting .....

Still let's confirm it with other plots to be safe""")

fig = px.box(df, x="Mode", y="Stipend", color="gender", color_discrete_sequence=px.colors.qualitative.Plotly)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""Look, out of 8 offcampus jobs atleast 5 are by males and 2 of them have nice stipend while females have totally struggled there. In case of Oncampus, you would see bigger blue shape and say males seem to have better condition, but nope! Some highest GPA holders and most skilled males have pushed it (As we saw previously) like, compare the mean and median. Despite have extreme cases on male data, still males are struggling in mean and median, which are real indicators when it comes to compering groups.""")

st.markdown("We still haven't found any reason behind higher stipend in females despite low GPA and sttruggle in offcampus(that can indicate skills tbh). So does being a female helps ? let's make algorithm to decide.")

st.markdown("### Again linear regression estimation of Stipend, but this time genderwise")
df_7to10 = df[df['CGPA'] > 7]
fig = px.scatter(df_7to10, x="CGPA", y="Stipend", trendline="ols", color='gender', color_discrete_sequence=px.colors.qualitative.Plotly)
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

st.markdown("### Let's remove extreme data and then check")

df_7to10 = df[(df['CGPA'] > 7) & (df['CGPA'] < 9.6)]
fig = px.scatter(df_7to10, x="CGPA", y="Stipend", trendline="ols", color='gender', color_discrete_sequence=px.colors.qualitative.Plotly)
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

st.markdown("From above examples we can see that above 9.6 section is owned by males, but except these 2-4 students; females have always stayed above males and more ahead as GPA has decreased according to regression model. It seems to make sense as we saw in data.")
st.markdown("Note that it is just a simple ML algo which has worked on given data, its analysis should not be taken that seriously without human and data verification. You can try various models and mess around.")

st.markdown("## Time for the Conclusion:")
st.markdown("""1. More than 50% students doesn't have paid internship, just shameful. No idea what ICC and T&P were doing.
2. The students with paid internships have quite good stipend with 30k average for passed students
3. You can have paid internship even if you have RE, but you would have to work on your skills and there are less chance of high stipend. 
4. High GPA helps a lot in Oncampus, while it has no impact in offcampus
5. OnCampus is great if get selected for almost all studens, have mostly higher stipend and Offcampus selection chancesare super rare.
6. Generally Offcampus selected peeps are boys and with GPA range of 8.4-8.7 for previously discussed reasons.
7. Though girls group has low GPA, they still are in much better intern, so being a girl definately helps by a lot. A lot varies as per GPA range
8. Highest stipend were secured by peeps with highest GPA, almost all boys, which pushed average stipend of boys data.
9. Girls didn't shine offcampus, but Oncampus, they did much better than avverage boys, couldn't find reasons except gender.
10. None of the above rules applied on MX (his nickname) who secured highest stipend with 8.6 GPA, offcampus and as a boy. Reason - skills (and a little bit of luck); so if you are extremely high skilled, you would end up somewhere nice.
""")

