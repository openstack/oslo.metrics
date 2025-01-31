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

import os
import select
import signal
import socket
import sys
import threading
from wsgiref.simple_server import make_server

from oslo_config import cfg
from oslo_log import log as logging
from prometheus_client import make_wsgi_app

from oslo_metrics import message_router


oslo_metrics_configs = [
    cfg.StrOpt('metrics_socket_file',
               default='/var/tmp/metrics_collector.sock',  # nosec
               help='Unix domain socket file to be used'
                    ' to send rpc related metrics'),
    cfg.PortOpt('prometheus_port', default=3000,
                help='Port number to expose metrics in prometheus format.'),
]
cfg.CONF.register_opts(oslo_metrics_configs, group='oslo_metrics')


LOG = logging.getLogger(__name__)
CONF = cfg.CONF
logging.register_options(CONF)
logging.setup(CONF, 'oslo-metrics')


class MetricsListener():

    def __init__(self, socket_path):
        self.socket_path = socket_path
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.unlink(socket_path)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.socket_path)
        self.start = True
        self.router = message_router.MessageRouter()

    def unlink(self, socket_path):
        try:
            os.unlink(socket_path)
        except OSError:
            if os.path.exists(socket_path):
                raise

    def serve(self):
        while self.start:
            readable, writable, exceptional = select.select(
                [self.socket], [], [], 1)
            if len(readable) == 0:
                continue
            try:
                LOG.debug("wait for socket.recv")
                # 1 message size should be smaller than 65565
                msg = self.socket.recv(65565)
                LOG.debug("got message")
                self.router.process(msg)
            except socket.timeout:
                pass

    def stop(self):
        self.socket.close()
        self.start = False


httpd = None


def handle_sigterm(_signum, _frame):
    LOG.debug("Caught sigterm")
    shutdown_thread = threading.Thread(target=httpd.shutdown)
    shutdown_thread.start()


def main():
    cfg.CONF(sys.argv[1:])
    socket_path = cfg.CONF.oslo_metrics.metrics_socket_file
    m = MetricsListener(socket_path)
    try:
        os.chmod(socket_path, 0o660)  # nosec
    except OSError:
        LOG.error("Changing the mode of the file failed.... continuing")
    mt = threading.Thread(target=m.serve)
    LOG.info("Start oslo.metrics")
    mt.start()

    app = make_wsgi_app()
    try:
        global httpd
        httpd = make_server('', CONF.oslo_metrics.prometheus_port, app)
        signal.signal(signal.SIGTERM, handle_sigterm)
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        LOG.info("Try to stop...")
        os.remove(cfg.CONF.oslo_metrics.metrics_socket_file)
        m.stop()
        httpd.server_close()


if __name__ == "__main__":
    main()
