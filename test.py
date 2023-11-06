#!/usr/bin/python3

import time
import requests
import concurrent.futures

PRED_URL = "http://localhost:8080/predictions/mike"
WORKERS = 4
REQUESTS = 10000

session = None


def initializer():
    global session
    session = requests.Session()


def worker(data):
    headers = {"Content-Type": "image/jpg"}
    with open(path, "rb") as f:
        data = f.read()
    req = requests.Request("POST", PRED_URL, data=data, headers=headers).prepare()
    global session
    resp = session.send(req)
    return (path, resp.text)


with concurrent.futures.ProcessPoolExecutor(
    max_workers=WORKERS, initializer=initializer
) as executor:
    futures = []
    start_time = time.time()
    for i in range(REQUESTS):
        path = "a321.jpg"
        futures.append(executor.submit(worker, path))
    uniq_results = {future.result() for future in futures}
    elapsed = time.time() - start_time
    print(uniq_results)
    print()
    print(elapsed, "s", REQUESTS / elapsed, "req/s")
