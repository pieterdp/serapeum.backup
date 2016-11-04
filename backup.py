#!/usr/bin/env python3
from backup import main
import logging


if __name__ == '__main__':
    if main() is not True:
        logging.error('An error occurred.')
    else:
        logging.info('Run completed.')
