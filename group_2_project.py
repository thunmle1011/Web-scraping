import requests as rq
import csv
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

#function to display menu bar
def displayMenuBar():
    print("----------------Menu----------------")
    print("1. Extract covid data")
    print("2. Extract jobs data")
    print("3. Exit")
    print("------------------------------------")

#function to download csv CA dataset
def CA1():
    # url of csv file
    url = "https://data.chhs.ca.gov/dataset/52e4aa7a-2ea3-4bfd-8cd6-7d653db1ee74/resource/d7f9acfa-b113-4cbc-9abc-91e707efc08a/download/covid19_variants.csv"
    
    # get request of csv file
    req = rq.get(url)
    csvContent = req.content

    # download csv file
    with open("CA1.csv", "wb") as csvDownload:
        csvDownload.write(csvContent)
        csvDownload.close() 

    #read csv file to data frame
    df = pd.read_csv("CA1.csv")
    
    #drop unneccessary features
    df.drop(["area", "area_type", "specimens_7d_avg", "percentage_7d_avg"], axis =1, inplace=True)
    df.insert(1, "state", "CA")

    #change header name
    df.columns.values[2] ="variant"

    #write dataframe to csv file
    df.to_csv("CA1.csv", index=False)

# funtion to extract data from covid api
def CA2():
    # api link
    url = "https://api.covidtracking.com/v1/states/ca/daily.json"

    #get request of api
    page = rq.get(url)
    document = page.json()

    # header for dataset
    header = [ "date", "state", "cases", "deaths", "positive_tests", "negative_tests", "case_increase", "hospitalized"]
    data = []

    #get data from api and store to a list
    for covid in document:
        cv = [covid["dateChecked"], covid["state"], covid["positive"], covid["death"], covid["positiveCasesViral"],
            covid["negativeTestsAntibody"], covid["positiveIncrease"], covid["hospitalizedCurrently"]]
        data.append(cv)

    #write data to a csv file
    with open ("CA2.csv", "w", newline="") as csvWriter:
        csvWrite = csv.writer(csvWriter)
        csvWrite.writerow(header)
        csvWrite.writerows(data)
        csvWriter.close()

    #read data from csv file to dataframe
    df2 = pd.read_csv("CA2.csv")

    # change datatime format of data
    df2['date'] = pd.to_datetime(df2["date"])
    df2["date"] = df2["date"].dt.date

    #write dataframe to a csv file
    df2.to_csv("CA2.csv", index= False)

#function to merge 2 covid data set from california to a single csv
def CA():
    #call function to download csv
    CA1()
    #call function to extract data by api
    CA2()

    #read data from csv to data frame
    df1 = pd.read_csv("CA1.csv")
    df2 = pd.read_csv("CA2.csv")

    #merge to data into a single csv file
    df = pd.merge(df2, df1)

    #insert ds_source field
    df.insert(0, "ds_source", "CHHS Open Data Portal and Covid Tracking API")

    # write dataframe to csv file
    df.to_csv("CA.csv", index=False)

def MN1():
    my_API_key = "cfeabe9a67fb4edc9342ed197af3daa8"
    apiurl = "https://api.covidactnow.org/v2/states.timeseries.csv?apiKey="
    url1 = apiurl + my_API_key  # get to the url endpoint
    r = rq.get(url1)  # use the requests module to send an HTTP GET request to the link

    # write content to a new CSV file
    f = open('MN1.csv', "w", newline="")
    f.write(r.text)
    f.close()

    # read recent CSV file to get the row and columns that has the data I want to extract
    dat1 = pd.read_csv("MN1.csv", index_col=False)
    data1 = pd.DataFrame(dat1)
    df1 = data1[['date', 'state', "actuals.cases", "actuals.deaths", "actuals.positiveTests", "actuals.negativeTests", 
                "actuals.newDeaths", "actuals.hospitalBeds.capacity"]]
    df_new = df1.loc[23441: 24445]
    df_new.to_csv("MN1.csv", index=False)
    dat11 = pd.read_csv("MN1.csv", skiprows=1)
    dat11.columns = ["date", "state", "cases", "deaths", "positive_tests", "negative_tests", "case_increase", "hospitalized"]
    dat11.to_csv("MN1.csv", index=False)

