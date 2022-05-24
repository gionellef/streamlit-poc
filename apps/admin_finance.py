import functools
from pathlib import Path
from turtle import color

import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    header = st.container()
    dataset = st.container()

    
    with header:
        st.title("Administration and Finance Executive Dashboard :bar_chart:")
        
       
    with dataset:
        student_df = pd.read_excel('data/studentdb.xlsx', sheet_name = 'students')
        demog_df = pd.read_excel('data/studentdb.xlsx', sheet_name = 'demographic')
        project_df = pd.read_excel('data/financedb.xlsx', sheet_name = 'Projects')
        payroll_df = pd.read_excel('data/financedb.xlsx', sheet_name = 'payroll_summary')
        
        st.markdown("### Key Metrics:")

        m1, m2, m3 = st.columns(3)

        m1.metric(label = "Total Current UPM Employees",
                value = len(student_df.value_counts()))

        m2.metric(label = "Job Order Staff",
                value = student_df.University_Scholar.value_counts().Yes)
        
        m3.metric(label = "Permanent Staff",
                value = student_df.Student_Loan.value_counts().Yes)


        st.markdown("### Visualizations: ")
        g1, g2 = st.columns((1,1))
        
        total_spending = pd.DataFrame(demog_df[['Year', 'Infrastructure', 'PGH', 'Payroll', 'Utilities']])
        total_spending = total_spending.reset_index()

        fig = px.line(total_spending,  x='Year', y=["Infrastructure", "PGH", 'Payroll', 'Utilities'], labels={"value": "Amount in millions"})

        g1.markdown("##### UPM Spending:")
        g1.plotly_chart(fig, use_container_width=True)
        
        
        project_df = pd.DataFrame(project_df[["R&D Spend", "Administration", "Marketing Spend", "State", "Profit"]])
        fig2 = px.bar(project_df, x='State', y=["R&D Spend", "Administration", "Marketing Spend", "Profit"], barmode='group', labels={"State": "College", "value": "Amount"})
        g2.markdown("##### Financial Breakdown:")
        g2.plotly_chart(fig2, use_container_width=True)


        ### Salary slider
        payroll_df = pd.DataFrame(payroll_df[["Designation", "Gross Salary", "Deduction Amount", "Net Pay", "Pay Hike Amount", "Incentive"]])
        salary = st.slider ('Salary filter', 0, 1000000, 1)

        payroll_df = payroll_df[payroll_df['Gross Salary'] <= salary]
        st.write(payroll_df)
        