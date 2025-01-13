# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
test_message_validation
--------------------
Check that messages validation is working properly
"""

import json
from oslo_metrics import message_type
from oslotest import base


class TestMetricValidation(base.BaseTestCase):
    def setUp(self):
        super().setUp()

    def assertRaisesWithMessage(self, message, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            self.assertFail()
        except Exception as e:
            self.assertEqual(message, e.message)

    def test_message_validation(self):
        metric = dict()
        message = "module should be specified"
        self.assertRaisesWithMessage(
            message, message_type.Metric.from_json, json.dumps(metric))

        metric['module'] = "test"
        message = "name should be specified"
        self.assertRaisesWithMessage(
            message, message_type.Metric.from_json, json.dumps(metric))

        metric['name'] = "test"
        message = "action should be specified"
        self.assertRaisesWithMessage(
            message, message_type.Metric.from_json, json.dumps(metric))

        metric['action'] = "test"
        message = "labels should be specified"
        self.assertRaisesWithMessage(
            message, message_type.Metric.from_json, json.dumps(metric))

        metric['labels'] = "test_label"
        message = "action need 'value' field"
        self.assertRaisesWithMessage(
            message, message_type.Metric.from_json, json.dumps(metric))

        metric['action'] = {"value": "1"}
        message = "action need 'action' field"
        self.assertRaisesWithMessage(
            message, message_type.Metric.from_json, json.dumps(metric))

        metric['action']['action'] = "test"
        message = "action should be choosen from ['inc', 'observe']"
        self.assertRaisesWithMessage(
            message, message_type.Metric.from_json, json.dumps(metric))
