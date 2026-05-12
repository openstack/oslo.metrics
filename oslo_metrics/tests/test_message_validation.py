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
-----------------------

Check that messages validation is working properly
"""

import json
from typing import Any

from oslo_metrics import message_type
from oslotest import base


class TestMetricValidation(base.BaseTestCase):
    def test_message_validation(self):
        metric: dict[str, Any] = {}
        self.assertRaisesRegex(
            message_type.MetricValidationError,
            r"^module should be specified$",
            message_type.Metric.from_json,
            json.dumps(metric),
        )

        metric['module'] = "test"
        self.assertRaisesRegex(
            message_type.MetricValidationError,
            r"^name should be specified$",
            message_type.Metric.from_json,
            json.dumps(metric),
        )

        metric['name'] = "test"
        self.assertRaisesRegex(
            message_type.MetricValidationError,
            r"^action should be specified$",
            message_type.Metric.from_json,
            json.dumps(metric),
        )

        metric['action'] = "test"
        self.assertRaisesRegex(
            message_type.MetricValidationError,
            r"^labels should be specified$",
            message_type.Metric.from_json,
            json.dumps(metric),
        )

        metric['labels'] = "test_label"
        self.assertRaisesRegex(
            message_type.MetricValidationError,
            r"^action need 'value' field$",
            message_type.Metric.from_json,
            json.dumps(metric),
        )

        metric['action'] = {"value": "1"}
        self.assertRaisesRegex(
            message_type.MetricValidationError,
            r"^action need 'action' field$",
            message_type.Metric.from_json,
            json.dumps(metric),
        )

        metric['action']['action'] = "test"
        self.assertRaisesRegex(
            message_type.MetricValidationError,
            r"^action should be choosen from \['inc', 'observe'\]$",
            message_type.Metric.from_json,
            json.dumps(metric),
        )
