Contributing
============

eTools
======

Each time eTools data models changes, it's needed to rebuild the datamart models and the sql
needed to run the tests

create or get a dump
--------------------

    pg_dump -Fc -Upostgres -a etools > etools_hope.sql

update dump location env var
----------------------------
    ETOOLS_BACKUP

update schema & check clean step
--------------------------------

update schema & check clean step

    cd db
    sh update_etools_schema.sh (gives error)
    sh update_etools_schema.sh -nd

Looks like there's a record failing import Intervention CHD/SSFA201853
while replacing chad with lebanon, 256 constraint raises
needed to replace it manually in dump 3
(Accord de financement pour la mise en oeuvre des activites de soins de sante et de nutrition d’urgence aux refugies, deplaces internes, retournes et populations hotes affectes par la crise nigeriane dans la region du Lac )

    open /Users/jojo/workspace/datamart/src/etools_datamart/apps/multitenant/postgresql/tenant3.sql
    
fix tests & update update COUNT_PARTNERS_PARTNERORGANIZATION
    
    pytest tests/api/interfaces/
    pytest tests/multitenant/


PRP
===    
    python manage.py inspectprp

Initialize app
==============

   Create a `.env` file in the root folder based on the content for `.env.tpl`

    $ pipenv sync
    $ pipenv shell
    $ ./manage.py init-setup --all
    $ ./manage.py runserver


EtoolsDataMartModel Options
==============

    
If any filtering of the queryset is requested (e.g. records for the past YEAR_DELTA years), 
then make sure to set in Option class, the **sync_deleted_records** flag to False if you don't want the diff records to be deleted: 

    sync_deleted_records = lambda a: False