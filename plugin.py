################################################################################
#                                                                              #
#                            BUYUKBANG PANEL 1.4.2                             #
# I want to thank to all open source Enigma2 developers and community,         #
# especially Crossepg and EPG Import plugin developers, since I inspired or    #
# directly used their codes to make BuyukBang Panel Project come true!         #
#                                                                              #
#                                                      Buyukbang @27.11.2018   #
#                                                                              #
################################################################################

import time
import enigma
import os
from Screens.Console import Console
from twisted.internet import threads
import twisted.python.runtime
import bbutill
log = bbutill

# EPG Copier + EPG Linker
from enigma import eEPGCache, eServiceCenter, eServiceReference

# EPG Linker
from enigma import iPlayableService, iServiceInformation
from Screens.EventView import EventViewEPGSelect
from ServiceReference import ServiceReference
from Components.Sources.EventInfo import EventInfo
from Screens.InfoBarGenerics import InfoBarEPG

# Hide Zap Errors
from enigma import iPlayableService

#Main Menu
from Tools.LoadPixmap import LoadPixmap
from Components.Sources.List import List
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest

# Config
from Screens.Standby import TryQuitMainloop, Standby
from Tools import Notifications
from Components.config import config, ConfigText, ConfigEnableDisable, ConfigSubsection, ConfigYesNo, ConfigClock, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigIP, ConfigLocations, configfile

import Screens.Standby
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.SelectionList import SelectionList, SelectionEntryComponent
from Components.ScrollLabel import ScrollLabel
import Components.PluginComponent
from Tools.Directories import fileExists

################################################
import gettext
from Components.Language import language
from os import environ, popen
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS

