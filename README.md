Check this page for more colorful version:) ==> https://buyukbang.blogspot.com/2012/02/buyukbang-panel-pugin-v12-for-enigma2.html

Please read below descriptions for the details on the features and usage instructions. You can see all screenshots in a slideshow by clicking the above picture. You can report bugs you find, share your thoughts and suggestions and read other users' comments on  this page.

Translation: 
Do you what to translate Buyukbang Panel to other languages? So, just open /usr/lib/enigma2/python/Plugins/Extensions/BuyukbangPanel/locale/BuyukbangPanel.pot with a text editor, write translations to the areas under the English words/sentences, save and send this file to buyukbang@gmail.com !

Supported STB's: 
- VU+
- Dreambox
- Xtrend
- Clarke-Tech 
- Azbox
- Other boxes using Enigma2...

Version History:

v1.4.1:
- Bug fix: Exception occurs during Copy EPG process on some images including Blackhole.

v1.4:
- "EPG file operations" menu is added. With this menu, you can delete, backup or restore epg.dat files containing EPG information.
- Bug fix: Errors preventing installation of Buyukbang Panel on some images.

v1.3.2:
- Bug fix: Copy EPG process and Scheduler work at wrong time or doesn't work at all when the box has invalid date/time (1970) at boot and time update via DVB/NTP delays.
- Bug fix: Scheduled Copy EPG doesn't work when Periodic Copy EPG is activated.
- Bug fix: Buyukbang Panel icon on Plugin Browser is not shown on nonPLi based images.
- Bug fix: Cannot install ipk file on Dreambox OE2 Experimental Image with an warning error.

v1.3.1:
- Bug fix: Green screen while Copy EPG process in some images is fixed.

v1.3:
- Both OE 1.6 and OE 2.0 images are supported by this version. Tests are done with PLi 2.1 and 3.0 images.
- Bug fix: Scheduled operations not functioning in some images.

v1.2.1:
- Norwegian translation is added. Thanks to Olebrumm from kvasirdo.com !
- Italian translation is added. Thanks to Doctor Who from wlgforever.info !

v1.2:
- User interface is redesigned.
- "Scheduler" is added.
- "Startup to Standby" is added.
- Several performance and stabilization improvements are implemented.

 v1.1:
- All bugs reported for different devices and images are fixed.

v1.0:
- Initial version

Known Issues:
- Copy EPG does not work on Dreambox OE2 Experimental Images since old EPG structure is changed and now none of the EPG importer plugins cannot work on this image as discussed at http://www.dream-multimedia-tv.de/board/index.php?page=Thread&threadID=16743 and http://www.dream-multimedia-tv.de/board/index.php?page=Thread&threadID=16710&pageNo=1.


Copy EPG:
Copies EPG data from source channels to the same channels without EPG data on other satellites or packages. For example Turkish users currently use Buyukbang Panel to copy EPG to 50+ channels on Turksat 42E from 7E. 

You need to create a bouquet named EPG and insert source and destination channels in it to use this feature. Ordering should be as follows: SourceChannel, DestinationChannel1, SEPARATOR (note: anything can be typed as a separator), SourceChannel, DestinationChannel1, DestinationChannel2, DestinationChannel3, - , ... and so on. As you can see you need to start with a source channel, then you can define one or more destination channels for a source channel and you need to use a separator between mapping groups. 

Here are some important notes on  this functionality:

1- Buyukbang panel does EPG Copy process in only one step without generating, exporting, importing any XML file. Everything happens on RAM, this is what makes Buyukbang Panel so fast!.

2- This functionality can be scheduled to run at a specific time with "Scheduled EPG Copy" or run periodically between user defined intervals with with "Periodic EPG Copy". 

3- It's suggested to use a source channel with EPG data as the startup service. Buyukbang Panel has an option named "Startup copy delay" to adjust waiting time for receiving of EPG data on startup.

4- Buyukbang Panel automatically detects supported EPG import methods provided by the image being used and chooses the fastest method. PLi/Oudeis/CrossEPG patches are supported. If the image contains one of these patches, EPG copy process does not require any restart to import EPG and everything completed on the fly. But if there is no EPG patch provided, Buyukbang Panel generates a new epg.dat, asks user confirmation for a restart, after the restart EPG is loaded. Additionally Buyukbang Panel uses twisted thread if the image supports it. With twisted thread method, EPG copy process runs on a different CPU thread, so that there will be freezing on Enigma2 user interface freezing during the process. 

