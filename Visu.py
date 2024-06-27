import pandas as pd

job_postings = pd.read_csv('Datasets//postings.csv') #1

benefits = pd.read_csv('Datasets//Benefits.csv') #2
companies = pd.read_csv('Datasets//companies.csv') #3
company_industries = pd.read_csv('Datasets//company_industries.csv') #5
employee_counts = pd.read_csv('Datasets//employee_counts.csv') #4
job_industries = pd.read_csv('Datasets//job_industries.csv')
job_skills = pd.read_csv('Datasets//job_skills.csv')

industries = pd.read_csv('Datasets//industries.csv')
salaries = pd.read_csv('Datasets//salaries.csv')
skills = pd.read_csv('Datasets//skills.csv')

merged_jobs = pd.merge(job_postings, benefits, on='job_id', how='left')

merged_companies = pd.merge(companies, employee_counts, on='company_id', how='left')
comprehensive_data_one_to_one = pd.merge(merged_jobs, merged_companies, on='company_id', how='left')
# #-------------------------------------CleanData-------------------------------------
missing_data = comprehensive_data_one_to_one.isnull().sum()

# Display columns with significant missing data
significant_missing_columns = missing_data[missing_data > 0].sort_values(ascending=False)
cols_fill_not_specified = ['skills_desc', 'type', 'pay_period', 'currency', 'compensation_type', 'posting_domain',
                           'application_url', 'formatted_experience_level', 'company_size', 'zip_code', 'address',
                           'state', 'url', 'city', 'country', 'name']
for col in cols_fill_not_specified:
    comprehensive_data_one_to_one[col].fillna("Not Specified", inplace=True)

# Fill numerical columns with zeros
cols_fill_zero = ['applies', 'views', 'follower_count', 'employee_count']
for col in cols_fill_zero:
    comprehensive_data_one_to_one[col].fillna(0, inplace=True)

# Fill remote_allowed with "Unknown"
comprehensive_data_one_to_one['remote_allowed'].fillna("Unknown", inplace=True)

# For salary columns, we'll leave NaNs for now and handle them during specific analyses
# Similarly, for other columns with missing values, we'll address them based on the context of the analysis

# Check remaining missing values
remaining_missing = comprehensive_data_one_to_one.isnull().sum()
remaining_missing_cols = remaining_missing[remaining_missing > 0].sort_values(ascending=False)
# Use "Still Open" for closed_time
comprehensive_data_one_to_one['closed_time'].fillna("Still Open", inplace=True)

# Use "Unknown" for inferred
comprehensive_data_one_to_one['inferred'].fillna("Unknown", inplace=True)

# Use "Not Specified" for company description
comprehensive_data_one_to_one['description_y'].fillna("Not Specified", inplace=True)

# Check for remaining missing values
remaining_missing = comprehensive_data_one_to_one.isnull().sum()
remaining_missing_cols = remaining_missing[remaining_missing > 0].sort_values(ascending=False)
comprehensive_data_one_to_one['description_x'].fillna("Not Specified", inplace=True)

# Remove duplicate rows
comprehensive_data_cleaned = comprehensive_data_one_to_one.drop_duplicates()

#---------------Merge
# Merging benefits with the comprehensive dataset to get work type and salary information
merged_with_benefits = pd.merge(comprehensive_data_cleaned, benefits, on='job_id', how='left')
comprehensive_data_with_industries = pd.merge(comprehensive_data_cleaned, company_industries, on='company_id', how='left')
industries_skills = pd.merge(job_industries, job_skills, on='job_id', how='left')
FinalData = pd.merge(comprehensive_data_with_industries, industries_skills, on='job_id', how='left')
print(FinalData.columns)
print(FinalData.isnull().sum())
print(FinalData.shape[0])

