# Blog API
ViBlogAPI, api for managing a blogging application, with user, token authentication, comments, likes and tags, with tests and documentation, using Test Driven Development.
> Python-DjangoRestFramework

## Table of contents
* [Technologies](#technologies)
* [Requirements](#requirements)
* [Setup](#setup)
* [Run Project](#run-project)
* [Run Tests](#run-tests)
* [Documentation](#documentation)
* [Contact](#contact)

<p align='center'>
  <img src="https://blog.mailrelay.com/wp-content/uploads/2018/03/que-es-un-blog-1.png" width="500" >
</p>

## Technologies
* Python
* Django
* DjangoRestFramework
* Heroku
* Swagger UI Documentation

## Requirements
* Git
* Python
* pip
* venv

## Setup
1. Clone and enter the repository:\
`git clone https://github.com/Erick-ViBe/ViBlogAPI.git`\
`cd ViBlogAPI`

2. Create and activate virtual environment:\
`python3 -m venv env`\
`source env/bin/activate`

> To disable the virtual environment: `deactivate`

3. Install all dependencies:\
`pip install -r requirements.txt`

4. Apply migrations:\
`python3 manage.py migrate`

## Run Project
`python3 manage.py runserver`

## Run Tests
`python3 manage.py test`

## Documentation
* [@Swagger UI](https://viblog.herokuapp.com/docs/)
* [@JSON](https://viblog.herokuapp.com/docs.json)

## Contact
Created by [@ErickViBe](https://erickvibe.xyz/) - feel free to contact me!