def localeInit():
	lang = language.getLanguage()
	environ["LANGUAGE"] = lang[:2]
	gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
	gettext.textdomain("enigma2")
	gettext.bindtextdomain("BuyukbangPanel", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/BuyukbangPanel/locale/"))

def _(txt):
	t = gettext.dgettext("BuyukbangPanel", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

localeInit()
language.addCallback(localeInit)

################################################

#Set default configuration
config.plugins.buyukbangpanel = ConfigSubsection()
if hasattr(eEPGCache, 'importEvent'):
	config.plugins.buyukbangpanel.periodic = ConfigEnableDisable(default=True)
	config.plugins.buyukbangpanel.interval = ConfigNumber(default=60)
elif hasattr(eEPGCache, 'load'):
	config.plugins.buyukbangpanel.periodic = ConfigEnableDisable(default=True)
	config.plugins.buyukbangpanel.interval = ConfigNumber(default=600)
else:
	config.plugins.buyukbangpanel.periodic = ConfigEnableDisable(default=False)
	config.plugins.buyukbangpanel.interval = ConfigNumber(default=600)
config.plugins.buyukbangpanel.scheduled = ConfigEnableDisable(default=True)
config.plugins.buyukbangpanel.scheduledepgcopytime = ConfigClock(default=((21 * 60) + 00) * 60) # 21:00
config.plugins.buyukbangpanel.startupcopydelay = ConfigNumber(default=2)
config.plugins.buyukbangpanel.forceepgdat = ConfigYesNo(default=False)
config.plugins.buyukbangpanel.linkepg = ConfigSelection(choices=[("0", _("Only infoBar and EPG info")), ("1", _("All EPG queries")), ("2", _("Disable"))], default="0")
config.plugins.buyukbangpanel.readepgboquet = ConfigSelection(choices=[("0", _("At startup <Changes requires restart>")), ("1", _("In realtime <Uses more CPU>"))], default="0")
config.plugins.buyukbangpanel.filterdummy = ConfigEnableDisable(default=True)
config.plugins.buyukbangpanel.dummystring = ConfigText(default='Current,Next,dummyEventName,.,', fixed_size=False)
config.plugins.buyukbangpanel.epgencoding = ConfigSelection(choices=[("ISO6397", _("ISO6397")),("ISO8859-1", _("ISO8859-1")),("ISO8859-2", _("ISO8859-2")), ("ISO8859-3", _("ISO8859-3")), ("ISO8859-4", _("ISO8859-4")), ("ISO8859-5", _("ISO8859-5")), ("ISO8859-6", _("ISO8859-6")), ("ISO8859-7", _("ISO8859-7")), ("ISO8859-8", _("ISO8859-8")), ("ISO8859-9", _("ISO8859-9")), ("ISO8859-10", _("ISO8859-10")), ("ISO8859-11", _("ISO8859-11")), ("ISO8859-13", _("ISO8859-13")), ("ISO8859-14", _("ISO8859-14")), ("ISO8859-15", _("ISO8859-15")), ("ISO8859-16", _("ISO8859-16"))], default="ISO8859-9")
try: #some old images may not have this key and crashes. "Try" fixes this possible bug.
	if config.osd.language.value == "tr_TR":
		config.plugins.buyukbangpanel.fixepgencoding = ConfigSelection(choices=[("disable", _("Disable")), ("afg", _("Afghan")), ("alb", _("Albanian")), ("amh", _("Amharic")), ("ara", _("Arabic")), ("arm", _("Armenian")), ("ast", _("Asturian")), ("aze", _("Azerian")), ("bas", _("Basque")), ("bel", _("Belarusian")), ("ben", _("Bengali")), ("ber", _("Berbere")), ("bos", _("Bosnian")), ("bre", _("Breton")), ("bul", _("Bulgarian")), ("cat", _("Catalan")), ("chi", _("Chinese")), ("cro", _("Croatian")), ("cze", _("Czech")), ("den", _("Danish")), ("ned", _("Dutch")), ("eng", _("English")), ("est", _("Estonian")), ("far", _("Farsi")), ("fin", _("Finnish")), ("fra", _("French")), ("fri", _("Frisian")), ("gla", _("Gaelic")), ("gal", _("Galician")), ("geo", _("Georgian")), ("ger", _("German")), ("gre", _("Greek")), ("guj", _("Gujarati")), ("heb", _("Hebrew")), ("hin", _("Hindi")), ("hun", _("Hungarian")), ("ice", _("Icelandic")), ("ind", _("India")), ("iri", _("Irish")), ("ita", _("Italian")), ("jap", _("Japanese")), ("kaz", _("Kazakh")), ("khm", _("Khmer")), ("kor", _("Korean")), ("kur", _("Kurdish")), ("kyr", _("Kyrgyz")), ("lat", _("Latvian")), ("lit", _("Lithuanian")), ("lux", _("Luxembourg")), ("mac", _("Macedonian")), ("mal", _("Malayalam")), ("mlt", _("Maltese")), ("mdr", _("Mandarin")), ("mol", _("Moldovan")), ("mya", _("Myanmar")), ("nep", _("Nepali")), ("nor", _("Norwegian")), ("pus", _("Pashto")), ("per", _("Persian")), ("pol", _("Polish")), ("por", _("Portuguese")), ("pun", _("Punjabi")), ("rom", _("Romanian")), ("rus", _("Russian")), ("ser", _("Serbian")), ("snd", _("Sindhi")), ("sin", _("Sinhala")), ("slk", _("Slovakian")), ("slo", _("Slovenian")), ("som", _("Somali")), ("esp", _("Spanish")), ("swa", _("Swali")), ("swe", _("Sweden")), ("tag", _("Tagalog")), ("taj", _("Tajik")), ("tam", _("Tamil")), ("tel", _("Telugu")), ("tha", _("Thailand")), ("tig", _("Tigrinya")), ("tur", _("Turkish")), ("ukr", _("Ukrainian")), ("urd", _("Urdu")), ("vie", _("Vietnamese")), ("wel", _("Welsh"))], default="tur")
	else:
		config.plugins.buyukbangpanel.fixepgencoding = ConfigSelection(choices=[("disable", _("Disable")), ("afg", _("Afghan")), ("alb", _("Albanian")), ("amh", _("Amharic")), ("ara", _("Arabic")), ("arm", _("Armenian")), ("ast", _("Asturian")), ("aze", _("Azerian")), ("bas", _("Basque")), ("bel", _("Belarusian")), ("ben", _("Bengali")), ("ber", _("Berbere")), ("bos", _("Bosnian")), ("bre", _("Breton")), ("bul", _("Bulgarian")), ("cat", _("Catalan")), ("chi", _("Chinese")), ("cro", _("Croatian")), ("cze", _("Czech")), ("den", _("Danish")), ("ned", _("Dutch")), ("eng", _("English")), ("est", _("Estonian")), ("far", _("Farsi")), ("fin", _("Finnish")), ("fra", _("French")), ("fri", _("Frisian")), ("gla", _("Gaelic")), ("gal", _("Galician")), ("geo", _("Georgian")), ("ger", _("German")), ("gre", _("Greek")), ("guj", _("Gujarati")), ("heb", _("Hebrew")), ("hin", _("Hindi")), ("hun", _("Hungarian")), ("ice", _("Icelandic")), ("ind", _("India")), ("iri", _("Irish")), ("ita", _("Italian")), ("jap", _("Japanese")), ("kaz", _("Kazakh")), ("khm", _("Khmer")), ("kor", _("Korean")), ("kur", _("Kurdish")), ("kyr", _("Kyrgyz")), ("lat", _("Latvian")), ("lit", _("Lithuanian")), ("lux", _("Luxembourg")), ("mac", _("Macedonian")), ("mal", _("Malayalam")), ("mlt", _("Maltese")), ("mdr", _("Mandarin")), ("mol", _("Moldovan")), ("mya", _("Myanmar")), ("nep", _("Nepali")), ("nor", _("Norwegian")), ("pus", _("Pashto")), ("per", _("Persian")), ("pol", _("Polish")), ("por", _("Portuguese")), ("pun", _("Punjabi")), ("rom", _("Romanian")), ("rus", _("Russian")), ("ser", _("Serbian")), ("snd", _("Sindhi")), ("sin", _("Sinhala")), ("slk", _("Slovakian")), ("slo", _("Slovenian")), ("som", _("Somali")), ("esp", _("Spanish")), ("swa", _("Swali")), ("swe", _("Sweden")), ("tag", _("Tagalog")), ("taj", _("Tajik")), ("tam", _("Tamil")), ("tel", _("Telugu")), ("tha", _("Thailand")), ("tig", _("Tigrinya")), ("tur", _("Turkish")), ("ukr", _("Ukrainian")), ("urd", _("Urdu")), ("vie", _("Vietnamese")), ("wel", _("Welsh"))], default="disable")
except:
	config.plugins.buyukbangpanel.fixepgencoding = ConfigSelection(choices=[("disable", _("Disable")), ("afg", _("Afghan")), ("alb", _("Albanian")), ("amh", _("Amharic")), ("ara", _("Arabic")), ("arm", _("Armenian")), ("ast", _("Asturian")), ("aze", _("Azerian")), ("bas", _("Basque")), ("bel", _("Belarusian")), ("ben", _("Bengali")), ("ber", _("Berbere")), ("bos", _("Bosnian")), ("bre", _("Breton")), ("bul", _("Bulgarian")), ("cat", _("Catalan")), ("chi", _("Chinese")), ("cro", _("Croatian")), ("cze", _("Czech")), ("den", _("Danish")), ("ned", _("Dutch")), ("eng", _("English")), ("est", _("Estonian")), ("far", _("Farsi")), ("fin", _("Finnish")), ("fra", _("French")), ("fri", _("Frisian")), ("gla", _("Gaelic")), ("gal", _("Galician")), ("geo", _("Georgian")), ("ger", _("German")), ("gre", _("Greek")), ("guj", _("Gujarati")), ("heb", _("Hebrew")), ("hin", _("Hindi")), ("hun", _("Hungarian")), ("ice", _("Icelandic")), ("ind", _("India")), ("iri", _("Irish")), ("ita", _("Italian")), ("jap", _("Japanese")), ("kaz", _("Kazakh")), ("khm", _("Khmer")), ("kor", _("Korean")), ("kur", _("Kurdish")), ("kyr", _("Kyrgyz")), ("lat", _("Latvian")), ("lit", _("Lithuanian")), ("lux", _("Luxembourg")), ("mac", _("Macedonian")), ("mal", _("Malayalam")), ("mlt", _("Maltese")), ("mdr", _("Mandarin")), ("mol", _("Moldovan")), ("mya", _("Myanmar")), ("nep", _("Nepali")), ("nor", _("Norwegian")), ("pus", _("Pashto")), ("per", _("Persian")), ("pol", _("Polish")), ("por", _("Portuguese")), ("pun", _("Punjabi")), ("rom", _("Romanian")), ("rus", _("Russian")), ("ser", _("Serbian")), ("snd", _("Sindhi")), ("sin", _("Sinhala")), ("slk", _("Slovakian")), ("slo", _("Slovenian")), ("som", _("Somali")), ("esp", _("Spanish")), ("swa", _("Swali")), ("swe", _("Sweden")), ("tag", _("Tagalog")), ("taj", _("Tajik")), ("tam", _("Tamil")), ("tel", _("Telugu")), ("tha", _("Thailand")), ("tig", _("Tigrinya")), ("tur", _("Turkish")), ("ukr", _("Ukrainian")), ("urd", _("Urdu")), ("vie", _("Vietnamese")), ("wel", _("Welsh"))], default="disable")
config.plugins.buyukbangpanel.hidezaperrors = ConfigEnableDisable(default=False)
config.plugins.buyukbangpanel.scheduledoperation = ConfigSelection(choices=[("0", _("Disable")), ("1", _("Shutdown")), ("2", _("Reboot")), ("3", _("Restart GUI")), ("4", _("Standby"))], default="0")
config.plugins.buyukbangpanel.scheduledoperationtime = ConfigClock(default=((5 * 60) + 00) * 60) # 5:00
config.plugins.buyukbangpanel.scheduledoperationmon = ConfigEnableDisable(default=True)
config.plugins.buyukbangpanel.scheduledoperationtue = ConfigEnableDisable(default=True)
config.plugins.buyukbangpanel.scheduledoperationwed = ConfigEnableDisable(default=True)
config.plugins.buyukbangpanel.scheduledoperationthu = ConfigEnableDisable(default=True)
config.plugins.buyukbangpanel.scheduledoperationfri = ConfigEnableDisable(default=True)
config.plugins.buyukbangpanel.scheduledoperationsat = ConfigEnableDisable(default=True)
config.plugins.buyukbangpanel.scheduledoperationsun = ConfigEnableDisable(default=True)
config.plugins.buyukbangpanel.restarttype = ConfigSelection(choices=[("3", _("Restart GUI")), ("2", _("Reboot"))], default="3")
config.plugins.buyukbangpanel.showinextensions = ConfigYesNo(default=True)
config.plugins.buyukbangpanel.lastcopyepgrestarttime = ConfigNumber(default=0)
config.plugins.buyukbangpanel.startuptostandby = ConfigSelection(choices=[("0", _("Disable")), ("1", _("Except GUI restarts")), ("2", _("On all startups"))], default="0")

# Plugin definition
from Plugins.Plugin import PluginDescriptor

# Global variable
_session = None 
autoStartTimer = None
autostartExecuted = None
timerEpgCopyRunning = False
manualEpgCopyRunning = False
scheduledOperation = None
reboot = False
lastrestartallowedtime = int(config.plugins.buyukbangpanel.lastcopyepgrestarttime.value)

###################################### GETEPGMAP ###################################
def getEPGMap(self):
	dst2src = {}
	src2dst = {}
	serviceHandler = eServiceCenter.getInstance()
	services = serviceHandler.list(eServiceReference('1:7:1:0:0:0:0:0:0:0:(type == 1) || (type == 17) || (type == 195) || (type == 25) FROM BOUQUET "bouquets.tv" ORDER BY bouquet'))
	bouquets = services and services.getContent("SN", True)
	#The first argument of getContent function is a format string to specify the order and
	#the content of the returned list
	#useable format options are
	#R = Service Reference (as swig object .. this is very slow)
	#S = Service Reference (as python string object .. same as ref.toString())
	#C = Service Reference (as python string object .. same as ref.toCompareString())
	#N = Service Name (as python string object)
	#n = Short Service Name (short name brakets used) (as python string object)
	#when exactly one return value per service is selected in the format string,
	#then each value is directly a list entry
	#when more than one value is returned per service, then the list is a list of
	#python tuples
	#unknown format string chars are returned as python None values !
	for bouquet in bouquets:
		if bouquet[1].replace('\xc2\x86', '').replace('\xc2\x87', '').lower() == "epg":
			services = serviceHandler.list(eServiceReference(bouquet[0]))
			channels = services and services.getContent("RSN", True)
			srcref = {}
			srcflag = '1'
			for channel in channels:
				if srcflag == '1':
					srcref = channel
					srcflag = '0'
				elif channel[1].startswith("1:64:"):
					srcflag = '1'
				else:
					#dst2src(ref string of destination channel)= destination channel ref swig object of, ref sting, name, source channel ref swig object of, ref sting, name)
					dst2src[channel[1]] = (channel[0], channel[1], channel[2], srcref[0], srcref[1], srcref[2])
					src2dst[srcref[1]] = (channel[0], channel[1], channel[2], srcref[0], srcref[1], srcref[2])
					#f = open('/media/hdd/deneme.txt', 'a')
					#f.write(channel[2].replace('\xc2\x86', '').replace('\xc2\x87', '') + "==>" + dst2src[channel[1]][5] + "\n")
					#f.write(channel[1] + "==>" + dst2src[channel[1]][4] + "\n")
					#f.close()
	return (dst2src, src2dst)

eEPGCache.getEPGMap = getEPGMap
EventInfo.getEPGMap = getEPGMap

###################################### COPYEPG ###################################
def copyEpg(self):
	global timerEpgCopyRunning, manualEpgCopyRunning, scheduledOperation, reboot
	epgpath = None
	epgfile = None
	epgfilenew = None
	epgdat = None
	channels = None
	if timerEpgCopyRunning or manualEpgCopyRunning:
		print>>log, "\n"
		print>>log, _("Another EPG copy operation is in progress. EPG copy will not start.")
		if hasattr(self, 'save_pre'):
			self.session.open(MessageBox, _("Buyukbang Panel\n\nAnother EPG copy operation is in progress. Please wait..."), MessageBox.TYPE_ERROR, timeout=10, close_on_any_key=True)
		return
	if hasattr(self, 'save_pre'):
		print>>log, _("Manual EPG copy started")
		self["statusbar"].setText(_("Manual EPG copy started"))
		manualEpgCopyRunning = True
		timerEpgCopyRunning = False
	elif scheduledOperation == "SCHEDULED":
		print>>log, _("Scheduled EPG copy started")
		manualEpgCopyRunning = False
		timerEpgCopyRunning = True
	elif scheduledOperation == "PERIODIC":
		print>>log, _("Periodic EPG copy started")
		manualEpgCopyRunning = False
		timerEpgCopyRunning = True
	epgcache = eEPGCache.getInstance()
	if not hasattr(eEPGCache, 'importEvent') or config.plugins.buyukbangpanel.forceepgdat.value:
		epgpath = "/hdd"
		epgfile = "/hdd/epg.dat"
		cfFound = False
		usbFound = False
		hddFound = False
		fmount = None
		# Reported: Some images don't support popen, may be they have a bad/missing implementation.
		try:
			fmount = os.popen('mount', "r")
		except:
			try:
				os.system('mount > /tmp/mount.log')
				fmount = open('/tmp/mount.log', 'r')
			except:
				pass
		if fmount:
			for l in fmount.xreadlines():
				if l.find('/media/cf') != -1:
					cfFound = True
				if l.find('/media/usb') != -1:
					usbFound = True
				if l.find('/media/hdd') != -1:
					hddFound = True
			fmount.close()
		if cfFound:
			epgpath = '/media/cf'
			epgfile = '/media/cf/epg.dat'
		if usbFound:
			epgpath = '/media/usb'
			epgfile = '/media/usb/epg.dat'
		if hddFound:
			epgpath = '/media/hdd'
			epgfile = '/media/hdd/epg.dat'
		try: #some old images do not have this key and crashes. "Try" fixes this bug.
			if config.misc.epgcache_filename.value:
				parent = os.path.split(config.misc.epgcache_filename.value)[0]
				if os.path.exists(parent):
					epgpath = parent
		except:
			pass
		epgfilenew = os.path.join(epgpath, 'epg.dat.bb')
		epgdat = epgdat_class(epgpath, '/etc/enigma2', epgfilenew)
	serviceHandler = eServiceCenter.getInstance()
	services = serviceHandler.list(eServiceReference('1:7:1:0:0:0:0:0:0:0:(type == 1) || (type == 17) || (type == 195) || (type == 25) FROM BOUQUET "bouquets.tv" ORDER BY bouquet'))
	bouquets = services and services.getContent("SN", True)
	#The first argument of getContent function is a format string to specify the order and
	#the content of the returned list
	#useable format options are
	#R = Service Reference (as swig object .. this is very slow)
	#S = Service Reference (as python string object .. same as ref.toString())
	#C = Service Reference (as python string object .. same as ref.toCompareString())
	#N = Service Name (as python string object)
	#n = Short Service Name (short name brakets used) (as python string object)
	#when exactly one return value per service is selected in the format string,
	#then each value is directly a list entry
	#when more than one value is returned per service, then the list is a list of
	#python tuples
	#unknown format string chars are returned as python None values !
	for bouquet in bouquets:
		if bouquet[1].replace('\xc2\x86', '').replace('\xc2\x87', '').lower() == "epg":
			services = serviceHandler.list(eServiceReference(bouquet[0]))
			channels = services and services.getContent("RSN", True)
			# Add one more dummy seperator at the end. So there will be no need to duplicate looped importEvents code part for just the last item.
			channels.append([None,"1:64:",None])
	srcChannel = None
	dstChannelList = []
	eventlist = {}
	timeAdjustment = 0
	if not channels:
		manualEpgCopyRunning = False
		timerEpgCopyRunning = False
		print>>log, _("Bouquet named EPG not found, EPG copy aborted")
		if hasattr(self, 'save_pre'):
			self["statusbar"].setText(_("Bouquet named EPG not found, EPG copy aborted"))
		return
	for channel in channels:
		if channel[1].startswith("1:64:"):
			timeAdjustment = 0
			timeAdjustmentStr = ''
			if channel[2]:
				timeAdjustmentStr = channel[2][channel[2].find('(') + 1: channel[2].find(')')]
				if len(timeAdjustmentStr) > 0:
					timeAdjustment = int(timeAdjustmentStr) * 3600
			if eventlist and dstChannelList:
				try:
					if hasattr(eEPGCache, 'importEvents') and not config.plugins.buyukbangpanel.forceepgdat.value:
						epgcache.importEvents(dstChannelList, eventlist)
					else:
						epgdat.importEvents(dstChannelList, eventlist)
					print>>log, _("%s copied") % srcChannel
					if hasattr(self, 'save_pre'):
						self["statusbar"].setText(_("%s copied") % srcChannel)
				except Exception, e:
					print>>log, _("Copy failed for %s") % srcChannel
					print>>log, e
					if hasattr(self, 'save_pre'):
						self["statusbar"].setText(_("Copy failed for %s") % srcChannel)
			elif not eventlist and srcChannel and dstChannelList:
				print>>log, _("No EPG data available for %s") % srcChannel
				if hasattr(self, 'save_pre'):
					self["statusbar"].setText(_("No EPG data available for %s") % srcChannel)
			srcChannel = None
			dstChannelList = []
			eventlist = {}
		elif srcChannel is None:
			srcChannel = channel[2].replace('\xc2\x86', '').replace('\xc2\x87', '')
			#B = Event Begin Time, D = Event Duration, T = Event Title, S = Event Short Description, E = Event Extended Description, 0 = PyLong(0)
			eventlist = epgcache.lookupEvent(['BDTSE0', (channel[1], -1, -1, -1)])
			for i in range(len(eventlist)):
				eventlist[i] = (eventlist[i][0] + timeAdjustment,eventlist[i][1],eventlist[i][2],eventlist[i][3],eventlist[i][4],eventlist[i][5])
		else:
			dstChannelList.append(channel[1])
	if epgdat is not None:
		try:
			print>>log, _("Writing %s") % epgfilenew
			if hasattr(self, 'save_pre'):
				self["statusbar"].setText(_("Writing %s") % epgfilenew)
			epgdat.final_process()
		except Exception, e:
			print>>log, _("%s write failed") % epgfilenew
			print>>log, e
			if hasattr(self, 'save_pre'):
				self["statusbar"].setText(_("%s write failed") % epgfilenew)
		reboot = True
		if hasattr(eEPGCache, 'load'):
			print>>log, _("Loading %s") % epgfilenew
			if hasattr(self, 'save_pre'):
				self["statusbar"].setText(_("Loading %s") % epgfilenew)
			try:
				try:
					os.unlink(epgfile)
				except:
					pass
				os.symlink(epgfilenew, epgfile)
				epgcache.load()
				try:
					os.unlink(epgfile)
				except:
					pass
				try:
					os.unlink(epgfilenew)
				except:
					pass
				reboot = False
				print>>log, _("%s loaded") % epgfilenew
				if hasattr(self, 'save_pre'):
					 self["statusbar"].setText(_("%s loaded") % epgfilenew)
			except Exception, e:
				print>>log, _("%s load failed") % epgfilenew
				print>>log, e
				if hasattr(self, 'save_pre'):
					self["statusbar"].setText(_("%s load failed") % epgfilenew)
	manualEpgCopyRunning = False
	timerEpgCopyRunning = False
	if hasattr(self, 'save_pre'):
		print>>log, _("Manual EPG copy completed")
		self["statusbar"].setText(_("Manual EPG copy completed"))
	elif scheduledOperation == "SCHEDULED":
		print>>log, _("Scheduled EPG copy completed")
		self.scheduledepgcopytime += 86400 # Tomorrow.
		self.oldscheduledepgcopytime = self.scheduledepgcopytime
		print>>log, _("Scheduled EPG copy time is set to %s") % time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(self.scheduledepgcopytime))
	elif scheduledOperation == "PERIODIC":
		print>>log, _("Periodic EPG copy completed")
		interval = int(config.plugins.buyukbangpanel.interval.value) * 60
		nowt = time.time()
		self.periodictime = nowt + interval
		self.oldperiodictime = self.periodictime
		print>>log, _("Periodic EPG copy time is set to %s") % time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(self.periodictime))


