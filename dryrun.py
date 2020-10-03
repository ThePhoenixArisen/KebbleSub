import praw
import json
import datetime
import random

with open("credentials.json") as f:
    creds = json.load(f)
with open("users.json") as g:
    users = json.load(g)

modlist = ["AcePhoenixGamer", "HiddenCornerBot"]
hitList = []
addList = []
selfText = "#Kicked:\n\n"

reddit = praw.Reddit(client_id=creds["client_id"],
                     client_secret=creds["client_secret"],
                     password=creds["password"],
                     user_agent=creds["user_agent"],
                     username=creds["username"])

for user in users:
    if user not in modlist:
        users[user]["Posted"] = 0


for submission in reddit.subreddit("HiddenCorner").new(limit=100):
    #Checks all posts from past week and flags author as active
    now = int(datetime.datetime.timestamp(datetime.datetime.today()))
    postAge = now - submission.created_utc
    if postAge <= 604800 and submission.author.name not in modlist:
        users[submission.author.name]["Posted"] = 1

    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        try:
            commentAge = now - comment.created_utc
            if commentAge <= 604800 and comment.author.name not in modlist:
                users[comment.author.name]["Posted"] = 1
        except:
            pass
for user in users:
    #Kick users and add to removal list
    if users[user]["Posted"] == 0 and user not in modlist:
        #reddit.subreddit("HiddenCorner").contributor.remove(user)
        #reddit.subreddit("HiddenCorner").flair.set(user, "Kicked", flair_template_id = "3bddf548-f29d-11e9-b16a-0ed4787532b4")
        hitList.append(user)
        selfText += "- \#" + str(users[user]["Rank"]) + "\t/u/" + user + "  \n"

for user in hitList:
    users.pop(user, None) #Remove kicked users from dict

for user in users:
    users[user]["Rank"] = list(users).index(user) - 1
    #if user not in modlist:
        #reddit.subreddit("HiddenCorner").flair.set(user, "#" + str(users[user]["Rank"]), flair_template_id = "9038eac4-f29f-11e9-95c4-0e1c0032dcda")


#Add new users

selfText += "#Added:\n\n"
numToAdd = 102 - len(users)
#if numToAdd > 40:
#    numToAdd = 40 #NOTE: Remove restriction after sub reaches 100 members for 1st time

while len(addList) < numToAdd:
    # Creates add list
    for submission in reddit.subreddit("all").hot(limit=100):

        for comment in submission.comments.list():
            try:
                if random.randint(0,499) == 0 and comment.author.name not in addList and len(addList) < numToAdd and comment.author.name not in list(users):
                    addList.append(comment.author.name)
            except:
                pass
            if len(addList) == numToAdd:
                break
        if len(addList) == numToAdd:
            break

lastRank = len(users) - 2
for user in addList:
    #Adds users
    #reddit.subreddit("HiddenCorner").contributor.add(user)
    users[user] = {"Rank":lastRank + 1, "Posted":0}
    #reddit.subreddit("HiddenCorner").flair.set(user, "#" + str(users[user]["Rank"]), flair_template_id = "676ff240-f29f-11e9-b538-0e052881cb30")
    lastRank = len(users) - 2
    selfText += "- \#" + str(users[user]["Rank"]) + "\t/u/" + user + "  \n"

# with open("users.json", "w") as g:
#     json.dump(users, g)

today = datetime.datetime.now()
today = str(today)
today = today.split(' ')[0]

title = today + " - Weekly Bot Recap"

selfText += "#Member List:\n\n"
selfText += "| \# | User |  \n"
selfText += "| --- | --- |  \n"

for user in users:
    if user not in modlist:
        selfText += "| \#" + str(users[user]["Rank"]) + " | " + user + " |  \n"

#reddit.subreddit("HiddenCorner").submit(title, selftext=selfText)
print(selfText)
