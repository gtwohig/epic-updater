# epic-updater
A script that does a bunch of Jira Magic For you

## What epic updater does
It goes through the epics in your Jira Project Key that are in certain statuses and for each of them it:
1. Creates or updates a fixVersion for the Epic
    1. Gives it a consistent name: "Epic - \<The Summary of the Epic ticket\>"
    1. Uses the estimated start and completion dates from the Epic as the start/finish dates
1. Updates all issues with the Epic's epic link to include the Epic fixVerion
1. Updates the Epic's Total Points to the sum of the points of the issues in it
1. Updates the Epic's fixVersion to include the Epic fixVersion and all of the fixVersions of its constituent tickets

## Usage
1. Update the CONSTANTS at the top of the script
1. run it ```python3 epic-updater.py```
1. watch the glorious print statements while you enjoy not doing these things manually

