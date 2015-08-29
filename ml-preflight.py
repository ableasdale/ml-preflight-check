import socket
import xml.etree.ElementTree as ET

MARKLOGIC_FOREST_ASSIGNMENTS_XML = "/var/opt/MarkLogic/assignments.xml"
XML_NAMESPACES = {'a': 'http://marklogic.com/xdmp/assignments'} 
MARKLOGIC_PORTS = [7997, 7998, 7999, 8000, 8001, 8002]
LOCALHOST = "0.0.0.0"

def DoesServiceExist(host, port):
    print("Checking port "+ str(port));
    captive_dns_addr = ""
    host_addr = ""

    try:
        captive_dns_addr = socket.gethostbyname(LOCALHOST)
    except:
        pass

    try:
        host_addr = socket.gethostbyname(host)

        if (captive_dns_addr == host_addr):
            return False

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((host, port))
        s.close()
    except:
        return False

    return True


# check ports
for x in MARKLOGIC_PORTS:
    print(DoesServiceExist(LOCALHOST, x)),



# check journals
print "Checking Journals for this host [TODO - host]\n"
tree = ET.parse(MARKLOGIC_FOREST_ASSIGNMENTS_XML)
root = tree.getroot()
for x in root.findall("a:assignment", XML_NAMESPACES):
    print x.find("a:forest-name", XML_NAMESPACES).text,
    print x.find("a:data-directory", XML_NAMESPACES).text,

