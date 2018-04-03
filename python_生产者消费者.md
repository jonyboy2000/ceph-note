from boto3.session import Session
import boto3
import argparse, Queue, logging, random, sys
import multiprocessing, signal, re
from multiprocessing.pool import ThreadPool


access_key = "user001"
secret_key = "user001"
url = "http://127.0.0.1"
session = Session(access_key, secret_key)
client = session.client('s3', endpoint_url=url)


paginator = client.get_paginator('list_objects')
operation_parameters = {'Bucket': 'bucket1',
                        'MaxKeys': 1000}

page_iterator = paginator.paginate(**operation_parameters)

def deleter(rmQueue):
    while True:
        rmKey = rmQueue.get()
        print "DELETE KEY:", rmKey
        with keysDeleted.get_lock():
            keysDeleted.value += 1
        rmQueue.task_done()

def listInit(arg2):
    global rmQueue
    rmQueue = arg2

def lister(page_iterator):
    for page in page_iterator:
        for item in page['Contents']:
            print "GET KEY:", item['Key']
            rmQueue.put(item['Key'])
            with keysFound.get_lock():
                keysFound.value += 1

def main():
    rmQueue = Queue.Queue(maxsize=100)
    signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
    global keysFound, keysDeleted
    keysFound = multiprocessing.Value("i", 0)
    keysDeleted = multiprocessing.Value("i", 0)
    listThreads = 1
    deleteThreads = 100
    deleterPool = ThreadPool(processes=deleteThreads,
                             initializer=deleter, initargs=(rmQueue,))

    listerPool = ThreadPool(processes=listThreads,
                            initializer=listInit, initargs=(rmQueue,))

    page_iterators = []
    page_iterators.append(page_iterator)

    listerPool.map(lister, page_iterators)
    rmQueue.join()
    print "keysFound.value", keysFound.value
    print "keysDeleted.value", keysDeleted.value

if __name__ == "__main__":
    main()





