# 0x01. NoSQL

## Tags

- Back-end
- NoSQL
- MongoDB

## Installation Guide 

        $ wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add -
        $ echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" > /etc/apt/sources.list.d/mongodb-org-4.2.list
        $ sudo apt-get update
        $ sudo apt-get install -y mongodb-org
        ...
        $  sudo service mongod status
        mongod start/running, process 3627
        $ mongo --version
        MongoDB shell version v4.2.8
        git version: 43d25964249164d76d5e04dd6cf38f6111e21f5f
        OpenSSL version: OpenSSL 1.1.1  11 Sep 2018
        allocator: tcmalloc
        modules: none
        build environment:
            distmod: ubuntu1804
            distarch: x86_64
            target_arch: x86_64
        $  
        $ pip3 install pymongo
        $ python3
        >>> import pymongo
        >>> pymongo.__version__
        '3.10.1'

## Projects

Write a script that lists all databases in MongoDB.
- [0-list_databases](/0x01-NoSQL/0-list_databases)

Write a script that creates or uses the database my_db
- [1-use_or_create_database](/0x01-NoSQL/1-use_or_create_database)
