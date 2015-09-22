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
$ fab bower:install   # fabric alias to run bower install
$ fab rs  # start the server and Grunt tasks
```

## data loading
1. Export data from Google sheets as .csv

- Affordable housing data: https://docs.google.com/a/sfchronicle.com/spreadsheets/d/18uW85ClV5zzbsuRO_9MUGCcKiXrONn_exeyTKnkC4LM/edit?usp=sharing
- Evictions data: https://docs.google.com/a/sfchronicle.com/spreadsheets/d/132QOVFY75AmwmdSAJuB2UpsfKzmexj42C6Mv3SiL3Ts/edit?usp=sharing
- San Francisco neighborhoods: https://data.sfgov.org/download/qc6m-r4ih/ZIP

2. create `data` directory for .csv files and a nested `shps` directory for neighborhood shapefiles

```bash
ellis_act/ellis_act/data  master ✔                                                                              
▶ tree .
.
├── 2015-21-09-affordable-housing.csv
├── 2015-21-09-all-evictions-clean.csv
└── shps
    ├── sf-neighborhoods.cpg
    ├── sf-neighborhoods.dbf
    ├── sf-neighborhoods.prj
    ├── sf-neighborhoods.qpj
    ├── sf-neighborhoods.shp
    ├── sf-neighborhoods.shx
    └── sf-neighborhoods.zip
```

3. load the data with management commands

```
$ python manage.py load_neighborhood  # loads neighborhood polygons from SF planning commission
$ python manage.py loaddataset  # load ellis act evictions data
$ python manage.py loadaffordabledata  # load affordable housing data
```

### Data clean diary
Went into Excel to make city column all read San Francisco. We're also loading the data with mostly CharFields since the data wasn't 100% clean.

Went and did this is open refine

had to convert data into utf-8 by uploading data to google sheets and downloading

using planning commission shapefile for neighborhoods
