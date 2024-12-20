import dotenv
from dotenv import load_dotenv
import os
from datetime import datetime
import ticktick

load_dotenv(dotenv_path='.envDates')
storedDateFood = os.getenv('FoodScript')
if storedDateFood:
    todaysDate = datetime.now().strftime("%Y-%m-%d")
    if storedDateFood != todaysDate:
        command = "streamlit run FoodScheduler.py"
        os.system(command)
        os.environ['FoodScript'] = todaysDate
        dotenv.set_key(dotenv_path='.envDates', key_to_set='FoodScript', value_to_set=todaysDate)
storedDateDaily = os.getenv('DailyScript')
if storedDateDaily:
    todaysDate = datetime.now().strftime("%Y-%m-%d")
    if storedDateDaily != todaysDate:
        command = "c:/Users/wyatt/Scripts/PythonScripts/.conda/python.exe c:/Users/wyatt/Scripts/PythonScripts/ScheduleDaily.py"
        os.system(command)
        os.environ['DailyScript'] = todaysDate
        dotenv.set_key(dotenv_path='.envDates', key_to_set='DailyScript', value_to_set=todaysDate)
