import os
import database

# Scale the number of workers with the number of cores for the CPU
workers = os.cpu_count()

def on_starting(server):
    # Initialize the peewee database. This is a one-time cost, but it'll 
    # speed up queries, as well as add features we want for filtering. 
    # We could even just have this as an in-mem db, since this dataset is
    # so small.
    database.init()