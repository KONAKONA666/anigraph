import pandas
from db import AnimeRelationDataBase
from anime import Anime
anime_df = pandas.read_csv("../data_concated.csv")
db = AnimeRelationDataBase("bolt://localhost:7687", " ", " ")
def process_anime_row(row):
   #i print(row)
    left = row['left']
    right = row['right']
    reason = row['reason']
    db.add_relation(left, right, reason)


anime_df.iloc[84000:].apply(process_anime_row, axis=1)



