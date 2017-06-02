###----Yash Shah----###
#---1001111714---#
#---Assignment 1 Cloud-Dropbox Encryption and signing with verify---#
#---Reference---
#---https://www.dropbox.com/developers/core/start/python
#---https://pythonhosted.org/python-gnupg/
#---http://stackoverflow.com/questions/479343/how-can-i-build-a-recursive-function-in-python
#---http://stackoverflow.com/questions/3964681/find-all-files-in-directory-with-extension-txt-with-python


import dropbox
import glob
import os
import gnupg

# App key and secret from the Dropbox developer website
app_key = '******'
app_secret = '******'

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

# The user sign in and authorize this token
authorize_url = flow.start()
print '1. Go to: ' + authorize_url
print '2. Click "Allow" (you might have to log in first)'
print '3. Copy the authorization code.'
code = raw_input("Enter the authorization code here: ").strip()


# This will fail if the user enters an invalid authorization code
access_token, user_id = flow.finish(code)


client = dropbox.client.DropboxClient(access_token)
print 'linked account: ', client.account_info()

directory='/Users/yashshah792/Desktop/Cloud/Dropbox/Utility'
dictionary_of_files_present={}
dictionary_of_files_added={}

# This will recursively call the function again if there name is a directory
def scandir(directory):
	dictionary_of_files_added.clear()
	for name in glob.glob(os.path.join(directory, '*')):
		if os.path.isdir(name):
			scandir(name)
		# As the file is already present hence will do nothing
		elif dictionary_of_files_present.has_key(os.path.basename(name)):
			'Do nothing'# Do Nothing as this file is already present
		else:
			# File is added to both the dictionaries 
			dictionary_of_files_added[os.path.basename(name)] = name
			dictionary_of_files_present[os.path.basename(name)] = name

	scandir(directory)
# We put this in a try block as this is an infinite loop and will always check for the directory as it has been called recursively.
gpg = gnupg.GPG(gnupghome='/Users/yashshah792/Desktop/Cloud/Dropbox/Utility/GUNPG/gnupg')
try:
       while True:
               for key, value in dictionary_of_files_added.iteritems():
                       fileName = os.path.splitext(key) # This will give name without the extension
                       outputFile = value
                       with open(outputFile, 'rb') as f:
                               status = gpg.encrypt_file( f, recipients=['yashashah@mavs.uta.edu'], sign = 'yash', passphrase='abcde',  output='Enc.txt.gpg')
                               
                       f = open('Enc.txt.gpg', 'rb')
                       response = client.put_file('/Encrypted_File.txt.gpg', f)
                       print 'ok: ', status.ok
                       print 'status: ', status.status
                       print 'stderr: ', status.stderr
                       print "uploaded:", response

                       f, metadata = client.get_file_and_metadata('/Encrypted_File.txt.gpg')
                       out = open('Encrypted_File.txt.gpg', 'wb')
                       out.write(f.read())
                       out.close()
                       print metadata


                       with open('Encrypted_File.txt.gpg', 'rb') as f:
                               status = gpg.decrypt_file(f, passphrase='abcde', output='/Users/yashshah792/Desktop/Cloud/Dropbox/dec.txt')

                       h = open('/Users/yashshah792/Desktop/Cloud/Dropbox/dec.txt', 'rb')
                       #response = client.put_file('/Decrypted_File.txt', h)
                       verified = gpg.verify_file(d)
                       print 'Verified', verified
                       print 'ok: ', status.ok
                       print 'status: ', status.status
                       print 'stderr: ', status.stderr

                       
               scandir(directory)
except (KeyboardInterrupt, SystemExit):
       print "Program Stopped"	
