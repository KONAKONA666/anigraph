import pandas as pd
from sqlalchemy import create_engine

#df = pd.read_csv('anime_descs.csv')
engine = create_engine("sqlite:///db.sqlite", echo=True)
#df.to_sql('animes', con=engine)
#print(engine.execute("SELECT * FROM animes WHERE anime LIKE 'Naruto: Shippuuden'").fetchall())