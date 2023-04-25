from os import getenv
from typing import Dict, Iterator
from certifi import where
from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient


class Database:

    """ Load in .env file with password to mongoDB, which will allow for a connection to the MongoDB client.
    A collection object is then created in the database."""

    load_dotenv()
    database = MongoClient(getenv("DB_URL"), tlsCAFile=where())["Database"]
    collection = database["Database"]

    """ Seed method takes in two parameters, self and amount. For loop is used to iterate through amount + 1 to generate
     a monster as a dictionary and inserts the results into the collection using the insert_one method."""

    def seed(self, amount):
        for x in range(1, amount+1):
            self.collection.insert_one(Monster().to_dict())

    """ Reset method is used to remove all monsters from the database using delete_many method."""

    def reset(self) -> bool:
        return self.collection.delete_many({})

    """ Count method uses count_documents method to count all documents (monsters) in collection. 
    The count of all monsters is returned as an integer. """

    def count(self) -> int:
        return self.collection.count_documents({})

    """ dataframe method takes all monsters in the collection and converts them to a pandas dataframe. Find method is 
    used to retrieve monsters and exclude the _id column when adding to the collection. Monsters are added into the 
    pandas dataframe as a list. """

    def dataframe(self) -> DataFrame:
        data = list(self.collection.find({}, {"_id": False}))
        return DataFrame(data)

    """ html_table method and returns a string. Retrieves all monsters and their attributes from collection and converts
    to html table string."""

    def html_table(self) -> str:
        return Database().dataframe().to_html()

    """ Creates read_many method that takes in two parameters, self and query as a dictionary. Then retrieves objects
    from collection using the find method, and excludes _id field from the returned objects. """

    def read_many(self, query: Dict) -> Iterator[Dict]:
        return self.collection.find(query, {"_id": False})


""" This is the main method executing the application. It resets, fills, and displays the database. """
if __name__ == "__main__":
    Database().reset()
    Database().seed(1000)
    Database().count()
    DataFrame(Database().read_many({}))


