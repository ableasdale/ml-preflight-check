#!/usr/bin/env python
"""MarkLogic pre-flight check"""

from __future__ import print_function
import os
import socket
#import psutil
#import psi.process
import xml.etree.ElementTree

###################################################################
# Global variables
###################################################################
import subprocess

MARKLOGIC_FOREST_DIRECTORY = "/var/opt/MarkLogic/Forests/"
MARKLOGIC_FOREST_ASSIGNMENTS_XML = "/var/opt/MarkLogic/assignments.xml"
XML_NAMESPACES = {'a': 'http://marklogic.com/xdmp/assignments'}
MARKLOGIC_PORTS = [7997, 7998, 7999, 8000, 8001, 8002]

BOUND_WARN = ('\033[31m' + "IN USE" + '\033[0m')
CHECK = ('\033[31m' + "CHECK" + '\033[0m')
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

def pass_or_fail(value):
    if (value > 0):
        return CHECK
    else:
        return OK

def is_marklogic_running():
    p = subprocess.Popen(['pgrep', 'MarkLogic'], stdout=subprocess.PIPE).communicate()[0]
    total_procs = len(p.splitlines())

    print (str(total_procs) + " running MarkLogic processes detected\t\t\t [  " + pass_or_fail(total_procs) + "  ]")

    if (total_procs > 0):
        for x in p.splitlines():
            print("\t - \tRunning MarkLogic process found with pid: " + x)

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
    print(forest_name + str(data_directory))
    journal_dir = os.listdir(MARKLOGIC_FOREST_DIRECTORY + forest_name + "/Journals")
    print(len(journal_dir))
    # for file in dirs:
    #    print(file)

    ###
    # simple version for working with CWD
    # print len([name for name in os.listdir('.') if os.path.isfile(name)])

    # path joining version for other paths
    # DIR = '/tmp'
    # print len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]

#ps = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE).communicate()[0]

# p = subprocess.Popen(['pgrep', '-l' , 'MarkLogic'], stdout=subprocess.PIPE).communicate()[0]

# out, err = p.communicate()

# processes = ps.split('\n')
# this specifies the number of splits, so the splitted lines
# will have (nfields+1) elements
# nfields = len(processes[0].split()) - 1
#for row in processes[1:]:
#    print(row.split(None, nfields))
