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

from oslo_log import log as logging
from oslo_utils import importutils

from oslo_metrics import message_type

LOG = logging.getLogger(__name__)


MODULE_LISTS = [
    "oslo_metrics.metrics.oslo_messaging",
]


class MessageRouter():

    def __init__(self):
        self.modules = {}
        for m_str in MODULE_LISTS:
            mod = importutils.try_import(m_str, False)
            if not mod:
                LOG.error("Failed to load module %s" % m_str)
            self.modules[m_str.split('.')[-1]] = mod

    def process(self, raw_string):
        try:
            metric = message_type.Metric.from_json(raw_string.decode())
            self.dispatch(metric)
        except Exception as e:
            LOG.error("Failed to parse: %s", e)

    def dispatch(self, metric):
        if metric.module not in self.modules:
            LOG.error("Failed to lookup modules by %s" % metric.module)
            return
        mod = self.modules.get(metric.module)

        # Get metric
        try:
            metric_definition = getattr(mod, metric.name)
        except AttributeError as e:
            LOG.error("Failed to load metrics {}: {}".format(metric.name, e))
            return

        # Get labels
        try:
            metric_with_label = getattr(metric_definition, "labels")
            metric_with_label = metric_with_label(**metric.labels)
        except AttributeError as e:
            LOG.error("Failed to load labels func from metrics %s: %s" %
                      (metric.name, e))
            return
        LOG.debug("Get labels with {}: {}".format(metric.name, metric.labels))

        # perform action
        try:
            embed_action = getattr(metric_with_label, metric.action.action)
            if metric.action.value is not None:
                embed_action(metric.action.value)
            else:
                embed_action()
        except AttributeError as e:
            LOG.error("Failed to perform metric actionv %s, %s: %s" %
                      (metric.action.action, metric.action.value, e))
            return
        LOG.debug("Perform action %s for %s metrics" %
                  (metric.action.action, metric.name))
