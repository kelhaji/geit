#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gitlab


class GitLabProject:

    DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'

    def __init__(self, url, token, project_id):
        self.url = url
        self.token = token
        self.project_id = project_id
        self.gitlab = gitlab.Gitlab(url, private_token=token)

        self.gitlab_project = self.gitlab.projects.get(self.project_id)

    def get_date_format(self):
        return self.DATE_FORMAT

    def get_users(self):
        users = []
        for user in self.gitlab_project.users.list(all=True):
            users.append({
                "id": user.attributes["id"],
                "name": user.attributes["name"],
                "username": user.attributes["username"]
            })

        return users

    def get_ssh_url(self):
        return self.gitlab_project.attributes['ssh_url_to_repo']

    def get_all_issues(self, include_notes=False):
        issues = []

        for issue in self.gitlab_project.issues.list(all=True):
            issue_dict = dict(issue.attributes)

            if include_notes:
                issue_dict['notes'] = [note.attributes for note
                                       in issue.notes.list(all=True)]

            issues.append(issue_dict)

        return issues

    def get_all_merge_requests(self, include_notes=False, include_changes=False):
        merge_requests = []

        for merge_request in self.gitlab_project.mergerequests.list(all=True):
            issue_dict = dict(merge_request.attributes)

            if include_changes:
                issue_dict['changes'] = merge_request.changes()

            if include_notes:
                issue_dict['notes'] = [note.attributes for note
                                       in merge_request.notes.list(all=True)]

            merge_requests.append(issue_dict)

        return merge_requests
