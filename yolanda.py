import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import matplotlib.pyplot as plt
from mySkillKeywords import SEskills_keywords, ISecskills_keywords

from andrea import excelConveter

baseURL = "https://www.jobstreet.com.sg"

jobTitles = []
jobPTimes = []
jobLevel = []
jobURLList = []
jobCompany = []
jobQuali = []
jobSkill = []
jobLocation = []

# ------------------------------------WEB SCRAP FUNCTION STARTS HERE------------------------------------

# By Yolanda
def scrapData(jobName):

    jobName = str(jobName).lower()

    jobTitles.clear()
    jobPTimes.clear()
    jobLevel.clear()
    jobURLList.clear()
    jobCompany.clear()
    jobQuali.clear()
    jobSkill.clear()
    jobLocation.clear()

    print("Retriving data of %s...This might take a while, please hold on..."%jobName)
    for i in range(1,6,1):
        jobNameWeb = '/' + jobName.replace(' ','-') + '-jobs'
        sURL = baseURL + jobNameWeb + ("/in-Singapore?pg=%d"%i)
        response = requests.get(sURL)
        soup = BeautifulSoup(response.text, "html.parser")

        # Get job title
        job_titles = soup.find_all("h1", class_="z1s6m00")
        for t in job_titles:
            t = t.text.strip()
            jobTitles.append(t)

        # Get job post time
        job_pTimes = soup.find_all("time", class_="z1s6m00")
        for pT in job_pTimes:
            times = str(pT["datetime"]).split("T")[0]
            jobPTimes.append(times)

        # Get company name
        job_Comp = soup.find_all("a", class_="_6xa4xb0")
        for comps in job_Comp:
            job_compLink = comps.get('data-automation')
            if "jobCardCompanyLink" in job_compLink:
                jobCompany.append(comps.text.strip())
            elif "jobCardLocationLink" in job_compLink:
                jobLocation.append(comps.text.strip())

        # For each job link, get job level and job qualification
        job_links = soup.find_all("a", class_="z1s6m00")
        for link in job_links:
            job_link = link.get('href')
            if "jobId" in job_link:
                jobURL = baseURL + job_link  # job url
                jobURLList.append(jobURL)
                response = requests.get(jobURL)
                soup = BeautifulSoup(response.text, "html.parser")

                time.sleep(0.5)  # May not scrap properly if no wait time
                try:
                    # Get job level
                    job_Level = soup.find(string="Career Level").findNext('span').text.strip()
                    jobLevel.append(job_Level)

                    # Get job qualifications
                    job_Qual = soup.find(string="Qualification").findNext('span').text.strip()
                    jobQuali.append(job_Qual)

                    # Get job skills
                    job_skills = soup.find_all("li")
                    mySkills = ""
                    for s in job_skills:
                        mySkills = mySkills + s.text.strip() + ","
                    jobSkill.append(mySkills)

                except:
                    print("")
    if jobName == "software engineer" and len(jobTitles) > 0:
        excelConveter(jobTitles, jobPTimes, jobLevel, jobCompany, jobQuali, jobLocation, jobSkill, jobURLList, "SEJobs")
        return True
    elif jobName == "information security" and len(jobTitles) > 0:
        excelConveter(jobTitles, jobPTimes, jobLevel, jobCompany, jobQuali, jobLocation, jobSkill, jobURLList, "ISJobs")
        return True
    else:
        return False

# ----------------------------------------WEB SCRAP FUNCTION END HERE----------------------------------------

# By Yolanda
# Clean string to get skills for each position in each excel (job position)
def refineSkillsReq(excelName):
    excelName = excelName + '.xlsx'
    df1 = pd.read_excel(excelName)
    my2ndList = []
    mySkills = []
    for index, row in df1.iterrows():
        myList = []
        jobSkill = row[6]
        if jobSkill != '' :
            jobSkill = str(jobSkill).split(",")
            if excelName == 'SEJobs.xlsx':
                for s in SEskills_keywords:
                    for j in jobSkill:
                        if s in j:
                            mySkills.append(s)
                            if s not in myList:
                                myList.append(s)
            if excelName == 'ISJobs.xlsx':
                for s in ISecskills_keywords:
                    for j in jobSkill:
                        if s in j:
                            mySkills.append(s)
                            if s not in myList:
                                myList.append(s)

            my2ndList.append(myList)
        else:
            my2ndList.append("")

    df1['Skills'] = my2ndList #Updating exisiting column Skills with new data (new data = each job row got how many skills etc)
    df1['Skills'] = df1['Skills'].astype(str).str.replace(r'[][]', '', regex=True) #Remove list [ ]s
    if df1.to_excel(excelName,index=False):#Save the update df1 into exisiting excel
        return True
    else:
        return False

    # if (excelName=='SEJobs.xlsx'):
    #     plotGraphAll(df_new, 'Software Engineer') #plot the graph
    #
    # elif (excelName=='ISJobs.xlsx'):
    #     plotGraphAll(df_new, 'Information Security')

# --------------------------------------------------------------------------------------------------------

# By Yolanda
# Plot top 10 skills from all post
def plotGraphAll(df, name):
    df.Skills.value_counts().iloc[:10].plot(kind='barh', edgecolor='black')
    plt.title('Popular Skills Of %s Jobs'%name)
    plt.tight_layout()
    #plt.savefig('Popular Skills Of %s Jobs.jpg'%name) #Save the plotted image
    plt.show()
# --------------------------------------------------------------------------------------------------------

# By Yolanda
# Get top skills of all jobs in job position
def getSkills(excelName):
    excelName = excelName + '.xlsx'
    df1 = pd.read_excel(excelName)
    mySkills = []
    for index, row in df1.iterrows():
            jobSkill = str(row[6])
            if jobSkill != '':
                jobSkill = str(jobSkill).split(",")
                if excelName == 'SEJobs.xlsx':
                    for s in SEskills_keywords:
                        for j in jobSkill:
                            if s in j:
                                mySkills.append(s)
                if excelName == 'ISJobs.xlsx':
                    for s in ISecskills_keywords:
                        for j in jobSkill:
                            if s in j:
                                mySkills.append(s)

    df = pd.DataFrame(mySkills) #Turn mySkills list to dataframe (this list contains ALL skills, doesnt care from which job)
    df_new = df.rename(columns={0: 'Skills'}) #name the column in this dataframe so can easily call it later

    if (excelName=='SEJobs.xlsx'):
        plotGraphAll(df_new, 'Software Engineer') #plot the graph
    elif (excelName=='ISJobs.xlsx'):
        plotGraphAll(df_new, 'Information Security')
# --------------------------------------------------------------------------------------------------------

# By Yolanda
# Menu to prompt user input
def menu():
    print("------------------------------------------")
    print("------------------ MENU ------------------")
    print("------------------------------------------")
    print("1: View top 10 skills of job position")
    print("2: View number of job post over time")
    print("3: View top 10 company of most job posting")
    print("4: View popular skills of job levels")
    print("5: View job count based on location")
    print("6: View job qualifications")
    print("7: Back")
    print("------------------------------------------")
# --------------------------------------------------------------------------------------------------------
