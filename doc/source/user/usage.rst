=====
Usage
=====

A simple example of oslo.metrics in use::

    $ oslo-metrics
    2020-06-11 15:59:53.459 5435 INFO oslo.metrics.__main__ [-] Start oslo.metrics

Testing with DevStack
---------------------

This section describes how to test out oslo.metrics and collect oslo.messaging metric data using Devstack.

Download DevStack
~~~~~~~~~~~~~~~~~

.. code-block:: console

   $ git clone https://opendev.org/openstack/devstack
   $ cd devstack

The ``devstack`` repo contains a script that installs OpenStack and
templates for configuration files.

Create a local.conf
~~~~~~~~~~~~~~~~~~~

Create a ``local.conf`` file with four passwords preset at the root of the
devstack git repo.

.. code-block:: ini

   [[local|localrc]]
   ADMIN_PASSWORD=secret
   DATABASE_PASSWORD=$ADMIN_PASSWORD
   RABBIT_PASSWORD=$ADMIN_PASSWORD
   SERVICE_PASSWORD=$ADMIN_PASSWORD
   LIBS_FROM_GIT=oslo.messaging

   [[post-config|$NOVA_CONF]]
   [oslo_messaging_metrics]
   metrics_enabled = True

This is the minimum required config to get started with Devstack including
oslo.metrics.

Start the install
~~~~~~~~~~~~~~~~~

.. code-block:: console

   $ ./stack.sh

This will take a 15 - 20 minutes, largely depending on the speed of
your internet connection. Many git trees and packages will be
installed during this process.

Start the Metrics Server
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

   $ oslo-metrics

This command will start oslo.metrics server and start collecting
oslo.messaging metrics sending from OpenStack services.

oslo.metrics exporter will serve on port 3000 by default.

Example Output
~~~~~~~~~~~~~~

An example of oslo.metrics collecting metrics from Nova:

.. code-block:: console

   ubuntu@devstack:~/devstack$ oslo-metrics
   2021-06-12 14:32:26.091 466289 INFO oslo.metrics.__main__ [-] Start oslo.metrics
   2021-06-12 14:57:50.632 466289 DEBUG oslo.metrics.__main__ [-] wait for socket.recv serve /usr/local/lib/python3.8/dist-packages/oslo_metrics/__main__.py:73
   2021-06-12 14:57:50.632 466289 DEBUG oslo.metrics.__main__ [-] got message serve /usr/local/lib/python3.8/dist-packages/oslo_metrics/__main__.py:76
   2021-06-12 14:57:50.633 466289 INFO oslo.metrics.message_router [-] Get labels with rpc_client_processing_seconds: {'call_type': 'call', 'exchange': None, 'topic': 'conductor', 'namespace': 'baseapi', 'version': '1.0', 'server': None, 'fanout': None, 'method': 'ping', 'timeout': None, 'process': ''}
   2021-06-12 14:57:50.633 466289 INFO oslo.metrics.message_router [-] Perform action observe for rpc_client_processing_seconds metrics
   2021-06-12 14:57:50.633 466289 DEBUG oslo.metrics.__main__ [-] wait for socket.recv serve /usr/local/lib/python3.8/dist-packages/oslo_metrics/__main__.py:73
   2021-06-12 14:57:50.633 466289 DEBUG oslo.metrics.__main__ [-] got message serve /usr/local/lib/python3.8/dist-packages/oslo_metrics/__main__.py:76
   2021-06-12 14:57:50.633 466289 INFO oslo.metrics.message_router [-] Get labels with rpc_client_invocation_end_total: {'call_type': 'call', 'exchange': None, 'topic': 'conductor', 'namespace': 'baseapi', 'version': '1.0', 'server': None, 'fanout': None, 'method': 'ping', 'timeout': None, 'process': ''}
   2021-06-12 14:57:50.633 466289 INFO oslo.metrics.message_router [-] Perform action inc for rpc_client_invocation_end_total metrics`

Gathering Metrics
~~~~~~~~~~~~~~~~~

To gather metrics from oslo.metrics, configure Prometheus to scrape from port
3000 where oslo.metrics is running.
