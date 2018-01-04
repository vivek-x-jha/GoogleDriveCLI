from pprint import pprint

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from apiclient import errors

try:
	import argparse

	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/script-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Apps Script Execution API Python Quickstart'


def getCredentials():
	"""Gets valid user credentials from storage.

	If nothing has been stored, or if the stored credentials are invalid,
	the OAuth2 flow is completed to obtain the new credentials.

	Returns:
		Credentials, the obtained credential.
	"""

	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)

	credential_PATH = os.path.join(credential_dir, 'script-python-quickstart.json')

	store = Storage(credential_PATH)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else:  # Needed only for compatibility with Python 2.6
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_PATH)

	return credentials


def main():
	"""Shows basic usage of the Apps Script Execution API.

	Creates a Apps Script Execution API service object and uses it to call an
	Apps Script function to print out a list of folders in the user's root
	directory.
	"""
	SCRIPT_ID = 'MZEXKHujnMUY2kJIai_mS_FvdjupD22X-'

	# Authorize and create a service object.
	credentials = getCredentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('script', 'v1', http=http)

	# Create an execution request object.
	request = {"function": "getFoldersUnderRoot"}

	try:
		# Make the API request.
		response = service.scripts().run(body=request,
		                                 scriptId=SCRIPT_ID).execute()

		pprint(response)
		if 'error' in response:
			# The API executed, but the script returned an error.

			# Extract the first (and only) set of error details. The values of
			# this object are the script's 'errorMessage' and 'errorType', and
			# an list of stack trace elements.
			error = response['error']['details'][0]
			print(f"Script error message: {error['errorMessage']}")

			if 'scriptStackTraceElements' in error:
				# There may not be a stacktrace if the script didn't start
				# executing.
				print('Script error stacktrace:')
				for trace in error['scriptStackTraceElements']:
					print(f"\t{trace['function']}: {trace['lineNumber']}")
		else:
			# The structure of the result will depend upon what the Apps Script
			# function returns. Here, the function returns an Apps Script Object
			# with String keys and values, and so the result is treated as a
			# Python dictionary (folderSet).
			folderSet = response['response'].get('result', {})
			if not folderSet:
				print('No folders returned!')
			else:
				print('Folders under your root folder:')
				for (folderId, folder) in folderSet.items():
					print(f'\t{folder} ({folderId})')

	except errors.HttpError as e:
		# The API encountered a problem before the script started executing.
		print(e.content)


if __name__ == '__main__':
	main()
