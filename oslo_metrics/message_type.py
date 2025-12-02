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
from typing import Any, TypedDict


class UnSupportedMetricActionError(Exception):
    def __init__(self, message: str | None = None) -> None:
        self.message = message


class MetricValidationError(Exception):
    def __init__(self, message: str | None = None) -> None:
        self.message = message


class _MetricActionDict(TypedDict, total=False):
    action: str
    value: str


class MetricAction:
    actions = ['inc', 'observe']

    def __init__(self, action: str, value: str) -> None:
        if action not in self.actions:
            raise UnSupportedMetricActionError(
                f"{action} action is not supported"
            )
        self.action = action
        self.value = value

    @classmethod
    def validate(cls, metric_action_dict: _MetricActionDict) -> None:
        if "value" not in metric_action_dict:
            raise MetricValidationError("action need 'value' field")
        if "action" not in metric_action_dict:
            raise MetricValidationError("action need 'action' field")
        if metric_action_dict["action"] not in cls.actions:
            raise MetricValidationError(
                f"action should be choosen from {cls.actions}"
            )

    @classmethod
    def from_dict(
        cls, metric_action_dict: _MetricActionDict
    ) -> 'MetricAction':
        return cls(metric_action_dict["action"], metric_action_dict["value"])


class Metric:
    def __init__(
        self, module: str, name: str, action: MetricAction, **labels: str
    ) -> None:
        self.module = module
        self.name = name
        self.action = action
        self.labels = labels

    def to_json(self) -> str:
        raw = {
            "module": self.module,
            "name": self.name,
            "action": {
                "value": self.action.value,
                "action": self.action.action,
            },
            "labels": self.labels,
        }
        return json.dumps(raw)

    @classmethod
    def from_json(cls, encoded: str) -> 'Metric':
        metric_dict = json.loads(encoded)
        cls._validate(metric_dict)
        return Metric(
            metric_dict["module"],
            metric_dict["name"],
            MetricAction.from_dict(metric_dict["action"]),
            **metric_dict["labels"],
        )

    @classmethod
    def _validate(cls, metric_dict: dict[str, Any]) -> None:
        if "module" not in metric_dict:
            raise MetricValidationError("module should be specified")

        if "name" not in metric_dict:
            raise MetricValidationError("name should be specified")

        if "action" not in metric_dict:
            raise MetricValidationError("action should be specified")

        if "labels" not in metric_dict:
            raise MetricValidationError("labels should be specified")

        MetricAction.validate(metric_dict["action"])
