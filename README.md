# Gmail Backup

This is a small command-line tool that backs up your Gmail.
It downloads your email messages as RFC822 format *.eml files, which can be opened in most email clients.


## Installation

This requires Python 2.7.
You can install dependencies using this command:

	pip install -r requirements.txt


## Usage Examples

Download all email messages into the "email" folder:

    ./gmail-backup.py -u <username> -p <password>

Download all email messages labeled "foo" and "bar" into their own subfolders:

	./gmail-backup.py -u <username> -p <password> -l foo,bar
