#!/usr/bin/env python
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import gmailbackup


class TestGmailBackup(unittest.TestCase):
    def test_authentication(self):
        # Password can be set by arg
        # User is prompted for password if no arg
        pass

    def test_all_mail(self):
        # All mail is fetched
        pass

    def test_labels(self):
        # One or more label
        # Zero labels has default
        pass

    def test_output_path(self):
        # Output folder gets created if it doesn't exist
        # Labels create output path subfolders
        pass


if __name__ == '__main__':
    unittest.main()
