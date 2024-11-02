import datetime
import dateutil
import dateutil.relativedelta
import ticktick
import json
import ticktick.api
import ticktick.cache
from ticktick.oauth2 import OAuth2  
from ticktick.api import TickTickClient

#modification to api.py file
#   USER_AGENT = 'Actual User Agent Would go Here' Also change in api.py
#   X_DEVICE_ = 'Actual X_Device would go here' Also change in api.py
#   Change login to logon?wc=true&remember=true and delete old params in api.py

#authenticate
auth_client = OAuth2(client_id="theoretical id",
                     client_secret="theoretical secret",
                     redirect_uri="http://127.0.0.1:8080")


#start client
client = TickTickClient("theoretical emailemail", "theoretical pass", auth_client)

#gets the two projects to mess with
insertAbleProject = client.get_by_fields(name='InsertIntoLearnList', search='projects')
projectToInsertTo = client.get_by_fields(name='LearningList', search='projects')
#print(insertAbleProject)

#gets the tasks
tasksToBeInserted = client.get_by_fields(projectId=insertAbleProject['id'], search='tasks')


# Check if the object is already an array
if not isinstance(tasksToBeInserted, (list, tuple)):
    tasksToBeInserted = [tasksToBeInserted]
#print(tasksToBeInserted)

#create new tasks and delete old one
for task in tasksToBeInserted:
    titleBase = task['title']
    start_base = datetime.datetime.now()
    datetimeModifications = [datetime.timedelta(0), datetime.timedelta(days=1), datetime.timedelta(weeks=1)
                             , dateutil.relativedelta.relativedelta(months=1), dateutil.relativedelta.relativedelta(months=3), 
                             dateutil.relativedelta.relativedelta(months=6)]
    printedNumberEndings = ["1st", "2nd", "3rd", "4th", "5th", "Final"]
    for i in range(0, 6):
        newTitle = titleBase + " " + printedNumberEndings[i] + " review"
        #print(newTitle)
        #print(start_base + datetimeModifications[i])
        taskNew = client.task.builder(title=newTitle, projectId=projectToInsertTo['id'],
                                     startDate=start_base + datetimeModifications[i])
        client.task.create(taskNew)
    client.task.delete(task)
    
#client.task.delete(tasksToBeInserted)

#NOTE: When creating the scheduled task, make sure the task starts in the directory of the python file to get the token