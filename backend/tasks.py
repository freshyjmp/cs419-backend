"""
In this file we define the tasks for our backend 
 application to perform. 

We would like for these tasks to be performed asynchronously, with the
 goal of building the result set for requests that come in to our 
 backend.

"""

import requests, validators
from celery import Celery, Task
from celery.contrib.methods import task_method
from backend.parser import WaltzHTMLParser
from backend.models import Edge
from backend.db import db

q = Celery('tasks',broker='redis://localhost:6379/0')


class AbstractTask(Task):
    abstract = True


@q.task(name='backend.tasks.get_links_on_page', base=AbstractTask)
def get_links_on_page(url, request, max_depth, current_depth, 
                      keyword, searchmode):

    # We're going to do this santization here for the initial request
    # so I can keep it out of javascript land and ensure that bad 
    # urls don't get populated in the database

    if not url.startswith('http'):
        url = 'http://' + url
    # In order to not make the application hang excessively, I'm setting
    # a timeout.
    try:
        response = requests.get(url, timeout=5)
    except Exception as e:
        raise
    if response.status_code != requests.codes.ok:
        raise ValueError("Expected to get a response for %s, but didn't! Abort! Abort!" % (url))
        return
    parser = WaltzHTMLParser()
    parser.feed(data=response.text)
    kw_was_found = False
    if keyword is not None:
        if response.text.find(keyword) != -1:
                kw_was_found = True

    for link in list(set(parser.links)):

        if link.startswith('/'):
            link = url + link

        if not link.startswith('http'):
            link = 'http://' + link

        if not validators.url(url):
            print("result of validators for %s: %r "  % ( link, validators.url(link)))
            # Try to see if it's a relative link or something
            # simple that would case this validator to fail
            if not validators.url(url + link):
                # give up, we can't fix it
                continue
            # it worked! move on with this as the link
            link = url + link

        e = Edge(request, url, link, current_depth, kw_was_found)
        db.session.add(e)
        db.session.commit()
        # Prepare for danger! Make another task for each link! #YOLO#
        if current_depth < max_depth:
            print("generating task for %s at %d" % (link, current_depth+1))
            get_links_on_page.delay(link, request, max_depth, 
                                        current_depth+1, keyword, searchmode)
    return "impolite words here"
