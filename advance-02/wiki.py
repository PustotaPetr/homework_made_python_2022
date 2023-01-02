import wikipedia
from wikipedia.exceptions import DisambiguationError
from queue import Queue
import threading


wikipedia.set_lang("ru")

WIKI_LINKS_FILE = "wiki_links.txt"
NUM_LINK = 100

page_count = 0
lock = threading.Lock()
queue_title_page = Queue()

def clear_link_file():
    with open(WIKI_LINKS_FILE, 'w') as file:
        file.write('')

def fill_queue_page_title():
    wiki_pages = wikipedia.random(NUM_LINK * 2)
    for title_page in wiki_pages:
        queue_title_page.put(title_page)


def get_page_url():
    global page_count
    while page_count < NUM_LINK:
        title_page = queue_title_page.get()
        try:
            page = wikipedia.page(title=title_page)
        except DisambiguationError as e:
            continue
        except:
            queue_title_page.put(title_page)

        with lock:
            print(title_page, page.url)
            with open(WIKI_LINKS_FILE, 'a') as file:
                file.write(page.url + '\n')
            page_count += 1


def fill_links_file():
    clear_link_file()
    page_count = 0
    for title_page in wiki_pages:
        if page_count == NUM_LINK:
            break

        try:
            page = wikipedia.page(title=title_page)
        except DisambiguationError as e:
            continue

        print(title_page, page.url)
        with open(WIKI_LINKS_FILE, 'a') as file:
            file.write(page.url + '\n')
        page_count += 1


if __name__ == '__main__':
    fill_links_file()
