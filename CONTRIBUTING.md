## Collaborate

### Prerequisites

 - [pipenv](https://github.com/pypa/pipenv)
 - [docker](https://www.docker.com/get-docker)


setup local en0 alias

    $ sudo ifconfig en0 alias 192.168.66.66

### Initialize app

   Create a `.env` file in the root folder based on the content for `.env.tpl`

    $ pipenv sync
    $ pipenv shell
    $ ./manage.py init-setup --all
    $ ./manage.py runserver


### How to run tests

Each time eTools data models changes, it's needed to rebuild the datamart models and the sql
needed to run the tests

 
    cd db
    sh update_etools_schema.sh
    
    
Looks like there's a record failing import Intervention CHD/SSFA201853
while replacing chad with lebanon, 256 constraint raises
needed to replace it manually in dump 3

also atm we need django 3.1 to read data

