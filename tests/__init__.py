import sys

if sys.argv[-1] == 'tests':
    print("\n----------------------------------------------------------------------")
    print("Please, run each type of tests separately. Ex:")
    print("$ python -m unittest tests.unit")
    print("$ python -m unittest tests.integration")
    print("$ python -m unittest tests.acceptance")
