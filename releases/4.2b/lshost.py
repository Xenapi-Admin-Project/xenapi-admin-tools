#!/usr/bin/python
# lshosts.py
# Display all hosts and parameters in a xenserver pool
#
# Date: 12/10/2013 
# Ver. 0.0.1
# Author: Matthew Spah
# Date: 12/19/2013
# Ver. 0.1.0
# Desc: Added formatarray() and made modifications to gethostdata()
# Ver. 0.1.1
# Desc: Added Tot mem and Free mem
# Date: 12/21/2013
# Ver. 0.2.0
# Desc: Added CSV output

import XenAPI
import sys, getopt
from XAPIlib import *

def syntax():
	print "lshost version 0.0.1"
	print ""
	print "Syntax: lshosts [options]"
	print "-h --help This help text"
	print "-u --uuid Show UUIDs"
	print "-n --name Show Names (default)"
	print "-c --csv output CSV"
	print "-w --wspace number of whitespaces between columns"
	print "-p --password root password"
	
def gethostdata(session):		
	
	records = session.xenapi.host.get_all_records()
	metrics = session.xenapi.host_metrics.get_all_records()
	
	hArray = []
	for x in records:
		
		metobjuuid = records[x]['metrics']
		totmem = float(metrics[metobjuuid]['memory_total'])
		freemem = float(metrics[metobjuuid]['memory_free']) 
		
		data = {
			"UUID":			records[x]['uuid'],
			"Name-label":	records[x]['name_label'],
			"Active-VMs":	len(records[x]['resident_VMs']),
			"CPU-Model":	records[x]['cpu_info']['modelname'],
			"CPUs":			len(records[x]['host_CPUs']),
			'Tot Mem':		sizeof_fmt(totmem),
			'Free Mem':		sizeof_fmt(freemem),
			"Ver":			records[x]['software_version']['platform_version'],
			"Network":		records[x]['software_version']['network_backend'],
		}
		hArray.append(data)
		
	return hArray	

def defineheadings(mode):

	if mode == "name":
		headings = ('Name-label', 'Active-VMs', 'CPU-Model', 'CPUs', 'Tot Mem', 'Free Mem', 'Ver', 'Network')
	elif mode == "uuid":
		headings = ('UUID', 'Active-VMs', 'CPU-Model', 'CPUs', 'Tot Mem', 'Free Mem', 'Ver', 'Network')
	
	return headings

def main():
	try:
		myopts, args = getopt.getopt(sys.argv[1:], "huncw:",["help", "uuid", "name", "csv", "wspace"])
	except getopt.GetoptError:
		print "Unknown options"
		syntax()
		sys.exit(1) 
	minspace = 4
	CSV = False
	mode = "name"
	for opt, arg in myopts:
		if opt in ("-h", "--help"):
			syntax()
			sys.exit(1)
		elif opt in ("-u", "--uuid"):
			mode = "uuid"			
		elif opt in ("-n", "--name"):
			mode = "name"
		elif opt in ("-c", "--csv"):
			CSV = True 
		elif opt in ("-w", "--wspace"):
			minspace = int(arg)
			
	session = XenAPI.xapi_local()
	
	session.xenapi.login_with_password("", "")
	
	hosts = gethostdata(session)
	
	headings = defineheadings(mode)
	
	print formatdarray(hosts, headings, CSV, minspace)
	
	session.xenapi.session.logout()
	
main()
