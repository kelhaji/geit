#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import pathlib
import statistics
import os

from os import walk, path

from git import Repo
from binaryornot.check import is_binary

from src.util import Util


class PhysicalProject:
    """Responsible for extracting and summarizing GIT repository data."""

    CONFIG_FILE_PREFIXES = ['.yml', '.whl', '.cfg', '.xml',
                            '.config', '.properties', '.rss', '.cmd', '.pub']

    CONFIG_FILENAMES = ['requirements-dev.txt', 'requirements_dev.txt',
                        'requirements.txt', 'setup.py', 'GruntFile.js',
                        'package.json', 'package-lock.json', '.gitignore', '.gitkeep',
                        'Dockerfile', '.classpath', 'mvnw', '.coveragerc', '.npmignore',
                        '.env', '.eslintignore', '.eslintrc.js']

    CODE_FILE_PREFIXES = ['.py', '.c', '.cpp', '.js', '.java', '.cs', '.ts',
                          '.jsx', '.tsx', '.scala', '.sc', '.php', '.go', '.swift',
                          '.h']

    UI_FILE_PREFIXES = ['.html', '.css', '.htmlx', '.htm', '.aspx', '.fxml',
                        '.jsp', '.ui']

    DOC_FILENAMES = ['README', 'LICENSE', 'SECURITY', 'CONTRIBUTING', 'CHANGELOG',
                     'BUILDING']

    DOC_FILE_PREFIXES = ['.md', '.txt', '.rst', '.rtf']

    LARGE_COMMIT_THRESHOLD = 500

    def __init__(self, folder, ssh_url=None):
        self.folder = folder
        self.ssh_url = ssh_url
        self.repo = Repo.init()

        if not os.path.exists(folder) and ssh_url is None:
            raise FileNotFoundError('Specified target repo was not found.')
            return

        if not os.path.isdir(folder):
            print("Cloning repo (" + self.ssh_url + ")...")
            self.repo.clone_from(self.ssh_url, self.folder)
            self.repo = Repo.init(folder)
        else:
            self.repo = Repo.init(folder)

    def get_number_of_branches(self):
        """Get number of branches. Note that this returns
        the remote number of branches."""
        branches = self.repo.git.branch('-r')

        print(self.repo.git.branch('-r').split('\n'))

        if branches == "":
            return 0

        return len(branches.split('\n'))

    def get_committer_count(self):
        """Get number of committers."""
        committers = self.repo.git.shortlog('-sne', all=True)

        if committers == "":
            return 0

        return len(committers.split('\n'))

    @staticmethod
    def __commit_stats(commit_stat_type, all_stats_total):
        """Calculates statistics using a certain commit statistics
        type (e.g. insertions)."""

        dataset = [stats[commit_stat_type] for stats in all_stats_total]

        stat_type_sum = sum(dataset)

        mean = statistics.mean(dataset)

        median = statistics.median(dataset)

        return {
            "sum": stat_type_sum,
            "mean": mean,
            "median": median
        }

    def __calculate_large_commit_ratio(self, all_stats_total):
        """Calculate large commit ratio. The large commit ratio is defined as the amount
        of large commits divided by the amount of commits."""

        large_commit_count = 0
        commit_count = 0

        for stats_total in all_stats_total:
            if stats_total["lines"] >= self.LARGE_COMMIT_THRESHOLD:
                large_commit_count += 1

            commit_count += 1

        return large_commit_count / commit_count

    def get_commit_statistics(self, return_data=False):
        """Get commit statistics.
        Based off: https://gist.github.com/mrVanDalo/6a1d1aed4bd613fbdf1fa751fca47c6a"""
        commit_timeline = []

        all_commits = []

        committers = {}

        commit_timeline_per_contributor = {}

        for log_entry in self.repo.iter_commits("--no-merges", all=True):
            commit = self.repo.commit(log_entry)

            commit_email = commit.committer.email
            commit_datetime = commit.committed_datetime.timestamp()
            commit_stats_total = commit.stats.total

            key_commit_data = {
                "committed_date": commit_datetime,
                "committer_email": commit_email,
                "stats_total": commit_stats_total
            }

            commit_timeline.append(key_commit_data)

            if commit_email not in commit_timeline_per_contributor:
                commit_timeline_per_contributor[commit_email] = []

            commit_timeline_per_contributor[commit_email].append({
                "committed_date": commit_datetime,
                "stats_total": commit_stats_total
            })

            if commit_email not in committers:
                committers[commit_email] = {
                    "count": 0,
                    "insertions": {},
                    "deletions": {},
                    "lines": {},
                    "files_touched": {},
                }

            Util.add_count_to_identifier(committers[commit_email], "count",
                                         add=1)
            if return_data:
                all_commits.append({
                    "author_email": commit.author.email,
                    "author_name": commit.author.name,
                    "authored_date": commit.authored_datetime.timestamp(),
                    "changes": commit.stats.files,
                    "committed_date": commit.committed_datetime.timestamp(),
                    "committer_email": commit.committer.email,
                    "committer_name": commit.committer.name,
                    "encoding": commit.encoding,
                    "hash": commit.hexsha,
                    "message": commit.message,
                    "summary": commit.summary,
                    "size": commit.size,
                    "stats_total": commit.stats.total
                })

        all_stats_total = [commit["stats_total"] for commit in commit_timeline]

        for commit_email in commit_timeline_per_contributor:
            committer_stats_total = [commit["stats_total"] for commit in
                                     commit_timeline_per_contributor[commit_email]]

            committers[commit_email]["insertions"] = \
                self.__commit_stats("insertions", committer_stats_total)

            committers[commit_email]["deletions"] = \
                self.__commit_stats("deletions", committer_stats_total)

            committers[commit_email]["lines"] = \
                self.__commit_stats("lines", committer_stats_total)

            committers[commit_email]["files_touched"] = \
                self.__commit_stats("files", committer_stats_total)

            committers[commit_email]["large_commit_ratio"] = \
                self.__calculate_large_commit_ratio(committer_stats_total)

        commit_statistics = {
            "overall": {
                "count": self.get_commit_count(),
                "insertions": self.__commit_stats("insertions", all_stats_total),
                "deletions": self.__commit_stats("deletions", all_stats_total),
                "lines": self.__commit_stats("lines", all_stats_total),
                "files_touched": self.__commit_stats("files", all_stats_total),
                "large_commit_ratio": self.__calculate_large_commit_ratio(
                    all_stats_total),
                "timeline": commit_timeline,
            },
            "committers": committers
        }

        if return_data:
            return commit_statistics, all_commits
        else:
            return commit_statistics

    def get_commit_count(self):
        """Commit count across all branches."""
        count = self.repo.git.rev_list("--all", "--no-merges", "--count")

        return int(count)

    def get_all_file_paths(self, return_file_names=False):
        """Get all file paths in the repository."""
        file_paths = []
        return_filenames = []

        for (dir_path, dir_names, filenames) in walk(self.folder):
            if ".git" not in dir_path:
                for filename in filenames:
                    if filename == ".git":
                        continue

                    path = dir_path.replace(self.folder, '')

                    if path == '':
                        file_paths.append(filename)
                        return_filenames.append(filename)
                    else:
                        file_paths.append(path.replace('/', '', 1) + '/' + filename)
                        return_filenames.append(filename)

        if return_file_names:
            return file_paths, return_filenames

        return file_paths

    def __yield_file_contributions(self, file_path):
        """Yields who-wrote-what for every line for a given file."""
        raw_contributor_data = self.repo.git.annotate(file_path, '-M', '-C', '--minimal',
                                                      '--show-email').split('\n')
        emails = []
        lines_of_code = []

        for line in raw_contributor_data:
            raw_split = line.split(')', 1)

            if line == "":
                continue

            email = re.search('<(.*)>', raw_split[0]).group(1)

            # This encoding and decoding exists because of some funky utf-8 error
            line_code = raw_split[1].encode('utf-8', 'surrogatepass').decode('utf-8',
                                                                             'replace')

            emails.append(email)
            lines_of_code.append(line_code)

            yield email, line_code

    def get_all_contributions(self, allow_print=False, all_files=False):
        """Get who-wrote-what for every file in a repository. Will be returned as a
        (non-binary) tree dictionary."""
        file_paths = self.get_all_file_paths()

        tree = {}

        # Populate tree based of paths
        for path in file_paths:
            sub_tree = tree

            for sub_path in path.split('/'):
                sub_tree = sub_tree.setdefault(sub_path, {})

        for path in file_paths:
            size_in_megabytes = os.path.getsize(self.folder + '/' + path) / 1000000

            sub_tree = tree

            if size_in_megabytes > 1 and not all_files:
                if allow_print:
                    print('Analyzing file ' + path + ' has been skipped as it larger than 1 MB. The size is ' + str(size_in_megabytes) + ' MB.')

                path = path.split('/')

                # TODO: Fix the repeating code
                for index in range(0, len(path)):
                    if index == len(path) - 1:
                        sub_tree[path[index]] = {
                            "is_file": True,
                            "contributors": None
                        }
                    else:
                        sub_tree = sub_tree[path[index]]

                continue

            if allow_print:
                print('Analyzing file ' + path + ', of size ' + str(size_in_megabytes) + ' MB.')

            try:
                contributors = self.__yield_file_contributions(path)

                contributor_data = {
                    "contributors": {}
                }

                for (email, line) in contributors:
                    Util.add_count_to_identifier(contributor_data["contributors"], email,
                                                 add=1)

                path = path.split('/')

                # Add data to certain tree node based of path
                for index in range(0, len(path)):
                    if index == len(path) - 1:
                        sub_tree[path[index]] = {
                            "is_file": True,
                            "contributors": contributor_data['contributors']
                        }
                    else:
                        sub_tree = sub_tree[path[index]]
            except Exception as e:
                if allow_print:
                    print('Failed to find contributors to ' + path + ' in git repository. The file is ignored.')

                path = path.split('/')

                for index in range(0, len(path)):
                    if index == len(path) - 1:
                        sub_tree[path[index]] = {
                            "is_file": True,
                            "contributors": None
                        }
                    else:
                        sub_tree = sub_tree[path[index]]

                continue

        return tree

    @staticmethod
    def __count_regex_based_comment_contribution(original_file, comment,
                                                 file_contribution_metadata,
                                                 email_and_line_combined,
                                                 comment_line_numbers):
        """Counts the line of the comments that have been written and keep tracks
        who-wrote-what line of a comment. Assumes the comment has been found
        with regex."""
        start = comment.start()
        end = comment.end()

        # Based off https://dzone.com/articles/finding-line-number-when
        begin_comment = original_file.count('\n', 0, start) + 1
        end_comment = original_file.count('\n', 0, end) + 1

        for line_number in range(begin_comment, end_comment + 1):
            Util.add_count_to_identifier(
                file_contribution_metadata["contribution_types"]["comments"],
                identifier=email_and_line_combined[line_number - 1][0],
                add=1)

            comment_line_numbers.append(line_number)

    def __recognize_and_count_comments(self, file_suffix, original_file,
                                       file_contribution_metadata,
                                       email_and_line_combined,
                                       comment_line_numbers):
        """Recognizes comments in code files and stores who-wrote-what
        for each comment. It should be noted that extracting comments from code using
        regex is suboptimal and has some caveats. Nonetheless, it serves as fast and
        a good-enough heuristic."""
        # Almost all recognized code file prefixes are of programming languages
        # that make use of C-style commenting, however the Python language
        # doesn't use C-style commenting. Hence, a special condition for it.
        if file_suffix == '.py':
            # Remove some poorly placed three-double quotes. The next regexp
            # after these two relies on them not being there.
            original_file = re.sub('\'"*\'', '""', original_file)
            original_file = re.sub("\"'*\"", '""', original_file)

            # Regex thanks to https://stackoverflow.com/questions/36341733/
            # regex-expression-for-multiline-comment-in-python
            for multiline_comment in re.finditer(r'''(['"])\1\1(.*?)\1{3}''',
                                                 original_file, re.DOTALL):
                self.__count_regex_based_comment_contribution(original_file,
                                                              multiline_comment,
                                                              file_contribution_metadata,
                                                              email_and_line_combined,
                                                              comment_line_numbers)

            # Regex thanks to https://hg.python.org/cpython/file/2.7/Lib/tokenize.py
            for comment in re.finditer("#[^\r\n]*", original_file):
                self.__count_regex_based_comment_contribution(original_file,
                                                              comment,
                                                              file_contribution_metadata,
                                                              email_and_line_combined,
                                                              comment_line_numbers)

        else:
            # Make all strings empty to prevent possible comment count skew.
            original_file = re.sub('"(.*?)"', '""', original_file)
            original_file = re.sub("'(.*?)'", "''", original_file)

            # Regex thanks to https://blog.ostermiller.org/find-comment
            for comment in re.finditer(
                    r"(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)", original_file):
                self.__count_regex_based_comment_contribution(original_file,
                                                              comment,
                                                              file_contribution_metadata,
                                                              email_and_line_combined,
                                                              comment_line_numbers)

    @staticmethod
    def __count_file_contributions(contribution_type, email_and_line_combined,
                                   file_contribution_metadata, excluded_lines=[]):
        """Count who-wrote-what for a certain file."""
        line_number = 0

        if len(email_and_line_combined) == 0:
            return

        for _ in range(len(email_and_line_combined)):
            if len(excluded_lines) > 0:
                if line_number not in excluded_lines:
                    Util.add_count_to_identifier(
                        file_contribution_metadata["contribution_types"]
                        [contribution_type],
                        identifier=email_and_line_combined[line_number - 1][0],
                        add=1)
            else:
                Util.add_count_to_identifier(
                    file_contribution_metadata["contribution_types"][contribution_type],
                    identifier=email_and_line_combined[line_number - 1][0],
                    add=1)

            line_number += 1

    @staticmethod
    def __is_test_file(file_path, filename):
        """Determine if a file is a test file based on the folder name or the filename."""
        is_test_file = False

        if any(word in file_path.split('/') for word in ['test', 'tests']):
            is_test_file = True
        elif re.match(
                r"(\A|[^A-Za-z])([_-]?[Tt][Ee][Ss][Tt][_-]?)([^A-Za-z]" +
                r"|\Z)|([a-z][T][Ee][Ss][Tt])([A-Z]|\Z)",
                filename):
            is_test_file = True

        return is_test_file

    @staticmethod
    def __aggregate_types_of_contributions(files):
        """Aggregate types of contribution data to show summary."""
        aggregate_data = {
            "overall": {
                "code": 0,
                "test": 0,
                "comments": 0,
                "configuration": 0,
                "user_interface": 0,
                "documentation": 0
            },
            "contributors": {}
        }

        for file in files:
            for contribution_type, contributors in file["contribution_types"].items():
                for contributor in contributors:
                    aggregate_data["overall"][contribution_type] += \
                        contributors[contributor]

                    if contributor not in aggregate_data["contributors"]:
                        aggregate_data["contributors"][contributor] = {
                            "code": 0,
                            "test": 0,
                            "comments": 0,
                            "configuration": 0,
                            "user_interface": 0,
                            "documentation": 0
                        }

                    Util.add_count_to_identifier(aggregate_data["contributors"]
                                                 [contributor], contribution_type,
                                                 add=contributors[contributor])

        return aggregate_data

    def get_types_of_contributions(self, return_data=False, allow_print=False, all_files=False):
        """Recognize certain types of contributions."""
        file_paths, filenames = self.get_all_file_paths(return_file_names=True)

        files_with_types_of_contribution = []

        for (file_path, filename) in list(zip(file_paths, filenames)):
            # Binary files are excluded
            if is_binary(self.folder + '/' + file_path):
                continue
   
            size_in_megabytes = os.path.getsize(self.folder + '/' + file_path) / 1000000

            if size_in_megabytes > 1 and not all_files:
                if allow_print:
                    print('Analyzing file ' + file_path + ' has been skipped as it larger than 1 MB. The size is ' + str(size_in_megabytes) + ' MB.')
                continue

            if allow_print:
                print('Analyzing file ' + file_path + ', of size ' + str(size_in_megabytes) + ' MB.')
  
            try:
                contributions = self.__yield_file_contributions(file_path)
                email_and_line_combined = list(contributions)
            except Exception:
                if allow_print:
                    print('Failed to find contributors to ' + file_path + ' in git repository. The file is ignored.')
                continue

            file_suffix = pathlib.Path(file_path).suffix.lower()

            # Dict to hold information on contribution
            file_contribution_metadata = {
                "file_path": file_path,
                "filename": filename,
                "file_suffix": file_suffix,
                "contribution_types": {
                    "code": {},
                    "test": {},
                    "comments": {},
                    "configuration": {},
                    "user_interface": {},
                    "documentation": {}
                }
            }

            if (file_suffix in self.CONFIG_FILE_PREFIXES) \
                    or (filename in self.CONFIG_FILENAMES):
                self.__count_file_contributions("configuration", email_and_line_combined,
                                                file_contribution_metadata)
            elif (file_suffix in self.DOC_FILE_PREFIXES) \
                    or (filename in self.DOC_FILENAMES):
                self.__count_file_contributions("documentation", email_and_line_combined,
                                                file_contribution_metadata)
            elif file_suffix in self.CODE_FILE_PREFIXES:
                original_file = ""

                # Recreate original file for regex parsing.
                for (email, line) in email_and_line_combined:
                    original_file += line + '\n'

                # Store all comment line numbers so that we can exclude them for
                # counting lines of code/test.
                comment_line_numbers = []

                # Recognize and count comments.
                self.__recognize_and_count_comments(file_suffix, original_file,
                                                    file_contribution_metadata,
                                                    email_and_line_combined,
                                                    comment_line_numbers)

                # Determine contribution type.
                contribution_type = "test" if self.__is_test_file(file_path, filename) \
                    else "code"

                # Count file contribution and exclude comment lines.
                self.__count_file_contributions(contribution_type,
                                                email_and_line_combined,
                                                file_contribution_metadata,
                                                excluded_lines=comment_line_numbers)
            elif file_suffix in self.UI_FILE_PREFIXES:
                self.__count_file_contributions("user_interface", email_and_line_combined,
                                                file_contribution_metadata)

            files_with_types_of_contribution.append(file_contribution_metadata)

        if return_data:
            return self.__aggregate_types_of_contributions(
                       files_with_types_of_contribution), files_with_types_of_contribution
        else:
            return self.__aggregate_types_of_contributions(
                       files_with_types_of_contribution)
