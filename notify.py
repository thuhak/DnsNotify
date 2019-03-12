#!/usr/bin/env python
# author: thuhak.zhou@nio.com
from argparse import ArgumentParser
import logging
import dns.flags
import dns.opcode
import dns.rcode
from dns import name, rdatatype, rdataclass, message, query


logging.basicConfig(level=logging.INFO)


def make_notify(qname):
    """
    according to RFC1035 and RFC1996
    """
    qname = name.from_text(qname)
    rdtype = rdatatype.SOA
    rdclass = rdataclass.IN

    m = message.Message()
    m.flags |= dns.flags.AA
    m.flags |= dns.opcode.to_flags(dns.opcode.NOTIFY)
    m.find_rrset(m.question, qname, rdclass, rdtype, create=True, force_unique=True)
    return m


def notify(nameserver , qname):
    request = make_notify(qname)
    response = query.udp(request, nameserver, timeout=3)
    rcode = response.rcode()
    if rcode == 0:
        logging.info('notifying server {} for zone {} success'.format(nameserver, qname))
    else:
        logging.error('notifying server {} for zone {} fail, reason {}'.format(nameserver, qname, dns.rcode.to_text(rcode)))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('server', help='the downstream nameserver')
    parser.add_argument('-z', '--zone', help='the zone you wanna sync')
    args = parser.parse_args()
    server = args.server
    zone = args.zone
    notify(server, zone)