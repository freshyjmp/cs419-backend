from flask_restless import APIManager
from backend.models import Request, Edge

# Start API-Manager
apimanager = APIManager()

# Create first API endpoint
apimanager.create_api(Request,
                      collection_name='requests',
                      methods=['GET','POST','DELETE'])
