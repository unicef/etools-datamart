eTools DataMart Docker images
=============================

To build docker image simply cd in `docker` directory and run 

    make build
    
default settings are for production ready environment, check `run` target in 
the `Makefile` to see how to run the container with debug/less secure configuration

Standard image contains launch the following components:

    - supervisord
    - application   
    - redis server
    - celery
    - flower

to configure which services should be started, set `SERVICES` appropriately, ie:


    docker run \
        ...
        -e SERVICES="redis,workers,beat,datamart,flower"
        
**Note** If `SERVICES` is empty internal `supervisord` daemon does not start. 


