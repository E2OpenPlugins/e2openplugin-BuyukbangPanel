DESCRIPTION = "This panel includes following unique features: Copy EPG, Link EPG, Filter EPG, Fix EPG Encoding, Delete/Backup/Restore EPG, Hide Zap Errors, Scheduler, Conditional Startup to Standby"
SECTION = "base"
PRIORITY = "optional"
LICENSE = "proprietary"
MAINTAINER = "Buyukbang"

PV = "1.4.2"
SRCDATE = "20181127"

SRC_URI = "file://enigma2-plugin-extensions-buyukbangpanel"
RDEPENDS = "libcurl4"
RPROVIDES = "enigma2-plugin-extensions-hidezaperrors enigma2-plugin-extensions-epgturkishfix enigma2-plugin-extensions-epgexporter enigma2-plugin-extensions-epgcurrentnextfix enigma2-plugin-extensions-startuptostandby"
RCONFLICTS = "enigma2-plugin-extensions-hidezaperrors enigma2-plugin-extensions-epgturkishfix enigma2-plugin-extensions-epgexporter enigma2-plugin-extensions-epgcurrentnextfix enigma2-plugin-extensions-startuptostandby"
RREPLACES = "enigma2-plugin-extensions-hidezaperrors enigma2-plugin-extensions-epgturkishfix enigma2-plugin-extensions-epgexporter enigma2-plugin-extensions-epgcurrentnextfix enigma2-plugin-extensions-startuptostandby"
PACKAGE_ARCH = "all"

S = "${WORKDIR}/"
FILES_${PN} = "/"

pkg_preinst () {
   exit 0
}

pkg_postinst () {
   chmod 755 /usr/lib/enigma2/python/Plugins/Extensions/BuyukbangPanel/buyukbang_panel.sh
   if [ `ls -al /usr/lib/python2.7 2>/dev/null | grep base64.py | wc -l` -gt 0 ]; then
    for py32o in /usr/lib/enigma2/python/Plugins/Extensions/BuyukbangPanel/*.py32o; do mv -f $py32o /usr/lib/enigma2/python/Plugins/Extensions/BuyukbangPanel/`basename $py32o .py32o`.pyo; done
    echo "-------> Buyukbang Panel for OE 2.0 installation completed <-------"
   else
    rm -rf /usr/lib/enigma2/python/Plugins/Extensions/BuyukbangPanel/*.py32o
    echo "-------> Buyukbang Panel for OE 1.6 installation completed <-------"
   fi
   echo " "
   echo "Quick Manual:"
   echo  "------------"
   echo "Copy EPG: Copies EPG data from source channels to the same channels without EPG data on other satellites or packages. Create a bouquet named EPG and insert source and destination channels in it. Ordering should be as follows: SourceChannel, DestinationChannel1, SEPERATOR (note: anything can be typed as a seperator), SourceChannel, DestinationChannel1, DestinationChannel2, DestinationChannel3, - , ... and so on. As you can see you need to start with a source channel, then you can define one or more destination channels for a source channel and you need to use a seperator between mapping groups. This functionality can be scheduled to run at a specific time or run periodically between user defined intervals."
   echo " "
   echo "Link EPG: Links EPG data source channels to the same channels without EPG data on other satellites or packages. Link EPG does not replicate EPG data on RAM and just link it dynamically, which differs Link EPG from Copy EPG. So RAM usage or epg.dat file will not be affected, which is good in terms of system resources. Another advantage of this option is that Link EPG updates EPG changes of source channels in realtime. So you always have the latest EPG! But there is a disadvantage, too: Setting this option as ALL EPG Queries causes enigma2 always try to record it from the source channel instead of the destination channel when you want to record the event selected in the single / multi EPG browsers. Setting this option as Only Infobar and EPG Info does not have this disadvantage, but it does not cover single / multi EPG browsers and EPG searches."
   echo " "
   echo "Filter EPG: Filters out unwanted EPG broadcasts like Current and Next. You can add/remove filtered EPG titles from the user interface. This user defined list is case insensitive. Use a comma as seperator between entries."
   echo " "
   echo "Fix EPG Encoding: Fixes EPG encoding problems by querying Kingofsat for selected language and adding missing entries to encoding.conf at startup once a day."
   echo " "
   echo "EPG File Operations: Includes file operation opptions to delete, backup or restore epg.dat files."
   echo " "
   echo "Hide Zap Errors: Hides zap errors displayed on the screen after switching to wrongly modified / broken channels."
   echo " "
   echo "Scheduler: Performs scheduled restart, reboot, shutdown and standby operations."
   echo " "
   echo "Conditional Startup to Standby: Takes STB to standby on startup. Differs from statuptostandby plugin by providing an option to exclude enigma2 restarts."
   echo " "
   exit 0
}


pkg_prerm () {
   exit 0
}

pkg_postrm () {
   mv -f /usr/share/enigma2/encoding.conf_BuyukbangPanelBackup /usr/share/enigma2/encoding.conf >/dev/null 2>/dev/null
   rm -r /usr/lib/enigma2/python/Plugins/Extensions/BuyukbangPanel >/dev/null 2>/dev/null
    echo "-------> Buyukbang Panel removed <-------"
   exit 0
}


do_install() {
   cp -a enigma2-plugin-extensions-buyukbangpanel/usr ${D}/
   install -m 0755 /home/user/Desktop/hound/hound ${D}/usr/lib/enigma2/python/Plugins/Extensions/BuyukbangPanel/bbutils.pyo
}

