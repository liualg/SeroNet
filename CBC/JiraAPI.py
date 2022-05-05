#				"token_seronet-07-26-2022"
import pandas as pd
from tqdm import tqdm

from collections import Counter
from typing import cast

from jira import JIRA
from jira.client import ResultList
from jira.resources import Issue

# Specify a server key. It should be your
# domain name link. yourdomainname.atlassian.net
jiraOptions = {'server': "https://tracker.nci.nih.gov/"}
token = "MzUyMjU5OTg4NzE5OnPkspkDA1jZhuVfljmWEsfMQCBH"
  
# Get a JIRA client instance, pass,
# Authentication parameters
# and the Server name.
# emailID = your emailID
# token = token you receive after registration
# jira = JIRA(
# 	server = "https://tracker.nci.nih.gov/", 
# 	basic_auth=(
# 		'alexander.liu@nih.gov', 
# 		"MzUyMjU5OTg4NzE5OnPkspkDA1jZhuVfljmWEsfMQCBH"
# 		)
# 	)
  



# singleIssue = jira.issue('SPDC-4256')
# print('{}: {}:{}'.format(singleIssue.key,
#                          singleIssue.fields.summary,
#                          singleIssue.fields.reporter.displayName))


# # Search all issues mentioned against a project name.
# for singleIssue in jira.search_issues(jql_str='project = SeroNet Public Data Curation'):
#     print('{}: {}:{}'.format(singleIssue.key, singleIssue.fields.summary,
#                              singleIssue.fields.reporter.displayName))

# and status = In Progress



jira = JIRA(
	server="https://tracker.nci.nih.gov",
	# token_auth=(token)

	basic_auth=('liualg', 'TRPTRPTRP1029e$$')
	)

# Get all projects viewable by anonymous users.
projects = jira.projects()

# Sort available project keys, then return the second, third, and fourth keys.
keys = sorted(project.key for project in projects)[2:5]

# Get an issue.
in_progress = jira.search_issues('project=SPDC and Type = epic',maxResults=1000000)

PMID=[]; key=[]; label1=[]; label2=[]; label3=[]; 

for issue in tqdm(in_progress):
	# print('{}: {} - {}'.format(issue.key, issue.fields.summary, issue.fields.labels))
	PMID.append(issue.fields.summary)
	key.append(issue.key)
	try:
		label1.append(issue.fields.labels[0])
		label2.append(issue.fields.labels[1])
		label3.append(issue.fields.labels[2])
	except:
		label1.append('NA')
		label2.append('NA')
		label3.append('NA')

import collections

all_labels = label1 + label2 + label3

print(list(set(all_labels)).sort())
print("########")

frequency = collections.Counter(all_labels)
print(dict(frequency))






# pd.DataFrame({
# 	'key':key,
# 	'PMID':PMID,
# 	'labels1':label1,
# 	'labels2':label2,
# 	'labels3':label3

# 	}).to_csv("~/Desktop/JiraInfo.csv")



# # Who has authenticated
# myself = jira.myself()

# # Get the mutable application properties for this server (requires
# # jira-system-administrators permission)
# props = jira.application_properties()

# # Find all issues reported by the admin
# # Note: we cast() for mypy's benefit, as search_issues can also return the raw json !
# #   This is if the following argument is used: `json_result=True`
# issues = cast(ResultList[Issue], jira.search_issues("assignee=liualg"))

# # Find the top three projects containing issues reported by admin
# top_three = Counter([issue.fields.project.key for issue in issues]).most_common(3)