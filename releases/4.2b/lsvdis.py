#!/usr/bin/python
# lsvdis.py
# Display VDIs and their parameters
#
# Date: 12/20/2013 
# Ver. 0.0.1
# Author: Matthew Spah
# Date: 12/26/2013
# Ver. 0.0.2
# Author: Matthew Spah
# Date: 1/3/2013
# Ver. 0.0.3
# Added comments 
# Author: Matthew Spah


import XenAPI
import sys, getopt
from XAPIlib import *

def syntax():
	print "lsvdis version 0.1.1"
	print ""
	print "Syntax: lsvdis [options]"
	print " -h This help text"
	print " -u - shows VDI UUID, Size, SR UUID, SR type, VM UUID and VM device"
	print "	-n - shows VDI Name, Size, SR Name, SR type, VM Name and VM device"
	print "	-m - shows VDI UUID, Size, SR Name, SR type, VM Name and VM device"
	print " -c --csv output CSV"
	print " -o <value> - change sort order by column, value can be vdi, size, sr, vm or device"
	print "	-s <host> - remote poolmaster host"
	print "	-p <password> - remote poolmaster password"
	print " -s <host> - remote poolmaster host"
	print "- w - number of whitespaces between columns"
	
	
def getvdidata(session):
	
	# returns vdi list
	vdis = session.xenapi.VDI.get_all()
	vdiArray = []
	

	# loop through each vdi
	for vdi in vdis:
		
		# grab the VDI's VBD, VDI's sr, and grabbing the size of the VDI in bytes
		vdivbds = session.xenapi.VDI.get_VBDs(vdi)
		vdisr = session.xenapi.VDI.get_SR(vdi)
		vdisize = float(session.xenapi.VDI.get_virtual_size(vdi))
		
		# if vdi has more than one vbd, loop through vbd's and create an entry for each vbd
		if len(vdivbds) > 1:
			for vbd in vdivbds:
				vdivm = session.xenapi.VBD.get_VM(vbd)
				data = {
					'UUID':		session.xenapi.VDI.get_uuid(vdi),
					'Name':		session.xenapi.VDI.get_name_label(vdi),
					'Size':		sizeof_fmt(vdisize),
					'SR UUID':	session.xenapi.SR.get_uuid(vdisr),
					'SR Name':	session.xenapi.SR.get_name_label(vdisr),
					'SR Type':	session.xenapi.SR.get_type(vdisr),
					'VM UUID':	session.xenapi.VM.get_uuid(vdivm),
					'VM Name':	session.xenapi.VM.get_name_label(vdivm),
					'VM Dev':	session.xenapi.VBD.get_userdevice(vbd),
				}
				vdiArray.append(data)
		elif len(vdivbds) == 1:
			vdivm = session.xenapi.VBD.get_VM(vdivbds[0])
			data = {
				'UUID':		session.xenapi.VDI.get_uuid(vdi),
				'Name':		session.xenapi.VDI.get_name_label(vdi),
				'Size':		sizeof_fmt(vdisize),
				'SR UUID':	session.xenapi.SR.get_uuid(vdisr),
				'SR Name':	session.xenapi.SR.get_name_label(vdisr),
				'SR Type':	session.xenapi.SR.get_type(vdisr),
				'VM UUID':	session.xenapi.VM.get_uuid(vdivm),
				'VM Name':	session.xenapi.VM.get_name_label(vdivm),
				'VM Dev':	session.xenapi.VBD.get_userdevice(vdivbds[0])
			}
			vdiArray.append(data)
		else:
			data = {
				'UUID':		session.xenapi.VDI.get_uuid(vdi),
				'Name':		session.xenapi.VDI.get_name_label(vdi),
				'Size':		sizeof_fmt(vdisize),
				'SR UUID':	session.xenapi.SR.get_uuid(vdisr),
				'SR Name':	session.xenapi.SR.get_name_label(vdisr),
				'SR Type':	session.xenapi.SR.get_type(vdisr),
				'VM UUID':	"-",
				'VM Name':	"-",
				'VM Dev':	"-",
			}
			vdiArray.append(data)
			
	return vdiArray

def defineheadings(mode):

	if mode == "uuid":
		headings = ('UUID', 'Size', 'SR UUID', 'SR Type', 'VM UUID', 'VM Dev')
	elif mode == "name":
		headings = ('Name', 'Size', 'SR Name', 'SR Type', 'VM Name', 'VM Dev')
	elif mode == "mix":
		headings = ('UUID', 'Size', 'SR Name', 'SR Type', 'VM Name', 'VM Dev')
	
	return headings

def main():
	try:
		myopts, args = getopt.getopt(sys.argv[1:], "hcunmw:",["help", "csv", "uuid", "name", "mix", "wspace"])
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

	vdidata = getvdidata(session)
	
	headings = defineheadings(mode)
	
	print formatdarray(vdidata, headings, CSV, minspace)
	
	session.xenapi.session.logout()


main()