##################### LOOKUPEVENTTIME #####################
baseeEPGCache_lookupEventTime = eEPGCache.lookupEventTime

def eEPGCache_lookupEventTime(self, ref, start_time, direction=None):
	if not hasattr(eEPGCache, 'dst2src') or config.plugins.buyukbangpanel.readepgboquet.value == "1":
		self.dst2src = self.getEPGMap()[0]
	if self.dst2src.has_key(ref.toString()):
		ref = self.dst2src[ref.toString()][3]
		#f = open('/media/hdd/deneme.txt', 'a')
		#f.write( "MAPPING IS " + ref.toString() + "==>" + self.dst2src[ref.toString()][4] + "\n")
		#f.close()
	if direction is None:
		return baseeEPGCache_lookupEventTime(self, ref, start_time, 0)
	else:
		return baseeEPGCache_lookupEventTime(self, ref, start_time, direction)

if config.plugins.buyukbangpanel.linkepg.value != "2":
	eEPGCache.lookupEventTime = eEPGCache_lookupEventTime


####################### LOOKUPEVENTID ######################
#baseeEPGCache_lookupeventid = eEPGCache.lookupeventid

def eEPGCache_lookupeventid(self, ref, eventid):
	if not hasattr(eEPGCache, 'dst2src') or config.plugins.buyukbangpanel.readepgboquet.value == "1":
		self.dst2src = self.getEPGMap()[0]
	if self.dst2src.has_key(ref.toString()):
		ref = self.dst2src[ref.toString()][3]
	return baseeEPGCache_lookupeventid(self, ref, eventid)

if config.plugins.buyukbangpanel.linkepg.value != "2":
	eEPGCache.lookupeventid = eEPGCache_lookupeventid


######################## LOOKUPEVENT #######################
baseeEPGCache_lookupEvent = eEPGCache.lookupEvent

# here we get a python list
# the first entry in the list is a python string to specify the format of the returned tuples (in a list)
#   0 = PyLong(0)
#   I = Event Id
#   B = Event Begin Time
#   D = Event Duration
#   T = Event Title
#   S = Event Short Description
#   E = Event Extended Description
#   C = Current Time
#   R = Service Reference
#   N = Service Name
#   n = Short Service Name
#   X = Return a minimum of one tuple per service in the result list... even when no event was found.
#       The returned tuple is filled with all available infos... non avail is filled as None
#       The position and existence of 'X' in the format string has no influence on the result tuple... its completely ignored..
# then for each service follows a tuple
#   first tuple entry is the servicereference (as string... use the ref.toString() function)
#   the second is the type of query
#     2 = event_id
#    -1 = event before given start_time
#     0 = event intersects given start_time
#    +1 = event after given start_time
#   the third
#      when type is eventid it is the event_id
#      when type is time then it is the start_time ( -1 for now_time )
#   the fourth is the end_time .. ( optional .. for query all events in time range)
def eEPGCache_lookupEvent(self, listoftuple, buildFunc=None):
	resultList = {}
	if not hasattr(eEPGCache, 'dst2src') or not hasattr(eEPGCache, 'src2dst') or config.plugins.buyukbangpanel.readepgboquet.value == "1":
		EPGMap = self.getEPGMap()
		self.dst2src = EPGMap[0]
		self.src2dst = EPGMap[1]
	#sample graphmultiepg list of tuples:		test = [ (service.ref.toString(), 0, self.time_base, self.time_epoch) for service in services ]
	#																				test.insert(0, 'XRnITBD')
	#sample multiepg list of tuples:				test = [ (service.ref.toString(), 0, stime) for service in services ]
	#																				test.insert(0, 'X0RIBDTCn')
	#sample singleepg list of tuples: 			test = [ 'RIBDT', (service.ref.toString(), 0, -1, -1) ]
	for i in range(len(listoftuple)):
		if self.dst2src.has_key(listoftuple[i][0]):
			if len(listoftuple[i]) == 4:
				listoftuple[i] = (self.dst2src[listoftuple[i][0]][4], listoftuple[i][1], listoftuple[i][2], listoftuple[i][3])
			else:
				listoftuple[i] = (self.dst2src[listoftuple[i][0]][4], listoftuple[i][1], listoftuple[i][2])
	if buildFunc is not None:
		resultList = baseeEPGCache_lookupEvent(self, listoftuple, buildFunc)
	else:
		resultList = baseeEPGCache_lookupEvent(self, listoftuple)
	#We now have a result with the linked service references. We need to replace this references with the original ones.
	#ref_position = listoftuple[0].replace('X', '').find('R')
	#f = open('/media/hdd/deneme.txt', 'a')
	#f.write("ref_position=%d\n" % (ref_position))
	#f.close
	#if ref_position != -1:
	#	for i in range(len(resultList)):
	#		if self.src2dst.has_key(resultList[i][ref_position]):
	#			tmpresultList=list(resultList[i])
	#			tmpresultList[ref_position] = self.src2dst[resultList[i][ref_position]][1]
	#			resultList[i] = tuple(tmpresultList)
	return resultList

if config.plugins.buyukbangpanel.linkepg.value == "1":
	eEPGCache.lookupEvent = eEPGCache_lookupEvent


########################### INFOBAR FIX STARTS  ###########################
EventInfo.lastdst = None

def EventInfo_gotEvent(self, what):
	refstr = None
	found = 0
	ret = None
	if what == iPlayableService.evEnd:
		self.changed((self.CHANGED_CLEAR,))
		return
	else:
		service = self.navcore.getCurrentService()
		info = service and service.info()
		refstr = info and info.getInfoString(iServiceInformation.sServiceref)
		ret = info and info.getEvent(self.now_or_next)
		if not ret and info:
			ret = refstr and self.epgQuery(eServiceReference(refstr), -1, self.now_or_next and 1 or 0)
		if ret and config.plugins.buyukbangpanel.filterdummy.value and config.plugins.buyukbangpanel.dummystring.value:
			eventName = ret.getEventName()
			if not eventName:
				return
			dummylist = config.plugins.buyukbangpanel.dummystring.value.split(',')
			for dummytxt in dummylist:
				if eventName.lower() == dummytxt.lower():
					return
		if ret:
			if refstr and config.plugins.buyukbangpanel.linkepg.value != "2":
				if not hasattr(eEPGCache, 'dst2src') or config.plugins.buyukbangpanel.readepgboquet.value == "1":
					self.dst2src = self.getEPGMap()[0]
				if self.dst2src.has_key(refstr):
					if self.lastdst != refstr:
						self.lastdst = refstr
						self.changed((self.CHANGED_ALL,))
					return
			self.lastdst = None
			self.changed((self.CHANGED_ALL,))

if config.plugins.buyukbangpanel.filterdummy.value:
	EventInfo.gotEvent = EventInfo_gotEvent


######################### EPG INFO FIX STARTS ##########################
def InfoBarEPG_openEventView(self):
	found = 0
	ref = self.session.nav.getCurrentlyPlayingServiceReference()
	self.epglist = []
	epglist = self.epglist
	self.is_now_next = False
	epg = eEPGCache.getInstance()
	ptr = ref and ref.valid() and epg.lookupEventTime(ref, -1)
	if ptr is not None:
		if config.plugins.buyukbangpanel.dummystring.value:
			eventName = ptr.getEventName()
			dummylist = config.plugins.buyukbangpanel.dummystring.value.split(',')
			for dummytxt in dummylist:
				if eventName.lower() == dummytxt.lower():
					found = 1
		if found == 0:
			epglist.append(ptr)
	if epglist:
		self.eventView = self.session.openWithCallback(self.closed, EventViewEPGSelect, self.epglist[0], ServiceReference(ref), self.eventViewCallback, self.openSingleServiceEPG, self.openMultiServiceEPG, self.openSimilarList)
		self.dlg_stack.append(self.eventView)
	else:
		print "No epg for the service available. So we show multiepg instead of eventinfo"
		self.openMultiServiceEPG(False)

if config.plugins.buyukbangpanel.filterdummy.value:
	InfoBarEPG.openEventView = InfoBarEPG_openEventView

########################## SERVICE LIST FIX STARTS ##########################
#Prevents updates when list is open. But does not help reopening of service list
#from Components.Sources.ServiceEvent import ServiceEvent
#
#def ServiceEvent_newService(self, ref):
#	pass
#
#ServiceEvent.newService = ServiceEvent_newService

