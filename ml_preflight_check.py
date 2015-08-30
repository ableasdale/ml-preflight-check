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
XML_NAMESPACES = {'a': 'http://marklogic.com/xdmp/assignments'}
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
for x in get_xml().findall("a:assignment", XML_NAMESPACES):
    forest_name = x.find("a:forest-name", XML_NAMESPACES).text
    data_directory = x.find("a:data-directory", XML_NAMESPACES).text
    # print(forest_name + str(data_directory))
    journal_dir = os.listdir(MARKLOGIC_FOREST_DIRECTORY + forest_name + "/Journals")
    total_jnl_str = pad_with_tabs(("Found " + str(len(journal_dir)) + " journal files for forest " + forest_name),
                                  LINE_WIDTH)
    print(total_jnl_str + pass_or_fail(len(journal_dir), 2))





















# TODO - crap below line
# for file in dirs:
#    print(file)

###
# simple version for working with CWD
# print len([name for name in os.listdir('.') if os.path.isfile(name)])

# path joining version for other paths
# DIR = '/tmp'
# print len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]

# ps = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE).communicate()[0]

# p = subprocess.Popen(['pgrep', '-l' , 'MarkLogic'], stdout=subprocess.PIPE).communicate()[0]

# out, err = p.communicate()

# processes = ps.split('\n')
# this specifies the number of splits, so the splitted lines
# will have (nfields+1) elements
# nfields = len(processes[0].split()) - 1
# for row in processes[1:]:
#    print(row.split(None, nfields))
