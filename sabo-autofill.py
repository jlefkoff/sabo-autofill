import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from os import getenv
import requests
import base64
import argparse

# read the env file
from dotenv import load_dotenv

load_dotenv()

# setup arguments
parser = argparse.ArgumentParser()
parser.add_argument("issueKey", help="The JIRA issue key to query")
args = parser.parse_args()

# hardcoded info for now:
treasurer_info = {
    "name_f": "Jonah",
    "name_l": "Lefkoff",
    "email": "lefkoff.h@northeastern.edu",
}

advisor_info = {
    "name_f": "Jeremy",
    "name_l": "Reger",
    "email": "j.reger@northeastern.edu",
}

index = "800040"
account_code = "73030"

# encode a basic auth token by building a string of the form useremail:api_token
# and then base64 encoding it
auth = base64.b64encode(
    f"{getenv('USER_EMAIL')}:{getenv('JIRA_TOKEN')}".encode()
).decode()

response_main = requests.get(
    f"https://api.atlassian.com/jira/forms/cloud/{getenv('CLOUD_ID')}/issue/{args.issueKey}/form",
    headers={
        "Content-Type": "application/json",
        "X-ExperimentalApi": "opt-in",
        "Authorization": f"Basic {auth}",
    },
)
print("Got Form ID" if (response_main.status_code == 200) else "Failed to Fetch ID")
# get the "id" value of the first element of the returned JSON
formID = response_main.json()[0]["id"]

# query the actual form now that we have an ID
response_form = requests.get(
    f"https://api.atlassian.com/jira/forms/cloud/{getenv('CLOUD_ID')}/issue/{args.issueKey}/form/{formID}",
    headers={
        "Content-Type": "application/json",
        "X-ExperimentalApi": "opt-in",
        "Authorization": f"Basic {auth}",
    },
)

print("Got Form Successfully" if (response_form.status_code == 200) else "Failed to Fetch Form")

# extract the form responses

form_responses = response_form.json()

responses = {
    "name_f": form_responses["state"]["answers"]["13"]["text"],
    "name_l": form_responses["state"]["answers"]["2"]["text"],
    "phone": form_responses["state"]["answers"]["50"]["text"],
    "email": form_responses["state"]["answers"]["49"]["text"],
    "nuid": form_responses["state"]["answers"]["3"]["text"],
    "addr1": form_responses["state"]["answers"]["25"]["text"],
    "city": form_responses["state"]["answers"]["28"]["text"],
    "state": form_responses["state"]["answers"]["24"]["text"],
    "zip": form_responses["state"]["answers"]["23"]["text"],
    "travel": form_responses["state"]["answers"]["15"]["choices"][0],
    "expense_descr": form_responses["state"]["answers"]["51"]["text"],
    "receipt_qty": form_responses["state"]["answers"]["14"]["choices"][0],
    "receipt_amounts": []
}

# ...

# Initialize an empty list to store the receipt amounts
responses["receipt_amounts"] = []

# Iterate over the range 39 through 42
for i in range(39, 43):
    # Check if the receipt amount exists
    if str(i) in form_responses["state"]["answers"]:
        # Add the receipt amount to the list
        responses["receipt_amounts"].append(form_responses["state"]["answers"][str(i)]["text"])

# print the responses
print(responses)

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# open the SABO form
browser.get(
    "https://sabo.studentlife.northeastern.edu/sabo-expense-reimbursement-voucher/"
)

# Wait until the div with the class "ginput_container_checkbox" is available
wait = WebDriverWait(browser, 10)
div = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".ginput_container_checkbox"))
)

# Find all checkboxes within the div
checkboxes = div.find_elements(By.CSS_SELECTOR, "input[type=checkbox]")

# Iterate over the checkboxes and click each one to check it
for checkbox in checkboxes:
    checkbox.click()

# fill out the requester info at the top of the form
first_name = browser.find_element(By.ID, "input_2_2_3")
last_name = browser.find_element(By.ID, "input_2_2_6")
nuid = browser.find_element(By.ID, "input_2_76")
address = browser.find_element(By.ID, "input_2_97")
city = browser.find_element(By.ID, "input_2_94")
state = browser.find_element(By.ID, "input_2_95")
zip = browser.find_element(By.ID, "input_2_96")

first_name.send_keys(responses["name_f"])
last_name.send_keys(responses["name_l"])
nuid.send_keys(responses["nuid"])
address.send_keys(responses["addr1"])
city.send_keys(responses["city"])
# clear the default state first
state.clear()
state.send_keys(responses["state"])
zip.send_keys(responses["zip"])

