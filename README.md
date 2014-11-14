# Gmail Backup

This is a small command-line tool that backs up your Gmail.
It downloads your email messages as [RFC822](http://www.w3.org/Protocols/rfc822/) format *.eml text files, which are compatible with most email clients.


## Installation

This requires Python 2.7.
You can install dependencies using this command:

    pip install gmailbackup


## Command Line Usage

Download all email messages into the "email" directory:

    gmailbackup -u <username> -p <password>

Download all email messages labeled "foo" and "bar" into their own subdirectories under "mydir":

    gmailbackup -u <username> -p <password> -l foo,bar -o mydir

## Python Usage

To get started, use the `GmailClient` class in a `with` statement, authenticate it, then iterate any mailbox (label) you'd like.
The `GmailClient` is a simple wrapper around the IMAP4 client.

    from gmailbackup import GmailClient
    	
    with GmailClient() as client:
        client.authentiate('me@gmail.com', 'mypassword')
        client.save_mailbox('Some Label', 'path/to/downloads')

