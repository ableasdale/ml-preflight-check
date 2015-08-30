#!/usr/bin/env python
"""MarkLogic pre-flight check"""

from __future__ import print_function
import socket
import xml.etree.ElementTree

###################################################################
# Global variables
###################################################################

MARKLOGIC_FOREST_DIRECTORY = "/var/opt/MarkLogic"
MARKLOGIC_FOREST_ASSIGNMENTS_XML = "/var/opt/MarkLogic/assignments.xml"
XML_NAMESPACES = {'a': 'http://marklogic.com/xdmp/assignments'}
MARKLOGIC_PORTS = [7997, 7998, 7999, 8000, 8001, 8002]

BOUND_WARN = ('\033[31m' + "IN USE" + '\033[0m')
OK = ('\033[32m' + "OK" + '\033[0m')
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

    if check_port_binding(tcp_port):
        print("Checking binding for port {0}: \t\t\t [  {1}  ]".format(str(tcp_port), BOUND_WARN))
    else:
        print("Checking binding for port {0}: \t\t\t [  {1}  ]".format(str(tcp_port), OK))


def get_xml():
    """Gets XML root

        Returns:
            parsed XML element tree."""
    return xml.etree.ElementTree.parse(MARKLOGIC_FOREST_ASSIGNMENTS_XML).getroot()


###################################################################
# Main
###################################################################

print("Running pre-flight check for host: " + HOSTNAME)

# Check ports
for port in MARKLOGIC_PORTS:
    is_port_open(port)

# Check journals
for x in get_xml().findall("a:assignment", XML_NAMESPACES):
    forest_name = x.find("a:forest-name", XML_NAMESPACES).text
    data_directory = x.find("a:data-directory", XML_NAMESPACES).text
    print(forest_name + str(data_directory))
