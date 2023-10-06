import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk.corpus import stopwords
# nltk.download('stopwords')
from mySkillKeywords import SEskills_keywords, ISecskills_keywords


#By Daniel
#Convert to lowercase and Remove non-english characters,punctuations and stop words
def cleanData(job_description):

    punctuation_list = '''!"$%&'()*,’-/:;<=>?@[\]^_`{|}~'''
    # Convert to lowercase
    description = str(job_description).lower()
    #Remove non-english characters
    filtered_string = ''.join(char for char in description if char.isascii() or char.isspace())

    #Remove specific punctuations
    translator = str.maketrans(punctuation_list, ' ' * len(punctuation_list))
    cleaned_sentence = filtered_string.translate(translator)

    #english_words = set(nltk.corpus.words.words())
    stop_words = set(stopwords.words('english'))
    #lowercase_list = [word.lower() for word in skills_keywords]
    #whitelist = set(lowercase_list)
    tokens = cleaned_sentence.split()

    #Remove stop words
    filtered_tokens = [token for token in tokens if token not in stop_words]
    #cleaned_tokens.extend(token for token in filtered_tokens if token in english_words or token in whitelist)
    cleaned_string = ' '.join([item for item in filtered_tokens])

    return cleaned_string


# By Daniel
# Save cleaned data to new excel
def saveCleanedData(excelName):
    skill_list = []

    data = pd.read_excel(excelName + '.xlsx')
    for index, column in data.iterrows():
        skill_list.append(cleanData(column[6]))

    data['Skills'] = skill_list

    data.to_excel(excelName+"cleanedData.xlsx", index=False, engine='openpyxl')

#By Daniel
#Keyword search
def analyzeData(excelName):
    saveCleanedData(excelName)
    data_list = {'Entry Level':{},'Junior Executive':{},'Manager':{},'Senior Manager':{},'Senior Executive':{},'Non-Executive': {}}

    data = pd.read_excel(excelName+".xlsx").dropna()
    for index, row in data.iterrows():
        if excelName == 'ISJobs':
            for keyword in ISecskills_keywords:
                if keyword in str(row[6]):
                    if keyword not in data_list[row[2]]:
                        data_list[row[2]][keyword] = 1
                    else:
                        data_list[row[2]][keyword] += 1
        elif excelName == 'SEJobs':
            for keyword in SEskills_keywords:
                if keyword in str(row[6]):
                    if keyword not in data_list[row[2]]:
                        data_list[row[2]][keyword] = 1
                    else:
                        data_list[row[2]][keyword] += 1


    filtered_list = {k: v for k, v in data_list.items() if v}
    showGraph(filtered_list)

#By Daniel
#Show only top 3 most popular skills
def filterDictionary(my_dict):
    result_dict = {}
    sorted_dict = sorted(my_dict.items(), key=lambda x: x[1], reverse=True)

    if len(my_dict) >= 3:
        for i in range(3):
            result_dict[sorted_dict[i][0]] = sorted_dict[i][1]
    elif len(my_dict) == 2:
        for i in range(2):
            result_dict[sorted_dict[i][0]] = sorted_dict[i][1]
    else:
        result_dict = my_dict

    return result_dict

#By Daniel
#Display bar chart
def showGraph(data_list):
    for key,value in data_list.items():
        data_list[key] = filterDictionary(value)

    job_levels = list(data_list.keys())
    all_skills = sorted(list(set(skill for skills in data_list.values() for skill in skills.keys())))

    bar_width = 0.2
    colors = plt.cm.tab10(np.linspace(0, 1, len(all_skills)))

    # Generating positions for each group of bars
    r = np.arange(len(job_levels))

    plt.figure(figsize=(15, 8))

    # Track which skills have been plotted to avoid duplicate legend items
    plotted_skills = set()

    for job_index, job in enumerate(job_levels):
        offset = 0  # Initialize the offset for each job level
        for idx, skill in enumerate(all_skills):
            if skill in data_list[job]:  # Check if the skill exists for the current job level
                label = skill if skill not in plotted_skills else ""  # Add label only if not yet plotted
                plt.bar(r[job_index] + offset, data_list[job][skill], width=bar_width, color=colors[idx], label=label)
                offset += bar_width  # Increase the offset only if the bar is plotted
                plotted_skills.add(skill)  # Mark the skill as plotted

    plt.xlabel('Job Levels')
    plt.ylabel('Popularity Value')
    plt.title('Skills for Each Job Level')
    plt.xticks(r + bar_width, job_levels)  # Adjusting x-ticks
    plt.legend(title="Skills", loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()

    plt.show()
