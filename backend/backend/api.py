import sys

from flask_restless import APIManager
from backend.models import Request
from backend.queue import q
from backend.tasks import get_links_on_page 

def post_requests_postprocessor(result=None,**kw):
    print("we got in here!", file=sys.stderr)
    print(result, file=sys.stderr)
    if 'id' in result:
        if result['id'] is not None:
            get_links_on_page.delay(result['url'], result['id'],
                                    result['depth'],0,result['keyword'],
                                    result['searchmode'])
    return

# Start API-Manager
apimanager = APIManager()

# Create first API endpoint
apimanager.create_api(Request,
                      collection_name='requests',
                      methods=['GET','POST','DELETE'],
                      postprocessors=
                          {'POST': [post_requests_postprocessor]})
