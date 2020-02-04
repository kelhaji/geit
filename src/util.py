#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime


class Util:

    @staticmethod
    def parse_git_datetime(timestamp):
        return datetime.strptime(timestamp, '%a %b %d %H:%M:%S %Y %z').timestamp()

    @staticmethod
    def add_count_to_identifier(dictionary, identifier, add):
        if identifier not in dictionary:
            dictionary[identifier] = 0

        dictionary[identifier] += add

    @staticmethod
    def add_object_to_identifier(dictionary, identifier, add):
        if identifier not in dictionary:
            dictionary[identifier] = 0

        dictionary[identifier] += add
