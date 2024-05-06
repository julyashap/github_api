import requests


def get_repos_stats(user_name: str) -> list[dict]:
    url = f"https://api.github.com/users/{user_name}/repos"
    response = requests.get(url)

    repositories = response.json()

    return repositories
