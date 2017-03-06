# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from pytest_testdox import parsers


class TestParseNodeId(object):

    def test_should_return_a_node_instance(self):
        nodeid = 'tests/test_module.py::test_title'
        node = parsers.parse_node(nodeid)

        assert isinstance(node, parsers.Node)
#        nodeid = 'tests/test_module.py::TestClassName::()::test_title'

    def test_should_parse_node_id_attributes(self):
        nodeid = 'tests/test_module.py::test_title'
        node = parsers.parse_node(nodeid)

        assert node.title == 'test_title'
        assert node.module_name == 'tests.test_module'

    @pytest.mark.parametrize('nodeid,class_name', (
        ('tests/test_module.py::test_title', None),
        (
            'tests/test_module.py::TestClassName::()::test_title',
            'TestClassName'
        )
    ))
    def test_should_parse_class_name(self, nodeid, class_name):
        node = parsers.parse_node(nodeid)

        assert node.class_name == class_name