# CS419 Capstone Project - flask backend

For this project we are implementing a graphical web crawler. The user will be able to input a URL, specify Depth-First-Search or Breadth-First-Search, depth of the graph, and an optional keyword to mark the resulting nodes if the keyword appears in that node. 

I am implementing the backend of this application. It consists of the following components:

* A Flask web server
* SQLite for persistent data storage of user requests
* A Redis task queue for processing the url requests and the subsequent child work created from them

The idea is that the child requests of building the graph can be very time-consuming. It would be better to have the frontend poll the backend server for updates while the application does the necessary HTTP requests, parses the output, and generates new HTTP requests for the next level of the graph.

### Getting Started

Check out the repository to whatever directory you want.

1. Enable the virtual environment

```
virtualenv --no-site-packages -p python3 venv
source ./venv/bin/activate
pip install -r ./requirements.txt
```

You will now be in the virtual environment. You can leave this by typing 
``` deactivate ```

2. Start the backend in a terminal
```
python -m backend.app
```

3. Access the application at http://localhost:5000. 


4. Make an HTTP POST request (you should install httpie for this, it's great!)
```
http POST localhost:5000/api/requests/ url=http://myfunwebsite.com keyword=fun dept=5 searchmode=DFS
```

5. View the data
..*Can go to http://localhost:5000/api/request to see all requests
..*Or can go to http://localhost:500/api/request/<your request id> to see a single request
..*Or you can use sqlite3 on /tmp/test.db to see the data. 



