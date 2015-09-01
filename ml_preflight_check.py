#!/usr/bin/env python
"""MarkLogic pre-flight check tool v 0.1 - 30/8/15"""

from __future__ import print_function
import os
import socket
import xml.etree.ElementTree
import subprocess

###################################################################
# Global variables
###################################################################

TABWIDTH = 8
LINE_WIDTH = 56

MARKLOGIC_FOREST_DIRECTORY = "/var/opt/MarkLogic/Forests/"
MARKLOGIC_FOREST_ASSIGNMENTS_XML = "/var/opt/MarkLogic/assignments.xml"
# XML_NAMESPACES = {'a': 'http://marklogic.com/xdmp/assignments'}
MARKLOGIC_PORTS = [7997, 7998, 7999, 8000, 8001, 8002]

BOUND_WARN = ('[  ' + '\033[31m' + "IN USE" + '\033[0m' + '  ]')
WARNING = ('[  ' + '\033[31m' + "WARNING" + '\033[0m' + '  ]')
OK = ('[  ' + '\033[32m' + "OK" + '\033[0m' + '  ]')

HOSTNAME = ('\033[34m' + socket.getfqdn() + '\033[0m')


###################################################################
# Functions
###################################################################

def check_port_binding(tcp_port):
    """Check a given TCP port using the hostname (FQDN) to ensure it's not already bound

        Args:
            tcp_port: the TCP port.

        Returns:
            true if the port is already bound."""

    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.settimeout(1)
        test_socket.connect((socket.getfqdn(), tcp_port))
        test_socket.close()
    except socket.error:
        return False

    return True


def is_port_open(tcp_port):
    """Check a given TCP port using the hostname (FQDN) to ensure it's not already bound

        Args:
            tcp_port: the TCP port.

        Returns:
            A formatted string to display the status of the port on-screen."""

    port_bindings_str = pad_with_tabs(("TCP binding for port " + str(tcp_port)), LINE_WIDTH)

    if check_port_binding(tcp_port):
        print(port_bindings_str + BOUND_WARN)
    else:
        print(port_bindings_str + OK)


def get_xml():
    """Gets XML root

        Returns:
            parsed XML element tree."""
   # try:
   #     ET.register_namespace('a', 'http://marklogic.com/xdmp/assignments')
   # except AttributeError:
   #     def register_namespace(prefix, uri):
   #         ET._namespace_map[uri] = prefix
    return xml.etree.ElementTree.parse(MARKLOGIC_FOREST_ASSIGNMENTS_XML).getroot()


def pass_or_fail(value, evaluator):
    """Pass it a value and one to eval against and it will return a colour formatted string to say whether condition
        passes or fails the test"""
    if value > evaluator:
        return WARNING
    else:
        return OK


def is_marklogic_running():
    """Runs pgrep for the MarkLogic process and reports all related process ids (if any)"""
    process_output = subprocess.Popen(['pgrep', 'MarkLogic'], stdout=subprocess.PIPE).communicate()[0]
    total_procs = len(process_output.splitlines())
    ml_procs_str = pad_with_tabs((str(total_procs) + " running MarkLogic processes detected"), LINE_WIDTH)
    print(ml_procs_str + pass_or_fail(total_procs, 0))

    if total_procs > 0:
        for pid in process_output.splitlines():
            print("\t - \tRunning MarkLogic process found with pid: " + str(pid))


def pad_with_tabs(string, maxlen):
    """Formats the line with tab padding for clear on-screen display"""
    return string + "\t" * ((maxlen - len(string) - 1) / TABWIDTH + 1)


###################################################################
# Main
###################################################################

print("Running pre-flight check for host: " + HOSTNAME)
# Check MarkLogic is not already running on the host
is_marklogic_running()

# Check ports
for port in MARKLOGIC_PORTS:
    is_port_open(port)

# Check journals
for x in get_xml().findall("{http://marklogic.com/xdmp/assignments}assignment"):
    forest_name = x.find("{http://marklogic.com/xdmp/assignments}forest-name").text
    data_directory = x.find("{http://marklogic.com/xdmp/assignments}data-directory").text

    if data_directory:
        # print("Non-default data dir: " + str(data_directory))
        try:
            journal_dir = os.listdir(str(data_directory) + "/Forests/" + forest_name + "/Journals")
            total_jnl_str = pad_with_tabs(
                ("Found " + str(len(journal_dir)) + " journal files for forest " + forest_name), LINE_WIDTH)

            print(total_jnl_str + pass_or_fail(len(journal_dir), 2))
        except OSError:
            print("Forest " + forest_name + " is not a directory on this host")

    else:
	try:
            journal_dir = os.listdir(MARKLOGIC_FOREST_DIRECTORY + forest_name + "/Journals")
            total_jnl_str = pad_with_tabs(("Found " + str(len(journal_dir)) + " journal files for forest " + forest_name),
                                      LINE_WIDTH)
            print(total_jnl_str + pass_or_fail(len(journal_dir), 2))
	except OSError:
 	    print("No directory found for "+forest_name)
