import functools
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


def app():
    header = st.container()
    dataset = st.container()

    
    with header:
        st.title("Administration and Finance Executive Dashboard :bar_chart:")
        
       
    with dataset:
        faculty_df = pd.read_excel('data/studentdb.xlsx', sheet_name = 'faculty')
        student_df = pd.read_excel('data/studentdb.xlsx', sheet_name = 'students')
        mask = (student_df['Enrollment_Date'] > '2021-1-1') & (student_df['Enrollment_Date'] <= '2022-02-02')
        curr_student_df = student_df.loc[mask]
        
        st.markdown("### Key Metrics:")

        m1, m2, m3 = st.columns(3)

        m1.metric(label = "Currently Enrolled Students",
                value = len(curr_student_df.value_counts()))

        m2.metric(label = "University Scholars",
                value = curr_student_df.University_Scholar.value_counts().Yes)
        
        m3.metric(label = "Students with Loans",
                value = curr_student_df.Student_Loan.value_counts().Yes)


        st.markdown("### Visualizations: ")
        g1, g2 = st.columns((1,1))
        
        college_dist = pd.DataFrame(curr_student_df['College'].value_counts())
        college_dist = college_dist.reset_index()
        college_dist = college_dist.head(15)
        college_dist.columns = ['College', 'count']
        fig = px.pie(college_dist, values = 'count', names = "College")
        g1.markdown("##### College distribution of currently enrolled students:")
        g1.plotly_chart(fig, use_container_width=True)
        
        
        g2.markdown("##### Faculty by department:")
        faculty_dist = pd.DataFrame(faculty_df[['Department', 'Type']].value_counts())
        #g2.bar_chart(faculty_dist, 0, 400, use_container_width=True)
        
        faculty_dist = faculty_dist.reset_index()
        faculty_dist['type_count'] = faculty_dist.groupby('Type')['Type'].transform('count')
        faculty_dist['count'] = faculty_dist.groupby('Department')['Department'].transform('count')
        # st.write(faculty_dist)
        fig = px.bar(faculty_dist, x="Department", y="count", color="Type")
        g2.plotly_chart(fig, use_container_width=True)


        student_df['Enrollment_Date'] = pd.to_datetime(student_df['Enrollment_Date']).dt.strftime('%Y-%m-%d')
        student_df = student_df.sort_values(by='Enrollment_Date', ascending=True)
        st.write(student_df)
        
        course_options = student_df['Course'].unique().tolist()

        # date_options = student_df['Enrollment_Date'].unique().tolist()
        # date = st.selectbox('Which date would you like to see?', date_options, 100)
        student_df['count'] = student_df.groupby('Course')['Course'].transform('count')
        course = st.multiselect('Which courses would you like to see?', course_options, ['BS Computer Science'])

        student_df = student_df[student_df['Course'].isin(course)]
        # student_df = student_df[student_df['Enrollment_Date']<date]

        fig2 = px.bar(student_df, x='Course', y='count', color='Course', animation_frame="Enrollment_Date", animation_group="Course")
        fig2.update_layout(width=800)
        st.write(fig2)
