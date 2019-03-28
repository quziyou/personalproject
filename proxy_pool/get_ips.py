from dboperations.db import DbOperation
from multiprocessing import Process
from config import CRAWL_URL
from util import checks
import random
import time

times = [300, 600, 900]

if __name__ == '__main__':
    mydb = DbOperation()
    mydb.init_db()
    while True:
        process_list = []
        for i in range(len(CRAWL_URL)):
            p = Process(target=checks.merge_info, args=(CRAWL_URL[i], mydb))
            process_list.append(p)
        for process in process_list:
            process.start()
        for process in process_list:
            process.join()
        time.sleep(random.choice(times))