######################### ZAP ERRORS FIX STARTS ##########################
if config.plugins.buyukbangpanel.hidezaperrors.value:
	iPlayableService.evTuneFailed = 121212


##################### IMPORTEVENTS WRAPPER #####################
def importEvents(self, services, events):
	for service in services:
		self.epgcache.importEvent(service, events)

if hasattr(eEPGCache, 'importEvent') and not hasattr(eEPGCache, 'importEvents'):
	eEPGCache.importEvents = importEvents

###################################### MAIN SCREEN ###################################
class mainMenu(Screen):
	skin = """
	<screen position="center,center" size="640,400" title="Buyukbang Panel v1.4.2             buyukbang.blogspot.com">
		<widget source="list" render="Listbox" position="0,0" size="640,400" scrollbarMode="showOnDemand">
			<convert type="TemplatedMultiContent">
				{"template": [
					MultiContentEntryPixmapAlphaTest(pos = (12, 4), size = (32, 32), png = 0),
					MultiContentEntryText(pos = (58, 5), size = (440, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),
					],
					"fonts": [gFont("Regular", 22)],
					"itemHeight": 40
				}
			</convert>
		</widget>	
	</screen>"""
	
	def __init__(self, session, args=0):
		
		self.session = session
		self.setup_title = _("Buyukbang Panel v1.4.2             buyukbang.blogspot.com")
		Screen.__init__(self, session)

		l = []
		l.append(self.buildListEntry(_("Copy EPG"), "copyepg.png"))
		l.append(self.buildListEntry(_("Link EPG"), "linkepg.png"))
		l.append(self.buildListEntry(_("Filter EPG"), "filter.png"))
		l.append(self.buildListEntry(_("Fix EPG encoding"), "encoding.png"))
		l.append(self.buildListEntry(_("EPG file operations"), "fileoperations.png"))
		l.append(self.buildListEntry(_("Hide zap errors"), "zaperror.png"))
		l.append(self.buildListEntry(_("Startup to standby"), "startuptostandby.png"))
		l.append(self.buildListEntry(_("Scheduler"), "scheduler.png"))
		l.append(self.buildListEntry(_("Show Log"), "log.png"))
		l.append(self.buildListEntry(_("Configuration"), "configure.png"))

		self["list"] = List(l)
		self["setupActions"] = ActionMap(["SetupActions"],
		{
			"cancel": self.quit,
			"ok": self.openSelected,
		}, -2)

	def buildListEntry(self, description, image):
		pixmap = LoadPixmap(cached=True, path="/usr/lib/enigma2/python/Plugins/Extensions/BuyukbangPanel/images/%s" % image)
		return((pixmap, description))

	def openSelected(self):
		global menuIndex
		menuIndex = self["list"].getIndex()
		if menuIndex == 0:
			self.session.open(EPGMainSetup)
		elif menuIndex == 1:
			self.session.open(EPGMainSetup)
		elif menuIndex == 2:
			self.session.open(EPGMainSetup)
		elif menuIndex == 3:
			self.session.open(EPGMainSetup)
		elif menuIndex == 4:
			self.session.open(EPGFileOperationsScreen)
		elif menuIndex == 5:
			self.session.open(EPGMainSetup)
		elif menuIndex == 6:
			self.session.open(EPGMainSetup)
		elif menuIndex == 7:
			self.session.open(EPGMainSetup)
		elif menuIndex == 8:
			self.session.open(LogScreen)
		elif menuIndex == 9:
			self.session.open(EPGMainSetup)
	def quit(self):
		self.close()


class EPGMainSetup(ConfigListScreen,Screen):
	skin = """
	<screen position="center,center" size="640,400" title="Buyukbang Panel v1.4.2             buyukbang.blogspot.com" >
		<ePixmap name="red"    position="0,0"   zPosition="2" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
		<ePixmap name="green"  position="160,0" zPosition="2" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
		<ePixmap name="yellow" position="320,0" zPosition="2" size="140,40" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on" /> 
		<ePixmap name="blue"   position="480,0" zPosition="2" size="140,40" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on" /> 
	
		<widget name="key_red" position="0,0" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="background" shadowOffset="-2,-2" /> 
		<widget name="key_green" position="160,0" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="background" shadowOffset="-2,-2" /> 
		<widget name="key_yellow" position="320,0" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="background" shadowOffset="-2,-2" />
		<widget name="key_blue" position="480,0" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="background" shadowOffset="-2,-2" />
	
		<widget name="config" position="10,60" size="620,300" scrollbarMode="showOnDemand" />
	
		<ePixmap alphatest="on" pixmap="skin_default/icons/clock.png" position="560,378" size="14,14" zPosition="3"/>
		<widget font="Regular;18" halign="left" position="585,375" render="Label" size="55,20" source="global.CurrentTime" transparent="1" valign="center" zPosition="3">
			<convert type="ClockToText">Default</convert>
		</widget>
		<widget name="statusbar" position="10,375" size="530,20" font="Regular;18" />
		<widget name="status" position="10,300" size="540,60" font="Regular;20" />
	</screen>"""
	
	def __init__(self, session, args=0):
		global menuIndex
		self.session = session
		self.copyEpg = copyEpg
		self.setup_title = _("Configuration")
		Screen.__init__(self, session)
		cfg = config.plugins.buyukbangpanel
		self.list = []
		if menuIndex == 0:
			self.list.append(getConfigListEntry(_("Copy EPG periodically") + ":", cfg.periodic))
			self.list.append(getConfigListEntry(_("Interval (>=2 min)") + ":", cfg.interval))
			self.list.append(getConfigListEntry(_("Copy EPG at a scheduled time") + ":", cfg.scheduled))
			self.list.append(getConfigListEntry(_("Scheduled EPG copy time") + ":", cfg.scheduledepgcopytime))
			self.list.append(getConfigListEntry(_("Startup copy delay (>=2 min)") + ":", cfg.startupcopydelay))
			self.list.append(getConfigListEntry(_("Force CrossEPG patch usage") + ":", cfg.forceepgdat))
			self.list.append(getConfigListEntry(_("Read EPG bouquet") + ":", cfg.readepgboquet))
		elif menuIndex == 1:
			self.list.append(getConfigListEntry(_("Link EPG") + ":", cfg.linkepg))
			self.list.append(getConfigListEntry(_("Read EPG bouquet") + ":", cfg.readepgboquet))
		elif menuIndex == 2:
			self.list.append(getConfigListEntry(_("Filter EPG") + ":", cfg.filterdummy))
			self.list.append(getConfigListEntry(_("EPG titles") + ":", cfg.dummystring))
		elif menuIndex == 3:
			self.list.append(getConfigListEntry(_("Language") + ":", cfg.fixepgencoding))
			self.list.append(getConfigListEntry(_("Encoding") + ":", cfg.epgencoding))
		elif menuIndex == 5:
			self.list.append(getConfigListEntry(_("Hide zap errors") + ":", cfg.hidezaperrors))
		elif menuIndex == 6:
			self.list.append(getConfigListEntry(_("Startup to standby") + ":", cfg.startuptostandby))
		elif menuIndex == 7:
			self.list.append(getConfigListEntry(_("Scheduled operation") + ":", cfg.scheduledoperation))
			self.list.append(getConfigListEntry(_("Time") + ":", cfg.scheduledoperationtime))
			self.list.append(getConfigListEntry(_("Monday") + ":", cfg.scheduledoperationmon))
			self.list.append(getConfigListEntry(_("Tuesday") + ":", cfg.scheduledoperationtue))
			self.list.append(getConfigListEntry(_("Wednesday") + ":", cfg.scheduledoperationwed))
			self.list.append(getConfigListEntry(_("Thursday") + ":", cfg.scheduledoperationthu))
			self.list.append(getConfigListEntry(_("Friday") + ":", cfg.scheduledoperationfri))
			self.list.append(getConfigListEntry(_("Saturday") + ":", cfg.scheduledoperationsat))
			self.list.append(getConfigListEntry(_("Sunday") + ":", cfg.scheduledoperationsun))
		elif menuIndex == 9:
			self.list.append(getConfigListEntry(_("When restart needed") + ":", cfg.restarttype))
			self.list.append(getConfigListEntry(_("Show in extensions") + ":", cfg.showinextensions))

		ConfigListScreen.__init__(self, self.list, session=self.session, on_change=self.changedEntry)
		self["config"].onSelectionChanged.append(self.selectionChanged)
		self["status"] = Label()
		self["statusbar"] = Label()
		self["key_red"] = Button(_("Cancel"))
		self["key_green"] = Button(_("Ok"))
		self["key_yellow"] = Button(_("Show Log"))
		if menuIndex == 0:
			self["key_blue"] = Button(_("Manual Copy"))
		else:
			self["key_blue"] = Button(_(" "))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "TimerEditActions"],
		{
			"red": self.cancel,
			"green": self.save_pre,
			"yellow": self.yellowAction,
			"blue": self.blueAction,
			"save": self.save_pre,
			"cancel": self.cancel,
			"ok": self.save_pre,
			"log": self.yellowAction,
		}, -2)
		self.onChangedEntry = []
		
		self.oldscheduled = config.plugins.buyukbangpanel.scheduled.value
		self.oldperiodic = config.plugins.buyukbangpanel.periodic.value
		self.oldstartupcopydelay = config.plugins.buyukbangpanel.startupcopydelay.value
		self.oldscheduledepgcopytime = config.plugins.buyukbangpanel.scheduledepgcopytime.value
		self.oldinterval = config.plugins.buyukbangpanel.interval
		self.oldlinkepg = config.plugins.buyukbangpanel.linkepg.value
		self.oldreadepgboquet = config.plugins.buyukbangpanel.readepgboquet.value
		self.oldfixepgencoding = config.plugins.buyukbangpanel.fixepgencoding.value
		self.oldepgencoding = config.plugins.buyukbangpanel.epgencoding.value
		self.oldhidezaperrors = config.plugins.buyukbangpanel.hidezaperrors.value
		self.oldfilterdummy = config.plugins.buyukbangpanel.filterdummy.value
		self.olddummystring = config.plugins.buyukbangpanel.dummystring.value
		self.oldscheduledoperation = config.plugins.buyukbangpanel.scheduledoperation.value
		self.oldscheduledoperationtime = config.plugins.buyukbangpanel.scheduledoperationtime.value
		self.oldscheduledoperationmon = config.plugins.buyukbangpanel.scheduledoperationmon.value
		self.oldscheduledoperationtue = config.plugins.buyukbangpanel.scheduledoperationtue.value
		self.oldscheduledoperationwed = config.plugins.buyukbangpanel.scheduledoperationwed.value
		self.oldscheduledoperationthu = config.plugins.buyukbangpanel.scheduledoperationthu.value
		self.oldscheduledoperationfri = config.plugins.buyukbangpanel.scheduledoperationfri.value
		self.oldscheduledoperationsat = config.plugins.buyukbangpanel.scheduledoperationsat.value
		self.oldscheduledoperationsun = config.plugins.buyukbangpanel.scheduledoperationsun.value
		self.oldstartuptostandby = config.plugins.buyukbangpanel.startuptostandby.value

	# for summary:
	def changedEntry(self):
		for x in self.onChangedEntry:
			x()

	def getCurrentEntry(self):
		return self["config"].getCurrent()[0]
		
	def getCurrentValue(self):
		return str(self["config"].getCurrent()[1].getText())
		
	def createSummary(self):
		from Screens.Setup import SetupSummary
		return SetupSummary
		
	def selectionChanged(self):
		self["statusbar"].setText(" ")

	def save_pre(self):
		if config.plugins.buyukbangpanel.fixepgencoding.value != "disable" \
		and (self.oldfixepgencoding != config.plugins.buyukbangpanel.fixepgencoding.value or self.oldepgencoding != config.plugins.buyukbangpanel.epgencoding.value):
			encodingConfirmation = self.session.openWithCallback(self.save,MessageBox,_("Buyukbang Panel\n\nUpdating encoding settings requires internet connection to query Kingofsat and this may take a few minutes.\n\nDo you want to continue?"), MessageBox.TYPE_YESNO, timeout=15, default=True)
			encodingConfirmation.setTitle(_("Continue?"))
		else:
			self.save(True)

	def save(self, answer):
		global autoStartTimer
		if answer is True:
			if config.plugins.buyukbangpanel.interval.value < 2:
				config.plugins.buyukbangpanel.interval.setValue(2)
			if config.plugins.buyukbangpanel.startupcopydelay.value < 2:
				config.plugins.buyukbangpanel.startupcopydelay.setValue(2)
			self.saveAll()
			print>>log, _("Settings saved")
			self["statusbar"].setText(_("Settings saved"))

			if self.oldscheduled != config.plugins.buyukbangpanel.scheduled.value \
			or self.oldperiodic != config.plugins.buyukbangpanel.periodic.value \
			or self.oldstartupcopydelay != config.plugins.buyukbangpanel.startupcopydelay.value \
			or self.oldscheduledepgcopytime != config.plugins.buyukbangpanel.scheduledepgcopytime.value \
			or self.oldinterval != config.plugins.buyukbangpanel.interval.value \
			or self.oldscheduledoperation != config.plugins.buyukbangpanel.scheduledoperation.value \
			or self.oldscheduledoperationtime != config.plugins.buyukbangpanel.scheduledoperationtime.value \
			or self.oldscheduledoperationmon != config.plugins.buyukbangpanel.scheduledoperationmon.value \
			or self.oldscheduledoperationtue != config.plugins.buyukbangpanel.scheduledoperationtue.value \
			or self.oldscheduledoperationwed != config.plugins.buyukbangpanel.scheduledoperationwed.value \
			or self.oldscheduledoperationthu != config.plugins.buyukbangpanel.scheduledoperationthu.value \
			or self.oldscheduledoperationfri != config.plugins.buyukbangpanel.scheduledoperationfri.value \
			or self.oldscheduledoperationsat != config.plugins.buyukbangpanel.scheduledoperationsat.value \
			or self.oldscheduledoperationsun != config.plugins.buyukbangpanel.scheduledoperationsun.value \
			or self.oldstartuptostandby != config.plugins.buyukbangpanel.startuptostandby.value:
				if autoStartTimer is not None:
					autoStartTimer.update()

			if self.oldfixepgencoding != config.plugins.buyukbangpanel.fixepgencoding.value \
			or self.oldepgencoding != config.plugins.buyukbangpanel.epgencoding.value:
				try:
					os.rename('/usr/share/enigma2/encoding.conf_BuyukbangPanelBackup','/usr/share/enigma2/encoding.conf')
					#Assure that encoding.conf is updated with the new encoding
					self.oldfixepgencoding = "disable"
				except Exception, e:
					print>>log, _("Updating EPG encoding setting failed")
					print>>log, e
			if config.plugins.buyukbangpanel.fixepgencoding.value != "disable" and (self.oldfixepgencoding != config.plugins.buyukbangpanel.fixepgencoding.value):
				try:
					if not os.path.exists('/usr/share/enigma2/encoding.conf') or not os.path.exists('/usr/share/enigma2/encoding.conf_BuyukbangPanelBackup'):
						os.system('T=/usr/share/enigma2/encoding.conf && touch $T && (! grep -q "### BUYUKBANG PANEL ENCODING FIX ###" $T || [ ! -s $T"_BuyukbangPanelBackup" ]) && cp $T $T"_BuyukbangPanelBackup" && echo "" >> $T && echo "### BUYUKBANG PANEL ENCODING FIX ###" >> $T; wget -qO- "http://en.kingofsat.net/find2.php?cl=' + config.plugins.buyukbangpanel.fixepgencoding.value + '&ordre=freq" | grep ">NID:.*>TID:" | while read line ; do TSID="$(echo "$line" | cut -d":" -f3 | cut -d"<" -f1)"; ONID="$(echo "$line" | cut -d":" -f2 | cut -d"<" -f1)"; [ "$(echo $TSID | awk "/^[0-9]+$/")" != "" ] && [ "$(echo $ONID | awk "/^[0-9]+$/")" != "" ] && ELINE="$TSID $ONID ' + config.plugins.buyukbangpanel.epgencoding.value + '" && ! grep -q "$ELINE" $T && echo "$ELINE" >> $T; done')
				except Exception, e:
					print>>log, _("Fixing EPG encoding failed")
					print>>log, e

			if self.oldlinkepg != config.plugins.buyukbangpanel.linkepg.value \
			or self.oldreadepgboquet != config.plugins.buyukbangpanel.readepgboquet.value \
			or self.oldfilterdummy != config.plugins.buyukbangpanel.filterdummy.value \
			or self.olddummystring != config.plugins.buyukbangpanel.dummystring.value \
			or self.oldfixepgencoding != config.plugins.buyukbangpanel.fixepgencoding.value \
			or self.oldepgencoding != config.plugins.buyukbangpanel.epgencoding.value and config.plugins.buyukbangpanel.fixepgencoding.value != "disable" \
			or self.oldhidezaperrors != config.plugins.buyukbangpanel.hidezaperrors.value:
				restartConfirmation = self.session.openWithCallback(self.restartEnigma,MessageBox,_("Buyukbang Panel\n\nRestart needed to apply the new settings.\n\nDo you want to restart now?"), MessageBox.TYPE_YESNO, timeout=15, default=True)
				restartConfirmation.setTitle(_("Restart now?"))

	def restartEnigma(self, answer):
		#Notifications.AddNotification(Screens.Standby.TryQuitMainloop, 3)
		#from enigma import quitMainloop
		#quitMainloop(5)
		if answer is True:
			self.session.open(TryQuitMainloop, int(config.plugins.buyukbangpanel.restarttype.value))
		
	def cancel(self):
		global manualEpgCopyRunning
		for x in self["config"].list:
			x[1].cancel()
		manualEpgCopyRunning = False
		self.close(False,self.session)

	def yellowAction(self):
		self.session.open(LogScreen)

	def blueAction(self):
		global reboot
		if menuIndex == 0:
			if twisted.python.runtime.platform.supportsThreads():
				threads.deferToThread(self.copyEpg,self).addCallback(lambda ignore: self.afterCopyEPG())
			else:
				self.copyEpg(self)
				self.afterCopyEPG()

	def onTimer(self):
		self.timer.stop()
		if twisted.python.runtime.platform.supportsThreads():
			threads.deferToThread(self.copyEpg,self).addCallback(lambda ignore: self.afterCopyEPG())
		else:
			self.copyEpg(self)
			self.afterCopyEPG()

	def afterCopyEPG(self):
		global reboot
		if reboot:
			restartConfirmation = self.session.openWithCallback(self.restartEnigma,MessageBox,_("Buyukbang Panel\n\nRestart needed to load the EPG data.\n\nDo you want to restart now?"), MessageBox.TYPE_YESNO, timeout=15, default=True)
			restartConfirmation.setTitle(_("Restart now?"))
		self.update()

