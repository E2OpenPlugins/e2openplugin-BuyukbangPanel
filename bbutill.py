# logging for XMLTV importer
#
# One can simply use
# import log
# print>>log, "Some text"
# because the log unit looks enough like a file!

import sys
from cStringIO import StringIO
import threading
import time
logfile = StringIO()
# Need to make our operations thread-safe.
mutex = threading.Lock() 


def write(data):
	timestamp = time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(time.time()))
	dataLength = len(data)
	# Do not print timestamp with long exception data
	if dataLength > 1 and dataLength < 110:
		data = timestamp + " - " + data
	mutex.acquire()
	try:
		if logfile.tell() > 24000:
			# Do a sort of 8k round robin
			logfile.reset()
		logfile.write(data)
	finally:
		mutex.release()
	sys.stdout.write(data)


def getvalue():
	mutex.acquire()
	try:
		pos = logfile.tell()
		head = logfile.read()
		logfile.reset()
		tail = logfile.read(pos)
	finally:
		mutex.release()
	return head + tail 
