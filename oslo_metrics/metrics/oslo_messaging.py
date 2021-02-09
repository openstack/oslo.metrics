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

rpc_server_common_labels = [
    'exchange', 'topic', 'server', 'endpoint', 'namespace',
    'version', 'method', 'process'
]
rpc_client_common_labels = [
    'call_type', 'exchange', 'topic', 'namespace', 'version',
    'server', 'fanout', 'process', 'method', 'timeout'
]

rpc_processing_seconds_buckets = [
    0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0,
    2.5, 5.0, 7.5, 10.0, 25.0, 50.0, 75.0, 100
]

# RPC Server Metrics
rpc_server_invocation_start_total = prometheus_client.Counter(
    'oslo_messaging_rpc_server_invocation_start_total',
    'Total number of RPC invocation start. This doesn\'t count'
    'if rpc server failed to find method from endpoints.',
    rpc_server_common_labels)

rpc_server_invocation_end_total = prometheus_client.Counter(
    'oslo_messaging_rpc_server_invocation_end_total',
    'Total number of RPC invocation end.',
    rpc_server_common_labels)

rpc_server_processing_seconds = prometheus_client.Histogram(
    'oslo_messaging_rpc_server_processing_seconds',
    'Duration of RPC processing.',
    rpc_server_common_labels,
    buckets=rpc_processing_seconds_buckets)

rpc_server_exception_total = prometheus_client.Counter(
    'oslo_messaging_rpc_server_exception_total',
    'Total number of exception while RPC processing.',
    rpc_server_common_labels + ['exception'])

# RPC Client Metrics
rpc_client_invocation_start_total = prometheus_client.Counter(
    'oslo_messaging_rpc_client_invocation_start_total',
    'Total number of RPC invocation start.',
    rpc_client_common_labels)

rpc_client_invocation_end_total = prometheus_client.Counter(
    'oslo_messaging_rpc_client_invocation_end_total',
    'Total number of RPC invocation end.',
    rpc_client_common_labels)

rpc_client_processing_seconds = prometheus_client.Histogram(
    'oslo_messaging_rpc_client_processing_seconds',
    'Duration of RPC processing.',
    rpc_client_common_labels,
    buckets=rpc_processing_seconds_buckets)

rpc_client_exception_total = prometheus_client.Counter(
    'oslo_messaging_rpc_client_exception_total',
    'Total number of exception while RPC processing.',
    rpc_client_common_labels + ['exception', ])
