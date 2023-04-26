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

    def seed(self, amount):
        """ Seed method takes in two parameters, self and amount. For loop is used to iterate through amount + 1 to
        generate a monster as a dictionary and inserts the results into the collection using the insert_many method for
        efficiency."""

        monster_list = []

        for x in range(1, amount+1):
            monster_list.append(Monster().to_dict())
        self.collection.insert_many(monster_list)

    def reset(self) -> bool:
        """ Reset method is used to remove all monsters from the database using delete_many method."""

        return self.collection.delete_many({})

    def count(self) -> int:
        """ Count method uses count_documents method to count all documents (monsters) in collection.
        The count of all monsters is returned as an integer. """

        return self.collection.count_documents({})

    def dataframe(self) -> DataFrame:
        """ dataframe method takes all monsters in the collection and converts them to a pandas dataframe. Find method is
        used to retrieve monsters and exclude the _id column when adding to the collection. Monsters are added into the
        pandas dataframe as a list. """

        data = list(self.collection.find({}, {"_id": False}))
        return DataFrame(data)

    def html_table(self) -> str:
        """ html_table method and returns a string. Retrieves all monsters and their attributes from collection and converts
        to html table string."""

        return self.dataframe().to_html()

    def read_many(self, query: Dict) -> Iterator[Dict]:
        """ Creates read_many method that takes in two parameters, self and query as a dictionary. Then retrieves objects
        from collection using the find method, and excludes _id field from the returned objects. """

        return self.collection.find(query, {"_id": False})


if __name__ == "__main__":
    db = Database()
    db.reset()
    db.seed(1000)
    print(db.count())
    print(db.dataframe())
