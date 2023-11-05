import argparse
import json
from pathlib import Path
from typing import TypedDict
import urllib.request
import os


def get_github_token():
    if not Path(".env").exists():
        return os.getenv("GITHUB_TOKEN")
    content = Path(".env").read_text()
    for line in content.splitlines():
        if line.startswith("GITHUB_TOKEN="):
            return line.split("=")[1]


GITHUB_TOKEN = get_github_token()
OPEN_SOURCE = "Open Source"


class Project(TypedDict):
    last_updated: str
    name: str
    description: str
    stack: str
    company: str
    web_url: str
    github_url: str
    featured: bool
    active: bool
    private: bool


def github_api_request(path: str) -> dict:
    url = f"https://api.github.com/{path}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    return json.load(response)


def update_dates():
    with open('data/projects.json') as file:
        projects: list[Project] = json.load(file)

    need_update = [
        project
        for project in projects
        if project.get("active") and project.get("company") == OPEN_SOURCE
    ]

    for project in need_update:
        github_url = project.get("github_url")
        repo_name = github_url.split("/")[-1]
        commits = github_api_request(f"repos/Tobi-De/{repo_name}/commits")
        last_update = commits[0]["commit"]["author"]["date"]
        last_update_date = last_update.split("T")[0]
        project["last_updated"] = last_update_date

    with open('data/projects.json', 'w') as file:
        json.dump(projects, file)


def add_project():
    # TODO: Implement the logic for the add-project command
    pass


def main():
    parser = argparse.ArgumentParser(description='Make update to my projects')
    subparsers = parser.add_subparsers(dest='command')

    update_dates_parser = subparsers.add_parser('update-dates', help='Update dates command')
    update_dates_parser.set_defaults(func=update_dates)

    add_project_parser = subparsers.add_parser('add-project', help='Add project command')
    add_project_parser.set_defaults(func=add_project)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func()


if __name__ == '__main__':
    main()
