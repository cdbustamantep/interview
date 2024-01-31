import requests
import pandas
import json
import smtplib
from pandas import json_normalize
from pretty_html_table import build_table
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
from pytimedinput import timedInput
import os

BASE_URL = "https://api.github.com"

def get_pull_requests(owner, repo):
    # Construct the URL to get pull requests
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls"
    # Set up parameters to filter pull requests by date
    since_date = (datetime.now() - timedelta(days=7)).isoformat()
    params = {"state": "all", "since": since_date}
    # Make a GET request to the GitHub API
    response = requests.get(url, params=params)
    #Check for ok status code
    if response.status_code == 200:
        #Load the response to turn in dictionary
        dict = json.loads(response.text)
        #Normalize json to get all the necesary data and convert in dataframe
        df1= pandas.json_normalize(dict, max_level=2)
        #Get the dataframe important columns
        df1.rename(columns={"base.repo.name": "Repository","number": "Number of PR","user.login": "user","head.label": "user:branch source","base.ref": "merged to","merged_at": "Merged at","created_at": "request creation"},inplace=True)
        df2=df1[["Repository","id","Number of PR","state","title","user","user:branch source","merged to","Merged at","request creation"]]
        return df2
    else:
        raise Exception(f"Failed to fetch pull requests. Status code: {response.status_code}")

def generate_email_summary(owner, repo, table, to_email):
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    #E-mail inputs
    from_email = 'cd.bustamante.p@gmail.com'
    to_email = to_email
    smtp_password = 'hkcn iyyn wbmi csxz'
    #Set mesasge parameters
    message = MIMEMultipart()
    message['Subject'] = f"GitHub Pull Request Summary - {owner}/{repo}"
    message['From'] = from_email
    message['To'] = to_email
    #Adjust table to html for mail
    output_table = build_table(table, 'grey_dark')
    output="Pull request summary at: "+date_time+" for: "+owner+"/"+repo+"\n"+output_table+"\nBest Regards,Christian Bustamante"
    message.attach(MIMEText(output, "html"))
    msg_body = message.as_string()
    #Send mail
    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(message['From'], smtp_password)
    server.sendmail(message['From'], message['To'], msg_body)
    server.quit()
    # Print the details of the email
    print(f"--------------------------------E-mail details-------------------------------------------------------------")
    print(f"From: {from_email}")
    print(f"To: {to_email}")
    print(f"Subject: {message['Subject']}")
    print("\nSummary Table:\n")
    print(table)

if __name__ == "__main__":
    # Replace these values with the target repository details
    owner = "cdbustamantep"
    repo = "interview"
    to_email= "chrisvy4895@gmail.com"

    if "Windows_NT" in os.environ['OS']:
        userText, timedOut = timedInput("Send to a different mail? (default: chrisvy4895@gmail.com) [y/n]: ", timeout=5)
        if(timedOut):
            print("Using Default...")
        else:
            print(f"User-input: '{userText}'")
        if(userText=="y"): 
            to_email=input('Insert the mail to send:')
            print(to_email)

        userText2, timedOut = timedInput("Use a different owner of repo? (default: cdbustamantep) [y/n]: ", timeout=5)
        if(timedOut):
            print("Using default...")
        else:
            print(f"User-input: '{userText2}'")
        if(userText2=="y"): 
            owner=input('Insert new repo owner:')
            print(owner)

        userText3, timedOut = timedInput("Use a different repo? (default: interview) [y/n]: ", timeout=5)
        if(timedOut):
            print("Using default...")
        else:
            print(f"User-input: '{userText3}'")
        if(userText3=="y"): 
            repo=input('Insert new repo name:')
            print(repo)
    else:
        print("Only default values will be used")
   
    # Get pull requests from the last week
    pull_requests = get_pull_requests(owner, repo)

    # Generate email summary
    mail = generate_email_summary(owner, repo, pull_requests, to_email)