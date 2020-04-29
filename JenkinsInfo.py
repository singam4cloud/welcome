import jenkins
import requests
from elasticsearch import Elasticsearch
import socket

# Elastic Search Server Info
elasticSrvrInfo = {
    "host": "http://localhost:9200",
    "port": 9200
}

socket.gethostbyname("localhost")

# Establish connection to Elastic Search Server using the API
# es = Elasticsearch([{'host': url, 'port': 9200}])
es2 = Elasticsearch([elasticSrvrInfo])
print("ES: ", es2)
# Establish connection to Elastic Search Server using Python REST API
r = requests.get('http://localhost:9200')

server = jenkins.Jenkins('http://ec2-34-210-110-131.us-west-2.compute.amazonaws.com:8080', username='singam', password='jenkins')
user = server.get_whoami()
version = server.get_version()
print('Hello %s from Jenkins %s' % (user['fullName'], version))
print("Job count: ", server.jobs_count())
# get the job list and store it in joblist of type LIST
joblist = server.get_jobs()
# print(type(joblist))

d1 = {}
for items in joblist:
    if "jobs" in items.keys():
        if len(items['jobs']) > 0:
            multijoblist = items["jobs"]
            print("Job List\n", multijoblist)
            for job in multijoblist:
                print("Job: ", job)
                d1[job['name']] = job
                print("Dictionary d1: ", d1)
                print("key = ", d1.keys())
                res1 = es2.index(index='jenkinsmul1', doc_type='buildinfo1', id=1, body=d1)
                print("Successful")
                del d1[job['name']]
