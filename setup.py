from distutils.core import setup

setup(
    name="Serapeum-backup",
    version="1.0.3",
    author="Pieter De Praetere",
    author_email="pieter.de.praetere@helptux.be",
    packages=[
        "backup",
        "backup.modules.config",
        "backup.modules.ds",
        "backup.modules.files",
        "backup.modules.log",
        "backup.modules.mail",
        "backup.modules.mysql",
        "backup.modules.rdiff",
        "backup.modules.remotes",
        "backup.modules.run",
        "backup.modules"
    ],
    url='',
    license='GPLv3',
    description="Backup script based on rdiff-backup.",
    long_description=open('README.txt').read(),
    scripts=[
        'bin/serapeum-backup'
    ],
    data_files=[
        ('config', ['config/example.ini']),
        ('remotes', ['remotes/list.json']),
        ('selection', ['selection/sources.json', 'selection/excludes.json'])
    ]
)
