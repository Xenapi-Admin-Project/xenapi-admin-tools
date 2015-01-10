#!/usr/bin/python
# lsvms.py
# Display VMs and their parameters
#
# Date: 1/2/2014 
# Ver. 0.0.1
# Author: Matthew Spah
# Date: 1/3/2014
# Ver. 0.0.2
# Displaying collumned values now

import XenAPI
import sys, getopt
from XAPIlib import *

def syntax():
	print ""
	print "	Syntax: $(basename $0) [options]"
	print "	Options:"
	print "	-d - shell debugging"
	print "	-c - output comma seperated values"
	print "	-u - shows VM UUID, Status, Host UUID"
	print "	-b - shows VM Name, Status, VMUUID, Host Name and Host UUID"
	print "	-n - shows VM Name, Status and Hostname"
	print "	-m - shows VM Name, Status, VM UUID and Hostname"
	print "	-o <value> - changes sort order by column, value can be vmname, hostname, vmuuid, hostuud"
	print "	-r - use local config files for remote poolmasters"
	print "	-s <host> - remote poolmaster host"
	print "	-p <password> - remote poolmaster password"
	print "	-h - this help text"
	print "	-w - number of whitespaces between columns"
	print ""


def getvmdata(session):
	vmArray = []
	vms = session.xenapi.VM.get_all()

	# Loop through each VM in vms, we'll skip it if the vm is a template, control domain, or a snapshot
	for vm in vms:
		if session.xenapi.VM.get_is_a_template(vm):
			continue
		elif session.xenapi.VM.get_is_control_domain(vm):
			continue
		elif session.xenapi.VM.get_is_a_snapshot(vm):
			continue
		else:
			vmhostref = session.xenapi.VM.get_resident_on(vm)

			# if no host is present use "-"
			if vmhostref == "OpaqueRef:NULL":
				Hostuuid = "-"
				Hostname = "-"
			else:
				Hostuuid = session.xenapi.host.get_uuid(vmhostref)
				Hostname = session.xenapi.host.get_name_label(vmhostref)

			data = {
				'UUID': session.xenapi.VM.get_uuid(vm),
				'Name': session.xenapi.VM.get_name_label(vm),
				'Host UUID': Hostuuid, 
				'Host Name': Hostname,
				'Dom ID': session.xenapi.VM.get_domid(vm), 
				'Status': session.xenapi.VM.get_power_state(vm)
			}

			vmArray.append(data)
			
	return vmArray

def defineheadings(mode):
	if mode == "uuid":
		headings = ("UUID", "Status", "Dom ID", "Host UUID")
	elif mode == "both":
		headings = ("Name", "Status", "UUID", "Dom ID", "Host Name", "Host UUID")
	elif mode == "name":
		headings = ("Name", "Status", "Dom ID", "Host Name")
	elif mode == "mix":
		headings = ("Name", "Status", "UUID", "Dom ID", "Host UUID")

	return headings

def main():
	try:
		myopts, args = getopt.getopt(sys.argv[1:], "hcubnmw:",["help", "csv", "uuid", "both", "name", "mix", "wspace"])
	except getopt.GetoptError:
		print "Unknown options"
		syntax()
		sys.exit(1)
	minspace = 3
	CSV = False
	mode = "uuid"
	for opt, arg in myopts:
		if opt in ("-h", "--help"):
			syntax()
			sys.exit(1)
		elif opt in ("-u", "--uuid"):
			mode = "uuid"
		elif opt in ("-b", "--both"):
			mode = "both"
		elif opt in ("-n", "--name"):
			mode = "name"
		elif opt in ("-m", "--mix"):
			mode = "mix"
		elif opt in ("-c", "--csv"):
			CSV = True
		elif opt in ("-w", "--wspace"):
			minspace = int(arg)

	session = XenAPI.xapi_local()

	session.xenapi.login_with_password("", "")

	vmdata = getvmdata(session)

	headings = defineheadings(mode)

	print formatdarray(vmdata, headings, CSV, minspace)

	session.xenapi.session.logout()


main()