# if this is a travel reimbursement, tick the travel radio box, otherwise tick the non-travel radio box
if responses["travel"] == "1":
    travel_radio = browser.find_element(By.ID, "choice_2_13_1")
    travel_radio.click()

else:
    non_travel_radio = browser.find_element(By.ID, "choice_2_13_0")
    non_travel_radio.click()


# travel reiumbursement specific info
if responses["travel"] == "1":

    # purpose info
    purpose = browser.find_element(By.ID, "input_2_143")
    expense = browser.find_element(By.ID, "input_2_5")
    travelStart = browser.find_element(By.ID, "input_2_6")
    travelEnd = browser.find_element(By.ID, "input_2_7")

    purpose.send_keys("Annual Trip to Acadia National Park")
    expense.send_keys(responses["expense_descr"])
    travelStart.send_keys("05/24/2024")
    travelEnd.send_keys("05/27/2024")

    # indexes
    index_1 = browser.find_element(By.ID, "input_2_40")
    index_2 = browser.find_element(By.ID, "input_2_41")
    index_3 = browser.find_element(By.ID, "input_2_45")
    index_4 = browser.find_element(By.ID, "input_2_49")
    index_5 = browser.find_element(By.ID, "input_2_53")

    # account codes
    account_1 = browser.find_element(By.ID, "input_2_37")
    account_2 = browser.find_element(By.ID, "input_2_42")
    account_3 = browser.find_element(By.ID, "input_2_46")
    account_4 = browser.find_element(By.ID, "input_2_50")
    account_5 = browser.find_element(By.ID, "input_2_54")

    # money amounts
    amount_1 = browser.find_element(By.ID, "input_2_38")
    amount_2 = browser.find_element(By.ID, "input_2_43")
    amount_3 = browser.find_element(By.ID, "input_2_47")
    amount_4 = browser.find_element(By.ID, "input_2_51")
    amount_5 = browser.find_element(By.ID, "input_2_55")

    # only fill out based on how many receips the user has
    for i in range(0, len(responses["receipt_amounts"])):
        if i == 0:
            index_1.send_keys(index)
            account_1.send_keys(account_code)
            amount_1.send_keys(responses["receipt_amounts"][i])
        if i == 1:
            index_2.send_keys(index)
            account_2.send_keys(account_code)
            amount_2.send_keys(responses["receipt_amounts"][i])
        if i == 2:
            index_3.send_keys(index)
            account_3.send_keys(account_code)
            amount_3.send_keys(responses["receipt_amounts"][i])
        if i == 3:
            index_4.send_keys(index)
            account_4.send_keys(account_code)
            amount_4.send_keys(responses["receipt_amounts"][i])
        if i == 4:
            index_5.send_keys(index)
            account_5.send_keys(account_code)
            amount_5.send_keys(responses["receipt_amounts"][i])

    # confirmation checkbox
    confirm = browser.find_element(By.ID, "choice_2_157_1")
    confirm.click()

# non-travel reimbursement specific info
if responses["travel"] == "2":
    
    # purpose info
    purpose = browser.find_element(By.ID, "input_2_141")
    expense = browser.find_element(By.ID, "input_2_142")

    purpose.send_keys("NUHOC")
    expense.send_keys(responses["expense_descr"])

    # confirmation checkbox
    confirm = browser.find_element(By.ID, "choice_2_156_1")
    confirm.click()

# student phone and email
phone = browser.find_element(By.ID, "input_2_153")
email = browser.find_element(By.ID, "input_2_98")

phone.send_keys(responses["phone"])
email.send_keys(responses["email"])

# treasurer info
treasurer_first = browser.find_element(By.ID, "input_2_165_3")
treasurer_last = browser.find_element(By.ID, "input_2_165_6")
treasurer_email = browser.find_element(By.ID, "input_2_166")

treasurer_first.send_keys(treasurer_info["name_f"])
treasurer_last.send_keys(treasurer_info["name_l"])
treasurer_email.send_keys(treasurer_info["email"])

# advisor info
advisor_first = browser.find_element(By.ID, "input_2_64_3")
advisor_last = browser.find_element(By.ID, "input_2_64_6")
advisor_email = browser.find_element(By.ID, "input_2_65")

advisor_first.send_keys(advisor_info["name_f"])
advisor_last.send_keys(advisor_info["name_l"])
# clear the default email first
advisor_email.clear()
advisor_email.send_keys(advisor_info["email"])

try:
    while True:
        # Poll the browser every second
        time.sleep(1)

        # This will throw an exception when the browser is closed
        browser.title
except:
    print("Browser has been closed.")