def MN2():
    q = "https://www.health.state.mn.us/diseases/coronavirus/stats/cvariant.csv"
    df = pd.read_csv(q)
    df.to_csv("MN2.csv", index=False)  # write to CSV file

    # read recent CSV file to get the row and columns that has the data I want to extract
    dat2 = pd.read_csv("MN2.csv", index_col=False)
    data2 = pd.DataFrame(dat2)
    df2 = data2[["variant_cat", "case_count", "mmwr_startdate"]]
    df2.to_csv("MN2.csv", index=False)
    df2_new = pd.read_csv("MN2.csv", skiprows=1)
    df2_new.columns = ["variant", "variant_cases", "date"]
    df2_new = df2_new[["date", "variant", "variant_cases"]]
    # convert the date format in this file to get the same format with the 1st one to easy to merge
    df2_new["date"] = pd.to_datetime(df2_new["date"])
    df2_new["date"] = df2_new["date"].dt.date
    df2_new.insert(1, "state", "MN")
    df2_new.to_csv("MN2.csv", index=False)

def MN():
    MN1()
    MN2()
    pls1 = pd.read_csv("MN1.csv")
    pls2 = pd.read_csv("MN2.csv")
    # using panda data frame to merge 2 csv files into 1
    pls = pd.merge(pls1, pls2)
    pls.insert(0, "ds_source", "Minnesota Department Of Health and Covid Act Now")
    pls.to_csv("MN.csv", index=False)

def TX1():
    # File path of 1st dataset about Texas Covid cases by county    
    file1 = 'https://www.dshs.state.tx.us/sites/default/files/chs/data/Texas%20COVID-19%20Cumulative%20Confirmed%20Cases%20by%20County.xlsx'
    df = pd.DataFrame(columns= None)

    # Since the excel file have 3 sheets, I create a loop to loop through all the sheet
    for i in range(0,3):
        # Access different sheets by changing the name of sheet.
        # Only read the excel file from the 3rd row
        df1 = pd.read_excel(file1, sheet_name='Cases by County 202{}'.format(i), header=2)
        # Create a new dataframe to store neccessary rows
        df2 = pd.DataFrame(columns=None)
        # We only need total cases daily of Texas so we only take the header, which is the date, and the last row, wich is the total case in a day.
        df2 = df2.append(df1.iloc[[255]],ignore_index=True)
        # Drop the first catergory column
        df2 = df2.drop(columns= ['County'])
        # Change 2 rows we just get into 2 columns
        df2 = df2.T
        # Append it to a different dataframe
        df = df.append(df2)

    # Drop unnessary row
    df = df.drop(df.index[302], axis=0)
    df = df.drop(df.index[301], axis=0)

    # Since I use transpose() to change the shape of the dataset so the date column now is the index column of the dataframe.
    # So I couldn't change the header of the data column. Therefore, I convert it to csv and convert it to dataframe again to change the headers.
    df.to_csv('TX1.csv')
    dff = pd.read_csv('TX1.csv')
    #Change headers
    dff.columns = ['date', 'cases']
    dff["date"] = pd.to_datetime(dff["date"])
    dff["date"] = dff["date"].dt.date
    dff.to_csv('TX1.csv', index=False)

