"""Creates helper methods for database"""
import sqlite3
import random
import datetime


def insert_random_data(db_name="healthdata.db", amt=200):
    """Fills the database with random data"""
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    my_data = [generate_data() for _ in range(amt)]

    cur.executemany("INSERT INTO daily_record (name, temperature, fatigue, sore_throat, other_pain, updated) VALUES ("
                    "?, ?, ?, ?, ?, ?);", my_data)

    con.commit()
    con.close()


def generate_data():

    names = ("Adib", "Afif", "Daniel", "Eiman", "Joseph")
    bools = ("Yes", "No")
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2021, 3, 30)
    days_between_dates = (end_date - start_date).days

    name = random.choice(names)
    temperature = round(random.uniform(35.0, 36.8), 2)
    fatigue = random.choice(bools)
    sore_throat = random.choice(bools)
    other_pain = random.choice(bools)
    updated = (start_date + datetime.timedelta(days=random.randrange(days_between_dates))).strftime("%Y-%m-%d %H:%M:%S")

    return name, temperature, fatigue, sore_throat, other_pain, updated


if __name__ == "__main__":
    insert_random_data()
