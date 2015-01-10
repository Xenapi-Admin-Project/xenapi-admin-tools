#!/usr/bin/python
#rscores.py
# List the load on each core


import XenAPI
import sys, getopt
from XAPIlib import *



def systax():
        print "lscores version 0.0.1"
        print ""
        print "Syntax: lshosts [options]"
        print "-h --help Display help"
        print "-f --follow continues updates"
        print "-n --names  Show Names (default)"
        print "-u --uuid Show UUIDs"
        # print "-t <seconds> - continoues updates every <seconds>
        # I'll need to add this later
        print ""


def defineheadings(mode):
	if mode == "names":
		headings = ('Host', 'CPU Core', 'Utilization')
	elif mode == "uuid":
		headings = ('Host UUID', 'CPU UUID', 'Utilization')
	return headings 
	



def getcpus(session, hosts):
	hostscpu = {}
	for host in hosts:
		hostname = session.xenapi.host.get_hostname(host)
		hostscpu[hostname] = session.xenapi.host.get_host_CPUs(host)

	return hostscpu


def gethosts(session):
	hosts = session.xenapi.host.get_all()
	return hosts

def gethostcpus(session, cpus):
	for x in cpus:
		print x
		for cpu in cpus[x]:
			print session.xenapi.host_cpu.get_number(cpu)
			print session.xenapi.host_cpu.get_utilisation(cpu)
			 	


def main():
   
	try:
                myopts, args = getopt.getopt(sys.argv[1:], "huncw:",["help", "follow", "names", "uuid"])
	except getopt.GetoptError:
                print "Unknown options"
                systax()
                sys.exit(1)

        minspace = 4
        mode = "name"
        follow = False

        for opt, arg in myopts:
                if opt in ("-h", "--help"):
                        syntax()
                        sys.exit(1)
                elif opt in ("-f", "--follow"):
                        follow = True
                elif opt in ("-n", "--name"):
                        mode = "name"
                elif opt in ("-u", "--uuid"):
                        mode = "uuid"


        session = XenAPI.xapi_local()

        session.xenapi.login_with_password("", "")


	hosts = gethosts(session)
	hostscpus = getcpus(session, hosts)
	gethostcpus(session, hostscpus)


main()