# Same functions but with the second dataset for Texas Covid deaths by county
def TX2():
    file = 'https://www.dshs.state.tx.us/sites/default/files/chs/data/Texas%20COVID-19%20Fatality%20Count%20Data%20by%20County.xlsx'

    death = pd.DataFrame(columns= None)
    df5 = pd.DataFrame()

    for i in range(0,3):
        df3 = pd.read_excel(file, sheet_name='Fatalities by County 202{}'.format(i), header=2)
        df4 = pd.DataFrame(columns=None)
        df4 = df4.append(df3.iloc[[255]],ignore_index=True)
        df4 = df4.drop(columns= ['County'])
        df4 = df4.T
        df5 = df5.append(df4)

    # death.columns = ['date', 'deaths']
    df5.to_csv('TX2.csv')
    death = pd.read_csv('TX2.csv')
    death.columns = ['date', 'deaths']
    death["date"] = pd.to_datetime(death["date"])
    death["date"] = death["date"].dt.date
    death.to_csv('TX2.csv', index=False)

def TX3():
    my_API_key = "cfeabe9a67fb4edc9342ed197af3daa8"
    apiurl = "https://api.covidactnow.org/v2/states.timeseries.csv?apiKey="
    url1 = apiurl + my_API_key  # get to the url endpoint
    r = rq.get(url1)  # use the requests module to send an HTTP GET request to the link
    # write content to a new CSV file
    f = open('TX3.csv', "w", newline="")
    f.write(r.text)
    f.close()

    # read recent CSV file to get the row and columns that has the data I want to extract
    dat1 = pd.read_csv("TX3.csv", index_col=False)
    data1 = pd.DataFrame(dat1)
    df1 = data1[['date', "actuals.positiveTests", "actuals.negativeTests", 
                "actuals.newDeaths", "actuals.hospitalBeds.capacity"]]
    df_new = df1.loc[45698: 46727]
    df_new.to_csv("TX3.csv", index=False)
    dat11 = pd.read_csv("TX3.csv", skiprows=1)
    dat11.columns = ["date", "positive_tests", "negative_tests", "case_increase", "hospitalized"]
    dat11.to_csv("TX3.csv", index=False)

# Function to merge 2 datasets
def TX():
    # Get 2 csv files by call 2 above functions
    TX1()
    TX2()
    TX3()

    # Create dataframes
    df1 = pd.read_csv('TX1.csv')
    df2 = pd.read_csv('TX2.csv')
    df3 = pd.read_csv('TX3.csv')

    # Merge the 2 datasets
    f1 = pd.merge(df1 , df2)
    # Insert the source name, state of the cases and deaths and variant types columns

    f1.to_csv('TX4.csv', index= False)
    df4 = pd.read_csv('TX4.csv')

    f= pd.merge(df4, df3)
    f.insert(0, 'ds_source', 'Texas Health, Human Service and Covid Act Now')
    f.insert(2, 'state', 'TX')
    f.insert(9, 'variant', '')
    f.to_csv('TX.csv', index=False)

# funtion to concat all data into a single csv file
def covid():
    CA()
    MN()
    TX()

    #read csv files to dataframe
    df1 = pd.read_csv("CA.csv")
    df2 = pd.read_csv("MN.csv")
    df3 = pd.read_csv("TX.csv")

    #concat into single csv
    df = pd.concat([df1, df2, df3])

    #write to csv file
    df.to_csv("group_2_covid.csv", index=False)
    covid = pd.read_csv("group_2_covid.csv")
    covid.fillna(0, inplace=True)
    covid.to_csv("group_2_covid.csv", index = False)


