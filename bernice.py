import pandas as pd
import matplotlib.pyplot as plt

# By Bernice
# Get Number of Job post over a period of time
def getNumJobsPostingOverTime(excelName):
    excelName = excelName+'.xlsx'
    data = pd.read_excel(excelName)
    data['Post Time'] = pd.to_datetime(data['Post Time'])

    # Group the data by the posting date and count the number of job postings per day
    job_posting_counts = data.groupby(data['Post Time'].dt.date)['Job Title'].count()

    # Create a time series plot
    plt.figure(figsize=(12, 6))
    plt.plot(job_posting_counts.index, job_posting_counts.values, marker='o', linestyle='-')
    plt.xlabel('Posting Date')
    plt.ylabel('Number of Job Postings')
    plt.title('Number of Job Postings Over Time')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.grid(True)  # Add grid lines
    plt.tight_layout()  # Ensure the labels fit within the figure
    # if (excelName == 'SEJobs.xlsx'):
    #     plt.savefig('Software Engineer job post over time.jpg')
    # elif (excelName == 'ISJobs.xlsx'):
    #     plt.savefig('Information Security job post over time.jpg')
    plt.show()
# --------------------------------------------------------------------------------------------------------

# By Bernice
# Get top 10 company with the most job posting
def getTop10CompanyofMostPost(excelName,top_n):
    # Load dataset
    excelName = excelName + '.xlsx'
    data = pd.read_excel(excelName)

    # count the frequency of each company
    company_counts = data['Company Name'].value_counts()

    # Set the number of top companies you want to display
    #top_n = 10  # adjust this number as needed

    # Select the top N companies
    top_companies = company_counts.head(top_n)

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    top_companies.plot(kind='barh')  # Use 'barh' for a horizontal bar chart
    plt.xlabel('Number of Job Postings')
    plt.ylabel('Company Name')
    plt.title(f'Top {top_n} Companies with Most Job Postings')
    plt.gca().invert_yaxis()  # Invert the y-axis for better readability
    plt.tight_layout()
    # if (excelName == 'SEJobs.xlsx'):
    #     plt.savefig('Top 10 Companies hiring SE.jpg')
    # elif (excelName == 'ISJobs.xlsx'):
    #     plt.savefig('Top 10 Companies hiring IS.jpg')
    plt.show()
# --------------------------------------------------------------------------------------------------------
