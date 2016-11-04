# backup

This script will perform a backup of a list of folders on your server and a dump of your MySQL database, and copy them both to a remote backup server via rdiff-backup. Failed runs will result in an email being sent.

It can be run in two ways: either to create a backup of a local system and store it on a remote server (_case 1_) or create a backup of a remote server and store it on a local system (_case 2_).

## Configuration
The application is designed to be used when you have a lot of servers, which contain mostly web applications, with assorted databases, and you want them all backed up hassle-free to a remote backup server. It is meant to be used on your server, not on your backup server.

All configuration options are in `config/config.ini`. Copy the provided `example.ini` file and modify its settings.

### Role

The setting `remote_role` determines whether the script will run as _case 1_ or as _case 2_.

* Setting it to `backup` will create a backup of the local system (i.e. _case 1_) and use the remote (hence the term `remote_role`) as its backup location.

* Setting it to `source` will create a backup of the remote system (_case 2_) and store the backup locally.

The key `backup_path` contains the path the backups will be written to, either a local path (_case 2_) or a remote (_case 1_) one. If it is a remote path, you do not have to include `user` and `host` (e.g. `user@host::path`), as this will be generated automatically from the remote configuration.

### File selection

`sources_file` and `excludes_file` refer to the selection of files (or directories) you want to backup. Both files must be json-files which have a key called `list`, which contains a list of fully qualified directories.

* `sources_file` contains a list of directories or files you want to have backed up.

* `excludes_file` has a list of files or directories inside your source directories you want to exclude from backing up. If, for example, you have `/home/pieter` in your `sources_file`, but want to exclude _LargeDir_ from the backup, you specify `/home/pieter/LargeDir` inside your `excludes_file`.

Your entire path will be replicated inside your backup location. If you specified `/home/pieter` inside `sources_file` your remote location will contain `/home/pieter` (and not just `pieter`, which some applications might do).

### Remote configuration
The application interacts with your remote backup server using rdiff-backup and ssh keys. You must have rdiff-backup installed on the remote server, inside `/usr/bin`. You must also have a user that is allowed to connect via ssh, with a key, and has the necessary rights to run `/usr/bin/rdiff-backup` as `sudo` without a password.

* `remote_user`, `remote_ssh` and `remote_loc` configure the remote. `remote_loc` contains the address (IP or FQDN) of your remote system. `user` and `ssh` refer to the user you want to log in as and the location of the private ssh key on this system.

#### Multiple remotes

It is possible to define multiple remotes, which will, depending on the setting of `remote_role`, be used to store your backups (_backup_) or be backed up (_source_). The remotes must be in a file in JSON-format with a key called `list`, containing either the IP addresses or the FQDN of every remote.

You must specify the location of the list as the `remote_list` parameter and remove the `remote_loc` key. Only one of those can appear in your configuration file.

If the `remote_role` is _source_, the script will create a subdirectory inside `backup_path` for every remote (using the IP/FQDN as defined in the list), in which the backups will be stored. This should prevent backup mix-ups.

The `remote_`-configuration in the MySQL section has the same functionality and is configured in the same manner.

### MySQL configuration

Backing up a MySQL installation can be enabled or disabled through the `backup_mysql` setting.

The application uses the `mysqldump` utility to perform backups of your MySQL (or equivalent) server. All databases will be dumped and the dump will be stored locally and then transferred to the remote location using rdiff-backup. The local copy will be deleted (for security reasons).

* `local_path` is the directory the dump will be stored in. This directory must exist. Not that this can be a path on a remote system if `remote_role` is set to `source`.

* `host`, `username` and `password` must refer to a user that has the necessary rights to execute a dump of the entire MySQL installation. This requires `SELECT`, `LOCK TABLES`, `SHOW VIEW` and `RELOAD` privileges on all databases.

* `remote_user`, `remote_ssh`, `remote_loc`/`remote_list` and `backup_path` are used to configure rdiff-backup for the backup of the MySQL dump. They can be the same settings as for the back-up of your files (see _Remote configuration_), but this is not a requirement.

### Email configuration

When a backup job fails, the application sends of an email with the output of rdiff-backup or mysqldump.

* `mail_dest` has the email address of the recipient (e.g. you).

* `smtp_server`, `smtp_port`, `smtp_username` and `smtp_password` configure the connection to a SMTP server.

## Usage

This script is designed to run in a cron job without any intervention. All settings must be set in the configuration file, command line parameters are not supported.