def OhioMeanJobs():
    url = "https://jobs.ohiomeansjobs.monster.com/Search.aspx?sort=date&tjt=data%20science"
    p = {"pg": "1"}  # let "pg" = "1" to run in the for loop
    data = []
    # run for loop form page 1 to page 200
    for pg in range(1, 201):
        p["pg"] = pg
        page = rq.get(url, params=p)
        # parse the contents of the page
        doc = BeautifulSoup(page.content, "html.parser")
        # finding their class to loop it through each header and store it in a list
        for i in range(1, 11):
            base = "_ctl0_PageTemplateContent__ctlResultsFlat_rptResults__ctl" + str(i) + "_jobRow"
            base1 = "_ctl0_PageTemplateContent__ctlResultsFlat_rptResults__ctl" + str(i) + "_topTitle"
            base2 = "_ctl0_PageTemplateContent__ctlResultsFlat_rptResults__ctl" + str(i) + "_lblCompany"
            container = doc.find(id=base)
            job = container.find("a", id=base1).text.replace("\n", "")
            company = container.find("span", id=base2).text.replace("\n", "")
            summary = container.find_all(class_="sr-info-row location")
            location = summary[0].text.split("\n")[2].replace("\r", "").strip()
            job_type = summary[1].text.split("\n")[2].replace("\r", "").strip()
            min_qual = summary[3].text.split("\n")[2].replace("\r", "").strip()
            salary = summary[4].text.split("\n")[2].replace("\r", "").strip().replace("more than ", ">")
            salary = salary.replace("less than ","<")
            value = [job, company, salary, location, job_type, min_qual]
            data.append(value)  # append to the list
    # write the content to a csv file
    with open("OhioMeanJobs.csv", "w", encoding="utf8", newline="") as f:
        writer = csv.writer(f, skipinitialspace=False)
        header = ["job_title", "company_name", "sal", "location", "job_type", "min_qual", "desired_qual"]
        writer.writerow(header)
        writer.writerows(data)
    f.close()

    data = pd.read_csv("OhioMeanJobs.csv", index_col=False)
    # since the place merges "city, state", I have to use dataframe to split it into 2 columns
    new = data["location"].str.split(", ", n=1, expand=True)
    data["city"] = new[0]
    data["state"] = new[1]
    data.drop(columns=["location"], inplace=True)
    # clean "salary" data to get just $ sign only
    new1 = data["sal"].str.split("(", n=1, expand=True)
    data["bo"] = new1[0]
    data["sala"] = new1[1]
    new2 = data["sala"].str.split(")", n=1, expand=True)
    data["salar"] = new2[0]
    data["salary"] = data["salar"]
    data.drop(columns=["bo"], inplace=True)
    # change the headers in correct order
    data = data[["job_title", "company_name", "salary", "city", "state", "job_type", "min_qual", "desired_qual"]]
    data.to_csv("OhioMeanJobs.csv", index=False)  # write it to new csv file

#function to scrape job from simplyhired web
def Simplyhired():
    # url of simplyhired
    url = "https://www.simplyhired.com/search?q=data+science&sb=dd"
    baseUrl = "https://www.simplyhired.com"
    # params to change page
    params = {"pn": "1"} 

    #header
    header = ["job_title", "company_name", "salary", "city", "state", "job_type", "min_qual", "desired_qual"]
    data = []

    # for loop to get data from 100 pages
    for i in range(1, 101):
        params["pn"] = i
        page = rq.get(url, params=params)
        document = BeautifulSoup(page.content, "html.parser")

        #get job cards
        jobcard = document.select("article")

        #get jobs' information from each card
        for article in jobcard:
            #get title
            title = article.find("a").text
            #get company name
            company = article.find(class_="JobPosting-labelWithIcon jobposting-company").text.strip()
            #get salary
            if(article.find(class_="jobposting-salary SerpJob-salary SerpJob-salary--is-estimate")):
                salary = article.find(class_="jobposting-salary SerpJob-salary SerpJob-salary--is-estimate").text.split(":")[1].strip("a year")
            else: salary = ""
            #get location
            location = article.find(class_="jobposting-location").text.split(",")
            city = location[0].strip()
            if(len(location)>1):
                city = location[0].strip()
                state = location[1].strip()
            else:
                city = ""
                state = location[0].strip()
            #get jobType andd qualifications 
            link =  baseUrl +article.find("a").get("href")
            jobPage = rq.get(link)
            jobDoc = BeautifulSoup(jobPage.content, "html.parser")
            if(jobDoc.find(class_="viewjob-jobDetails")):
                jt = jobDoc.find(class_="viewjob-jobDetails")
                if(jt.find(class_="viewjob-labelWithIcon viewjob-jobType")):
                    jobType = jt.find(class_="viewjob-labelWithIcon viewjob-jobType").find("span").text
                else:
                    jobType = ""
            else: 
                jobType = ""
            #get job qualification
            jq = jobDoc.find_all(class_="viewjob-qualification")
            jobQualification = []
            for jqualification in jq:
                jobQualification.append(jqualification.text)

            #list to store min and desired qualification
            min_qual = []
            des_qual = []

            # split min and desired qualification
            for qual in jobQualification:
                if (qual == "Bachelor's degree" or qual == 'Bachelor of Science in Nursing' or qual == 'High school diploma or GED' 
                    or qual ==  "Master's degree" or qual == 'Doctoral degree' or qual =='Bachelor of Science' or qual == 'Master of Science'
                    or qual == 'Bachelor of Arts' or qual == 'Master of Public Health' or qual == "Master of Business Administration" 
                    or qual == "Associate's degree" or qual == 'Bachelor of Electrical Engineering' or qual == 'Doctor of Philosophy'
                    or qual == 'Master of Public Administration' or qual == 'Master of Arts' or qual == 'Master of Management'
                    or qual ==  'Master of Education' or qual == 'Master of Health Administration'):
                    min_qual.append(qual)
                else:
                    des_qual.append(qual)
            minQualResult = ', '.join(min_qual)
            desQualResult = ', '.join(des_qual)
            #append all data into data list
            data.append([title, company, salary, city, state, jobType, minQualResult, desQualResult])
        
    # write information to a csv file
    with open ("Simplyhired.csv", "w", newline="", encoding="UTF-8") as csvWriter:
        csvWrite = csv.writer(csvWriter)
        csvWrite.writerow(header)
        csvWrite.writerows(data)
        csvWriter.close()

