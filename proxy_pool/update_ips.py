from dboperations.db import DbOperation
from util import checks


if __name__ == '__main__':
    mydb = DbOperation()
    while True:
        checks.update_info(mydb)
