from fastapi import FastAPI
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL) # Create a SQL alchemy engine

# What is an SQL alchemy engine
#  An Engine is a factory for connection objects. It encapsulates a connection pool that
#  minimizes the cost of connecting to the database by reusing existing connections and 
#  provides a consistent API for working with transactions.

metadata = MetaData() # Creates a SQL alchemy metadata object
Sessionlocal = sessionmaker(autocommit = False, autoflush = False, bind = engine) # Creates a SQL alchemy sessionmaker object
Base = declarative_base() # Creates a SQL alchemy declarative base object

