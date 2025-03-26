import concurrent
import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Thread
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.ERROR)

HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Referer": "https://www.pixiv.net/",
}
PROXIES = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}
PIDS = [
    128546580,
    120395983,
    "119334001",
    "119101871",
    "118898849",
    118792406,
    118760444,
    118682412,
    118589293,
]


def get_filename_from_url(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = path.split("/")[-1]
    return filename if filename else None


def download(url, max_retries=3, retry_delay=3):
    Path("download").mkdir(exist_ok=True)
    for attempt in range(max_retries):
        filename_ = get_filename_from_url(url)
        try:
            res = requests.get(url, proxies=PROXIES, headers=HEADER)
            res.raise_for_status()

            Path(f"download/{filename_}").write_bytes(res.content)
            return True, ""
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                return False, str(e)


def get_durl(pid):
    try:
        pid = str(pid)
        pid_url = f"https://www.pixiv.net/artworks/{pid}"

        res = requests.get(url=pid_url, headers=HEADER)

        soup = BeautifulSoup(res.text, "html.parser")

        meta_tags = soup.find_all("meta")
        global_data = None
        preload_data = None

        for meta in meta_tags:
            if meta.get("name") == "global-data":
                global_data = meta.get("content")
            elif meta.get("name") == "preload-data":
                preload_data = meta.get("content")

        if global_data:
            global_data_json = json.loads(global_data)

        if preload_data:
            preload_data_json = json.loads(preload_data)

        count = preload_data_json["illust"][pid]["pageCount"]
        first_url = preload_data_json["illust"][pid]["urls"]["original"]

        return (
            True,
            [first_url.replace("_p0.", f"_p{i}.") for i in range(count)],
            str(count),
        )
    except Exception as e:
        return False, [], str(e)


durls = []
with ThreadPoolExecutor() as executor:
    futures = {executor.submit(get_durl, pid): pid for pid in PIDS}
    for future in concurrent.futures.as_completed(futures):
        succeed, result, msg = future.result()
        flag = "√" if succeed else "×"
        print(flag, "[get_durl]", futures[future], msg, sep=" ")
        durls.extend(result)

with ThreadPoolExecutor(max_workers=30) as executor:
    futures = {executor.submit(download, durl): durl for durl in durls}
    for future in concurrent.futures.as_completed(futures):
        succeed, msg = future.result()
        flag = "√" if succeed else "×"
        print(flag, "[download]", futures[future], msg, sep=" ")