def AIJobs() :
    # Create header list
    header = ['job_title', 'company_name', 'salary', 'location', 'job_type', 'min_qual', 'desired_qual']

    with open('AIJobs.csv', 'w', newline='', encoding='utf-8') as new:
        writer_obj = csv.writer(new)
        writer_obj.writerow(header)

        # Job search website url
        url = 'https://ai-jobs.net/?cat=3&cou=238&key=&exp='
        # Require authorization
        doc = rq.get(url)
        # Parse to html format
        document = BeautifulSoup(doc.content, 'html.parser')
        
        # Find all card that contains 1 job description
        for card in document.find_all('div', class_='list-group-item px-2 px-lg-3 py-0'):
            # Scrap job title
            job_title = card.find('h2', class_= 'h4 mb-1').text
            # Scrap company name
            company_name = card.find('p', class_= 'm-0 text-muted job-list-item-company').text
            # Scrap location
            location = card.find('span', class_= 'd-block d-md-none text-break job-list-item-location').text

            # Find the block that contains info
            for element in card.find_all('div', class_='d-block'):
                # Find the tag that contains salary info block by block
                wage = element.find('span', class_= 'badge badge-success badge-pill d-md-none')
                # If that block does not contain the salary tag, leave it blank
                if wage == None:
                    salary = ''
                # If it does, fill the cell with salary info
                else:
                    salary = wage.text

                    
            # Access to each job description url
            for card_url in card.find_all('a', class_= 'col list-group-item-action px-2 py-3'):
                link = 'https://ai-jobs.net{}'.format(card_url.get('href'))
                link_req= rq.get(link)
                link_html = BeautifulSoup(link_req.content, 'html.parser')

                # Same process with salary info
                for detail in link_html.find_all('h5', class_= 'pb-2'):
                    category = detail.find('span', class_= 'badge badge-secondary badge-pill my-1')
                    if category == None:
                        job_type = ''
                    else:
                        job_type = category.text

                    require = detail.find('span', class_= 'badge badge-info badge-pill my-1')
                    if require == None:
                        min_quals = ''
                    else:
                        min_quals = require.text


        
            # Write all extract infomations to csv file. Remove unicode character in location column
            job = [job_title, company_name, salary, location.encode('ascii','ignore').decode('unicode_escape'), job_type, min_quals]
            writer_obj.writerow(job)
            
        new.close()

    # Create a dataframe to clean csv file
    df = pd.read_csv('AIJobs.csv', encoding='utf-8-sig')

    # Split location to city, state and country columna
    df[['city','state','country']] = df.location.str.split(",",expand=True,)
    # Find the row in city columns that contains 'remote' value
    remote = df['city'].str.contains('remote', case=False)
    # Get the index of the rows
    idx1 = df.index[remote == True]

    # Change the cell value to remote value
    for i in idx1:
        df.at[i,'city'] = 'Remote'
        df.at[i,'state'] = 'Remote'

    # Change t 'united' value to 'remote' because working in the us without specific location can consider is a remote job
    remote2 = df['city'].str.contains('united', case=False)
    idx2 = df.index[remote2 == True]
    for i in idx2:
        df.at[i,'city'] = 'Remote'
        df.at[i,'state'] = 'Remote'

    united = df['state'].str.contains('united', case=False)
    idx3 = df.index[united == True]
    for i in idx3:
        df.at[i,'state'] = ''

    us = df['state'].str.contains('us', case=False)
    idx5 = df.index[us == True]
    for i in idx5:
        df.at[i,'state'] = ''

    ny = df['city'].str.contains('new york', case=False)
    idx4 = df.index[ny == True]
    for i in idx4:
        df.at[i,'state'] = 'NY'

    # Replace all irregular characters or terms
    df['city'] = df['city'].str.replace('- will also', '')
    df['city'] = df['city'].str.replace('-', '')
    df['salary'] = df['salary'].str.replace('*', '')
    df['salary'] = df['salary'].str.replace('USD ', '>$')
    df['salary'] = df['salary'].str.replace('+', '')
    df['state'] = df['state'].str.replace(' or ', '/Remote')
    df['state'] = df['state'].str.replace(';', '/')
    df['state'] = df['state'].str.replace('RemoteRemote', 'Remote')

    # Drop unnessary columns
    df.drop(columns=['location'])
    df.drop(columns=['country'])
    df = df[["job_title", "company_name", "salary", "city", "state", "job_type", "min_qual", "desired_qual"]]
    
    # Convert it to csv file
    df.to_csv('AIJobs.csv', index = False)     
                
