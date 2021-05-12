import random
import time
from apscheduler.schedulers.blocking import BlockingScheduler

def test():
    phrases = ["Bot talking: Don't worry I'm working...", "Bot talking: Aghh! I'm working shut up...",
               "Bot talking: I'm working! do you ?", "Bot talking: Do something else, I'm working!",
               "Bot talking: Are you gonna watch me all day? Leave me alone, I'm working!",
               "Bot talking: I'm doing my job!", "Bot talking: Working on it! so you don't have to dumbass"]
    random_fromlist = random.choice(phrases)
    print(random_fromlist)

scheduler = BlockingScheduler()
scheduler.add_job(test, 'interval', seconds=5)

while True:
    print('still')
    time.sleep(2)
    scheduler.start()
