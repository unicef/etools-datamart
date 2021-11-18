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

    pip install django==3.1.13
    cd db
    sh update_etools_schema.sh (gives error)
    sh update_etools_schema.sh -nd
    open /Users/ddinicola/workspace/etools-datamart/src/etools_datamart/apps/multitenant/postgresql/tenant3.sql
    
     
    
Looks like there's a record failing import Intervention CHD/SSFA201853
while replacing chad with lebanon, 256 constraint raises
needed to replace it manually in dump 3
(Accord de financement pour la mise en oeuvre des activites de soins de sante et de nutrition d’urgence aux refugies, deplaces internes, retournes et populations hotes affectes par la crise nigeriane dans la region du Lac )

also atm we need django 3.1 to read data
