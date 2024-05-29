# SABO Autofill from Jira Service Ticket

This custom script is a pipe between [NUHOC's](https://nuhoc.com/) internal finance ticketing system and the Northeastern Student Activities Business Office ([SABO](https://sabo.studentlife.northeastern.edu/)) which handles reimbursments for university funds. 

As the club's treasurer, I have to fill this form out approximately 300 times in a given year. That gets pretty tiring, so I though it [would be worth](https://xkcd.com/1205/) automating. This is an incredubily hacky solution, as it depends on the exact form of our tickets and the SABO from staying the same. Nevertheless, it serves as a good example of connecting to the Jira forms API to a Selenium autofill system.

## Running

Activate and install these requirements: `pip install -r requirements.txt`.

Then, add your Jira email as well as instance cloud ID and token to a `.env` file (see the example for variable names). To generate an API key and get your instance Cloud ID, [see here](https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/).

Finally, just run the script by doing `python sabo-autofill.py [TICKET-NR]`. This should open a new instance of chrome and autofill the fields. It watches for when you submit and close the browser and ends the script. Future support for listing all tickets is in the works.