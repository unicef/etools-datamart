## Collaborate

### Prerequisites

 - [pipenv](https://github.com/pypa/pipenv)
 - [docker](https://www.docker.com/get-docker)



setup local en0 alias 

    $ sudo ifconfig en0 alias 192.168.66.66

### Initialize app

    $ make init-demo

**Note** `admin` user password will be displayed. You'll need to remember this in
order to login.


 
### Make a release

    
#### Build a Release

Every release should start from develop:

To create ie. release 1.0 we create a branch named `1.0` into `releases` virtual folder
 
    git checkout develop
    git checkout -b releases/1.0
    
This branch contains our "release candidate".

Now we can apply some minor changes like

- bump vesion number
- update CHANGES
- any other release related activity

As we are ready for the release, we commit those changes and push the branch

    git commit -am "bump version 1.0"
    git push origin release/1.0
    
Continuos integration flow on CircleCi does the rest of the job, it:

- run tests
- create a tag named `1.0`
- close the branch and merge it back to `develop` and `master`
- push everything on GitHub
- uses GitHub API to create a releases availiable under https://github.com/unicef/sir-poc-fe/releases
- trigger new CircleCI flow to build Backend Docker image (see https://github.com/unicef/sir-releases)


**Note:** Tagging should follow Semantic Versioning convention. Any tag suffixed with letters (usually `a`,`b`,`c`, `rc`) is marked as `pre-release` 

    
