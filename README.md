Taxfix
======

## Getting Started

1. Download and install the lastest version of Docker
2. Clone the project
3. Fill the missing values in the luigi.cfg with s3 bucket and redshift data ( must be create in your account )/
4. Build the images:
    ~~~~
    docker-compose build
    ~~~~
5. To execute tests and developing machine
    ~~~~
    docker-compose up --force-recreate -d app-dev
    docker-compose exec app-dev bash
    ~~~~

    Execute tests:
    ~~~~
    make test
    ~~~~

    To stop developer machine:
    ~~~~
    docker-compose stop app-dev
    ~~~~

6. Access the Redshift cluster

## Solution

Implement a batch job that transforms the given events predicting the following output and visualizing in any tool of our choice

For the pipeline, I used **Luigi** (http://luigi.readthedocs.io/en/stable/)
as the Pipeline framework, the reason is because the Luigi handles dependency resolution,
workflow management, visualization, handling failures ad command line integration
