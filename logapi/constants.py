import os
import sys

# We assume all tests ran have the word 'test' in the command line
# This assumption may prove untrue if we wrap running the test in other commands
IS_TEST = 'test' in sys.argv

LOGS_DIRECTORY = '/var/log'

if IS_TEST:
  LOGS_DIRECTORY = os.path.join(os.getcwd(), 'tests/log')
    
