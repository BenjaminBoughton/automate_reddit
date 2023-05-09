import praw
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import yaml

# Read the YAML file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Reddit API credentials
reddit_client_id = config['reddit_credentials']['reddit_client_id']
reddit_client_secret = config['reddit_credentials']['reddit_client_secret']
reddit_user_agent = config['reddit_credentials']['reddit_user_agent']
reddit_username = config['reddit_credentials']['reddit_username']
reddit_password = os.environ.get('REDDIT_PASSWORD')

# Email configuration
smtp_server = config['email_configuration']['smtp_server']
smtp_port = config['email_configuration']['smtp_port']
smtp_username = config['email_configuration']['smtp_username']
smtp_password = os.environ.get('SMTP_PASSWORD')
email_from = config['email_configuration']['email_from']
email_to = config['email_configuration']['email_to']

# Connect to Reddit API
reddit = praw.Reddit(client_id=reddit_client_id,
                     client_secret=reddit_client_secret,
                     user_agent=reddit_user_agent,
                     username=reddit_username,
                     password=reddit_password)

# Select the subreddit to monitor
subreddit = reddit.subreddit("Kitboga")


# Check for new posts in the subreddit
for submission in subreddit.stream.submissions():
    # Email subject and body
    email_subject = f"New post in r/{subreddit.display_name}: {submission.title}"
    email_body = f"Author: {submission.author}\n\n{submission.selftext}\n\nLink: {submission.url}"

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = email_subject
    msg.attach(MIMEText(email_body, 'plain'))

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        print("Email sent successfully!")