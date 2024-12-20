import datetime
import dateutil
import dateutil.relativedelta
import json
import ticktick.api
import ticktick.cache
from ticktick.oauth2 import OAuth2        # OAuth2 Manager
from ticktick.api import TickTickClient   # Main Interface
from dotenv import load_dotenv
import os
import pandas as pd
import time

#since the wrapper can't see time zones
TIME_ZONE_DIFFERENCE = datetime.timedelta(hours=-6)
load_dotenv()
clientId = os.getenv('CLIENT_ID')
clientSecret = os.getenv('CLIENT_SECRET')
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
auth_client = OAuth2(client_id=clientId,
                     client_secret=clientSecret,
                     redirect_uri="http://127.0.0.1:8080")
client = TickTickClient(email, password, auth_client)
#gets the two projects to mess with
dailyPrebaked = client.get_by_fields(name='Today AutoGenerated', search='projects')
DailyGenerated = client.get_by_fields(name='Scheduled DayWeekly', search='projects')
#print(insertAbleProject)

#gets the tasks
tasksInPrebaked = client.get_by_fields(projectId=dailyPrebaked['id'], search='tasks')
DailyStuff = client.get_by_fields(projectId=DailyGenerated['id'], search='tasks')

ListOfItems = []

ListOfItems.extend([[task for task in DailyStuff if "preworkout" in task['tags']]])
ListOfItems.extend([[task for task in DailyStuff if "afterworkout" in task['tags']]])
ListOfItems.extend([[task for task in DailyStuff if "breakfast" in task['tags']]])
ListOfItems.extend([[task for task in DailyStuff if "snack" in task['tags']]])
ListOfItems.extend([[task for task in DailyStuff if "lunch" in task['tags']]])
ListOfItems.extend([[task for task in DailyStuff if "dinner" in task['tags']]])
ListOfItems.extend([[task for task in DailyStuff if "endday" in task['tags']]])

descriptionArray = ["preworkout", "afterworkout", "breakfast", "snack", "lunch", "dinner", "endday"]
countTypeOfTask = 0

def convertDateToTime(str):
    is_negative = str.startswith('-')
    if is_negative:
        str = str[1:]
    
    hours, minutes, seconds = map(int, str.split(':'))
    delta = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
    if is_negative:
        delta = -delta

    return delta

for item in ListOfItems:
    itemBase = [task for task in tasksInPrebaked if descriptionArray[countTypeOfTask] in task['content']]
    print("Item base")
    print(itemBase[0])
    startTimeBase = datetime.datetime.strptime(itemBase[0]['startDate'], "%Y-%m-%dT%H:%M:%S.%f%z")
    endTimeBase = datetime.datetime.strptime(itemBase[0]['dueDate'], "%Y-%m-%dT%H:%M:%S.%f%z")
    for task in item:
        try:
            deltaFromTag = convertDateToTime((task['content']).splitlines()[0])
            deltaLength = convertDateToTime((task['content']).splitlines()[1])
            taskNew = client.task.builder(title=task['title'], projectId=dailyPrebaked['id'],
                                     startDate=startTimeBase + deltaFromTag + TIME_ZONE_DIFFERENCE
                                     , dueDate=startTimeBase + deltaFromTag + deltaLength + TIME_ZONE_DIFFERENCE)
        except:
            taskNew = client.task.builder(title=task['title'], projectId=dailyPrebaked['id'],
                                     startDate=startTimeBase + TIME_ZONE_DIFFERENCE, dueDate=endTimeBase + TIME_ZONE_DIFFERENCE)
        client.task.create(taskNew)
    countTypeOfTask += 1

#special case items
workoutItem = [task for task in DailyStuff if "workout" in task['tags'] and 
               (datetime.datetime.strptime(task['startDate'], "%Y-%m-%dT%H:%M:%S.%f%z")).date()
                 == datetime.datetime.today().date()]
startTimeBase = [task['dueDate'] for task in tasksInPrebaked if descriptionArray[0] in task['content']]
endTimeBase = [task['startDate'] for task in tasksInPrebaked if descriptionArray[1] in task['content']]
startTimeBase = datetime.datetime.strptime(startTimeBase[0], "%Y-%m-%dT%H:%M:%S.%f%z")
endTimeBase = datetime.datetime.strptime(endTimeBase[0], "%Y-%m-%dT%H:%M:%S.%f%z")

taskNew = client.task.builder(title=workoutItem[0]['title'], projectId=DailyGenerated['id'],
                                 startDate=startTimeBase + TIME_ZONE_DIFFERENCE, dueDate=endTimeBase + TIME_ZONE_DIFFERENCE)