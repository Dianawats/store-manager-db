[![Build Status](https://travis-ci.org/Dianawats/store-manager-db.svg?branch=develop-db)](https://travis-ci.org/Dianawats/store-manager-db)
[![Coverage Status](https://coveralls.io/repos/github/Dianawats/store-manager-db/badge.svg?branch=develop-db)](https://coveralls.io/github/Dianawats/store-manager-db?branch=develop-db)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0e8d6a26c54142b3a2b367fbabcf4b82)](https://www.codacy.com/app/Dianawats/store-manager-db?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Dianawats/store-manager-db&amp;utm_campaign=Badge_Grade)
# store-manager

### Project Overview
Store Manager is a web application that helps store owners manage sales and product inventory
records. This application is meant for use in a single store..

### Prerequisites

##Built with;
- `Python3.6` - Programming language that lets you work more quickly
- `Flask` - Python based web framework
- `Virtualenv` - A tool to create isolated virtual environment
- `PostgreSQl` - An Open source relational database 

## Project branch link:
```sh
   $ git clone https://github.com/Dianawats/store-manager-db
   ```

## API Endpoints
```
    - Login
    - Create an attendant's account
    - Fetch all products
    - Fetch a single product record
    - Fetch all sale records
    - Fetch a single sale record
    - Create a product
    - Create a sale order
    - Update a product item
    - Delete a product item
```

## Endpoints to create an attendants account and login into the application
HTTP Method|End point | Public Access|Action
-----------|----------|--------------|------
POST | /api/auth/register | False | Create an attendant's account
POST | /api/auth/login | True | Login a user

## Endpoints to create, views available products and create sale records
HTTP Method|End point | Public Access|Action
-----------|----------|--------------|------
POST | /api/v2/products | False | Create a product
POST | /api/v2/sales | False | Create a sale order
GET | /api/v2/products | False | Fetch all available products
GET | /api/v2/products/<product_id> | False | Fetch details of a single product
DELETE | /api/v2/products/<product_id> | False | Delete a single product
PUT | /api/v2/products/<product_id> | False | Edit details of a single product
GET | /api/v2/sales/<sale_id> | False | Fetch details of a single sale record
GET | /api/v2/sales | False | Fetch all sale records created
PUT | /api/auth/users | False | Change the role of an attendant

## Install all the necessary dependencies by
```
$ pip install -r requirements.txt
$ Install PostgreSQL
$ CREATE DATABASE storemanager
$ CREATE TABLE users
$ CREATE TABLE products
$ CREATE TABLE sales
```


### Heroku deployment:

## Author

## Diana Nakiwala**

## Acknowledgments

* Andela Software Development Community
* Inspiration
* Bootcamp 13 team-mates


