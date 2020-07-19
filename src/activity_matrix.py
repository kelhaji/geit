#!/usr/bin/env python
# -*- coding: utf-8 -*-

from statistics import mean
from datetime import datetime


class ActivityMatrix:
    """Responsible for creating an activity matrix
    from git data, issues, pull/merge requests."""

    def __init__(self, physical_project, git_platform=None):
        self.physical_project = physical_project
        self.git_platform = git_platform

    @staticmethod
    def __extract_user_issue_statistics(issues, all_issues, username):
        """Extract issue statistics related to a single user."""
        total_notes_on_issues = 0
        total_system_notes_on_issues = 0
        total_times_assigned_to_issues = 0
        total_time_spent_individually_on_issues = 0

        for issue in all_issues:
            for note in issue["notes"]:
                if note["author"]["username"] == username:
                    if note["system"]:
                        total_system_notes_on_issues += 1
                    else:
                        total_notes_on_issues += 1

            assigned = False

            for assignee in issue["assignees"]:
                if assignee["username"] == username:
                    total_times_assigned_to_issues += 1
                    assigned = True

            if assigned:
                time_spent = 0

                total_assignees = len(issue["assignees"])

                if total_assignees != 0:
                    time_spent = issue["time_stats"]["total_time_spent"]/total_assignees

                total_time_spent_individually_on_issues += time_spent

        return {
            "total_issues": len(issues),
            "total_notes_on_issues": total_notes_on_issues,
            "total_system_notes_on_issues": total_system_notes_on_issues,
            "total_closed_issues":
                len([1 for issue in issues if issue["state"] == "closed"]),
            "average_time_in_hours_estimated_on_issues":
                (mean([issue["time_stats"]["time_estimate"] for issue in issues]) / 60) / 60,
            "average_time_in_hours_all_assignees_spent_on_issues":
                (mean([issue["time_stats"]["total_time_spent"] for issue in issues]) / 60) / 60,
            "total_time_spent_in_hours_individually_on_all_issues":
                (total_time_spent_individually_on_issues / 60) / 60,
            "average_assignees_per_issue": mean([len(issue["assignees"]) for issue in issues]),
            "total_times_assigned_to_issues": total_times_assigned_to_issues,
            "total_issues_self_assigned_only": len([1 for issue in issues
                                                    if len(issue["assignees"]) == 1
                                                    and issue["assignee"][
                                                        "username"] == username]),
            "total_issues_without_milestones": len([1 for issue in issues
                                                    if not issue["milestone"]]),
            "total_issues_without_labels": len([1 for issue in issues
                                                if len(issue["labels"]) == 0]),
            "total_issues_without_description":  len([1 for issue in issues if
                                                      not issue["description"]
                                                      or issue["description"] == ""]),
            "total_issues_without_assignee":  len([1 for issue in issues
                                                   if len(issue["assignees"]) == 0])
        }

    def get_aggregate_issues_statistics(self):
        """Extract issue statistics per user. Note that when a user hasn't authored
        any issues he/she won't be included."""
        aggregate_object = {}

        all_issues = self.git_platform.get_all_issues(include_notes=True)

        for issue in all_issues:
            username = issue["author"]["username"]

            if username not in aggregate_object:
                aggregate_object[username] = []

            aggregate_object[username].append(issue)

        for key in aggregate_object:
            aggregate_object[key] = self.__extract_user_issue_statistics(
                aggregate_object[key], all_issues, key)

        return aggregate_object

    def __get_average_lifetime_of_merge_requests(self, merge_requests):
        """Calculates the average lifetime of merge requests in seconds. Only accounts
        merges that are merged or closed."""

        life_time_merge_requests = []

        if len(merge_requests) == 0:
            return 0

        date_format = self.git_platform.get_date_format()

        for merge_request in merge_requests:
            if merge_request["closed_at"] is not None or\
                    merge_request["merged_at"] is not None:
                finish_time = 0

                created_at = datetime. \
                    strptime(merge_request["created_at"], date_format).timestamp()

                if merge_request["closed_at"] is not None:
                    finish_time = datetime. \
                        strptime(merge_request["closed_at"], date_format).timestamp()

                if merge_request["merged_at"] is not None:
                    finish_time = datetime. \
                        strptime(merge_request["merged_at"], date_format).timestamp()

                time_spent = abs(created_at - finish_time)

                life_time_merge_requests.append(time_spent)

        return mean(life_time_merge_requests)

    def __extract_user_merge_request_statistics(self,
                                                merge_requests, all_merge_requests,
                                                username):
        """Extract merge request statistics related to a single user."""
        total_notes_on_merge_requests = 0
        total_system_notes_on_merge_requests = 0
        total_times_merged = 0
        total_times_assigned_to_merge_requests = 0
        average_lifetime_of_merge_requests = \
            self.__get_average_lifetime_of_merge_requests(merge_requests)

        for merge_request in all_merge_requests:
            for note in merge_request["notes"]:
                if note["author"]["username"] == username:
                    if note["system"]:
                        total_system_notes_on_merge_requests += 1
                    else:
                        total_notes_on_merge_requests += 1

            if merge_request["merged_by"] is not None \
                    and merge_request["merged_by"]["username"] == username:
                total_times_merged += 1

            for assignee in merge_request["assignees"]:
                if assignee["username"] == username:
                    total_times_assigned_to_merge_requests += 1

        return {
            "total_merge_requests": len(merge_requests),
            "total_notes_on_merge_requests": total_notes_on_merge_requests,
            "total_system_notes_on_merge_requests": total_system_notes_on_merge_requests,
            "total_merge_requests_merged": len([1 for merge_request in merge_requests if
                                                merge_request["state"] == "merged"]),
            "total_merge_requests_closed": len([1 for merge_request in merge_requests if
                                                merge_request["state"] == "closed"]),
            "average_assignees_per_merge_requests": mean([len(merge_request["assignees"])
                                                for merge_request in merge_requests]),
            "total_times_assigned_to_merge_requests": total_times_assigned_to_merge_requests,
            "total_times_merged": total_times_merged,
            "average_lifetime_in_hours_of_merge_requests": (average_lifetime_of_merge_requests / 60) / 60,
            "total_merge_requests_merged_by_self": len([1 for merge_request in
                                                        merge_requests if merge_request[
                                                            "merged_by"] is not None and
                                                        merge_request["merged_by"][
                                                            "username"] == username]),
            "total_merge_requests_without_milestones": len([1 for merge_request in merge_requests
                                                             if not merge_request["milestone"]]),
            "total_merge_requests_without_labels": len([1 for merge_request in merge_requests
                                                        if len(merge_request["labels"]) == 0]),
            "total_merge_requests_without_description":  len([1 for merge_request in merge_requests if
                                                              not merge_request["description"]
                                                              or merge_request["description"] == ""]),
            "total_merge_requests_without_assignee":  len([1 for merge_request in merge_requests
                                                           if len(merge_request["assignees"]) == 0])
        }

    def get_aggregate_merge_request_statistics(self):
        """Extract merge requests statistics per user. Note that when a user hasn't
        authored any merge requests he/she won't be included."""
        aggregate_object = {}

        all_merge_requests = self.git_platform.\
            get_all_merge_requests(include_notes=True)

        for issue in all_merge_requests:
            username = issue["author"]["username"]

            if username not in aggregate_object:
                aggregate_object[username] = []

            aggregate_object[username].append(issue)

        for key in aggregate_object:
            aggregate_object[key] = self.__extract_user_merge_request_statistics(
                aggregate_object[key], all_merge_requests, key)

        return aggregate_object

    def get_aggregate_commit_statistics(self):
        """Extract commit statistics per committer."""
        commit_statistics = self.physical_project.get_commit_statistics()["committers"]

        aggregate_object = {}

        for committer in commit_statistics:
            if committer not in aggregate_object:
                aggregate_object[committer] = {
                    "total_commits": 0,
                    "large_commit_ratio": 0,
                    "median_of_lines_per_commit": 0,
                    "average_of_lines_per_commit": 0
                }

            aggregate_object[committer]["total_commits"] = \
                commit_statistics[committer]["count"]
            aggregate_object[committer]["large_commit_ratio"] = \
                commit_statistics[committer]["large_commit_ratio"]
            aggregate_object[committer]["median_of_lines_per_commit"] = \
                commit_statistics[committer]["lines"]["median"]
            aggregate_object[committer]["average_of_lines_per_commit"] = \
                commit_statistics[committer]["lines"]["mean"]

        return aggregate_object

    def get_aggregate_contribution_types_statistics(self):
        """Extract commit statistics per committer."""
        return self.physical_project.get_types_of_contributions()["contributors"]

    def get_aggregate_matrix_activity_data(self):
        """Get the all the aggregate activity data to be used in a matrix."""
        if self.git_platform:
            return {
                "issues": self.get_aggregate_issues_statistics(),
                "merge_requests": self.get_aggregate_merge_request_statistics(),
                "committs": self.get_aggregate_commit_statistics(),
                "contribution_types": self.get_aggregate_contribution_types_statistics()
            }
        else: 
            return {
                "committs": self.get_aggregate_commit_statistics(),
                "contribution_types": self.get_aggregate_contribution_types_statistics()
            }
