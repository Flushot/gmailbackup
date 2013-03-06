#!/usr/bin/env python
from __future__ import print_function

import os
import email
import imaplib

# gmail credentials
USERNAME = 'username@gmail.com'
PASSWORD = 'wouldntyouliketoknow'

# directory *.eml files are stored in
emailPath = 'email'
if not os.path.exists(emailPath):
	os.mkdir(emailPath)

client = imaplib.IMAP4_SSL('imap.gmail.com', 993) # connect
login_method = client.login_cram_md5 if 'AUTH=CRAM-MD5' in client.capabilities else client.login
login_method(USERNAME, PASSWORD) # login

client.select('[Gmail]/All Mail', readonly=True)
typ, messageIds = client.search(None, 'ALL') # search for all messages
messageIds = messageIds[0].split()
total = len(messageIds)
count = 0
for messageId in messageIds:
	emailFile = '%s/%s.eml' % (emailPath, messageId)
	if os.path.exists(emailFile) and os.stat(emailFile).st_size > 0:
		continue
	typ, data = client.fetch(message_set=messageId, message_parts='(RFC822)') # rfc822 = eml file format
	rawMessage = data[0][1]
	with open(emailFile, 'w+') as f:
		f.write(rawMessage)
	count += 1
	print('%s [ %.2f%% ]' % (messageId, count / (total / 100.0)))
client.close() # close mailbox

client.logout() # logout