###################################### LOG SCREEN ###################################
class LogScreen(Screen):
	skin = """
	<screen position="center,center" size="640,400" title="Buyukbang Panel v1.4.2             buyukbang.blogspot.com" >
		<ePixmap name="red"    position="0,0"   zPosition="2" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
		<ePixmap name="green"  position="160,0" zPosition="2" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
		<ePixmap name="yellow" position="320,0" zPosition="2" size="140,40" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on" /> 
		<ePixmap name="blue"   position="480,0" zPosition="2" size="140,40" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on" /> 

		<widget name="key_red" position="0,0" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="background" shadowOffset="-2,-2" /> 
		<widget name="key_green" position="160,0" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="background" shadowOffset="-2,-2" /> 
		<widget name="key_yellow" position="320,0" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="background" shadowOffset="-2,-2" />
		<widget name="key_blue" position="480,0" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="background" shadowOffset="-2,-2" />
	
		<ePixmap alphatest="on" pixmap="skin_default/icons/clock.png" position="560,378" size="14,14" zPosition="3"/>
		<widget font="Regular;18" halign="left" position="585,375" render="Label" size="55,20" source="global.CurrentTime" transparent="1" valign="center" zPosition="3">
			<convert type="ClockToText">Default</convert>
		</widget>
	
		<widget name="list" position="10,60" size="620,320" />
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self["key_red"] = Button(_("Clear"))
		self["key_green"] = Button()
		self["key_yellow"] = Button()
		self["key_blue"] = Button(_("Save"))
		self["list"] = ScrollLabel(log.getvalue())
		self["actions"] = ActionMap(["DirectionActions", "OkCancelActions", "ColorActions"],
		{
			"red": self.clear,
			"save": self.save,
			"blue": self.save,
			"cancel": self.cancel,
			"ok": self.cancel,
			"left": self["list"].pageUp,
			"right": self["list"].pageDown,
			"up": self["list"].pageUp,
			"down": self["list"].pageDown,
			"pageUp": self["list"].pageUp,
			"pageDown": self["list"].pageDown
		}, -2)

	def save(self):
		try:
			f = open('/tmp/buyukbangpanel.log', 'w')
			f.write(log.getvalue())
			f.close()
		except Exception, e:
			self["list"].setText("Failed to write /tmp/buyukbangpanel.log")
		self.close(True)

	def cancel(self):
		self.close(False)

	def clear(self):
		log.logfile.reset()
		log.logfile.truncate()
		self.close(False)

############################## EPG FILE OPERATIONS SCREEN ###########################
class EPGFileOperationsScreen(Screen):
	skin = """
	<screen position="center,center" size="640,400" title="Buyukbang Panel v1.4.2             buyukbang.blogspot.com" >
		<ePixmap name="red"    position="0,0"   zPosition="2" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
		<ePixmap name="green"  position="160,0" zPosition="2" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
		<ePixmap name="yellow" position="320,0" zPosition="2" size="140,40" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on" /> 
		<ePixmap name="blue"   position="480,0" zPosition="2" size="140,40" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on" /> 

		<widget name="key_red" position="0,0" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="background" shadowOffset="-2,-2" /> 
		<widget name="key_green" position="160,0" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="background" shadowOffset="-2,-2" /> 
		<widget name="key_yellow" position="320,0" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="background" shadowOffset="-2,-2" />
		<widget name="key_blue" position="480,0" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="background" shadowOffset="-2,-2" />
	
		<ePixmap alphatest="on" pixmap="skin_default/icons/clock.png" position="560,378" size="14,14" zPosition="3"/>
		<widget font="Regular;18" halign="left" position="585,375" render="Label" size="55,20" source="global.CurrentTime" transparent="1" valign="center" zPosition="3">
			<convert type="ClockToText">Default</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self["key_red"] = Button(_("Delete"))
		self["key_green"] = Button(_("Backup"))
		self["key_yellow"] = Button(_("Restore"))
		self["key_blue"] = Button()
		self["actions"] = ActionMap(["DirectionActions", "OkCancelActions", "ColorActions"],
		{
			"red": self.deleteEpg,
			"green": self.backupEpg,
			"yellow": self.restoreEpg,
			"blue": self.cancel,
			"cancel": self.cancel,
			"ok": self.cancel,
		}, -2)

	def cancel(self):
		self.close(False)

	def deleteEpg(self):
		self.session.open(Console, title=_("Delete"), cmdlist=['E=`ls -tr /hdd/epg.dat /media/hdd/epg.dat /media/usb/epg.dat /media/cf/epg.dat 2>/dev/null | tail -n1`; [ "$E" != "" ] && [ -f "$E" ] ; then rm "$E" && init 4 && sleep 5 && init 3'])

	def backupEpg(self):
		self.session.open(Console, title=_("Backup"), cmdlist=['E=`ls -tr /hdd/epg.dat /media/hdd/epg.dat /media/usb/epg.dat /media/cf/epg.dat 2>/dev/null | tail -n1`; [ "$E" != "" ] && [ -f "$E" ] ; then cp "$E" "$E"_backup'])

	def restoreEpg(self):
		self.session.open(Console, title=_("Restore"), cmdlist=['E=`ls -tr /hdd/epg.dat_backup /media/hdd/epg.dat_backup /media/usb/epg.dat_backup /media/cf/epg.dat_backup 2>/dev/null | tail -n1`; [ "$E" != "" ] && [ -f "$E" ] ; then cp "$E" "${E%???????}" && init 4 && sleep 5 && init 3'])


