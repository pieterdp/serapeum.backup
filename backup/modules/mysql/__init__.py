from backup.modules.rdiff.__init__ import RdiffRole
from backup.modules.run import Run
from os.path import isfile, isdir
from os import mkdir, remove
from backup.modules.config import Config
import logging


class MySQLBackup:
    def __init__(self, local_path, server_host, server_user, server_password, backup_destination_path,
                 backup_remote_user, backup_remote_host, backup_ssh):
        self.c = Config(config_file='config/config.ini')
        self.local_path = local_path
        self.server_host = server_host
        self.server_user = server_user
        self.server_password = server_password
        self.destination_path = backup_destination_path
        self.remote_user = backup_remote_user
        self.remote_host = backup_remote_host
        self.remote = self.remote_host
        self.backup_ssh = backup_ssh
        self.cmd_output = ''
        if self.c.config['BACKUP']['remote_role'] == 'backup':
            if not isdir(local_path):
                mkdir(local_path)
        else:
            if not isdir(backup_destination_path):
                mkdir(backup_destination_path)
            self.create_ssh(local_path)

    def dump_command(self, shell=False):
        dump_command = [
            self.c.config['SYSTEM']['mysqldump_path'],
            '--all-databases'
        ]
        if shell is False:
            dump_command += [
                '--user={0}'.format(self.server_user),
                '--password={0}'.format(self.server_password),
                '--host={0}'.format(self.server_host)
            ]
        else:
            dump_command += [
                '--user="{0}"'.format(self.server_user),
                '--password="{0}"'.format(self.server_password),
                '--host="{0}"'.format(self.server_host)
            ]
        return dump_command

    def dump(self):
        Run().zip_output(self.dump_command(), '{0}/dump.sql.gz'.format(self.local_path))
        return True

    def remote_dump(self):
        dump_command = [
            '/usr/bin/ssh',
            '-i',
            self.backup_ssh,
            '{user}@{host}'.format(user=self.remote_user, host=self.remote_host),
            '{command} | /bin/gzip > "{path}/dump.sql.gz"'.format(command=' '.join(self.dump_command(shell=True)),
                                                                path=self.local_path)
        ]
        Run().run(dump_command)
        return True

    def backup(self):
        rdiff = RdiffRole(remote_role=self.c.config['BACKUP']['remote_role'], sources=[self.local_path],
                          destination_path=self.destination_path, remote_user=self.remote_user,
                          remote_host=self.remote_host, ssh_key=self.backup_ssh, delete_older_than='6M',
                          sources_is_file=False, excludes_is_file=False)
        try:
            rdiff.run()
        except Exception as e:
            if self.c.config['BACKUP']['remote_role'] == 'backup':
                remove('{0}/dump.sql.gz'.format(self.local_path))
            else:
                self.remove_ssh('{0}/dump.sql.gz'.format(self.local_path))
            self.cmd_output = rdiff.cmd_output
            raise e
        if self.c.config['BACKUP']['remote_role'] == 'backup':
            remove('{0}/dump.sql.gz'.format(self.local_path))
        else:
            self.remove_ssh('{0}/dump.sql.gz'.format(self.local_path))
        self.cmd_output = rdiff.cmd_output
        return True

    def remove_ssh(self, filename):
        rm_command = [
            '/usr/bin/ssh',
            '-i',
            self.backup_ssh,
            '{user}@{host}'.format(user=self.remote_user, host=self.remote_host),
            'rm "{path}"'.format(path=filename)
        ]
        Run().run(rm_command)
        return True

    def create_ssh(self, directory):
        mkdir_command = [
            '/usr/bin/ssh',
            '-i',
            self.backup_ssh,
            '{user}@{host}'.format(user=self.remote_user, host=self.remote_host),
            'mkdir -p "{path}"'.format(path=directory)
        ]
        Run().run(mkdir_command)
        return True

    def run(self):
        if self.c.config['BACKUP']['remote_role'] == 'backup':
            logging.info('Performing MySQL dump of {0} to {1}::{2}.'
                         .format(self.server_host, self.remote_host, self.destination_path))
        elif self.c.config['BACKUP']['remote_role'] == 'source':
            logging.info('Performing backup of {0} on {1} to {2}.'
                         .format(self.server_host, self.remote_host, self.destination_path))
        if self.c.config['BACKUP']['remote_role'] == 'backup':
            self.dump()
        else:
            self.remote_dump()
        self.backup()
