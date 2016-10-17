"""
In this file we define the tasks for our backend 
 application to perform. 

We would like for these tasks to be performed asynchronously, with the
 goal of building the result set for requests that come in to our 
 backend.

"""

import requests
from celery import Celery
from backend.parser import WaltzHTMLParser
from backend.models import Edge
from backend.db import db

q = Celery('tasks',broker='redis://localhost:6379/0')

@q.task
def get_links_on_page(url, request, max_depth, current_depth, 
                      keyword, searchmode):
        response = requests.get(url)
        print(response.text)
        if not response:
            raise ValueError("Expected to get a response for %s, but didn't! Abort! Abort!" % (url))
        parser = WaltzHTMLParser()
        parser.feed(data=response.text)
        print(list(set(parser.links)))
        for link in list(set(parser.links)):
            e = Edge(request, url, link, current_depth, False)
            db.session.add(e)
            db.session.commit()
            # Prepare for danger! Make another task for each link! #YOLO#
            if current_depth < max_depth:
                get_links_on_page.delay(link, request, max_depth, 
                                        current_depth+1, keyword, searchmode)
        return "impolite words here"
