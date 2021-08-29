from bs4 import BeautifulSoup
import requests
import re
print('timesjobs site job opportunities')
jobkey = input('Enter skills or designation > ').strip()
jobkey = jobkey.replace(' ','%20')
joblocation = input('Job location desired > ')
joblocation = joblocation.replace(' ','%20')
jobexperience = input('your job experience > ')
if jobexperience == '': jobexperience = 0
resultcount = input('Total Result count > ')
if resultcount == '': resultcount=20
postdays = input('Posted days ago (3,7,30,60) > ')
if postdays == '': postdays=60
url = f'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords={jobkey}&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&txtLocation={joblocation}&luceneResultSize={resultcount}&postWeek={postdays}&txtKeywords={jobkey}&cboWorkExp1={jobexperience}&pDate=I&sequence=1&startPage=1'
unfamiliar_skills = input('Skills to avoid > ').split(',')
unfamiliar_skills = [skill.strip() for skill in unfamiliar_skills]
def find_jobs():
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')
    with open('jobs.txt','w'):
        for job in jobs:
            company_name = job.find('h3', class_ = 'joblist-comp-name').text.strip()
            skills = ",".join(job.find('span', class_ = 'srp-skills').text.split("  ,  ")).strip()
            experience = job.find('ul', class_ = 'top-jd-dtl clearfix').find('li')
            experience.i.decompose()
            experience = experience.text
            location = job.find('ul', class_ = 'top-jd-dtl clearfix').find_all('li')[1]
            location.i.decompose()
            location = location.text.strip()
            when_posted = job.find('span', class_ = 'sim-posted').text.strip()
            joblink = job.header.h2.a['href']
            if [i for i in unfamiliar_skills if any (j in i for j in skills.split(','))] == []:
                with open('jobs.txt', 'a') as f:
                    f.write(f'Company Name: {company_name}\n')
                    f.write(f'Required Skills: {skills}\n')
                    f.write(f'Experience: {experience}\n')
                    f.write(f'Location: {location}\n')
                    f.write(f'When posted: {when_posted}\n')
                    f.write(f'For more info : {joblink}\n\n')

if __name__== '__main__':
    find_jobs()
