import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys
import urllib2,urllib
import time
import downloader
import common as Common
import wipe
import zipfile
import hashlib

AddonTitle="[COLOR ghostwhite]Imperio Tuga[/COLOR] [COLOR lightsteelblue]Wizard[/COLOR]"
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
CHECKVERSION  =  os.path.join(USERDATA,'version.txt')

############################
###INSTALL BUILD############
############################

def INSTALL(name,url,description):

	#Check is the packages folder exists, if not create it.
	path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
	if not os.path.exists(path):
		os.makedirs(path)

	wipeme = 0

	if name == "ImperioTuga SLIM":
		wipeme = 1
		choice = xbmcgui.Dialog().yesno(AddonTitle, 'Imperiotuga was designed for low end machines like Firesticks.','Recomended: Single Core CPU | 1GB RAM or more','[I][COLOR lightsteelblue]Would you like to download this build now?[/I][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
		if choice == 0:
			sys.exit(1)

	if name == "ImperioTuga":
		wipeme = 1
		choice = xbmcgui.Dialog().yesno(AddonTitle, 'ImperioTugaSLIM was designed for high end machines like the Amazon Fire TV & Nvidia Shield.','Recomended: Quad Core CPU | 4GB RAM or more','[I][COLOR lightsteelblue]Would you like to download this build now?[/I][/COLOR]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
		if choice == 0:
			sys.exit(1)

	if name == "ImperioTuga ESPANHA #BREVEMENTE#":
		wipeme = 1
		choice = xbmcgui.Dialog().yesno(AddonTitle, 'ImperioTuga ESPANHA #BREVEMENTE# was designed for mid-level machines like MX8 & T8.','Recomended: Dual Core CPU | 2GB RAM or more','[I][COLOR lightsteelblue]Would you like to download this build now?[/I][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
		if choice == 0:
			sys.exit(1)

	if name == "ImperioTuga ITALIA #BREVEMENTE#":
		wipeme = 1
		choice = xbmcgui.Dialog().yesno(AddonTitle, 'ImperioTuga ITALIA #BREVEMENTE# was designed for mid-level machines like MX8 & T8.','Recomended: Dual Core CPU | 2GB RAM or more','[I][COLOR lightsteelblue]Would you like to download this build now?[/I][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
		if choice == 0:
			sys.exit(1)
			
			
	if wipeme == 1:
		wipe.WIPERESTORE()

	path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
	if not os.path.exists(path):
		os.makedirs(path)
	buildname = name
	dp = xbmcgui.DialogProgress()
	dp.create(AddonTitle,"","","Build: " + buildname)
	name = "build"
	lib=os.path.join(path, name+'.zip')
	
	try:
		os.remove(lib)
	except:
		pass
	
	downloader.download(url, lib, dp)
	addonfolder = xbmc.translatePath(os.path.join('special://','home'))
	time.sleep(2)
	dp.update(0,"","Extracting Zip Please Wait","")
	unzip(lib,addonfolder,dp)
	dialog = xbmcgui.Dialog()
	time.sleep(1)
	try:
		os.remove(lib)
	except:
		pass
	dialog.ok(AddonTitle, "To save changes you now need to force close Kodi, Press OK to force close Kodi")
	time.sleep(2)
	Common.killxbmc()
	
def INSTALLCOM(name,url,description):
	
	wipe.WIPERESTORE()
	#Check is the packages folder exists, if not create it.
	path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
	if not os.path.exists(path):
		os.makedirs(path)
	buildname = "[COLOR orangered]" + name + "[/COLOR]"
	dp = xbmcgui.DialogProgress()
	dp.create(AddonTitle,"","","Build: " + buildname)
	name = "build"
	lib=os.path.join(path, name+'.zip')
	
	try:
		os.remove(lib)
	except:
		pass
	
	downloader.download(url, lib, dp)
	addonfolder = xbmc.translatePath(os.path.join('special://','home'))
	time.sleep(2)
	dp.update(0,"","Extracting Build...","")
	unzip(lib,addonfolder,dp)
	dialog = xbmcgui.Dialog()
	time.sleep(1)
	try:
		os.remove(lib)
	except:
		pass
	dialog.ok(AddonTitle, "To save changes you now need to force close Kodi, Press OK to force close Kodi")
	time.sleep(2)
	Common.killxbmc()
	
def unzip(_in, _out, dp):
	__in = zipfile.ZipFile(_in,  'r')
	
	nofiles = float(len(__in.infolist()))
	count   = 0
	
	try:
		for item in __in.infolist():
			count += 1
			update = (count / nofiles) * 100
			
			if dp.iscanceled():
				dialog = xbmcgui.Dialog()
				dialog.ok(AddonTitle, 'Extraction was cancelled.')
				
				sys.exit()
				dp.close()
			
			try:
				dp.update(int(update))
				__in.extract(item, _out)
			
			except Exception, e:
				print str(e)

	except Exception, e:
		print str(e)
		return False
		
	return True