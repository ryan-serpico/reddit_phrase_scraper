import psraw
import praw
import csv
import datetime
import time
from config2 import reddit
from teams import teamName
from swear_words import swearWords

csvFile = open('playoff_freeagency4.csv', 'w')
writer = csv.writer(csvFile)

writer.writerow(['team', 'word', 'comment', 'date', 'timestamp'])


before = 1565495999

for team in teamName:
    print(team)
    for submission in psraw.submission_search(reddit, subreddit=team, limit=400000000, sort='asc', after=1554955140):

        # I want the script to count up one so that I know what number of submission the script is on when it
        count = 0

        # Get necessary info from the submission and store in a variable.
        # submission_title = submission.title
        submission_timestamp = submission.created_utc
        submission_id = submission.id
        # submission_ratio = submission.upvote_ratio
        # submission_score = submission.score

        submission = reddit.submission(id=submission_id)

        submission.comments.replace_more(limit=None)

        for top_level_comments in submission.comments:
            if any(word in top_level_comments.body for word in swearWords):
                for i in range(len(swearWords)):
                    if swearWords[i] in top_level_comments.body:
                        count = count + 1
                        # print(str(count) + ': ' + swearWords[i])
                        top_level_comments_body = top_level_comments.body
                        top_level_comments_timestamp = top_level_comments.created_utc
                        top_level_comments_date = datetime.datetime.fromtimestamp(
                            int(float(top_level_comments.created_utc))).strftime('%m-%d-%Y')
                        writer.writerow([team, swearWords[i], top_level_comments_body,
                                         top_level_comments_date, top_level_comments_timestamp])

            for second_level_comment in top_level_comments.replies:
                if any(word in second_level_comment.body for word in swearWords):
                    for i in range(len(swearWords)):
                        if swearWords[i] in second_level_comment.body:
                            count = count + 1
                            # print(str(count) + ': ' + swearWords[i])
                            second_level_comment_body = second_level_comment.body
                            second_level_comment_timestamp = second_level_comment.created_utc
                            second_level_comment_date = datetime.datetime.fromtimestamp(
                                int(float(second_level_comment.created_utc))).strftime('%m-%d-%Y')
                            writer.writerow([team, swearWords[i], second_level_comment_body,
                                             second_level_comment_date, second_level_comment_timestamp])

        # As long as the timestamp of the current submission is less than or equal to the set before param, keeping going. Otherwise, shut it down.
        if submission_timestamp <= before:
            pass
        else:
            break

csvFile.close()

print('Done!')
