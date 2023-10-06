import pandas as pd
import matplotlib.pyplot as plt

# By Andrea
# Save scrapped data into an excel
def excelConveter(jobTitles, jobPTimes, jobLevel, jobCompany, jobQuali, jobLocation, jobSkill,jobURLList,fileName):
    # creating excel headers
    columns = ['Job Title', 'Post Time', 'Job Level', 'Company Name', 'Qualifications','Location', 'Skills','Job URL']
    # Creating dataframe for pandas to convert into excel
    df = pd.DataFrame(list(zip(jobTitles, jobPTimes, jobLevel, jobCompany, jobQuali,jobLocation, jobSkill, jobURLList)), columns=columns)
    # Convert dataframe into excel
    newfileName = fileName + ".xlsx"
    df.to_excel(newfileName,index=False)
# --------------------------------------------------------------------------------------------------------

# By Andrea
# Get job count by location
def getJobCountOfLocation(excelName):

    # State file name to be read
    excelName = excelName + '.xlsx'

    # Convert excel to dataframe
    data = pd.read_excel(excelName)

    # Exclude generic location
    # filteredData = data[data['Location'] !="Singapore"]
    region = ['Central', 'West', 'East', 'North', 'South']
    filteredData = data[data['Location'].isin(region)]

    # Get job count based on location
    location_count = filteredData['Location'].value_counts()

    # Initilise graph size
    plt.figure(figsize=(11, 6))

    # Plot dataframe to bar graph
    location_count.plot(kind='bar')
    plt.title('Job Postings by Location')
    plt.xticks(rotation=0)
    plt.xlabel('Locations',rotation='horizontal')
    plt.ylabel('Job Postings')
    plt.tight_layout()

    # Set name based on request data type
    # if excelName == 'SEJobs.xlsx':
    #     plt.savefig('Software Engineer job post over time.jpg')
    # elif excelName == 'ISJobs.xlsx':
    #     plt.savefig('Information Security job post over time.jpg')
    plt.show()
# --------------------------------------------------------------------------------------------------------
