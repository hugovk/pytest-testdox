# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import namedtuple

import six

from . import formatters

PatternConfig = namedtuple('PatternConfig', 'files functions classes')


@six.python_2_unicode_compatible
class Node(object):

    def __init__(self, title, class_name, module_name):
        self.title = title
        self.class_name = class_name
        self.module_name = module_name

    def __str__(self):
        return self.title

    def __repr__(self):
        return '{}(title={!r}, class_name={!r}, module_name={!r})'.format(
            type(self).__name__,
            self.title,
            self.class_name,
            self.module_name
        )

    def __eq__(self, other):
        return (
            type(self) == type(other) and
            self.title == other.title and
            self.class_name == other.class_name and
            self.module_name == other.module_name
        )

    @classmethod
    def parse(cls, nodeid, pattern_config, overwrite_title=None):
        node_parts = nodeid.split('::')

        if overwrite_title:
            title = overwrite_title
        else:
            title = formatters.format_title(
                node_parts[-1],
                pattern_config.functions
            )

        module_name = formatters.format_module_name(
            node_parts[0],
            pattern_config.files
        )

        class_name = None
        if '()' in node_parts[-2]:
            class_name = formatters.format_class_name(
                node_parts[-3],
                pattern_config.classes
            )
        elif len(node_parts) > 2:
            class_name = formatters.format_class_name(
                node_parts[-2],
                pattern_config.classes
            )

        return cls(title=title, class_name=class_name, module_name=module_name)


@six.python_2_unicode_compatible
class Result(object):

    _OUTCOME_REPRESENTATION = {
        'passed': '[x]',
        'failed': '[ ]',
        'skipped': '>>>',
    }
    _default_outcome_representation = '>>>'

    def __init__(self, outcome, node):
        self.outcome = outcome
        self.node = node

    def __repr__(self):
        return '{}(outcome={!r}, node={!r})'.format(
            type(self).__name__,
            self.outcome,
            self.node
        )

    def __str__(self):
        representation = self._OUTCOME_REPRESENTATION.get(
            self.outcome,
            self._default_outcome_representation
        )

        line = ' {outcome_representation} {node}'.format(
            outcome_representation=representation,
            node=self.node
        )

        return line

    @property
    def header(self):
        return self.node.class_name or self.node.module_name

    @classmethod
    def create(cls, report, pattern_config):
        try:
            overwrite_title = report.testdox_title
        except AttributeError:
            overwrite_title = None

        node = Node.parse(
            nodeid=report.nodeid,
            pattern_config=pattern_config,
            overwrite_title=overwrite_title
        )
        return cls(report.outcome, node)
