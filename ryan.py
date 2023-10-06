import pandas as pd
import matplotlib.pyplot as plt


def getQualifications(excelName):

    excelName = excelName + '.xlsx'

    # Define a list to keep all captured Qualifications from 'Qualifications' column
    newQualificationList = []

    # Drop any rows with NaN values
    df = pd.read_excel(excelName).dropna()

    # Retrieve each row of qualifications
    for i in df['Qualifications']:
        # Split each row of qualifications by comma
        for s in i.split(","):
            # Don't retrieve/keep rows with 'Not Specified'
            if s.strip() != 'Not Specified':
                # print(s.strip())
                # Save all the qualifications retrieved into a list
                newQualificationList.append(s.strip())

    # Define a dict to keep all the qualifications with their counts
    qualificationCount = {}
    for i in newQualificationList:
        if i in qualificationCount:
            qualificationCount[i] += 1
        else:
            qualificationCount[i] = 1

    # print(newQualificationList)
    # print(qualificationCount)
    df = pd.DataFrame({'Qualifications': newQualificationList})

    # Sort from low to high to present bar chart from high to low(reverse)
    sortedQualificationCount = dict(sorted(qualificationCount.items(), key=lambda x: x[1], reverse=False))

    # Labels are the qualifications
    labels = list(sortedQualificationCount.keys())

    # Values are the total numbers/counts of each qualification
    values = list(sortedQualificationCount.values())

    # Plot horizontal bar chart for the qualifications
    plt.barh(labels, values, edgecolor='black', linewidth=1)
    plt.tight_layout()
    plt.title('Frequency of Qualifications needed')
    plt.show()
