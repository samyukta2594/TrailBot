import sqlite3
import random
from pathlib import Path
import requests

# def create_connection(db_file):
#     """ create a database connection to the SQLite database
#         specified by the db_file
#     :param db_file: database file
#     :return: Connection object or None
#     """
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#     except Exception as e:
#         print(e)

#     return conn



# def select_by_slot(conn,slot_name, slot_value):
#     """
#     Query all rows in the tasks table
#     :param conn: the Connection object
#     :return:
#     """
#     cur = conn.cursor()
#     cur.execute(f"""SELECT * FROM trail_1
#                  where {slot_name} = "{slot_value}"
#                  """)

#     rows = cur.fetchall()

#     if len(list(rows)) < 1:
#         print("There are no resources matching your query")
#     else:
#         for row in random.sample(rows,1):
#             print(row[0])

# fpath = Path('db_data/trail_DB').absolute()
# print(fpath)

# select_by_slot(create_connection(fpath), slot_name="Place", slot_value="Cupertino")


limit = 1
api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
response = requests.get(api_url, headers={'X-Api-Key': 'W0HcbiGniznn5xptoSKCNQ==Uh8q5B5CReBlGMGB'})
if response.status_code == requests.codes.ok:
    data = response.json()
    print(data[0]['fact'])