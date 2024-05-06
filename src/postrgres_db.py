from config import config
import psycopg2
import os.path
import json


class PostresDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.params = config()

    def create_database(self) -> None:
        conn = psycopg2.connect(dbname="postgres", **self.params)

        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute(f"drop database if exists {self.db_name};")
            cur.execute(f"create database {self.db_name};")

        conn.close()

    def create_table(self) -> None:
        conn = psycopg2.connect(dbname=self.db_name, **self.params)

        with conn.cursor() as cur:
            cur.execute("""
                create table repositories (
                    repository_id char(9) primary key,
                    repository_name varchar(100) not null,
                    repository_private bool not null,
                    repository_url varchar not null
                );
            """)

        conn.commit()
        conn.close()

    def insert_into_table(self, data: list[dict]) -> None:
        conn = psycopg2.connect(dbname=self.db_name, **self.params)

        with conn.cursor() as cur:
            for repository in data:
                cur.execute("""
                    insert into repositories (repository_id, repository_name, repository_private, repository_url) 
                    values (%s, %s, %s, %s)
                """, (repository['id'], repository['name'], repository['private'], repository['url']))

        conn.commit()
        conn.close()

    def export_data_to_json(self, file_name: str) -> None:
        path_to_file = os.path.join("..", file_name)

        data_for_json = []

        conn = psycopg2.connect(dbname=self.db_name, **self.params)

        with conn.cursor() as cur:
            cur.execute("select * from repositories;")
            data_from_table = cur.fetchall()

        conn.close()

        for repository_data in data_from_table:
            data_for_json.append({'id': repository_data[0], 'name': repository_data[1],
                                 'private': repository_data[2], 'url': repository_data[3]})

        with open(path_to_file, 'w') as json_file:
            json.dump(data_for_json, json_file)

    def select_data(self, data: str) -> list[tuple]:
        conn = psycopg2.connect(dbname=self.db_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(f"select {data} from repositories;")
            data_from_table = cur.fetchall()

        conn.close()

        return data_from_table
