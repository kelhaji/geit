<p align="center">
  <p align="center">
     <img src="/logos/logo-white.png" alt="Geit" width="400">
  </p>
  <p align="center">
    <b>G</b>it <b>e</b>ducational <b>i</b>nsights <b>t</b>ool. Because f*#k slackers.
  </p>
</p>

## About Geit

Geit is a tool developed to aggregate contribution data of developers in a software development group project that uses Git. It is designed for teachers and teaching assistants to asses an entire group project and its individual members in terms of their code contributions behaviour.

## Features

- Shows contributions by contribution types (code, documentation, user interface, etc.) for each developer
- Shows issues and merge requests contribution activity
- Heuristically points out developers who are performing below average, above average, or need attention in certain categories
- Shows project files and folders with percentage of contribution for each developer
- Displays overall commit distribution for last 60 days
- GitLab integration

## Requirements

- [Python 3.6](https://www.python.org/downloads/) or greater
- [PIP](https://pypi.org/project/pip/)
- [Git](https://git-scm.com/)

## Installation
Install the latest version using PIP:

```
pip install geit
```
Note that Geit is currently in alpha and still under development. 

## How to run

```
geit --gitlab-url <YOUR_GITLAB_URL> --gitlab-api-key <YOUR_API_KEY> --gitlab-project-id <YOUR_PROJECT_ID>

```

Note that currently only GitLab is supported. GitHub support will be introduced later this week.

