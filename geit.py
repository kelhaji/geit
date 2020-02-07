#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
import click
import shutil
import time
from src.gitlab.project import GitLabProject
from src.physical.project import PhysicalProject
from src.activity_matrix import ActivityMatrix


@click.command()
@click.option('--gitlab-url', help='GitLab API key', required=True)
@click.option('--gitlab-api-key', help='GitLab API key', required=True)
@click.option('--gitlab-project-id', help='GitLab Project ID', required=True)
@click.option('--output', help='The output type (html/json)', default='html')
def handle_cli(gitlab_url, gitlab_api_key, gitlab_project_id, output):
    platform_project = GitLabProject(gitlab_url, gitlab_api_key, gitlab_project_id)

    temp_folder_name = "temp_" + str(int(time.time()))

    shutil.rmtree(temp_folder_name, ignore_errors=True)
    physical_project = PhysicalProject(temp_folder_name, platform_project.get_ssh_url())

    committer_count = physical_project.get_committer_count()

    if committer_count > 24:
        shutil.rmtree(temp_folder_name, ignore_errors=True)
        print("Repository has more than 24 (exactly " + str(committer_count) + ") committers. This is currently not supported.")
        return

    matrix = ActivityMatrix(physical_project, platform_project)

    physical_data = {
        "commits": physical_project.get_commit_statistics(),
        "contribution": {
            "tree": physical_project.get_all_contributions(),
            "types": physical_project.get_types_of_contributions()
        },
        "matrix": matrix.get_aggregate_matrix_activity_data()
    }

    json_physical_data = json.dumps(physical_data)

    if output == 'html':
        write_html_output(json_physical_data, gitlab_project_id)
    elif output == 'json':
        write_json_output(json_physical_data, gitlab_project_id)
    else:
        print(json_physical_data)

    shutil.rmtree(temp_folder_name, ignore_errors=True)


def write_json_output(data, project_id):
    f = open("data_" + project_id + ".json", "w+")
    f.write(data)
    f.close()


def write_html_output(data, project_id):
    f = open("webpage/src/client/index.html", "r")
    index_file = f.read()

    updated_file = re.sub(r'<script tag="data-entry-tag">.*<\/script>',
                          '<script tag="data-entry-tag">var data = ' + str(data) + ';</script>',
                          index_file)
    f.close()

    f = open("index_" + project_id + ".html", "w+")
    f.write(updated_file)
    f.close()


if __name__ == '__main__':
    handle_cli()

