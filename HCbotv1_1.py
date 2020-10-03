import praw
import json
import datetime
import random

with open("credentials.json") as f:
    creds = json.load(f)



modlist = ["AcePhoenixGamer", "HiddenCornerBot"]
hitList = []
addList = []
selfText = "#Kicked:\n\n"

reddit = praw.Reddit(client_id=creds["client_id"],
                     client_secret=creds["client_secret"],
                     password=creds["password"],
                     user_agent=creds["user_agent"],
                     username=creds["username"])


now = int(datetime.datetime.timestamp(datetime.datetime.today()))
for submission in reddit.redditor("HiddenCornerBot").submissions.new(limit=1):
    lastPostAge = submission.created_utc
ageLimit = now - lastPostAge



contributors = []
for c in reddit.subreddit("HiddenCorner").contributor():
    contributors.append(c)
contributors.reverse()

if len(contributors) < 100:
    selfText += "***NOTE: Kick numbers may be shifted due to recent leaves/bans.***  \n"

for contributor in contributors:
    postAge = 0
    posted = 0
    while postAge <= ageLimit and posted == 0:
        now = int(datetime.datetime.timestamp(datetime.datetime.today()))
        for post in contributor.new(limit=None):
            postAge = now - post.created_utc
            if post.subreddit == reddit.subreddit("HiddenCorner") and postAge < ageLimit:
                posted = 1
                break
            if postAge > ageLimit:
                break
    if posted == 0:
        selfText += "- \#" + str(contributors.index(contributor) + 1) + "\t /u/" + contributor.name + "  \n"
        try:
            reddit.subreddit("HiddenCorner").contributor.remove(contributor)
        except:
            pass
        reddit.subreddit("HiddenCorner").flair.set(contributor, "Kicked", flair_template_id = "3bddf548-f29d-11e9-b16a-0ed4787532b4")
        hitList.append(contributor)

for victim in hitList:
    contributors.remove(victim)



for contributor in contributors:
    rank = contributors.index(contributor) + 1
    if contributor not in modlist:
        reddit.subreddit("HiddenCorner").flair.set(contributor, "#" + str(rank), flair_template_id = "9038eac4-f29f-11e9-95c4-0e1c0032dcda")


#Add new users

selfText += "#Added:\n\n"
numToAdd = 100 - len(contributors)


while len(addList) < numToAdd:
    # Creates add list
    for submission in reddit.subreddit("all").hot(limit=100):
        #submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            try:
                if random.randint(0,299) == 0 and comment.author not in addList and len(addList) < numToAdd and comment.author not in contributors:
                    addList.append(comment.author.name)
            except:
                pass
            if len(addList) == numToAdd:
                break
        if len(addList) == numToAdd:
            break


for user in addList:
    #Adds users
    reddit.subreddit("HiddenCorner").contributor.add(user)
    contributors.append(user)
    reddit.subreddit("HiddenCorner").flair.set(user, "#" + str(contributors.index(user) + 1), flair_template_id = "676ff240-f29f-11e9-b538-0e052881cb30")
    selfText += "- \#" + str(contributors.index(user) + 1) + "\t /u/" + user + "  \n"



today = datetime.datetime.now()
today = str(today)
today = today.split(' ')[0]

title = today + " - Weekly Bot Recap"

selfText += "#Member List:\n\n"
selfText += "| \# | User |  \n"
selfText += "| --- | --- |  \n"

for user in contributors:
    if user not in modlist:
        selfText += "| \#" + str(contributors.index(user) + 1) + " | " + str(user) + " |  \n"

reddit.subreddit("HiddenCorner").submit(title, selftext=selfText).mod.distinguish(how='yes', sticky=True)
print(selfText)
