import queue

import wikipedia
from wikipedia.exceptions import DisambiguationError
from queue import Queue
import threading

from settings import WIKI_LINKS_FILE


wikipedia.set_lang("ru")


NUM_LINK = 100
NUM_THREAD = 5

page_count = 0
lock = threading.Lock()


def clear_link_file():
    with open(WIKI_LINKS_FILE, 'w') as file:
        file.write('')


def fill_queue_page_title():
    queue_title_page = Queue()
    wiki_pages = wikipedia.random(NUM_LINK * 2)
    for title_page in wiki_pages:
        queue_title_page.put(title_page)
    return queue_title_page


def get_page_url(queue_title_page: queue.Queue):
    global page_count
    print(page_count)
    while page_count < NUM_LINK:
        title_page = queue_title_page.get()
        try:
            page = wikipedia.page(title=title_page)
        except DisambiguationError as e:
            print(f"DisambiguationError. Page: {title_page}")
            continue
        except Exception as exc:
            print(f"Exception type: {type(exc).__name__} \n{exc}")
            queue_title_page.put(title_page)
            continue

        with lock:
            print(title_page, page.url)
            with open(WIKI_LINKS_FILE, 'a') as file:
                file.write(page.url + '\n')
            page_count += 1


def fill_links_file():
    clear_link_file()
    queue_title_page = fill_queue_page_title()
    print(queue_title_page.qsize())

    thread_list = [threading.Thread(target=get_page_url, args=[queue_title_page]) for _ in range(NUM_THREAD)]

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()


if __name__ == '__main__':
    fill_links_file()
