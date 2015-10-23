#!/usr/bin/env python

# quick checker for nagios status
import json
import socket
import sys

def get_statusfiles(services):
    # parse the status.dat files listed in the config
    # return the status of the servers in a hash
    nagstatus = {}
    nagstatus['critical'] = 0
    nagstatus['warning'] = 0
    for region in services.keys():
        nagstatus[region] = {}
        nagstatus[region]['warning'] = 0
        nagstatus[region]['critical'] = 0
        nagstatus[region]['unknown'] = 0
        try:
            result = get_livestatus(services[region]['host'],
                                    services[region]['port'])
            nagstatus[region] = {'warning': result['critical'],
                                 'critical': result['warning']}
            nagstatus['critical'] += result['critical']
            nagstatus['warning'] += result['warning']
        except:
            nagstatus[region] = {'warning': 'Unknown',
                                 'critical': 'Unknown'}
    return nagstatus


def get_livestatus(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print "socket error"
        sys.exit()

    try:
        remote_ip = socket.gethostbyname(host)

    except socket.gaierror:
        sys.exit()

    #Connect to remote server
    s.connect((remote_ip, port))

    try :
        s.sendall('hitme')
    except socket.error:
        #Send failed
        print "socket error"
        sys.exit()

    reply = s.recv(16384)
    s.close()
    return json.loads(reply)

