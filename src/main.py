from src.utils import get_repos_stats
from src.postrgres_db import PostresDB


def main():
    repositories = get_repos_stats("julyashap")

    pDB = PostresDB("github")
    pDB.create_database()
    pDB.create_table()
    pDB.insert_into_table(repositories)

    pDB.export_data_to_json("data_from_github.json")

    result_data = pDB.select_data("repository_id, repository_name")
    for result in result_data:
        print(result)


if __name__ == '__main__':
    main()
