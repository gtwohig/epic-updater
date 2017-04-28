from jira import JIRA

JIRA_USERNAME = 'greg' # your jira username
JIRA_PASSWORD = 'PPPPPPP' # put your password here
JIRA_PROJECT = 'PAPI' # the key of the project you want to have epics updated for
JIRA_EPIC_STATUS_TO_UPDATE = '("Shovel Ready","Being Built","Pending Release")' # A JQL-ish list of statuses you want magic done for

jira_options = {'server': 'https://jwplayer.atlassian.net'}
jira = JIRA(jira_options, basic_auth=(JIRA_USERNAME,JIRA_PASSWORD))

epics_to_update = jira.search_issues('project = ' + JIRA_PROJECT + ' and issuetype = Epic and status in ' + JIRA_EPIC_STATUS_TO_UPDATE)

for epic in epics_to_update:
	# find the Epic fixVersion and make it correct
	print('Updating Epic:' + epic.key + ' - ' + epic.fields.summary)
	epic_version_name = 'Epic - ' + epic.fields.summary
	found_epic_fix_version = False
	for fix_version in epic.fields.fixVersions:
		if fix_version.name[0:4] == 'Epic':
			found_epic_fix_version = True
			version_id = fix_version.id
			epic_version = jira.version(version_id)
			epic_version.update(
				name=epic_version_name,
				description= 'Epic release version for ' + epic.key + ' \n' + epic.fields.summary,
				startDate= epic.fields.customfield_12200,
				releaseDate= epic.fields.customfield_12201
				)
			print('Updated fixVersion: ' + epic_version.name)
			break

	if found_epic_fix_version == False:
		new_version = jira.create_version(
			project=JIRA_PROJECT,
        	name=epic_version_name,
			description= 'Epic release version for ' + epic.key + ' \n' + epic.fields.summary,
			startDate= epic.fields.customfield_12200,
			releaseDate= epic.fields.customfield_12201,
        	released=False)
		all_fix_versions = []
		for fix_version in epic.fields.fixVersions:
			all_fix_versions.append({'name': fix_version.name})
		all_fix_versions.append({'name': epic_version_name})
		epic.update(fields={'fixVersions': all_fix_versions})
		print('Created and added new fixVersion to Epic ' + epic.key)


	total_points = 0
	all_epic_fix_versions = [{'name': epic_version_name}]
	# sum up all the children's points and add them to the Epic fixVersion
	for child in jira.search_issues('project = ' + JIRA_PROJECT + ' and "Epic Link" = ' + epic.key):
		if 'customfield_10005' in child.fields.__dict__.keys():
			total_points = total_points + (child.fields.customfield_10005 or 0)
		all_fix_versions = []
		already_has_epic_version = False
		for fix_version in child.fields.fixVersions:

			if not {'name': fix_version.name} in all_epic_fix_versions:
				all_epic_fix_versions.append({'name': fix_version.name})
			
			if fix_version.name == epic_version_name:
				already_has_epic_version = True
				print(child.key + ' already had the Epic fixVersion')
			else:
				all_fix_versions.append({'name': fix_version.name})

		if already_has_epic_version == False:
			all_fix_versions.append({'name': epic_version_name})
			child.update(fields={'fixVersions': all_fix_versions})
			print('Added fixVersion "' + epic_version_name +'" to ' + child.key)

	#update total_points
	epic.update(fields={'customfield_12305':total_points})
	print('Epic ' + epic.key + ' now has ' + str(total_points) + ' points.')
	
	# add all child fixVersions to the epic
	epic.update(fields={'fixVersions': all_epic_fix_versions})
	print('Epic ' + epic.key + ' now has ' + str(len(all_epic_fix_versions)) + ' FixVersions.')

print('All Done')
