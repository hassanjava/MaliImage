from pysnmp.hlapi import *
import json
import logging

logging.basicConfig(filename='getlogger.log', level=logging.DEBUG)


def bulkQuery(hostip, oid):
    snmp_iter = bulkCmd(SnmpEngine(),
                        CommunityData('public'),
                        UdpTransportTarget((hostip, 161)),
                        ContextData(),
                        0, 100,
                        ObjectType(ObjectIdentity(oid)),
                        lexicographicMode=True)
    for errorIndication, errorStatus, errorIndex, varBinds in snmp_iter:
        # Check for errors and print out results
        if errorIndication:
            logging.debug(errorIndication)
        elif errorStatus:
            logging.debug('%s at %s' % (errorStatus.prettyPrint(),
                                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            # logging.debug('Log GetBulk command is sent')
            for varBind in varBinds:
                logging.debug(' = '.join([x.prettyPrint() for x in varBind]))


def get_query(ip_address, oid):
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in getCmd(SnmpEngine(),
                             CommunityData('public'),
                             UdpTransportTarget(transportAddr=(ip_address, 161)

                                                ),
                             ContextData(),
                             ObjectType(ObjectIdentity(oid)),
                             lexicographicMode=False,
                             lookupMib=False):
        if errorIndication:
            raise Exception("SNMP nextCmd {}".format(str(errorIndication)))
        elif errorStatus:
            raise Exception('SNMP nextCmd %s at %s' % (
                errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            # logging.debug('Log Software version:')
            for varBind in varBinds:
                logging.debug(' = '.join([x.prettyPrint() for x in varBind]))


def walk_query(ip_address, oid):
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in nextCmd(SnmpEngine(),
                              CommunityData('public'),
                              UdpTransportTarget(transportAddr=(ip_address, 161)

                                                 ),
                              ContextData(),
                              ObjectType(ObjectIdentity(oid)),
                              lexicographicMode=False,
                              lookupMib=False):
        if errorIndication:
            raise Exception("SNMP nextCmd {}".format(str(errorIndication)))
        elif errorStatus:
            raise Exception('SNMP nextCmd %s at %s' % (
                errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            #logging.debug('Log GetBulk command is sent')
            for varBind in varBinds:
                logging.debug(' = '.join([x.prettyPrint() for x in varBind]))


with open('devices.json', 'rt') as f:
    devices = json.load(f)
oid = devices['oid']
for ip in devices['ip']:
    logging.debug('Log Software version (etsiVersion):')
    get_query(ip, '1.3.6.1.4.1.637.61.1.9.28.1.0')
#for ip in devices['ip']:
    #logging.debug('Log Next command is sent')
    #walk_query(ip,oid)
    #logging.debug('Log Next command is finished for ip '+ip)
for ip in devices['ip']:
    logging.debug('Log GetBulk command is sent')
    bulkQuery(ip, oid)
    logging.debug('Log GetBulk command is finished for ip '+ip)

