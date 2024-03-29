#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gitlab


class GitLabProject:
    """Responsible retrieving information on GitLab projects."""

    DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'

    def __init__(self, url, token, project_id):
        self.url = url
        self.token = token
        self.project_id = project_id
        self.gitlab = gitlab.Gitlab(url, private_token=token)

        print("Getting GitLab project metadata...")
        self.gitlab_project = self.gitlab.projects.get(self.project_id) 

    def get_date_format(self):
        """Get date format that is used in Gitlab's API."""
        return self.DATE_FORMAT

    def get_users(self):
        """Get all users in of the project."""
        users = []
        for user in self.gitlab_project.users.list(all=True):
            users.append({
                "id": user.attributes["id"],
                "name": user.attributes["name"],
                "username": user.attributes["username"]
            })

        return users

    def get_ssh_url(self):
        """Get SSH url for cloning."""
        return self.gitlab_project.attributes['ssh_url_to_repo']

    def get_all_issues(self, include_notes=False):
        """Get all issues with all their metadata and optionally including
        their notes (comments)."""
        issues = []

        for issue in self.gitlab_project.issues.list(all=True):
            issue_dict = dict(issue.attributes)

            if include_notes:
                issue_dict['notes'] = [note.attributes for note
                                       in issue.notes.list(all=True)]

            issues.append(issue_dict)

        return issues

    def get_all_merge_requests(self, include_notes=False, include_changes=False):
        """Get all merge request with all their metadata and optionally including
        their notes (comments)."""
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
