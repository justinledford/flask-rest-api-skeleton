# Flask REST API Skeleton

This is just a very opinionated skeleton for a Flask REST API with:

- MySQL/SQLAlchemy (w/ PyMySQL)
    - with extended Flask-SQLAlchemy Query and Model classes
- Automatically conversion of JSON keys between snake and camel case on
  requests and responses
- CLI commands
    - `initdb` - create tables from models


## Setup

### Create virtualenv and install dependencies
```
$ mkvirtualenv myproject
(myproject) $ pip install -r api/requirements.txt
```

### Set environment variables
Set these in `myproject/bin/postactivate`
```bash
export DBUSER=user
export DBPASS=pass
export DBHOST=localhost
export DBNAME=foobar
export FLASK_APP=app.py
export FLASK_DEBUG=1
export PYTHONPATH=.
```
