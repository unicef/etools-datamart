## Collaborate

### Prerequisites

 - [pipenv](https://github.com/pypa/pipenv)
 - [docker](https://www.docker.com/get-docker)
 - [pipsi](https://github.com/mitsuhiko/pipsi/)



setup local en0 alias 

    $ sudo ifconfig en0 alias 192.168.66.66

### Initialize app
   
   Create a `.env` file in the root folder based on the content for `.env.tpl`
   
    $ pipenv sync
    $ pipenv shell
    $ ./manage.py init-setup --all
    $ ./manage.py runserver


### How to run tests

Each time Etools data models changes, it's needed to rebuild the datamart models and the sql
needed to run te tests

- Rebuild django models

        $ ./manage.py inspectschema --database etools  > src/etools_datamart/apps/etools/models/public_new.py
        $ ./manage.py inspectschema --database etools --schema=bolivia > src/etools_datamart/apps/etools/models/tenant_new.py

compare ad fix 
    src/etools_datamart/apps/etools/models/tenant_new.py .. tenant.py 
    src/etools_datamart/apps/etools/models/public_new.py .. public.py 
    
- Dump one schema
   
        $  pg_dump --inserts -O -U postgres -p 15432 -h 127.0.0.1 -d etools -n chad | sed 's/chad/[[schema]]/g' >src/etools_datamart/apps/multitenant/postgresql/tenant.sql


- Dump public schema

        $  pg_dump --inserts -O \
                -U postgres -p 15432 -h 127.0.0.1 -d etools -n public \
                --format c \
                --blobs \
                --exclude-table-data celery_* \
                --exclude-table-data django_admin_log \
                --exclude-table-data django_celery_* \
                --exclude-table-data django_migrations \
                --exclude-table-data django_session \
                --exclude-table-data djcelery_* \
                --exclude-table-data drfpasswordless_* \
                --exclude-table-data easy_* \
                --exclude-table-data environment_* \
                --exclude-table-data filer_* \
                --exclude-table-data generic_* \
                --exclude-table-data notification_* \
                --exclude-table-data permissions2_* \
                --exclude-table-data post_office_* \
                --exclude-table-data purchase_order_* \
                --exclude-table-data registration_* \
                --exclude-table-data reversion_* \
                --exclude-table-data social_account_* \
                --exclude-table-data spatial_* \
                --exclude-table-data tpm_partners_* \
                --exclude-table-data unicef_notification_* \
                --exclude-table-data vision_* \
                --exclude-table-data waffle_* \
                -f src/etools_datamart/apps/multitenant/postgresql/public.sqldump
