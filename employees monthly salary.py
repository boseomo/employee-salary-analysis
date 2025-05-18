import pandas as pd
from scipy.stats import ttest_ind
from scipy.stats import chi2_contingency
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

file_path = r"C:\Users\mshbt\Downloads\Employee_monthly_salary.csv"
data = pd.read_csv(file_path)
print(data)
print(data.head())
print(data.describe())
print(data.isnull().sum())
print(data.info)
print(data.shape)
print(data.columns)

# Do male employees earn significantly more than female employeee?
male_salaries = data[data['Gender'] == 'M']['GROSS']
female_salaries = data[data['Gender'] == 'F']['GROSS']
# Perform t-statistic
t_stat, p_value = ttest_ind(male_salaries,female_salaries)


print("\nMale and Female Salary Comparison-----")
print("t-statistic:", t_stat)
print("P_value:", p_value)


# Interpretation
if p_value < 0.05:
    print("✅ There is a statistically significant difference in salaries between males and females.")
else:
    print("❌ No statistically significant difference found.")


# Extract male and female groups
male_data = data[data['Gender'] == 'M']
female_data = data[data['Gender'] == 'F']

# 1. Compare GROSS Salary
t_salary, p_salary = ttest_ind(male_data['GROSS'], female_data['GROSS'], nan_policy='omit')

print("\n--- Salary Comparison ---")
print("t-statistic:", t_salary)
print("p-value:", p_salary)

if p_salary < 0.05:
    print("✅ Statistically significant difference in salary between genders.")
else:
    print("❌ No statistically significant difference in salary.")

# 2. Compare AGE
t_age, p_age = ttest_ind(male_data['Age'], female_data['Age'], nan_policy='omit')

print("\n--- Age Comparison ---")
print("t-statistic:", t_age)
print("p-value:", p_age)

if p_age < 0.05:
    print("✅ Statistically significant difference in age between genders.")
else:
    print("❌ No statistically significant difference in age.")

# what is the relation between gender and leadership roles in the organization?

leadership_titles = ['Manager', 'Head', 'Lead', 'Supervisor', 'Director']

# Normalize designation column
data['Designation'] = data['Designation'].str.strip().str.title()

# Create a new column: 'Leadership' = Yes or No
data['Leadership'] = data['Designation'].apply(lambda x: 'Yes' if any(title in x for title in leadership_titles) else 'No')
table = pd.crosstab(data['Gender'], data['Leadership'])
print(table)

chi2, p, dof, expected = chi2_contingency(table)

print("Chi2 Statistic:", chi2)
print("p-value:", p)

if p < 0.05:
    print("✅ Significant relationship between gender and leadership roles.")
else:
    print("❌ No significant relationship between gender and leadership roles.")

sns.countplot(data=data, x='Leadership', hue='Gender')
plt.title('Leadership Roles by Gender')
plt.show()

# what is the relation between age and leadership roles in the organization?
leadership_titles = ['Manager', 'Head', 'Lead', 'Supervisor', 'Director']

# Clean and classify
data['Designation'] = data['Designation'].str.strip().str.title()
data['Leadership'] = data['Designation'].apply(lambda x: 'Yes' if any(title in x for title in leadership_titles) else 'No')

leaders = data[data['Leadership'] == 'Yes']['Age']
non_leaders = data[data['Leadership'] == 'No']['Age']
from scipy.stats import ttest_ind

t_stat, p_value = ttest_ind(leaders, non_leaders, nan_policy='omit')

print("t-statistic:", t_stat)
print("p-value:", p_value)

if p_value < 0.05:
    print("✅ There is a statistically significant difference in age between leaders and non-leaders.")
else:
    print("❌ No statistically significant difference in age.")

sns.boxplot(data=data, x='Leadership', y='Age')
plt.title('Age Distribution by Leadership Role')
plt.show()

# Are Data Scientiests getting paid significantly more than others in this company?

# Standardize case for matching
data['Designation'] = data['Designation'].str.strip().str.title()
# Group 1: Data Scientists
ds_salary = data[data['Designation'] == 'Data Scientist']['GROSS']

# Group 2: All others
others_salary = data[data['Designation'] != 'Data Scientist']['GROSS']

t_stat, p_value = ttest_ind(ds_salary, others_salary, nan_policy='omit')

print("t-statistic:", t_stat)
print("p-value:", p_value)

if p_value < 0.05:
    print("✅ Data Scientists are paid significantly more than others.")
else:
    print("❌ No significant difference in pay for Data Scientists.")

# Does the salary depend on Age
# Create a simplified role column
data['Is_Data_Scientist'] = data['Designation'].apply(lambda x: 'Data Scientist' if x == 'Data Scientist' else 'Others')

sns.boxplot(data=data, x='Is_Data_Scientist', y='GROSS')
plt.title('GROSS Salary: Data Scientist vs Others')
plt.show()

correlation = data['Age'].corr(data['GROSS'])
print("Correlation between Age and Salary:", correlation)


sns.regplot(x='Age', y='GROSS', data=data)
plt.title('Relationship Between Age and Salary')
plt.xlabel('Age')
plt.ylabel('Gross Salary')
plt.show()


X = data['Age']
y = data['GROSS']

# Add constant for intercept
X = sm.add_constant(X)

model = sm.OLS(y, X).fit()
print(model.summary())

import pandas as pd
from scipy.stats import ttest_ind, chi2_contingency

# Example results (replace with your actual test results)
results = {
    'Salary_vs_Gender': {'t_stat': 8.97, 'p_value': 7.13e-19, 'significant': True},
    'Age_vs_Gender': {'t_stat': 7.19, 'p_value': 9.44e-13, 'significant': True},
    'Gender_vs_Leadership': {'chi2_stat': 10.5, 'p_value': 0.0012, 'significant': True},
    # Add more...
}

# Convert dicts to DataFrames for easier saving
salary_gender_df = pd.DataFrame([results['Salary_vs_Gender']])
age_gender_df = pd.DataFrame([results['Age_vs_Gender']])
gender_leadership_df = pd.DataFrame([results['Gender_vs_Leadership']])

with pd.ExcelWriter('hypothesis_results.xlsx', engine='openpyxl') as writer:
    salary_gender_df.to_excel(writer, sheet_name='Salary vs Gender', index=False)
    age_gender_df.to_excel(writer, sheet_name='Age vs Gender', index=False)
    gender_leadership_df.to_excel(writer, sheet_name='Gender vs Leadership', index=False)

print("Employees Ananlysis save successfully")

import os
print(os.getcwd())

