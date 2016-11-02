from os.path import isfile
import subprocess
import json
from backup.modules.run import Run
from backup.modules.rdiff.__init__ import RdiffRole
import logging
##
# TODO
# Make destination OK
# Use configuration file OK
# Implement delete-older-than OK
# Logger OK


class Files:

    def __init__(self, remote_role, sources_file, destination_path, remote_user, remote_host, ssh_key, excludes_file=None, delete_older_than=None):
        self.rdiff = RdiffRole(remote_role=remote_role, sources=sources_file, destination_path=destination_path,
                               remote_user=remote_user, remote_host=remote_host, ssh_key=ssh_key,
                               excludes=excludes_file, delete_older_than=delete_older_than, sources_is_file=True,
                               excludes_is_file=True)
        self.cmd_output = ''

    def run(self):
        try:
            self.rdiff.run()
        except Exception as e:
            self.cmd_output = self.rdiff.cmd_output
            raise e
        self.cmd_output = self.rdiff.cmd_output
        return True
