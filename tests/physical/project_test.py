#!/usr/bin/env python
# -*- coding: utf-8 -*-


from src.physical.project import PhysicalProject


class TestProject:
    """We use a test repo (that is added as a submodule to the Geit repo) to verify
    the behaviour of PhysicalProject functions."""
    project = PhysicalProject("../resources/geit-test-repo")

    # Constants derived from test-repo
    AMOUNT_OF_INSERTIONS_IN_TEST_REPO = 21
    AMOUNT_OF_COMMITS_IN_TEST_REPO = 2
    AMOUNT_OF_FILES = 2
    COMMIT_RATIO = 0.0
    AMOUNT_OF_COMMENTS = 10
    AMOUNT_OF_CODE = 11
    AMOUNT_OF_BRANCHES = 2
    AMOUNT_OF_COMMITTERS = 1
    FILE_PATHS = ['comments.c', 'comments.py']

    def test_number_of_branches(self):
        # Note this function returns the remote number of branches
        assert self.project.get_number_of_branches() is self.AMOUNT_OF_BRANCHES

    def test_get_committer_count(self):
        assert self.project.get_committer_count() is self.AMOUNT_OF_COMMITTERS

    def test_get_commit_count(self):
        assert self.project.get_commit_count() == self.AMOUNT_OF_COMMITS_IN_TEST_REPO

    def test_get_commit_statistics_overall_count(self):
        data = self.project.get_commit_statistics()

        assert data["overall"]["count"] == self.AMOUNT_OF_COMMITS_IN_TEST_REPO

    def test_get_commit_statistics_overall_insertions(self):
        data = self.project.get_commit_statistics()

        assert data["overall"]["insertions"]["sum"] == \
            self.AMOUNT_OF_INSERTIONS_IN_TEST_REPO

    def test_get_commit_statistics_overall_timeline(self):
        data = self.project.get_commit_statistics()

        assert len(data["overall"]["timeline"]) == self.AMOUNT_OF_COMMITS_IN_TEST_REPO

    def test_get_commit_statistics_files_touched(self):
        data = self.project.get_commit_statistics()

        assert data["overall"]["files_touched"]["sum"] == self.AMOUNT_OF_FILES

    def test_get_commit_statistics_commit_ratio(self):
        data = self.project.get_commit_statistics()

        assert data["overall"]["large_commit_ratio"] == self.COMMIT_RATIO

    def test_get_all_file_paths(self):
        data = self.project.get_all_file_paths()

        assert data == self.FILE_PATHS

    def test_get_types_of_contributions_code_count(self):
        data = self.project.get_types_of_contributions()

        assert data["overall"]["code"] == self.AMOUNT_OF_CODE

    def test_get_types_of_contributions_comment_count(self):
        data = self.project.get_types_of_contributions()

        assert data["overall"]["comments"] == self.AMOUNT_OF_COMMENTS
