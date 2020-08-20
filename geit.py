#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
import click
import shutil
import time
import os

from src.gitlab.project import GitLabProject
from src.physical.project import PhysicalProject
from src.activity_matrix import ActivityMatrix


@click.command()
@click.option('--target-repo', help='The target repo', required=False)
@click.option('--gitlab-url', help='GitLab API key', required=False)
@click.option('--gitlab-api-key', help='GitLab API key', required=False)
@click.option('--gitlab-project-id', help='GitLab Project ID', required=False)
@click.option('--output', help='The output type (html/json)', default='html')
@click.option('--all-files', help='Analyze all files indepedent of their size. By default all files that exceed 1 MB are excluded from analysis.', default=False)
def handle_cli(target_repo, gitlab_url, gitlab_api_key, gitlab_project_id, output, all_files):
    if os.name == 'nt':
        print('Currently Geit does not support Windows :(\n' +
            'You can run Geit on Windows via the Windows Subsystem for Linux (WSL) module. Check the README file.')
        return

    identifier = ""

    temp_folder_name = "temp_" + str(int(time.time()))
    shutil.rmtree(temp_folder_name, ignore_errors=True)

    platform_project = None
    physical_project = None

    if gitlab_url != None and gitlab_api_key != None and gitlab_project_id != None:
        identifier = gitlab_project_id

        platform_project = GitLabProject(gitlab_url, gitlab_api_key, gitlab_project_id)
        physical_project = PhysicalProject(temp_folder_name, platform_project.get_ssh_url())
    elif target_repo != None:
        identifier = os.path.basename(target_repo)
        #target_repo = target_repo[1:]
        physical_project = PhysicalProject(target_repo)
    else:
        print('No git repo specified, or project was not (or incorrectly) specified. Check the README file.')
        return

    physical_data = dict()

    print("Collecting commit statistics...")
    physical_data["commits"] = physical_project.get_commit_statistics()

    print("Collecting and analyzing contribution data...")
    physical_data["contribution"] = {
        "tree": physical_project.get_all_contributions(all_files=all_files),
        "types": physical_project.get_types_of_contributions(all_files=all_files)
    }

    if platform_project:
        matrix = ActivityMatrix(physical_project, platform_project)

        print("Collecting and generating issue, merge requests, "
              "commits, and contribution matrices...")
    else:
        matrix = ActivityMatrix(physical_project)

        print("Collecting and generating commits and contribution matrices...")

    physical_data["matrix"] = matrix.get_aggregate_matrix_activity_data()

    json_physical_data = json.dumps(physical_data, ensure_ascii=False)

    filename = None

    if output == 'html':
        print("Writing HTML output...")
        filename = write_html_output(json_physical_data, identifier)
    elif output == 'json':
        print("Writing JSON output...")
        filename = write_json_output(json_physical_data, identifier)
    else:
        print(json_physical_data)

    if filename:
        print("Done. See output at: " + filename)

    if platform_project:
        shutil.rmtree(temp_folder_name, ignore_errors=True)


def write_json_output(data, identifier):
    filename = "data_" + identifier + ".json"

    f = open(filename, "w+", encoding='utf-8')
    f.write(data)
    f.close()

    return filename


def write_html_output(data, identifier):
    f = open("webpage/src/client/public/index.html", "r", encoding='utf-8')
    index_file = f.read()

    updated_file = re.sub(r'<script tag="data-entry-tag">.*<\/script>',
                          '<script tag="data-entry-tag">var data = ' + str(re.escape(data)) + ';</script>',
                          index_file)
    f.close()

    filename = "index_" + identifier + ".html"

    f = open(filename, "w+", encoding='utf-8')
    f.write(updated_file)
    f.close()

    return filename


if __name__ == '__main__':
    # I hate windows
    # win_unicode_console.enable()

    handle_cli()

