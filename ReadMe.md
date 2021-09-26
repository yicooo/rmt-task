This piece of software is written for job application.

Yiğitcan Çoban

Docker is used to create containers and docker-compose is used to manage containers.

Prerequisites:

    - Docker
    - Docker-Compose

Containers:

    - db : Creates a MongoDB database container. 
    - web : Python Flask based web application. 
    - nginx : nginx http server

API Specifications: 

    - Project follows REST principles. Input and output HTTP calls carry json loads.
    - Project is using http://0.0.0.0 and port 80 by default.
    - Endpoints are 
        - /createuser, PUT
        - /login, POST
        - /blocksender, PUT
        - /sendmessage, PUT
        - /showmessages, POST
        - /showloginhistory, POST

Code Structure:
    - nginx folder contains configuration and dockerfile for nginx container
    - app.py -> Flask file to handle requests.
    - config.py -> Configuration of flask-mongoengine
    - models.py -> Contains models which indicates database structure
    - test.py -> Contains unit tests
    - wsgi.py -> Gunicorn uses it
    - functions.py -> Contains helper functions used by app.py
    - Dockerfile -> Indicates python version and creates workspace for Docker
    - docker-composem.yml -> Docker-Compose configurations

Additional Notes: 
    - Tested on MacOS and Ubuntu
    - To test endpoints you can use:
        - 'examplerequest.sh' boilerplate script. In case of any problem about certification (not likely), you can use '--insecure' option.
        - 'test.py' contains some unit tests and example flow. To run this test, you can simply use 'docker-compose run web python test.py'
    - Debug mode is on. DO NOT USE FOR PRODUCTION obviously. 
    - Expected input syntax can be seen as comments in app.py

You may question:
    - Log-in sessions which are stored in persistent memory does not have timeout, each log-in operation creates tokens to authenticate the user.
    - Timestamps are based on UTC +0 because why not.
    - In app.py, jsonify automatically returns status code 200, so for other status codes, they are wrapped with make_response method.