import dataclass_factory
import json
import logging
import aiosqlite


async def init_sqlite(conf, loop):
    connection = await aiosqlite.connect(conf['path_db'], loop=loop)
    return connection


async def get_autocomplete(conn, prefix):
    cursor = await conn.execute("SELECT anime FROM animes WHERE anime LIKE '{}%' LIMIT 10".format(prefix))
    autocomplete_list = await cursor.fetchall()
    await cursor.close()
    return autocomplete_list


async def get_points(conn):
    cursor = await conn.execute("SELECT anime, x, y FROM animes")
    animes = await cursor.fetchall()
    await cursor.close()
    return animes


async def get_region_neighbours(conn, title, radius):
    cursor = await conn.execute("SELECT x, y FROM animes WHERE anime = '{}'".format(title))
    x, y = await cursor.fetchone()
    logger = logging.getLogger("sqlite")
    logger.info("SELECT anime, x, y FROM animes "
                "WHERE (x-{1})*(x-{1}) + (y-{2})*(y-{2}) < {0}*{0}".format(radius, x, y))
    cursor_region = await conn.execute("SELECT anime, x, y FROM animes "
                                       "WHERE (x-({1}))*(x-({1})) + (y-({2}))*(y-({2})) < {0}*{0}".format(radius, x, y))
    animes = await cursor_region.fetchall()
    await cursor.close()
    await cursor_region.close()
    return animes

# class AnimeRelationDataBase(object):
#
#     def __init__(self, uri: str, user: str, password: str):
#         self._driver_neo4j = GraphDatabase.driver(uri, auth=(user, password))
#
#     def close(self):
#         self._driver_neo4j.close()
#
#     def add_genre(self, name: str) -> bool:
#         with self._driver_neo4j.session() as session:
#             added_name: str = session.write_transaction(self.__add_genre, name)
#             if added_name:
#                 return True
#             else:
#                 return False
#
#     def add_anime(self, anime: Anime)->None:
#         with self._driver_neo4j.session() as session:
#             return session.write_transaction(self.__add_anime, anime)
#
#     def add_recommendation_two_anime(self, left: str, right: str, reason: str):
#         with self._driver_neo4j.session() as session:
#             return session.write_transaction(self.__add_relation_anime, left, right, reason)
#
#     def get_anime(self, name: str):
#         with self._driver_neo4j.session() as session:
#             return session.write_transaction(self.__get_anime, name)
#
#     @staticmethod
#     def __get_anime(tx: Transaction, name: str):
#         return tx.run("MATCH (a: Anime) WHERE a.name = %name", name=name)
#
#     @staticmethod
#     def __add_relation_anime(tx: Transaction, left: str, right: str, reason: str):
#         return tx.run("MATCH (a: Anime), (b: Anime) "
#                       "WHERE a.name = $left AND b.name = $right "
#                       "CREATE (a)-[:RECOMMENDED {reason: $reason}]->(b) ",
#                       left=left, right=right, reason=reason)
#
#     @staticmethod
#     def __add_genre(tx: Transaction, name: str) -> str:
#         return tx.run("CREATE (g: Genre {name: $name}) RETURN g.name", name=name).single().value()
#
#     @staticmethod
#     def __add_anime(tx: Transaction, anime: Anime):
#         props = anime_dataclass_serializer(anime)
#         return tx.run("CREATE (a: Anime {name: $name, genres: $genres, rating: $rating}) "
#                       "WITH a "
#                       "MATCH (g: Genre) "
#                       "WHERE g.name IN a.genres "
#                       "CREATE (a)-[r:HAS_GENRE]->(g) ", name=anime.name, genres=anime.genres, rating=anime.rating)
#

#db = AnimeRelationDataBase("bolt://localhost:7687", "neo4j", "password")
#print(db.add_genre("C"))