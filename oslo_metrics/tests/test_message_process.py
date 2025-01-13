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
test_message_process
--------------------
Check that messages are processed correctly
"""

from unittest import mock

from oslo_metrics import message_router
from oslotest import base
import prometheus_client


class TestProcessMessage(base.BaseTestCase):

    def setUp(self):
        super().setUp()

    def test_process_counter(self):
        received_json = b"""{
  "module": "oslo_messaging",
  "name": "rpc_server_invocation_start_total",
  "action": {
    "action": "inc",
    "value": null
  },
  "labels": {
    "exchange": "foo",
    "topic": "bar",
    "server": "foobar",
    "endpoint": "endpoint",
    "namespace": "ns",
    "version": "v2",
    "method": "get",
    "process": "done"
  }
}"""

        with mock.patch.object(
            prometheus_client.Counter, 'inc',
        ) as mock_inc:
            router = message_router.MessageRouter()
            router.process(received_json)
            mock_inc.assert_called_once_with()

    def test_process_histogram(self):
        received_json = b"""{
  "module": "oslo_messaging",
  "name": "rpc_client_processing_seconds",
  "action": {
    "action": "observe",
    "value": 1.26
  },
  "labels": {
    "call_type": "call",
    "exchange": "foo",
    "topic": "bar",
    "method": "get",
    "server": "foobar",
    "namespace": "ns",
    "version": "v2",
    "process": "done",
    "fanout": "foo",
    "timeout": 10
  }
}"""

        with mock.patch.object(
            prometheus_client.Histogram, 'observe',
        ) as mock_inc:
            router = message_router.MessageRouter()
            router.process(received_json)
            mock_inc.assert_called_once_with(1.26)
