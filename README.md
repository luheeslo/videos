# Videos

A working Pyramid project that uses Mongo for the database based in https://gist.github.com/csaftoiu/c3fe054624ab5f3de803d317b357b5b3

## Setup

Install [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/)

## First Build

From a terminal:

    make build_app

This will build the base container, and is only required the first time the project is run.

## Running Dev Server

    make run_dev_server
    
## Stopping Dev Server

    make stop_dev_server

## Views Testing

    make run_tests
