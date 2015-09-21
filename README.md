# Ellis Act Map

## Requirements
- Python 2.7.x
  - Django 1.8.1+
  - virtualenv
  - virtualenvwrapper

- Node.js 0.12.x
  - grunt-cli
  - bower

## Installation
```bash
$ mkvirutalenv ellis-act  # make a Python virtual environment for the project
$ git clone repo && cd $_  # clone the repo from Github
$ pip install requirements/project.txt  # install Python dependencies
$ fab npm:install  # fabric alias to run npm install
$ fab bower:install   # fanric alias to run bower install
$ fab rs  # start the server and Grunt tasks
```

## data loading

```
$ python manage.py load_neighborhood
$ python manage.py loaddataset
```

## Data clean
Went into Excel to make city column all read San Francisco. We're also loading the data with mostly CharFields since the data wasn't 100% clean.

Went and did this is open refine

had to convert data into utf-8 by uploading data to google sheets and downloading

using planning commision shapefle for neighborhoods