def main(session, **kwargs):
	session.openWithCallback(doneConfiguring(session), mainMenu)

def doneConfiguring(self):
	global autoStartTimer
	if autoStartTimer is not None:
		autoStartTimer.update()

###################################### EPGDAT ###################################
import sys
import codecs
import struct
from datetime import datetime

try:
	import dreamcrc
	crc32_dreambox = lambda d,t: dreamcrc.crc32(d,t) & 0xffffffff
except:
	# this table is used by CRC32 routine below (used by Dreambox for
	# computing REF DESC value).
	# The original DM routine is a modified CRC32 standard routine,
	# so cannot use Python standard binascii.crc32()
	CRCTABLE = (
		0x00000000, 0x04C11DB7, 0x09823B6E, 0x0D4326D9,
		0x130476DC, 0x17C56B6B, 0x1A864DB2, 0x1E475005,
		0x2608EDB8, 0x22C9F00F, 0x2F8AD6D6, 0x2B4BCB61,
		0x350C9B64, 0x31CD86D3, 0x3C8EA00A, 0x384FBDBD,
		0x4C11DB70, 0x48D0C6C7, 0x4593E01E, 0x4152FDA9,
		0x5F15ADAC, 0x5BD4B01B, 0x569796C2, 0x52568B75,
		0x6A1936C8, 0x6ED82B7F, 0x639B0DA6, 0x675A1011,
		0x791D4014, 0x7DDC5DA3, 0x709F7B7A, 0x745E66CD,
		0x9823B6E0, 0x9CE2AB57, 0x91A18D8E, 0x95609039,
		0x8B27C03C, 0x8FE6DD8B, 0x82A5FB52, 0x8664E6E5,
		0xBE2B5B58, 0xBAEA46EF, 0xB7A96036, 0xB3687D81,
		0xAD2F2D84, 0xA9EE3033, 0xA4AD16EA, 0xA06C0B5D,
		0xD4326D90, 0xD0F37027, 0xDDB056FE, 0xD9714B49,
		0xC7361B4C, 0xC3F706FB, 0xCEB42022, 0xCA753D95,
		0xF23A8028, 0xF6FB9D9F, 0xFBB8BB46, 0xFF79A6F1,
		0xE13EF6F4, 0xE5FFEB43, 0xE8BCCD9A, 0xEC7DD02D,
		0x34867077, 0x30476DC0, 0x3D044B19, 0x39C556AE,
		0x278206AB, 0x23431B1C, 0x2E003DC5, 0x2AC12072,
		0x128E9DCF, 0x164F8078, 0x1B0CA6A1, 0x1FCDBB16,
		0x018AEB13, 0x054BF6A4, 0x0808D07D, 0x0CC9CDCA,
		0x7897AB07, 0x7C56B6B0, 0x71159069, 0x75D48DDE,
		0x6B93DDDB, 0x6F52C06C, 0x6211E6B5, 0x66D0FB02,
		0x5E9F46BF, 0x5A5E5B08, 0x571D7DD1, 0x53DC6066,
		0x4D9B3063, 0x495A2DD4, 0x44190B0D, 0x40D816BA,
		0xACA5C697, 0xA864DB20, 0xA527FDF9, 0xA1E6E04E,
		0xBFA1B04B, 0xBB60ADFC, 0xB6238B25, 0xB2E29692,
		0x8AAD2B2F, 0x8E6C3698, 0x832F1041, 0x87EE0DF6,
		0x99A95DF3, 0x9D684044, 0x902B669D, 0x94EA7B2A,
		0xE0B41DE7, 0xE4750050, 0xE9362689, 0xEDF73B3E,
		0xF3B06B3B, 0xF771768C, 0xFA325055, 0xFEF34DE2,
		0xC6BCF05F, 0xC27DEDE8, 0xCF3ECB31, 0xCBFFD686,
		0xD5B88683, 0xD1799B34, 0xDC3ABDED, 0xD8FBA05A,
		0x690CE0EE, 0x6DCDFD59, 0x608EDB80, 0x644FC637,
		0x7A089632, 0x7EC98B85, 0x738AAD5C, 0x774BB0EB,
		0x4F040D56, 0x4BC510E1, 0x46863638, 0x42472B8F,
		0x5C007B8A, 0x58C1663D, 0x558240E4, 0x51435D53,
		0x251D3B9E, 0x21DC2629, 0x2C9F00F0, 0x285E1D47,
		0x36194D42, 0x32D850F5, 0x3F9B762C, 0x3B5A6B9B,
		0x0315D626, 0x07D4CB91, 0x0A97ED48, 0x0E56F0FF,
		0x1011A0FA, 0x14D0BD4D, 0x19939B94, 0x1D528623,
		0xF12F560E, 0xF5EE4BB9, 0xF8AD6D60, 0xFC6C70D7,
		0xE22B20D2, 0xE6EA3D65, 0xEBA91BBC, 0xEF68060B,
		0xD727BBB6, 0xD3E6A601, 0xDEA580D8, 0xDA649D6F,
		0xC423CD6A, 0xC0E2D0DD, 0xCDA1F604, 0xC960EBB3,
		0xBD3E8D7E, 0xB9FF90C9, 0xB4BCB610, 0xB07DABA7,
		0xAE3AFBA2, 0xAAFBE615, 0xA7B8C0CC, 0xA379DD7B,
		0x9B3660C6, 0x9FF77D71, 0x92B45BA8, 0x9675461F,
		0x8832161A, 0x8CF30BAD, 0x81B02D74, 0x857130C3,
		0x5D8A9099, 0x594B8D2E, 0x5408ABF7, 0x50C9B640,
		0x4E8EE645, 0x4A4FFBF2, 0x470CDD2B, 0x43CDC09C,
		0x7B827D21, 0x7F436096, 0x7200464F, 0x76C15BF8,
		0x68860BFD, 0x6C47164A, 0x61043093, 0x65C52D24,
		0x119B4BE9, 0x155A565E, 0x18197087, 0x1CD86D30,
		0x029F3D35, 0x065E2082, 0x0B1D065B, 0x0FDC1BEC,
		0x3793A651, 0x3352BBE6, 0x3E119D3F, 0x3AD08088,
		0x2497D08D, 0x2056CD3A, 0x2D15EBE3, 0x29D4F654,
		0xC5A92679, 0xC1683BCE, 0xCC2B1D17, 0xC8EA00A0,
		0xD6AD50A5, 0xD26C4D12, 0xDF2F6BCB, 0xDBEE767C,
		0xE3A1CBC1, 0xE760D676, 0xEA23F0AF, 0xEEE2ED18,
		0xF0A5BD1D, 0xF464A0AA, 0xF9278673, 0xFDE69BC4,
		0x89B8FD09, 0x8D79E0BE, 0x803AC667, 0x84FBDBD0,
		0x9ABC8BD5, 0x9E7D9662, 0x933EB0BB, 0x97FFAD0C,
		0xAFB010B1, 0xAB710D06, 0xA6322BDF, 0xA2F33668,
		0xBCB4666D, 0xB8757BDA, 0xB5365D03, 0xB1F740B4
	)
	# CRC32 in Dreambox/DVB way (see CRCTABLE comment above)
	# "crcdata" is the description string
	# "crctype" is the description type (1 byte 0x4d or 0x4e)
	# !!!!!!!!! IT'S VERY TIME CONSUMING !!!!!!!!!
	def crc32_dreambox(crcdata, crctype, crctable=CRCTABLE):
		# ML Optimized: local CRCTABLE (locals are faster), remove self, remove code that has no effect, faster loop    
		#crc=0x00000000L
		#crc=((crc << 8 ) & 0xffffff00L) ^ crctable[((crc >> 24) ^ crctype) & 0x000000ffL ]
		crc = crctable[crctype & 0x000000ffL]
		crc = ((crc << 8) & 0xffffff00L) ^ crctable[((crc >> 24) ^ len(crcdata)) & 0x000000ffL]
		for d in crcdata:
		    crc = ((crc << 8) & 0xffffff00L) ^ crctable[((crc >> 24) ^ ord(d)) & 0x000000ffL]
		return crc

# convert time or length from datetime format to 3 bytes hex value 
# i.e. 20:25:30 -> 0x20 , 0x25 , 0x30
def TL_hexconv(dt):
	return (
		(dt.hour % 10) + (16 * (dt.hour / 10)),
		(dt.minute % 10) + (16 * (dt.minute / 10)),
		(dt.second % 10) + (16 * (dt.second / 10))
		)


