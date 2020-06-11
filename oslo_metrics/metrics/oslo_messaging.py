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

import prometheus_client

standard_labels_for_server = [
    'exchange', 'topic', 'server', 'endpoint', 'namespace',
    'version', 'method', 'process'
]
standard_labels_for_client = [
    'call_type', 'exchange', 'topic', 'namespace', 'version',
    'server', 'fanout', 'process'
]


# RPC Server Metrics
rpc_server_count_for_exception = prometheus_client.Counter(
    'oslo_messaging_rpc_server_exception',
    'The number of times to hit Exception',
    standard_labels_for_server + ['exception', ])

rpc_server_count_for_invocation_start = prometheus_client.Counter(
    'oslo_messaging_rpc_server_invocation_start',
    'The number of times to attempt to invoke method. It doesn\'t count'
    'if rpc server failed to find method from endpoints',
    standard_labels_for_server)

rpc_server_count_for_invocation_end = prometheus_client.Counter(
    'oslo_messaging_rpc_server_invocation_end',
    'The number of times to finish to invoke method.',
    standard_labels_for_server)

rpc_server_processing_time = prometheus_client.Histogram(
    'oslo_messaging_rpc_server_processing_second',
    'rpc server processing time[second]',
    standard_labels_for_server)


# RPC Client Metrics
rpc_client_count_for_exception = prometheus_client.Counter(
    'oslo_messaging_rpc_client_exception',
    'The number of times to hit Exception',
    standard_labels_for_client + ['exception', ])

rpc_client_count_for_invocation_start = prometheus_client.Counter(
    'oslo_messaging_rpc_client_invocation_start',
    'The number of times to invoke method',
    standard_labels_for_client)

rpc_client_count_for_invocation_end = prometheus_client.Counter(
    'oslo_messaging_rpc_client_invocation_end',
    'The number of times to invoke method',
    standard_labels_for_client)

rpc_client_processing_time = prometheus_client.Histogram(
    'oslo_messaging_rpc_client_processing_second',
    'rpc client processing time[second]',
    standard_labels_for_client)