# function for final job csv file
def job():
    OhioMeanJobs()
    Simplyhired()
    AIJobs()

    # Read csv files to dataframe to concat and clean
    df1 = pd.read_csv("Simplyhired.csv")
    df2 = pd.read_csv("OhioMeanJobs.csv")
    df3 = pd.read_csv("AIJobs.csv")

    # Concat dataframes
    df = pd.concat([df1, df2, df3])

    # Fill empty cell in desired_qual by 'Not Mention'
    df["desired_qual"].fillna('Not Mention', inplace= True)

    # Replace irregular values of state
    df["state"] = df["state"].str.replace(" California", "CA")
    df["state"] = df["state"].str.replace(" Colorado", "CO")
    df["state"] = df["state"].str.replace(" New Jersey", "NJ")
    df["state"] = df["state"].str.replace(" Utah", "UT")
    df["state"] = df["state"].str.replace(" Texas", "TX")
    df["state"] = df["state"].str.replace(" Illinois", "IL")
    df["state"] = df["state"].str.replace(" Virginia", "VA")
    df["state"] = df["state"].str.replace(" GA/Remote", "GA")
    df["state"] = df["state"].str.replace(" Maryland", "MD")
    df["state"] = df["state"].str.replace(" Washington", "WA")
    df["state"] = df["state"].str.replace(" CA/ Remote", "CA")
    df["state"] = df["state"].str.replace(" CA/Remote", "CA")
    df["state"] = df["state"].replace("Remote", pd.NA)
    df["state"] = df["state"].str.replace(" ", "")
    df["state"] = df["state"].str.replace(r"[\xa0+1location]", "")
    df["state"] = df["state"].str.replace(r"[\xa0+10locations]", "")
    df["state"] = df["state"].str.replace(r"[\xa0+13locations]", "")
   
    #Drop row that contains empty cells
    df.dropna(inplace=True)
    # Drop duplicated row
    df.drop_duplicates(inplace=True)

    # Replace irregular values of job_type
    df["job_type"] = df["job_type"].str.replace("Full-TimeInternship", "Full-Time")
    df["job_type"] = df["job_type"].str.replace("Part-TimeFull-TimePermanentInternship", "Part-Time/Full-Time")
    df["job_type"] = df["job_type"].str.replace("Full-TimePermanent", "Full-Time")
    df["job_type"] = df["job_type"].str.replace("Full-TimeTemporaryInternship", "Full-Time")
    df["job_type"] = df["job_type"].str.replace("Part-TimeFull-TimeInternship", "Part-Time/Full-Time")
    df["job_type"] = df["job_type"].str.replace("Part-TimeFull-TimePermanent", "Part-Time/Full-Time")
    df["job_type"] = df["job_type"].str.replace("Full-TimeContract", "Full-Time")
    df["job_type"] = df["job_type"].str.replace("Part-TimeFull-TimeTemporary", "Part-Time/Full-Time")
    df["job_type"] = df["job_type"].str.replace("Part-TimeFull-TimeTemporaryInternship", "Part-Time/Full-Time")
    df["job_type"] = df["job_type"].str.replace("Part-TimePermanent", "Part-Time")
    df["job_type"] = df["job_type"].str.replace("Part-TimeTemporary", "Part-Time")
    df["job_type"] = df["job_type"].str.replace("Full-TimeTemporary", "Full-Time")
    df["job_type"] = df["job_type"].str.replace("Full Time", "Full-time")
    df["job_type"] = df["job_type"].str.replace("Part-TimeFull-Time Temporary Internship", "Part-Time/Full-Time")
    df["job_type"] = df["job_type"].str.replace("Full-Time PermanentTemporaryInternship", "Full-Time")
    df["job_type"] = df["job_type"].str.replace("Part-TimeFull-Time Contract", "Part-Time/Full-Time")
    df["job_type"] = df["job_type"].str.replace("Full-Time PermanentTemporary", "Full-Time")
    df["job_type"] = df["job_type"].str.replace("Part-TimeInternship", "Part-Time")
    df["job_type"] = df["job_type"].str.replace("Part-TimeFull-Time ContractInternship", "Part-Time/Full-Time")
    df["job_type"] = df["job_type"].str.replace("Part-TimeFull-Time PermanentTemporary", "Part-Time/Full-Time")
    df["job_type"] = df["job_type"].str.replace("Part-TimeFull-Time PermanentTemporaryInternship", "Part-Time/Full-Time")
    df["job_type"] = df["job_type"].str.replace("Full-time", "Full-Time")
    df["job_type"] = df["job_type"].str.replace("Part-time", "Part-Time")
    df["job_type"] = df["job_type"].str.replace("Part-TimeFull-Time", "Part-Time/Full-Time")
    df["job_type"] = df["job_type"].str.replace("Full-TimeInternship", "Full-Time")
    df["job_type"] = df["job_type"].str.replace("Full-TimeCo-opInternship", "Full-Time")
    df["job_type"] = df["job_type"].str.replace("Part-TimeFull-TimeInternship", "Part-Time/Full-Time")

    # Drop irregular rows
    df = df.drop(df.index[301], axis=0)
    df = df.drop(df.index[300], axis=0)

    # Convert dataframe to final csv file
    df.to_csv("group_2_dsc_jobs.csv", index=False, encoding="utf-8-sig")

# main program
# call display menu function
displayMenuBar()

# promp user to enter choice
choice = int(input("Enter your choice: "))

# corresponding tasks with choices
while(choice!=3):
    if (choice==1):
        covid()
    elif (choice==2):
        job()
    else:
        print("Invalid choice")
    print()
    displayMenuBar()
    choice = int(input("Enter your choice: "))