class epgdat_class:
	# temp files used for EPG.DAT creation
	LAMEDB = '/etc/enigma2/lamedb'
	EPGDAT_FILENAME = 'epg.dat'
	EPGDAT_TMP_FILENAME = 'epg.dat.tmp'
	LB_ENDIAN = '<'
	EPG_HEADER1_channel_count = 0
	EPG_HEADER2_description_count = 0
	EPG_TOTAL_EVENTS = 0

	EXCLUDED_SID = []

	# initialize an empty dictionary (Python array)
	# as total events container postprocessed
	EPGDAT_HASH_EVENT_MEMORY_CONTAINER = {}

	# initialize an empty dictionary (Python array)
	# as channel events container before preprocessing
	events = []

	# initialize an empty dictionary (Python array)
	# the following format can handle duplicated channel name 
	# format: { channel_name : [ sid , sid , .... ] }
	lamedb_dict = {}

	# DVB/EPG count days with a 'modified Julian calendar' where day 1 is 17 November 1858
	# Python can use a 'proleptic Gregorian calendar' ('import datetime') where day 1 is 01/01/0001
	# Using 'proleptic' we can compute correct days as difference from NOW and 17/11/1858
	#   datetime.datetime.toordinal(1858,11,17) => 678576
	EPG_PROLEPTIC_ZERO_DAY = 678576

	def __init__(self,tmp_path,lamedb_path,epgdat_path):
		self.EPGDAT_FILENAME = epgdat_path
		self.EPGDAT_TMP_FILENAME = os.path.join(tmp_path,self.EPGDAT_TMP_FILENAME)
		self.EPG_TMP_FD = open(self.EPGDAT_TMP_FILENAME,"wb")
		self.LAMEDB = lamedb_path
		self.s_B = struct.Struct("B")
		self.s_BB = struct.Struct("BB")
		self.s_BBB = struct.Struct("BBB")
		self.s_b_HH = struct.Struct(">HH")
		self.s_I = struct.Struct(self.LB_ENDIAN + "I")
		self.s_II = struct.Struct(self.LB_ENDIAN + "II")     
		self.s_IIII = struct.Struct(self.LB_ENDIAN + "IIII")     
		self.s_B3sBBB = struct.Struct("B3sBBB")     
		self.s_3sBB = struct.Struct("3sBB")     

	def set_endian(self,endian):
		self.LB_ENDIAN = endian
		self.s_I = struct.Struct(self.LB_ENDIAN + "I")
		self.s_II = struct.Struct(self.LB_ENDIAN + "II")     
		self.s_IIII = struct.Struct(self.LB_ENDIAN + "IIII")

	def set_excludedsid(self,exsidlist):
		self.EXCLUDED_SID = exsidlist

	# assembling short description (type 0x4d , it's the Title) and compute its crc
	def short_desc(self, s):
		# 0x15 is UTF-8 encoding.
		res = self.s_3sBB.pack('eng', len(s) + 1, 0x15) + str(s) + "\0"
		return (crc32_dreambox(res,0x4d),res)

	# assembling long description (type 0x4e) and compute its crc
	def long_desc(self,s):
		r = []
		# compute total number of descriptions, block 245 bytes each
		# number of descriptions start to index 0
		num_tot_desc = (len(s) + 244) // 245
		for i in range(num_tot_desc):
			ssub = s[i * 245:i * 245 + 245]
			sres = self.s_B3sBBB.pack((i << 4) + (num_tot_desc - 1),'eng',0x00,len(ssub) + 1,0x15) + str(ssub)
			r.append((crc32_dreambox(sres,0x4e), sres))
		return r

	def add_event(self, starttime, duration, title, description):
		#print "add event : ",event_starttime_unix_gmt, "title : " ,event_title
		self.events.append((starttime, duration, self.short_desc(title[:240]), self.long_desc(description)))

	def importEvents(self, services, events):
		# We need to combine short and long descriptions since add_event function has only one description input parameter
		# def add_event(self, starttime, duration, title, description):		
		# Event tuple structure is BDTSE0 ==> B = Event Begin Time, D = Event Duration, T = Event Title, S = Event Short Description, E = Event Extended Description, 0 = PyLong(0)
		for event in events:
			desc = None
			if event[3]:
				desc = event[3] + '\n' + event[4]
			else:
				desc = event[4]
			self.add_event(event[0], event[1], event[2], desc)
		self.preprocess_events_channel(services)

	def preprocess_events_channel(self, services):
		EPG_EVENT_DATA_id = 0
		for service in services:
			# prepare and write CHANNEL INFO record
			ssid = service.split(":")
			# write CHANNEL INFO record (sid, onid, tsid, eventcount)
			self.EPG_TMP_FD.write(self.s_IIII.pack(
				int(ssid[3],16), int(ssid[5],16),
				int(ssid[4],16), len(self.events)))
			self.EPG_HEADER1_channel_count += 1
			# event_dict.keys() are numeric so indexing is possibile
			# key is the same thing as counter and is more simple to manage last-1 item
			events = self.events
			s_BB = self.s_BB
			s_BBB = self.s_BBB
			s_I = self.s_I
			for event in events:
				# **** (1) : create DESCRIPTION HEADER / DATA ****
				EPG_EVENT_HEADER_datasize = 0
				# short description (title) type 0x4d
				short_d = event[2]
				EPG_EVENT_HEADER_datasize += 4  # add 4 bytes for a sigle REF DESC (CRC32)
				#if not epg_event_description_dict.has_key(short_d[0]):
				#if not exist_event(short_d[0]) :
				if not self.EPGDAT_HASH_EVENT_MEMORY_CONTAINER.has_key(short_d[0]):
					# DESCRIPTION DATA
					pack_1 = s_BB.pack(0x4d,len(short_d[1])) + short_d[1]
					# DESCRIPTION HEADER (2 int) will be computed at the end just before EPG.DAT write
					# because it need the total number of the same description called by many channel section
					#save_event(short_d[0],[pack_1,1])
					self.EPGDAT_HASH_EVENT_MEMORY_CONTAINER[short_d[0]] = [pack_1,1]
					self.EPG_HEADER2_description_count += 1
				else:
					#increment_event(short_d[0])
					self.EPGDAT_HASH_EVENT_MEMORY_CONTAINER[short_d[0]][1] += 1
				# long description type 0x4e
				long_d = event[3]
				EPG_EVENT_HEADER_datasize += 4 * len(long_d) # add 4 bytes for a single REF DESC (CRC32)
				for desc in long_d:
					#if not epg_event_description_dict.has_key(long_d[i][0]):
					#if not exist_event(long_d[i][0]) :
					if not self.EPGDAT_HASH_EVENT_MEMORY_CONTAINER.has_key(desc[0]):
						# DESCRIPTION DATA
						pack_1 = s_BB.pack(0x4e,len(desc[1])) + desc[1]
						self.EPG_HEADER2_description_count += 1
						# DESCRIPTION HEADER (2 int) will be computed at the end just before EPG.DAT write
						# because it need the total number of the same description called by different channel section
						#save_event(long_d[i][0],[pack_1,1])
						self.EPGDAT_HASH_EVENT_MEMORY_CONTAINER[desc[0]] = [pack_1,1]
					else:
						#increment_event(long_d[i][0])
						self.EPGDAT_HASH_EVENT_MEMORY_CONTAINER[desc[0]][1] += 1
				# **** (2) : have REF DESC and now can create EVENT HEADER / DATA ****
				# EVENT HEADER (2 bytes: 0x01 , 10 bytes + number of CRC32 * 4)
				pack_1 = s_BB.pack(0x01,0x0a + EPG_EVENT_HEADER_datasize)
				self.EPG_TMP_FD.write(pack_1)
				# extract date and time from <event>
				# unix format (second since 1970) and already GMT corrected
				event_time_HMS = datetime.utcfromtimestamp(event[0])
				event_length_HMS = datetime.utcfromtimestamp(event[1])
				# epg.dat date is = (proleptic date - epg_zero_day)
				dvb_date = event_time_HMS.toordinal() - self.EPG_PROLEPTIC_ZERO_DAY            
				# EVENT DATA
				# simply create an incremental ID,  starting from '1'
				# event_id appears to be per channel, so this should be okay.
				EPG_EVENT_DATA_id += 1
				pack_1 = self.s_b_HH.pack(EPG_EVENT_DATA_id,dvb_date) # ID and DATE , always in BIG_ENDIAN
				pack_2 = s_BBB.pack(*TL_hexconv(event_time_HMS)) # START TIME
				pack_3 = s_BBB.pack(*TL_hexconv(event_length_HMS)) # LENGTH 
				pack_4 = s_I.pack(short_d[0]) # REF DESC short (title)            
				for d in long_d:
					pack_4 += s_I.pack(d[0]) # REF DESC long
				self.EPG_TMP_FD.write(pack_1 + pack_2 + pack_3 + pack_4)
		# reset again event container
		self.EPG_TOTAL_EVENTS += len(self.events)
		self.events = []

	def final_process(self):
		if self.EPG_TOTAL_EVENTS > 0:
			self.EPG_TMP_FD.close()
			epgdat_fd = open(self.EPGDAT_FILENAME,"wb")
			# HEADER 1
			pack_1 = struct.pack(self.LB_ENDIAN + "I13sI",0x98765432,'ENIGMA_EPG_V7',self.EPG_HEADER1_channel_count)
			epgdat_fd.write(pack_1)
			# write first EPG.DAT section
			EPG_TMP_FD = open(self.EPGDAT_TMP_FILENAME,"rb")
			while True:
				pack_1 = EPG_TMP_FD.read(4096)
				if not pack_1:
					break
				epgdat_fd.write(pack_1)
			EPG_TMP_FD.close()
			# HEADER 2
			s_ii = self.s_II     
			pack_1 = self.s_I.pack(self.EPG_HEADER2_description_count)
			epgdat_fd.write(pack_1)
			# event MUST BE WRITTEN IN ASCENDING ORDERED using HASH CODE as index
			for temp in sorted(self.EPGDAT_HASH_EVENT_MEMORY_CONTAINER.keys()):
				pack_2 = self.EPGDAT_HASH_EVENT_MEMORY_CONTAINER[temp]
				#pack_1=struct.pack(LB_ENDIAN+"II",int(temp,16),pack_2[1])
				pack_1 = s_ii.pack(temp,pack_2[1])
				epgdat_fd.write(pack_1 + pack_2[0])
			epgdat_fd.close()
		# *** cleanup **
		if os.path.exists(self.EPGDAT_TMP_FILENAME):
			os.unlink(self.EPGDAT_TMP_FILENAME)


