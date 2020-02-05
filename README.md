# 🐐 Git Educational Insights Tool (GEIT)

GEIT is a tool developed to aggregate contribution data of developers in a software development group project. It is designed for teachers and teaching assistant to asses an entire group project and its individual members in terms of their code contributions behaviour.


## Features

- Shows contributions by contribution types (code, documentation, user interface, etc.) for each developer
- Shows issues and merge requests contribution activity
- Heuristically points out developers who are performing below average, above average, or need attention
- Show project files with percentage of contribution from each user
- Displays overall commit distribution for last 60 days

# Installation prerequisites

- Python 3.7 or greater
- Terminal git access
- Python PIP

## Installation
Install the latest version using PIP:

```
pip install geit
```


## How to run

```
geit --gitlab-url <YOUR_GITLAB_URL> --gitlab-api-key <YOUR_API_KEY> --gitlab-project-id <YOUR_PROJECT_ID>

```

Note that currently only GitLab is supported. GitHub support will be introduced later this week.

