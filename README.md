project-template
==============================

template for the team to use

Project Organization
------------

    ├── LICENSE
    ├── Makefile                                <- Makefile with commands like `make data` or `make train`
    ├── Pipfile                                 <- Pipfile stating package configuration as used by Pipenv.
    ├── Pipfile.lock                            <- Pipfile.lock stating a pinned down software stack with as used by Pipenv.
    ├── README.md                               <- The top-level README for developers using this project.
    ├── data
    │   ├── external                            <- Data from third party sources.
    │   ├── interim                             <- Intermediate data that has been transformed.
    │   ├── processed                           <- The final, canonical data sets for modeling.
    │   └── raw                                 <- The original, immutable data dump.
    │
    ├── docs                                    <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models                                  <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks                               <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                                               the creator's initials, and a short `-` delimited description, e.g.
    │                                               `1.0-jqp-initial-data-exploration`.
    │
    ├── references                              <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports                                 <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures                             <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt                        <- The requirements file stating direct dependencies if a library
    │                                               is developed.
    │
    ├── setup.py                                <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                                     <- Source code for use in this project.
    │   ├── __init__.py                         <- Makes src a Python module
    │   │
    │   ├── data                                <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features                            <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models                              <- Scripts to train models and then use trained models to make
    │   │   │                                       predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization                       <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    ├── .thoth.yaml                             <- Thoth's configuration file
    ├── .aicoe-ci.yaml                          <- AICoE CI configuration file (https://github.com/AICoE/aicoe-ci)
    │
    ├── .github                                 <- GitHub configuration folder
    │   ├── PULL_REQUEST_TEMPLATE               <- GitHub templates for pull requests
    │   │
    │   ├── ISSUE_TEMPLATE                      <- GitHub templates for issues
    |       ├── {major|minor|patch}_release.md  <- If Khebut GitHub App Bot (https://github.com/apps/khebhut) is installed, the issue will trigger a major|minor|patch release.
    │       |                                       The bot will open a Pull Request to update the CHANGELOG and fix the opened issue.
    │       |                                       NOTE: only users that are allowed to release (a.k.a. maintainers specified in the .thoth.yaml file) should open the issue, otherwise bot will
    │       |                                       reject them, commenting and closing the issue.
    │       |                                       If AICoE CI GitHub App (https://github.com/apps/aicoe-ci) is installed, once the pull request is merged a new tag is created by the bot
    │       |                                       and the pipeline to build and push image starts.
    │       |
    |       └── redeliver_container_image.md    <- If the tag exists and AICoE CI GitHub App (https://github.com/apps/aicoe-ci) is installed, the issue will retrigger the pipeline to build and
    │                                               push image container image. NOTE: It should be used if the pipeline triggered with the {major|minor|patch}_release failed for any reason.
    |
    └── tox.ini                                 <- tox file with settings for running tox; see tox.readthedocs.io

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
