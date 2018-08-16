## Collaborate

### Prerequisites

 - [pipenv](https://github.com/pypa/pipenv)
 - [docker](https://www.docker.com/get-docker)



setup local en0 alias 

    $ sudo ifconfig en0 alias 192.168.66.66

### Initialize app

    $ pipenv install
    $ pipenv shell
    $ ./manage.py init-setup --all
    $ ./manage.py runserver
