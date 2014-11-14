#!/usr/bin/env python
from __future__ import print_function

import os
import sys
import email
import imaplib
import logging
import getpass
import hashlib

import argparse


# Gmail server
IMAP_HOST = 'imap.gmail.com'
IMAP_PORT = 993
DEFAULT_FOLDER = '[Gmail]/All Mail'

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Gmail backup tool')
    parser.add_argument('-u', '--username', metavar='username', required=True,
                        help='Gmail username')
    parser.add_argument('-p', '--password', metavar='password', 
                        help='Gmail password')
    parser.add_argument('-o', '--output-path', metavar='directory', default='email',
                        help='Output directory where *.eml files will be downloaded to')
    parser.add_argument('-l', '--labels', metavar='label1,labelN,...',
                        help='Comma-separated list of labels to download (when omitted, downloads all mail)')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode')
    args = vars(parser.parse_args())

    # Init logging
    logging.basicConfig(level=logging.DEBUG if args['debug'] else logging.INFO)

    # Get username and password
    username = args['username']
    password = args.get('password')
    if not password:
        # Prompt for password, since it wasn't specified as an arg
        password = getpass.getpass('Password for %s: ' % username)
        if not password:
            print('Password is required!', file=sys.stderr)
            return 1

    # Directory *.eml files are stored in
    output_path = args['output_path']
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    # Connect to server
    client = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)

    # Determine authentication method
    if 'AUTH=CRAM-MD5' in client.capabilities:
        login_method = client.login_cram_md5
    else:
        login_method = client.login

    # Authenticate
    try:
        login_method(username, password)
    except imaplib.IMAP4.error, ex:
        logger.error('Authentication error: %s' % ex.message)
        return 1

    logger.info('Logged in as %s' % username)

    try:
        # Iterate folders
        folders = map(lambda x: x.strip(), args.get('labels', DEFAULT_FOLDER).split(','))
        for folder in folders:
            logger.info('Selecting "%s" folder...' % folder)
            client.select(folder, readonly=True)
            try:
                # Determine download path
                if folder == DEFAULT_FOLDER:
                    folder_path = 'inbox'
                else:
                    folder_path = folder
                folder_output_path = os.path.join(output_path, folder_path)
                if not os.path.exists(folder_output_path):
                    os.mkdir(folder_output_path)

                # Search for messages in folder
                message_type, messages_indices = client.search(None, 'ALL') # search for all messages
                messages_indices = messages_indices[0].split()

                # Iterate messages
                total_messages = len(messages_indices)
                download_count = 0
                for message_index in messages_indices:
                    # Download message in RFC822 (*.eml file) format
                    message_type, message_data = client.fetch(message_set=message_index, 
                                                              message_parts='(RFC822)')
                    raw_message = message_data[0][1]

                    # Parse real message ID from message
                    # Using a SHA-256 hash because message IDs may contain chars incompatible with filesystem paths
                    parsed_message = email.message_from_string(raw_message)
                    message_key = hashlib.sha256(parsed_message['Message-ID']).hexdigest()

                    # Determine file name (should be unique after multiple runs)
                    email_file = '%s/%s.eml' % (folder_output_path, message_key)
                    if os.path.exists(email_file) and os.stat(email_file).st_size > 0:
                        logger.warn('Skipping %s...' % email_file)
                        continue

                    with open(email_file, 'w+') as f:
                        f.write(raw_message)

                    download_count += 1
                    logger.info('Downloaded message %s [ %.2f%% ]' % (message_key, download_count / (total_messages / 100.0)))

                return 0

            finally:
                # Close mailbox
                logger.info('Closing mailbox...')
                client.close()

    except KeyboardInterrupt, ex:
        if args['debug']:
            raise ex
        else:
            logger.warn('^C pressed. Terminating...')

    finally:
        # Logout
        logger.info('Logging out...')
        client.logout()


if __name__ == '__main__':
    sys.exit(main())
