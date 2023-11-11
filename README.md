
# Weather serving app

This is a small app built using [Flask](https://flask.palletsprojects.com/en/3.0.x/) and [peewee](https://docs.peewee-orm.com/en/latest/) (on top of a [SQLite](https://www.sqlite.org/) DB) to help manage and serve requested weather data. It uses flask's built in dev server when deployed locally, and uses [gunicorn](https://gunicorn.org/) for the production server.

## How to run

### For development

From within the directory:

```python3 app.py```

This'll run Flask using its built in development server. It is not robust, and not intended for production use. The development server is set to reload on filesystem changes, and so will relaunch new changes when you make them.

### For production

```docker build -t app . && docker run -p 8000:8000 app```

Within this directory is also included a compose.yaml file which can be used with docker-compose.

```docker-compose up --build```

This will build a docker container containing the required python and csv files to run the server. It'll
 subsequently start a server running on port 8000 that can be queried.
