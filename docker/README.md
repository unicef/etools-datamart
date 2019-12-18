eTools DataMart Docker images
=============================

[![](https://images.microbadger.com/badges/version/unicef/datamart.svg)](https://microbadger.com/images/unicef/datamart)

To build docker image simply cd in `docker` directory and run 

    make build
    
default settings are for production ready environment, check `run` target in 
the `Makefile` to see how to run the container with debug/less secure configuration

Image provides following services:

    - datamart   
    - celery workers
    - celery beat