###################################### TIMER ###################################
class AutoStartTimer:
	def __init__(self, session):
		self.copyEpg = copyEpg
		self.periodictime = 0
		self.oldperiodictime = 0
		self.scheduledepgcopytime = 0
		self.oldscheduledepgcopytime = 0
		self.scheduledoperationtime = 0
		self.oldscheduledoperationtime = 0
		self.oldinterval = 0
		self.firstPeriodicEPGCopy = 1
		self.session = session
		self.timer = enigma.eTimer() 
		self.timer.callback.append(self.onTimer)
		self.update()

	def getWakeTime(self):
		global scheduledOperation
		wakeTime = -1
		nowt = time.time()
		now = time.localtime(nowt)
		startupcopydelay = int(config.plugins.buyukbangpanel.startupcopydelay.value) * 60
		delay = 0

		if config.plugins.buyukbangpanel.scheduled.value:
			if self.scheduledepgcopytime == 0:
				delay = startupcopydelay
			scheduledepgcopytimevalue = config.plugins.buyukbangpanel.scheduledepgcopytime.value
			self.scheduledepgcopytime = int(time.mktime((now.tm_year, now.tm_mon, now.tm_mday, scheduledepgcopytimevalue[0], scheduledepgcopytimevalue[1], 0, 0, now.tm_yday, now.tm_isdst)))
			if self.scheduledepgcopytime < nowt + delay:
				self.scheduledepgcopytime += 86400 # Tomorrow.
			if self.scheduledepgcopytime != self.oldscheduledepgcopytime:
				self.oldscheduledepgcopytime = self.scheduledepgcopytime
				print>>log, _("Scheduled EPG copy time is set to %s") % time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(self.scheduledepgcopytime))
			wakeTime = self.scheduledepgcopytime
			scheduledOperation = "SCHEDULED"

		if config.plugins.buyukbangpanel.periodic.value:
			global lastrestartallowedtime
			interval = int(config.plugins.buyukbangpanel.interval.value) * 60
			nextrestartallowedtime = lastrestartallowedtime + interval
			if self.periodictime == 0:
				self.periodictime = nowt + startupcopydelay
			elif self.oldinterval != interval:
				self.periodictime = nowt + interval
				self.oldinterval = interval
			#Invalid clock fix for periodic epg copy (firstPeriodicEPGCopy check added)
			while (self.periodictime <= nowt or (self.firstPeriodicEPGCopy == 0 and self.periodictime < nextrestartallowedtime)):
				self.periodictime += interval
			if self.periodictime != self.oldperiodictime:
				self.oldperiodictime = self.periodictime
				self.oldinterval = interval
				if lastrestartallowedtime > 0:
					print>>log, _("Previous restart detected. Periodic EPG copy time recalculated.")
				print>>log, _("Periodic EPG copy time is set to %s") % time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(self.periodictime))
			if wakeTime == -1 or self.periodictime < wakeTime:
				wakeTime = self.periodictime
				scheduledOperation = "PERIODIC"
				
		if config.plugins.buyukbangpanel.scheduledoperation.value != "0":
			scheduledoperationtimevalue = config.plugins.buyukbangpanel.scheduledoperationtime.value
			self.scheduledoperationtime = int(time.mktime((now.tm_year, now.tm_mon, now.tm_mday, scheduledoperationtimevalue[0], scheduledoperationtimevalue[1], 0, 0, now.tm_yday, now.tm_isdst)))
			if self.scheduledoperationtime < nowt:
				self.scheduledoperationtime += 86400 # Tomorrow
			dayFound = 0
			if config.plugins.buyukbangpanel.scheduledoperationmon.value == False \
			and config.plugins.buyukbangpanel.scheduledoperationtue.value == False \
			and config.plugins.buyukbangpanel.scheduledoperationwed.value == False \
			and config.plugins.buyukbangpanel.scheduledoperationthu.value == False \
			and config.plugins.buyukbangpanel.scheduledoperationfri.value == False \
			and config.plugins.buyukbangpanel.scheduledoperationsat.value == False \
			and config.plugins.buyukbangpanel.scheduledoperationwed.value == False:
				dayFound = 2
				print>>log, _("No weekday selected, scheduled operation is disabled")
			while (dayFound == 0):
				weekday = (int(time.strftime("%w", time.localtime(self.scheduledoperationtime))) - 1) % 7 #strftime retuns 0 as sunday, we normalize this and make monday 0
				if weekday == 0:
					if config.plugins.buyukbangpanel.scheduledoperationmon.value == False:
						self.scheduledoperationtime += 86400 # Add one day
					else:
						dayFound = 1
				elif weekday == 1:
					if config.plugins.buyukbangpanel.scheduledoperationtue.value == False:
						self.scheduledoperationtime += 86400 # Add one day
					else:
						dayFound = 1
				elif weekday == 2:
					if config.plugins.buyukbangpanel.scheduledoperationwed.value == False:
						self.scheduledoperationtime += 86400 # Add one day
					else:
						dayFound = 1
				elif weekday == 3:
					if config.plugins.buyukbangpanel.scheduledoperationthu.value == False:
						self.scheduledoperationtime += 86400 # Add one day
					else:
						dayFound = 1
				elif weekday == 4:
					if config.plugins.buyukbangpanel.scheduledoperationfri.value == False:
						self.scheduledoperationtime += 86400 # Add one day
					else:
						dayFound = 1
				elif weekday == 5:
					if config.plugins.buyukbangpanel.scheduledoperationsat.value == False:
						self.scheduledoperationtime += 86400 # Add one day
					else:
						dayFound = 1
				elif weekday == 6:
					if config.plugins.buyukbangpanel.scheduledoperationsun.value == False:
						self.scheduledoperationtime += 86400 # Add one day
					else:
						dayFound = 1
				if dayFound == 1:
					if self.scheduledoperationtime != self.oldscheduledoperationtime:
						self.oldscheduledoperationtime = self.scheduledoperationtime
						print>>log, _("Scheduled operation time is set to %s") % time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(self.scheduledoperationtime))
					if wakeTime == -1 or self.scheduledoperationtime < wakeTime:
						wakeTime = self.scheduledoperationtime
						scheduledOperation = "OPERATION"

		return wakeTime

	def update(self):
		global scheduledOperation
		self.timer.stop()
		wakeTime = self.getWakeTime()
		if wakeTime > 0:
			now = int(time.time())
			next = long(wakeTime - now)
			#Invalid clock fix starts (for scheduled epg copy and scheduled operations)
			if now < 1300000000 and next > 420 and (not config.plugins.buyukbangpanel.periodic.value or self.firstPeriodicEPGCopy == 0) and (config.plugins.buyukbangpanel.scheduled.value or config.plugins.buyukbangpanel.scheduledoperation.value != "0"):
				# If calculated next wake time is smaller than 7 minutes than replace it with 3 minutes 1970 time check
				next = 180
				scheduledOperation = "CHECKCORRECTTIME"
			#Invalid clock fix ends
			self.timer.startLongTimer(next)
		else:
			wakeTime = -1

	def onTimer(self):
		global scheduledOperation, reboot
		self.timer.stop()
		if scheduledOperation == "OPERATION":
			self.doOperation()
		elif scheduledOperation == "CHECKCORRECTTIME":
			self.update()
		elif twisted.python.runtime.platform.supportsThreads():
			threads.deferToThread(self.copyEpg,self).addCallback(lambda ignore: self.afterCopyEPG())
		else:
			self.copyEpg(self)
			self.afterCopyEPG()

	def doOperation(self):
		operationType = int(config.plugins.buyukbangpanel.scheduledoperation.value)
		if 0 < operationType < 4:
			self.session.open(TryQuitMainloop, operationType)
		elif operationType == 4:
			self.session.open(Standby)
		print>>log, _("Scheduled operation executed")
		self.update()

	def afterCopyEPG(self):
		global reboot
		self.firstPeriodicEPGCopy = 0
		if reboot:
			config.plugins.buyukbangpanel.lastcopyepgrestarttime.setValue(int(time.time()))
			config.plugins.buyukbangpanel.lastcopyepgrestarttime.save()
			restartConfirmation = self.session.openWithCallback(self.restartEnigma,MessageBox,_("Buyukbang Panel\n\nRestart needed to load the EPG data.\n\nDo you want to restart now?"), MessageBox.TYPE_YESNO, timeout=15, default=True)
			restartConfirmation.setTitle(_("Restart now?"))
		nowt = time.time()
		if time.time() - 3600 < self.scheduledoperationtime < time.time() + 60:
			scheduledOperation = "OPERATION"
			self.doOperation()
		else:
			self.update()

	def restartEnigma(self, answer):
		# Notifications.AddNotification(Screens.Standby.TryQuitMainloop, 3)
		# Below works like init 4; init3
		# from enigma import quitMainloop
		# quitMainloop(5)
		if answer is True:
			self.session.open(TryQuitMainloop, int(config.plugins.buyukbangpanel.restarttype.value))

###################################### PLUGIN MAIN FUNCTIONS ###################################
def autostart(reason, session=None, **kwargs):
	"called with reason=1 to during shutdown, with reason=0 at startup?"
	global autoStartTimer
	global _session
	global autostartExecuted
	if autostartExecuted is None:
		autostartExecuted = True
		print>>log, _("Buyukbang Panel started")
		if config.plugins.buyukbangpanel.startuptostandby.value == "1" and reason == 0:
			if not fileExists("/tmp/buyukbangpanel.boot"):
				os.system("touch /tmp/buyukbangpanel.boot")
				Notifications.AddNotification(Standby)
				print>>log, _("Startup to standby function is activated")
		elif config.plugins.buyukbangpanel.startuptostandby.value == "2" and reason == 0:
			Notifications.AddNotification(Standby)
			print>>log, _("Startup to standby function is activated")
		if hasattr(eEPGCache, 'importEvents'):
			print>>log, _("PLi EPG patch detected")
		else:
			print>>log, _("PLi EPG patch not present on this image")
		if hasattr(eEPGCache, 'importEvent'):
			print>>log, _("Oudeis EPG patch detected")
		else:
			print>>log, _("Oudeis EPG patch not present on this image")
		if hasattr(eEPGCache, 'load'):
			print>>log, _("CrossEPG patch detected")
		else:
			print>>log, _("CrossEPG patch not present on this image")
		if twisted.python.runtime.platform.supportsThreads():
			print>>log, _("Thread support detected")
		else:
			print>>log, _("Thread support not present on this image")
		if not config.plugins.buyukbangpanel.readepgboquet.value == "1":
			eEPGCache.dst2src = getEPGMap(_session)[0]
			EventInfo.dst2src = eEPGCache.dst2src
		#Reset lastcopyepgrestarttime, it was read as a global variable.
		config.plugins.buyukbangpanel.lastcopyepgrestarttime.setValue(0)
		config.plugins.buyukbangpanel.lastcopyepgrestarttime.save()
		# Fix encoding
		if config.plugins.buyukbangpanel.fixepgencoding.value != "disable":
			try:
				# Check at most once a day
				now = time.time()
				mtime = None
				if os.path.exists('/usr/share/enigma2/encoding.conf'):
					mtime = os.path.getmtime('/usr/share/enigma2/encoding.conf')
				if not os.path.exists('/usr/share/enigma2/encoding.conf_BuyukbangPanelBackup') or not mtime or (mtime + 86400 < now):
					os.system('T=/usr/share/enigma2/encoding.conf && touch $T && (! grep -q "### BUYUKBANG PANEL ENCODING FIX ###" $T || [ ! -s $T"_BuyukbangPanelBackup" ]) && cp $T $T"_BuyukbangPanelBackup" && echo "" >> $T && echo "### BUYUKBANG PANEL ENCODING FIX ###" >> $T; nohup wget -qO- "http://en.kingofsat.net/find2.php?cl=' + config.plugins.buyukbangpanel.fixepgencoding.value + '&ordre=freq" | grep ">NID:.*>TID:" | while read line ; do TSID="$(echo "$line" | cut -d":" -f3 | cut -d"<" -f1)"; ONID="$(echo "$line" | cut -d":" -f2 | cut -d"<" -f1)"; [ "$(echo $TSID | awk "/^[0-9]+$/")" != "" ] && [ "$(echo $ONID | awk "/^[0-9]+$/")" != "" ] && ELINE="$TSID $ONID ' + config.plugins.buyukbangpanel.epgencoding.value + '" && ! grep -q "$ELINE" $T && echo "$ELINE" >> $T; done &')
			except Exception, e:
				print>>log, _("Fixing EPG encoding failed")
				print>>log, e
		try:
			os.system('S=/usr/lib/enigma2/python/Plugins/Extensions/BuyukbangPanel/buyukbang_panel.sh; T=/usr/bin/enigma2_pre_start.sh; if [ -s $T ]; then !grep -q $S $T && echo "" >> $T && echo $S >> $T; else echo "#!/bin/sh" > $T && echo $S >> $T && chmod +x $T; fi')
		except:
			pass
	if reason == 0:
		if session is not None:
			_session = session
			if autoStartTimer is None:
				autoStartTimer = AutoStartTimer(session)
	else:
		print>>log, _("Stop")

# we need this helper function to identify the descriptor
def extensionsmenu(session, **kwargs):
	main(session, **kwargs)

def housekeepingExtensionsmenu(el):
	try:
		if el.value:
			Components.PluginComponent.plugins.addPlugin(extDescriptor)
		else:
			Components.PluginComponent.plugins.removePlugin(extDescriptor)
	except Exception, e:
		print>>log, _("Failed to update extensions menu")
		print>>log, e

description = _("Miscellaneous tools for Enigma2")
config.plugins.buyukbangpanel.showinextensions.addNotifier(housekeepingExtensionsmenu, initial_call=False, immediate_feedback=False)
extDescriptor = PluginDescriptor(name="Buyukbang Panel", description=description, where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=extensionsmenu)

def Plugins(**kwargs):
	result = [
		PluginDescriptor(
			name="Buyukbang Panel",
			description=description,
			where=[
				PluginDescriptor.WHERE_AUTOSTART,
				PluginDescriptor.WHERE_SESSIONSTART
			],
			fnc=autostart,
		),
		PluginDescriptor(
			name="Buyukbang Panel",
			description=description,
			where=PluginDescriptor.WHERE_PLUGINMENU,
			icon='plugin.png',
			fnc=main
		),
	]
	if config.plugins.buyukbangpanel.showinextensions.value:
		result.append(extDescriptor)
	return result
