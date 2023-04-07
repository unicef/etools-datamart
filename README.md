eTools DataMart
===============

[![CircleCI](https://circleci.com/gh/unicef/etools-datamart/tree/develop.svg?style=svg&circle-token=)](https://circleci.com/gh/unicef/etools-datamart/tree/develop)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/819135a936894e678066e895604fd24f)](https://www.codacy.com/app/UNICEF/etools-datamart?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=unicef/etools-datamart&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/unicef/etools-datamart/branch/develop/graph/badge.svg)](https://codecov.io/gh/unicef/etools-datamart)

[![docker-badge]][docker]
[![microbadger-badge]][microbadger-link]


UNICEF eTools API and Datamart



### Project Links

 - Continuos Integration - https://circleci.com/gh/unicef/etools-datamart/tree/develop
 - Source Code - https://github.com/unicef/etools-datamart
 - Codacy - https://app.codacy.com/project/unicef/etools-datamart/dashboard
 - Docker - https://hub.docker.com/r/unicef/datamart/
 

[docker-badge]: https://images.microbadger.com/badges/version/unicef/datamart.svg
[docker]: https://hub.docker.com/r/unicef/datamart "Download docker image"

[microbadger-badge]: https://images.microbadger.com/badges/image/unicef/datamart.svg
[microbadger-link]: https://microbadger.com/images/unicef/datamart "Docker image infos"


### restore environment

#### Non replicable tables

* unicef_security_user_groups
* unicef_security_users
* unicef_rest_framework_export

#### Partner refresh every 4 hours

scheduler 0 0,4,8,12,16,20 * * *

#### Tasks

- Preload: 1.00 am
- Force Refresh: * 1 * * 0 (304 cached)