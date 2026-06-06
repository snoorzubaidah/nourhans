import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

st.image('Sunset.png')

st.date_input("Select a date")

st.title("""Gaming and Academic Performance""")

df = pd.read_csv("clean_data.csv")
#df = pd.read_csv(upload_file)

#show data
st.subheader("Raw Data")
st.write(df)

df["Gaming Group"] = df["Gaming Hours"]

df_grouped = (df.groupby("Gaming Group")[["Sleep Hours", "Grades"]].mean().reset_index())

#Bar Chart and Line Chart
st.subheader("Gaming vs Sleep & Academic Performance")
fig = px.bar(
    df_grouped,
    x="Gaming Group",
    y="Sleep Hours",
    title="Gaming vs Sleep & Academic Performance",
    labels={
        "Gaming Group": "Daily Gaming Hours",
        "Sleep Hours": "Avg Sleep Hours",},)

fig.add_scatter(
    x=df_grouped["Gaming Group"],
    y=df_grouped["Grades"],
    name="Avg Grades",
    mode="lines+markers",
    yaxis="y2",)  # Map line to the secondary right-hand Y-axis

fig.update_layout(
    yaxis2=dict(
        title="Academic Performance (Grades)",
        overlaying="y",
        side="right",),
    hovermode="x unified",)

fig.data[0].marker.color = "#F4A261"
fig.data[1].line.color = "#1D3557"
fig.data[1].marker.color = "#1D3557"
st.plotly_chart(fig)

st.subheader("Relationship Between Study Hours and Academic Performance")

sns.set_theme(style="whitegrid")

df['Study Hours Group'] = df['Study Hours'].round().astype(int)

summary = df.groupby('Study Hours Group', observed=False)['Grades'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))

line, = ax.plot(
    summary['Study Hours Group'], 
    summary['Grades'], 
    marker='o',              
    color="#E67E22",          
    linewidth=2.5,            
    markersize=8,            
    label='Average Grade (%)')

for xval, yval in zip(summary['Study Hours Group'], summary['Grades']):
    ax.text(
        xval, 
        yval + 1.5, 
        f"{yval:.2f}%",     
        ha='center',         
        va='bottom',         
        fontweight='bold',  
        color='black',  
        fontsize=11)

ax.set_xlabel('Daily Study Hours (Hours)', fontsize=12, fontweight='bold', labelpad=10)
ax.set_ylabel('Average Grades (%)', fontsize=12, fontweight='bold')
ax.set_title('Relationship Between Study Hours and Academic Performance', fontsize=14, fontweight='bold', pad=15)

ax.set_ylim(0, 110)
ax.set_xticks(range(1, 11))

ax.legend(loc='upper left', fontsize=11, frameon=True, shadow=True)
ax.grid(True, linestyle='--', alpha=0.4)

plt.tight_layout()
st.pyplot(fig)

st.subheader("Distribution of Gaming Hours by Age Group and Gender")

df["age"] = df["Age"].astype(str)

fig = px.box(
    df,
    x="Age",
    y="Gaming Hours",
    color="Gender",
    title="Distribution of Gaming Hours by Age Group and Gender",
    labels={
        "Age": "Age Group",
        "Gaming Hours": "Gaming Hours (Daily)",
        "Gender": "Gender",},
    category_orders={
        "Age": sorted(df["Age"].unique(), key=int)},
    color_discrete_sequence=["#4A90E2", "#F4ACB7", "#E67E22"],)

fig.update_layout(
    boxmode="group",  # Essential: places the Gender boxes side-by-side for each Age
    plot_bgcolor="white",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor="#F0F0F0"),)

st.plotly_chart(fig)

st.subheader("Distribution of Study Hours by Age Group and Gender")

fig = px.box(
    df,
    x="Age",
    y="Study Hours",
    color="Gender",
    title="Distribution of Study Hours by Age Group and Gender",
    labels={
        "Age": "Age Group",
        "Study Hours": "Study Hours (Daily)",
        "Gender": "Gender",},
    category_orders={
        "Age": sorted(df["Age"].unique(), key=int)},
    color_discrete_sequence=["#4A90E2", "#F4ACB7", "#E67E22"],)

fig.update_layout(
    boxmode="group",  # Essential: places the Gender boxes side-by-side for each Age
    plot_bgcolor="white",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor="#F0F0F0"),)

st.plotly_chart(fig)

st.subheader("Comparison of Average Grades across Genders Groups")

sns.set_theme(style="whitegrid")

gender_grades = df.groupby("Gender")["Grades"].mean().reset_index()

fig, ax = plt.subplots(figsize=(8, 8))

colors = ["#F4ACB7", "#4A90E2", "#E67E22"]

wedges, texts, autotexts = ax.pie(
    gender_grades['Grades'], 
    labels=gender_grades['Gender'],

    autopct=lambda p: f"{p * sum(gender_grades['Grades']) / 100:.2f}%",
    startangle=140, 
    colors=colors,
    textprops=dict(color="black", fontweight="bold", fontsize=12),

    wedgeprops=dict(edgecolor='white', linewidth=3))

for autotext in autotexts:
    autotext.set_fontsize(11)

ax.set_title("Comparison of Average Grades across Gender Groups", fontsize=14, fontweight='bold', pad=20)
ax.legend(
    wedges, 
    gender_grades['Gender'], 
    title="Gender Group", 
    loc="center right", 
    bbox_to_anchor=(1.1, 0, 0.2, 1), 
    fontsize=11,
    title_fontsize=12,
    frameon=True,
    shadow=True)

st.pyplot(fig)