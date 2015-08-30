#!/usr/bin/env python
"""MarkLogic pre-flight check"""

from __future__ import print_function
import socket
import xml.etree.ElementTree as et

###################################################################
# Global variables
###################################################################

MARKLOGIC_FOREST_DIRECTORY = "/var/opt/MarkLogic"
MARKLOGIC_FOREST_ASSIGNMENTS_XML = "/var/opt/MarkLogic/assignments.xml"
XML_NAMESPACES = {'a': 'http://marklogic.com/xdmp/assignments'}
MARKLOGIC_PORTS = [7997, 7998, 7999, 8000, 8001, 8002]
LOCALHOST = "0.0.0.0"

# BOUND_WARN = ('\033[91m'+"PORT ALREADY BOUND"+'\033[0m')
# OK = ('\033[92m'+"OK"+'\033[0m')
BOUND_WARN = ('\033[91m'+"IN USE"+'\033[0m')
OK = ('\033[32m'+"OK"+'\033[0m')


###################################################################
# Functions
###################################################################

def check_port_binding(hostname, port):
    """Check a given TCP port to ensure it's not already bound

        Args:
            hostname: the hostname (FQDN) or IP address.
        port: the TCP port.

        Returns:
            true if the port is already bound.

    pydoc -w checkPortBinding"""
    # print("Checking port " + str(port))
    captive_dns_addr = ""
    host_addr = ""

    try:
        captive_dns_addr = socket.gethostbyname(LOCALHOST)
    except:
        pass

    try:
        host_addr = socket.gethostbyname("example.com")

        if captive_dns_addr == host_addr:
            return False

        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.settimeout(1)
        test_socket.connect((hostname, port))
        test_socket.close()
    except:
        return False

    return True

def is_port_open(hostname, port):
    if check_port_binding(hostname,port):
        print("Checking binding for port {0}: \t\t\t [  {1}  ]".format(str(port),  BOUND_WARN) )
    else:
        print("Checking binding for port {0}: \t\t\t [  {1}  ]".format(str(port),  OK) )

def get_xml():
    """Gets XML root

        Returns:
            parsed XML element tree."""
    return et.parse(MARKLOGIC_FOREST_ASSIGNMENTS_XML).getroot()


###################################################################
# Main
###################################################################


# Check ports
for x in MARKLOGIC_PORTS:
    is_port_open(LOCALHOST, x)

# Check journals
print("Checking Journals for this host [TODO - host]")
for x in get_xml().findall("a:assignment", XML_NAMESPACES):
    print(x.find("a:forest-name", XML_NAMESPACES).text)
    print(x.find("a:data-directory", XML_NAMESPACES).text)
