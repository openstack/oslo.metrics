# Copyright 2020 LINE Corp.
# All Rights Reserved.
#
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

import json


class UnSupportedMetricActionError(Exception):
    def __init__(self, message=None):
        self.message = message


class MetricValidationError(Exception):
    def __init__(self, message=None):
        self.message = message


class MetricAction():
    actions = ['inc', 'observe']

    def __init__(self, action, value):
        if action not in self.actions:
            raise UnSupportedMetricActionError(
                "%s action is not supported" % action)
        self.action = action
        self.value = value

    @classmethod
    def validate(cls, metric_action_dict):
        if "value" not in metric_action_dict:
            raise MetricValidationError("action need 'value' field")
        if "action" not in metric_action_dict:
            raise MetricValidationError("action need 'action' field")
        if metric_action_dict["action"] not in cls.actions:
            raise MetricValidationError(
                "action should be choosen from %s" % cls.actions)

    @classmethod
    def from_dict(cls, metric_action_dict):
        return cls(
            metric_action_dict["action"],
            metric_action_dict["value"]
        )


class Metric():
    def __init__(self, module, name, action, **labels):
        self.module = module
        self.name = name
        self.action = action
        self.labels = labels

    def to_json(self):
        raw = {
            "module": self.module,
            "name": self.name,
            "action": {
                "value": self.action.value,
                "action": self.action.action
            },
            "labels": self.labels
        }
        return json.dumps(raw)

    @classmethod
    def from_json(cls, encoded):
        metric_dict = json.loads(encoded)
        cls._validate(metric_dict)
        return Metric(
            metric_dict["module"],
            metric_dict["name"],
            MetricAction.from_dict(metric_dict["action"]),
            **metric_dict["labels"])

    @classmethod
    def _validate(cls, metric_dict):
        if "module" not in metric_dict:
            raise MetricValidationError("module should be specified")

        if "name" not in metric_dict:
            raise MetricValidationError("name should be specified")

        if "action" not in metric_dict:
            raise MetricValidationError("action should be specified")

        if "labels" not in metric_dict:
            raise MetricValidationError("labels should be specified")

        MetricAction.validate(metric_dict["action"])
