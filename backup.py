#!/usr/bin/env python3
from backup import main
from backup.modules.log import logger


if __name__ == '__main__':
    if main() is not True:
        logger.error('An error occurred.')
    else:
        logger.info('Run completed.')
