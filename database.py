from peewee import *
from datetime import date
import csv

from playhouse.shortcuts import model_to_dict

# We'll use a proxy, this is dynamically configurable by runtime environment,
# even though we'll stick to Sqlite for this exercise
database_proxy = DatabaseProxy()


class Weather(Model):
    date = DateField(unique=True)
    precipitation = FloatField()
    temp_max = FloatField()
    temp_min = FloatField()
    wind = FloatField()
    weather = CharField()

    class Meta:
        database = database_proxy


def init():
    database = SqliteDatabase("weather.db")
    database_proxy.initialize(database)
    database.create_tables([Weather])
    with open("seattle-weather.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        index_row = next(reader)
        # We can probably assume the ordering of the data is static,
        # but also, lets not assume that and make the ordering dynamic
        indices = {
            "date": index_row.index("date"),
            "precipitation": index_row.index("precipitation"),
            "temp_max": index_row.index("temp_max"),
            "temp_min": index_row.index("temp_min"),
            "wind": index_row.index("wind"),
            "weather": index_row.index("weather"),
        }
        for row in reader:
            # it's not explicitly stated, but we will assume
            # the date is in ISO format
            Weather.replace(
                date=date.fromisoformat(row[indices["date"]]),
                precipitation=float(row[indices["precipitation"]]),
                temp_max=float(row[indices["temp_max"]]),
                temp_min=float(row[indices["temp_min"]]),
                wind=float(row[indices["wind"]]),
                weather=row[indices["weather"]],
            ).execute()

    # This needs to be closed, gunicorn is going to fork the process,
    # and having multiple open connections will cause I/O errors.
    database.close()


def get_all():
    return [model_to_dict(entry) for entry in Weather.select()]


def get_by_parameters(query_date, weather, limit):
    query = Weather.select()

    if query_date:
        query = query.where(Weather.date == query_date)

    if weather:
        query = query.where(Weather.weather == weather)

    if limit:
        query = query.limit(limit)

    return [model_to_dict(entry) for entry in query]
