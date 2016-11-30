"""
In this file we define the tasks for our backend
 application to perform.

We would like for these tasks to be performed asynchronously, with the
 goal of building the result set for requests that come in to our
 backend.

"""

import requests
import validators
from urllib.parse import urlparse
from celery import Celery, Task
from celery.contrib.methods import task_method
from backend.parser import WaltzHTMLParser
from backend.models import Edge
from backend.db import db
from sqlalchemy import and_

q = Celery('tasks',broker='redis://localhost:6379/0')


class AbstractTask(Task):
    abstract = True

def validate_link(url, link):

    # Sometimes links may not be as pretty as we expect,
    # try to handle them here so that we can succeed in
    # more cases
    if link == '':
        return False

    parsed_url = urlparse(url)
    parsed_link = urlparse(link)

    if parsed_url.scheme == '':
        url = 'http://' + url
        # noticed that the netloc is empty and misplaced in the path
        # when there is no scheme provided. Add a default scheme
        # and reparse for more successes
        parsed_url = urlparse(url)

    new_link = ''
    if parsed_link.netloc == '':
        if parsed_url.netloc != '' and parsed_link.path != '':
            new_link = parsed_url.scheme + '://' + parsed_url.netloc
            if parsed_link.path.startswith('/'):
                new_link += parsed_link.path
            else:
                new_link += '/' + parsed_link.path
            print("appended scheme to %s" %(new_link))
        else:
            return False
    else:
        new_link = link

    if validators.url(new_link) is False:
        return False
    # if validators.url(new_link) is False:
    #     print("result of validators for %s: %r "  % ( link, validators.url(link)))
    #     # Try to see if it's a relative link or something
    #     # simple that would case this validator to fail
    #     if validators.url(url + link) is False:
    #         # give up, we can't fix it
    #         return False
    #     else:
    #         print("prepended %s to %s" % (url, link))
    #         link = url + link
    #     # it worked! move on with this as the link
    return new_link

def check_for_keyword(response, keyword):
    if keyword is not None and response.text.find(keyword) != -1:
        return True
    else:
        return False

def make_request(url):
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
        print(e)
        return False
    if response.status_code != requests.codes.ok:
        print("Expected to get a response for %s, but didn't! Skipping." % (url))
        return
    else:
        return response

def recursive_dfs_approach(url, visited, request, max_depth, current_depth, keyword, parser):
    # I'm not proud of this.
    response = make_request(url)
    if not response:
        # Just quit, no response means it's pointless to proceed
        return visited
    parser.feed(data=response.text)
    kw_was_found = check_for_keyword(response, keyword)
    # Hard capping this at 10
    link_set = list(set(parser.links))[:10]
    print(link_set)
    print(url)
    for link in link_set:
        index = link_set.index(link)
        request_link = validate_link(url, link)
        if request_link is False:
            print("Failed to validate link, skipping")
            continue
        # Database action here, add the found edge to database
        e = Edge(request, visited, url, request_link, current_depth, kw_was_found)
        visited += 1
        db.session.add(e)
        db.session.commit()
        if kw_was_found is True:
            print("Found keyword at the %dth page" % visited)
            return -1
        if current_depth < max_depth:
            print("DFS Recursion - idx:%d link:%s depth: %d visited:%d" % (index, request_link, current_depth+1, visited))
            # Recursion should make the search appear like a stack.
            # The most recent links are the ones we check first.
            visited = recursive_dfs_approach(request_link, visited, request, max_depth,
                                    current_depth+1, keyword, parser)
            # If we encounter a keyword, we have to stop processing but also
            # bubble this up so we don't process any more links
            if visited == -1:
                print("We found the keyword!")
                return -1

    return visited

@q.task(name='backend.tasks.get_links_on_page', base=AbstractTask)
def get_links_on_page(url, request, max_depth, current_depth,
                      keyword, searchmode):

    # I'm going to try two approaches here. For the DFS approach, we'll
    # re-use the parser class since we are going to do some ugly
    # recursion, completely negating the cool task system we use with the BFS
    # approach.

    parser = WaltzHTMLParser()
    visited = 0
    if searchmode == 'DFS':
        recursive_dfs_approach(url, visited, request, max_depth, current_depth, keyword, parser)
    elif searchmode == 'BFS':
        if keyword is not None:
            was_kw_found = Edge.query.filter(and_(Edge.request == request,
                  Edge.had_keyword == True)).count()
            print("was_kw_found was %d" % was_kw_found)
            if was_kw_found != 0:
                print("Another task found the keyword!")
                return
        # make the request
        response = make_request(url)
        if not response:
            # Just quit, no response means it's pointless to proceed
            return
        # Run response text through our parser to get the links
        parser.feed(data=response.text)
        # Check for the keyword in the response text
        kw_was_found = check_for_keyword(response, keyword)

        for link in list(set(parser.links)):
            # Many of our links are poorly-formatted or garbage, try to fix
            # them if possible
            link = validate_link(url, link)
            if link is False:
                continue
            # Database action here, add the found edge to database
            e = Edge(request, visited, url, link, current_depth, kw_was_found)
            db.session.add(e)
            db.session.commit()
            if kw_was_found is True:
                return "I got what I need"
            # Prepare for danger! Make another task for each link!
            if current_depth < max_depth:
                print("generating task for %s at %d" % (link, current_depth+1))
                get_links_on_page.delay(link, request, max_depth,
                                        current_depth+1, keyword, searchmode)

    return "impolite words here"
