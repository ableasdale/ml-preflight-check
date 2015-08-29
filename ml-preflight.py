import socket
import xml.etree.ElementTree as ET

###################################################################
# Global variables
###################################################################

MARKLOGIC_FOREST_DIRECTORY = "/var/opt/MarkLogic"
MARKLOGIC_FOREST_ASSIGNMENTS_XML = "/var/opt/MarkLogic/assignments.xml"
XML_NAMESPACES = {'a': 'http://marklogic.com/xdmp/assignments'} 
MARKLOGIC_PORTS = [7997, 7998, 7999, 8000, 8001, 8002]
LOCALHOST = "0.0.0.0"

###################################################################
# Functions 
###################################################################

"""Check a given TCP port to ensure it's not already bound

    Args:
        hostname: the hostname (FQDN) or IP address.
	port: the TCP port.

    Returns:
        true if the port is already bound.

    pydoc -w checkPortBinding

"""
def checkPortBinding(hostname, port):
    print("Checking port "+ str(port));
    captive_dns_addr = ""
    host_addr = ""

    try:
        captive_dns_addr = socket.gethostbyname(LOCALHOST)
    except:
        pass

    try:
        host_addr = socket.gethostbyname(hostname)

        if (captive_dns_addr == host_addr):
            return False

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((hostname, port))
        s.close()
    except:
        return False

    return True


###################################################################
# Main
###################################################################

# Check ports
for x in MARKLOGIC_PORTS:
    print(checkPortBinding(LOCALHOST, x)),

# Check journals
print "Checking Journals for this host [TODO - host]\n"
tree = ET.parse(MARKLOGIC_FOREST_ASSIGNMENTS_XML)
root = tree.getroot()
for x in root.findall("a:assignment", XML_NAMESPACES):
    print x.find("a:forest-name", XML_NAMESPACES).text,
    print x.find("a:data-directory", XML_NAMESPACES).text,

