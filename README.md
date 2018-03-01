Taxfix
======

## Getting Started

1. Download and install the lastest version of Docker
2. Clone the project
3. Fill up the missing values in the luigi.cfg
    ~~~~
    s3 bucket (insert some files inside a folder ("/events") as sample sent)
    ~~~~
    ~~~~
    redshift data ( must be create in your account )
    ~~~~
4. Build the images:
    ~~~~
    docker-compose build
    ~~~~
5. To execute tests and developing machine
    ~~~~
    docker-compose up --force-recreate -d app-dev
    ~~~~

    Execute tests:
    ~~~~
    docker-compose exec app-dev make test
    ~~~~

    Execute pipeline:
    ~~~~
    docker-compose exec app-dev luigi --module taxfix.tasks.DimensionLoader
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
