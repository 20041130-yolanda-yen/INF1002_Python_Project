from yolanda import scrapData, refineSkillsReq, menu, getSkills
from daniel import analyzeData
from bernice import getNumJobsPostingOverTime, getTop10CompanyofMostPost
from andrea import getJobCountOfLocation
from ryan import getQualifications

start = 'y'
while start == 'y':
    jobPost = str(input("Enter a job position you would like to get data on: "))
    if scrapData(jobPost):

        choice = 0
        excelName = ""

        if jobPost.lower() == 'software engineer':
            excelName = 'SEJobs'
            if refineSkillsReq(excelName):
                print('Refine skills done')
        elif jobPost.lower() == 'information security':
            excelName = 'ISJobs'
            if refineSkillsReq(excelName):
                print('Refine skills done')

        while choice != 7:
            menu()
            choice = int(input("Enter choice: "))
            if choice == 1:
                getSkills(excelName)
            elif choice == 2:
                getNumJobsPostingOverTime(excelName)
            elif choice == 3:
                getTop10CompanyofMostPost(excelName, 10)
            elif choice == 4:
                analyzeData(excelName)
            elif choice == 5:
                getJobCountOfLocation(excelName)
            elif choice == 6:
                getQualifications(excelName)
        start = str(input("Search another job position? [y/n] "))