5- If you have any problem with EPG copy process on an image with PLi/Oudeis/CrossEPG patches, you can activate "Force CrossEPG patch usage" option which disables PLi/Oudeis support and forces CrossEPG patch usage. 

6- All settings can be changed on a user friendly interface. 

7- You can easily show and save all process details by using the log screen. Saved log file is generated as /tmp/buyukbangpanel.log .

Notes on EPG Bouquet: You can insert - markers while you are editing EPG bouquet with Enigma2 channel list by using menu button of remote controller. It you are using dbedit'te to edit EPG bouquet, just use "Insert marker" option from the right click menu while pointing on the  bouquet. You can use whatever you want  as a marker, there is no restriction for that. 

EPG Overlap Problem: Enigma2 imports EPG by using NID, SID ve TSID parameters. So EPG of the channels with the same NID, SID ve TSID parameters unfortunately overlaps. If you have this kind of problem in your EPG bouquet, there is a method to prevent the overlapping. You need to edit your channel list with DreamEdit and differentiate the parameters of the problematic channels. 

You can see how to use this method on the following screenshots. Select the channel from the channel list, right click, select "Show/Edit Details"option. Now you'll have a screen like the one on the second screenshot. Here, use different values as "Service ID" to differentiate channel parameters and click "Save" button. Now delete the old channel from your EPG bouquet and add the new one and that's all! Be sure that Buyukbang Panel reload your new EPG bouquet which depends on the "Read EPG bouquet" option. If you didn't change its default value, you need a restart to load new EPG bouquet.

Link EPG:
Links EPG data source channels to the same channels without EPG data on other satellites or packages. Link EPG does not replicate EPG data on RAM and just link it dynamically, which differs Link EPG from Copy EPG. There will be no RAM usage or epg.dat file creation, which is good in terms of system resources. 

Another advantage of this option is that Link EPG updates EPG changes of source channels in real time. So you always have the latest EPG! 

But there is a disadvantage, too: Setting this option as "ALL EPG Queries" causes enigma2 always try to record it from the source channel instead of the destination channel when you want to record the event selected in the single / multi EPG browsers. Setting this option as "Only Infobar and EPG Info" does not have this disadvantage, but it does not cover single / multi EPG browsers and EPG searches.

Buyukbang Panel uses "Only Infobar and EPG Info" option as default. Because this solves "Infobar EPG Flickering" problem. This problem occurs when EPG data on RAM and on the loaded epg.dat differs. You will not have such a problem with Buyukbang Panel!

Link EPG will be very useful for the images that have problems with Copy EPG. If you encounters such a situation, just disable Copy EPG and set Link EPG as "ALL EPG Queries". This option provides EPG linking of single/multi  EPG  lists of the target channels to the source channels in real time.

Filter EPG:
Filters out unwanted EPG broadcasts like "Current" and "Next". You can add/remove filtered EPG titles to "EPG titles" option by using the user interface. This user defined list is case insensitive. You can add different text to this list by using comma as seperator between entries.


Fix EPG Encoding:
Fixes EPG encoding problems by querying Kingofsat for selected language and adding missing entries to encoding.conf at startup once a day. Everything happens automatically on the background without any user intervention. All languages and encoding formats are supported.

EPG File Operations:
With this menu, you can delete, backup or restore epg.dat files containing EPG information. "Delete" operation is useful for cases when having problems with EPG data or if fresh EPG data creation is needed.  "Backup" and "Restore" operations are useful when you want to save current EPG data. Enigma 2 interface is restarted automatically after "Delete" and "Restore" operations.

Hide Zap Errors:
Hides SID/PAT zap errors displayed on the screen after switching to wrongly modified / broken channels. This is a integrated feature of PLi image and Buyukbang Panel provides this to the other images!

Startup to Standby:
Takes STB to standby on startup. Differs from statuptostandby plugin by providing an option to exclude enigma2 restarts.
 
Scheduler:
Performs scheduled restart, reboot, shutdown and standby operations. You can choose specific time and day of the week as the schedule.

