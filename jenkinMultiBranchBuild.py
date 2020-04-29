import jenkins
import requests
from elasticsearch import Elasticsearch
from requests.auth import HTTPBasicAuth
import json

# Jenkins Server Info
jenkinSrvrInfo = {
    "url": "http://ec2-34-210-110-131.us-west-2.compute.amazonaws.com:8080",
    "usrname": "singam",
    "paswd": "jenkins"
}

# Elastic Search Server Info
elasticSrvrInfo = {
    "host": "http://localhost:9200",
    "port": 9200
}

# Establish connection to Jenkins Server
jenserv = jenkins.Jenkins(jenkinSrvrInfo['url'], username=jenkinSrvrInfo['usrname'], password=jenkinSrvrInfo['paswd'])
user = jenserv.get_whoami()
print("Logged in User: ", user['fullName'])
print("Job count: ", jenserv.jobs_count())
print("\n")

# Establish connection to Elastic Search Server using the API
# es = Elasticsearch([{'host': url, 'port': 9200}])
es = Elasticsearch([elasticSrvrInfo])
print("ES: ", es)

# Establish connection to Elastic Search Server using Python REST API
r = requests.get('http://localhost:9200')

if r.status_code == 200:
    print("REST Call to Elastic Search is Successfull")
else:
    print("REST Call to Elastic Search is Failed")

# Declaring List Variables to store the job type
multiBranchJobs = []
otherJobs = []

# Get all the list of jobs and filter the jobs only with MULTI BRANCH and add it into a list
joblist = jenserv.get_jobs()

for items in joblist:
    if "jobs" in items:
        multiBranchJobs.append(items['name'])
    else:
        otherJobs.append(items['name'])

print("Multi Branch Pipeline Jobs: ", multiBranchJobs)
print("Other Pipeline Job: ", otherJobs)

# Now we have separated the multi branch pipeline job and get the job details
i = 1
for each in multiBranchJobs:
    print("Loading Build Info of Job : ", each)
    print(jenserv.get_job_info(each))
    e1 = jenserv.get_job_info(each)
    # j1 = json.dumps(jenserv.get_job_info(each))


    print(("Sending GET Request to Jenkins Host"))
    r = requests.get(e1['url'], auth=(jenkinSrvrInfo['usrname'], jenkinSrvrInfo['paswd']))
    print(r.content, "\n")

    print("JSON LOADS: \n", json.loads(r.content))

    res = es.index(index='jenkinsmultibranch', doc_type='buildinfo', id=i, body=json.loads(r.content))
    i += 1
    print("Push Successfull. Incrementing next record")

    #res = es.index(index='singamapi1', doc_type='employee', id=1, body=e1)
