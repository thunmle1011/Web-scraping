from bs4 import BeautifulSoup
import csv
import requests as rq

url = "https://www.simplyhired.com/search?q=data+science&sb=dd"

header = ["job title", "company name", "salary", "city", "state", "job type", "min_qual", "desired_qual"]

baseUrl = "https://www.simplyhired.com"

params = {"pn": "1"} 

data = []

for i in range(1, 101):
    params["pn"] = i
    page = rq.get(url, params=params)
    document = BeautifulSoup(page.content, "html.parser")

    jobcard = document.select("article")

    count = 0
    for article in jobcard:

        count += 1

        title = article.find("a").text

        company = article.find(class_="JobPosting-labelWithIcon jobposting-company").text.strip()

        if(article.find(class_="jobposting-salary SerpJob-salary SerpJob-salary--is-estimate")):
            salary = article.find(class_="jobposting-salary SerpJob-salary SerpJob-salary--is-estimate").text.split(":")[1].strip("a year")
        else: salary = ""

        location = article.find(class_="jobposting-location").text.split(",")

        city = location[0].strip()

        if(len(location)>1):
            city = location[0].strip()
            state = location[1].strip()
        else:
            city = ""
            state = location[0].strip()
        
        link =  baseUrl +article.find("a").get("href")

        jobPage = rq.get(link)
        jobDoc = BeautifulSoup(jobPage.content, "html.parser")
        print("page", i, "count", count, ", ", company)

        if(jobDoc.find(class_="viewjob-jobDetails")):
            jt = jobDoc.find(class_="viewjob-jobDetails")
            if(jt.find(class_="viewjob-labelWithIcon viewjob-jobType")):
                jobType = jt.find(class_="viewjob-labelWithIcon viewjob-jobType").find("span").text
            else:
                jobType = ""
        else: 
            jobType = ""

        jq = jobDoc.find_all(class_="viewjob-qualification")
        jobQualification = []
        for jqualification in jq:
            jobQualification.append(jqualification.text)

        min_qual = []
        des_qual = []

        for qual in jobQualification:
            if (qual == "Bachelor's degree" or qual == 'Bachelor of Science in Nursing' or qual == 'High school diploma or GED' 
                or qual ==  "Master's degree" or qual == 'Doctoral degree' or qual =='Bachelor of Science' or qual == 'Master of Science'
                or qual == 'Bachelor of Arts' or qual == 'Master of Public Health' or qual == "Master of Business Administration" 
                or qual == "Associate's degree" or qual == 'Bachelor of Electrical Engineering' or qual == 'Doctor of Philosophy'
                or qual == 'Master of Public Administration' or qual == 'Master of Arts' or qual == 'Master of Management'
                or qual ==  'Master of Education'):
                min_qual.append(qual)
            else:
                des_qual.append(qual)
        data.append([title, company, salary, city, state, jobType, min_qual, des_qual])
    

with open ("job.csv", "w", newline="", encoding="UTF-8") as csvWriter:
    csvWrite = csv.writer(csvWriter)
    csvWrite.writerow(header)
    csvWrite.writerows(data)
    csvWriter.close()

        

