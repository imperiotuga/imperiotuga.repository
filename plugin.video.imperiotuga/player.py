# -*- coding: utf-8 -*-

"""
Copyright (C) 2015

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>
############################################################
Desenvolvido por Discave para imperiotuga TV
"""

import urllib, urllib2, sys, re, os, unicodedata
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import xbmcvfs,socket,urlparse,time,threading,HTMLParser

plugin_handle = int(sys.argv[1])

mysettings = xbmcaddon.Addon(id = 'plugin.video.imperiotuga')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
artfolder = (home + '/resources/img/')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
#############################
f_music = xbmc.translatePath(os.path.join(artfolder, 'music.jpg'))
f_sport = xbmc.translatePath(os.path.join(artfolder, 'sport.jpg'))
f_beach = xbmc.translatePath(os.path.join(artfolder, 'beach.jpg'))
f_child = xbmc.translatePath(os.path.join(artfolder, 'child.jpg'))
f_movie = xbmc.translatePath(os.path.join(artfolder, 'movie.jpg'))
f_nasa = xbmc.translatePath(os.path.join(artfolder, 'nasa.jpg'))
f_news = xbmc.translatePath(os.path.join(artfolder, 'news.jpg'))
f_pt = xbmc.translatePath(os.path.join(artfolder, 'pt.jpg'))
f_ru = xbmc.translatePath(os.path.join(artfolder, 'radio.jpg'))
f_tvshow = xbmc.translatePath(os.path.join(artfolder, 'tvshow.jpg'))
f_uk = xbmc.translatePath(os.path.join(artfolder, 'uk.jpg'))
##############################3
i_music = xbmc.translatePath(os.path.join(artfolder, 'music.png'))
i_sport = xbmc.translatePath(os.path.join(artfolder, 'sport.png'))
i_beach = xbmc.translatePath(os.path.join(artfolder, 'beach.png'))
i_child = xbmc.translatePath(os.path.join(artfolder, 'EU.png'))
i_movie = xbmc.translatePath(os.path.join(artfolder, 'movie.png'))
i_nasa = xbmc.translatePath(os.path.join(artfolder, 'nasa.png'))
i_news = xbmc.translatePath(os.path.join(artfolder, 'news.png'))
i_pt = xbmc.translatePath(os.path.join(artfolder, 'pt.png'))
i_ru = xbmc.translatePath(os.path.join(artfolder, 'radio.png'))
i_tvshow = xbmc.translatePath(os.path.join(artfolder, 'tvshow.png'))
i_uk = xbmc.translatePath(os.path.join(artfolder, 'uk.png'))

music_m3u = mysettings.getSetting('music_m3u')
online_m3u = mysettings.getSetting('online_m3u')
filmes_m3u = mysettings.getSetting('filmes_m3u')
infantil_m3u = mysettings.getSetting('infantil_m3u')
nasa_m3u = mysettings.getSetting('nasa_m3u')
noticias_m3u = mysettings.getSetting('noticias_m3u')
pt_m3u = mysettings.getSetting('pt_m3u')
ru_m3u = mysettings.getSetting('ru_m3u')
desporto_m3u = mysettings.getSetting('desporto_m3u')
series_m3u = mysettings.getSetting('series_m3u')
uk_m3u = mysettings.getSetting('uk_m3u')
praias_m3u = mysettings.getSetting('praias_m3u')
pessoal_m3u = mysettings.getSetting('pessoal_m3u')
pessoal_local_m3u = mysettings.getSetting('pessoal_local_m3u')
online_xml = mysettings.getSetting('online_xml')
local_xml = mysettings.getSetting('local_xml')
####################################
log_m3u = mysettings.getSetting('log_m3u')

xml_regex = '<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>'
m3u_thumb_regex = 'tvg-logo=[\'"](.*?)[\'"]'
m3u_regex = '#(.+?),(.+)\s*(.+)\s*'

u_tube = 'http://www.youtube.com'

def removeAccents(s):
	return ''.join((c for c in unicodedata.normalize('NFD', s.decode('utf-8')) if unicodedata.category(c) != 'Mn'))
					
def read_file(file):
    try:
        f = open(file, 'r')
        content = f.read()
        f.close()
        return content
    except:
        pass

def make_request(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
		response = urllib2.urlopen(req)	  
		link = response.read()
		response.close()  
		return link
	except urllib2.URLError, e:
		print 'We failed to open "%s".' % url
		if hasattr(e, 'code'):
			print 'We failed with error code - %s.' % e.code	
		if hasattr(e, 'reason'):
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason
			
def main():
	if len(log_m3u) > 0:	
		add_dir('[COLOR red]Versao: 1.0[/COLOR]', u_tube, 111, icon, fanart)
	if len(music_m3u) > 0:	
		add_dir('[COLOR blue][B] MUSICA [/B][/COLOR]', u_tube, 2, i_music, f_music)
	if len(filmes_m3u) > 0:	
		add_dir('[COLOR blue][B] FILMES [/B][/COLOR]', u_tube, 3, i_movie, f_movie)
	if len(infantil_m3u) > 0:	
		add_dir('[COLOR red][B] EURO MIX [/B][/COLOR]', u_tube, 4, i_child, f_child)
	if len(nasa_m3u) > 0:	
		add_dir('[COLOR green][B] NASA [/B][/COLOR]', u_tube, 5, i_nasa, f_nasa)
	if len(noticias_m3u) > 0:	
		add_dir('[COLOR yellow][B] NOTICIAS [/B][/COLOR]', u_tube, 6, i_news, f_news)
	if len(pt_m3u) > 0:	
		add_dir('[COLOR yellow][B] PORTUGAL [/B][/COLOR]', u_tube, 7, i_pt, f_pt)
	if len(ru_m3u) > 0:	
		add_dir('[COLOR yellow][B] RADIOS [/B][/COLOR]', u_tube, 8, i_ru, f_ru)
	if len(desporto_m3u) > 0:	
		add_dir('[COLOR lawngreen][B] DESPORTO [/B][/COLOR]', u_tube, 9, i_sport, f_sport)
	if len(series_m3u) > 0:	
		add_dir('[COLOR red][B] SERIES [/B][/COLOR]', u_tube, 10, i_tvshow, f_tvshow)
	if len(uk_m3u) > 0:	
		add_dir('[COLOR red][B] INGLATERRA[/B][/COLOR]', u_tube, 11, i_uk, f_uk)
	if len(praias_m3u) > 0:	
		add_dir('[COLOR gray][B] MUNDO e PRAIAS [/B][/COLOR]', u_tube, 12, i_beach, f_beach)
	if len(pessoal_m3u) > 0:	
		add_dir('[COLOR gray][B] MINHA M3U ONLINE [/B][/COLOR]', u_tube, 13, icon, fanart)
	if len(pessoal_local_m3u) > 0:	
		add_dir('[COLOR gray][B] MINHA M3U LOCAL [/B][/COLOR]', u_tube, 14, icon, fanart)
	if len(online_xml) > 0:	
		add_dir('[COLOR orangered][B] LISTA MAGELLAN [/B][/COLOR]', u_tube, 15, icon, fanart)
	if len(local_xml) > 0:	
		add_dir('[COLOR gray][B] MINHA XML LOCAL [/B][/COLOR]', u_tube, 16, icon, fanart)	
	if (len(online_m3u) < 1 and len(filmes_m3u) < 1 and len(infantil_m3u) < 1 and len(nasa_m3u) < 1 and len(noticias_m3u) < 1 and len(pt_m3u) < 1 and len(ru_m3u) < 1 and len(desporto_m3u) < 1 and len(series_m3u) < 1 and len(uk_m3u) < 1 and len(praias_m3u) < 1 and len(pessoal_m3u) < 1 and len(pessoal_local_m3u) < 1 and len(online_xml) < 1 and len(local_xml) < 1 and len(log_m3u) < 1 ):
		mysettings.openSettings()
		xbmc.executebuiltin("Container.Refresh")		

def search(): 	
	try:
		keyb = xbmc.Keyboard('', 'Procurar por:')
		keyb.doModal()
		if (keyb.isConfirmed()):
			searchText = urllib.quote_plus(keyb.getText()).replace('+', ' ')
		if len(online_m3u) > 0:		
			content = make_request(online_m3u)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
		if len(filmes_m3u) > 0:		
			content = make_request(filmes_m3u)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
		if len(infantil_m3u) > 0:		
			content = make_request(infantil_m3u)
			match = re.compile(m3u_regex).findall(content)		
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		if len(nasa_m3u) > 0:		
			content = make_request(nasa_m3u)
			match = re.compile(m3u_regex).findall(content)		
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		if len(noticias_m3u) > 0:		
			content = make_request(noticias_m3u)
			match = re.compile(m3u_regex).findall(content)		
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		if len(pt_m3u) > 0:		
			content = make_request(pt_m3u)
			match = re.compile(m3u_regex).findall(content)		
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		if len(ru_m3u) > 0:		
			content = make_request(ru_m3u)
			match = re.compile(m3u_regex).findall(content)		
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		if len(desporto_m3u) > 0:		
			content = make_request(desporto_m3u)
			match = re.compile(m3u_regex).findall(content)		
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		if len(series_m3u) > 0:		
			content = make_request(series_m3u)
			match = re.compile(m3u_regex).findall(content)		
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		if len(uk_m3u) > 0:		
			content = make_request(uk_m3u)
			match = re.compile(m3u_regex).findall(content)		
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		if len(praias_m3u) > 0:		
			content = make_request(praias_m3u)
			match = re.compile(m3u_regex).findall(content)		
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		if len(pessoal_m3u) > 0:		
			content = make_request(pessoal_m3u)
			match = re.compile(m3u_regex).findall(content)		
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		if len(pessoal_local_m3u) > 0:		
			content = read_file(pessoal_local_m3u)
			match = re.compile(m3u_regex).findall(content)		
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		if len(online_xml) > 0:					
			content = make_request(online_xml)
			match = re.compile(xml_regex).findall(content)	
			for name, url, thumb in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					xml_playlist(name, url, thumb)	
		if len(local_xml) > 0:		
			content = read_file(local_xml)
			match = re.compile(xml_regex).findall(content)		
			for name, url, thumb in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					xml_playlist(name, url, thumb)					
	except:
		pass
	
		
def m3u_log():		
	content = make_request(log_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_online():		
	content = make_request(online_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_filmes():		
	content = make_request(filmes_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_infantil():
	content = make_request(infantil_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:	
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_nasa():
	content = make_request(nasa_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:	

		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_noticias():
	content = make_request(noticias_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:	
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_pt():
	content = make_request(pt_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:	
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_ru():
	content = make_request(ru_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:	
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_desporto():
	content = make_request(desporto_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:	
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_series():
	content = make_request(series_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:	
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_uk():
	content = make_request(uk_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:	
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_praias():
	content = make_request(praias_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:	
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_pessoal():
	content = make_request(pessoal_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:	
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def m3u_pessoal_local():
	content = read_file(pessoal_local_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:	
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass

def xml_online():			
	content = make_request(online_xml)
	match = re.compile(xml_regex).findall(content)
	for name, url, thumb in match:
		try:
			xml_playlist(name, url, thumb)
		except:
			pass
			
def xml_local():		
	content = read_file(local_xml)
	match = re.compile(xml_regex).findall(content)
	for name, url, thumb in match:	
		try:
			xml_playlist(name, url, thumb)
		except:
			pass
			
def m3u_playlist(name, url, thumb):	
	name = re.sub('\s+', ' ', name).strip()			
	url = url.replace('"', ' ').replace('&amp;', '&').strip()
	if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
		if 'tvg-logo' in thumb:
			thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')			
			add_dir(name, url, '', thumb, thumb)			
		else:	
			add_dir(name, url, '', icon, fanart)
	else:
		if 'youtube.com/watch?v=' in url:
			url = 'plugin://plugin.video.youtube/play/?video_id=%s' % (url.split('=')[-1])
		elif 'dailymotion.com/video/' in url:
			url = url.split('/')[-1].split('_')[0]
			url = 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=%s' % url	
		else:			
			url = url
		if 'tvg-logo' in thumb:				
			thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
			add_link(name, url, 1, thumb, thumb)			
		else:				
			add_link(name, url, 1, icon, fanart)

def xml_playlist(name, url, thumb):
	name = re.sub('\s+', ' ', name).strip()			
	url = url.replace('"', ' ').replace('&amp;', '&').strip()
	if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
		if len(thumb) > 0:	
			add_dir(name, url, '', thumb, thumb)			
		else:	
			add_dir(name, url, '', icon, fanart)
	else:
		if 'youtube.com/watch?v=' in url:
			url = 'plugin://plugin.video.youtube/play/?video_id=%s' % (url.split('=')[-1])
		elif 'dailymotion.com/video/' in url:
			url = url.split('/')[-1].split('_')[0]
			url = 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=%s' % url	
		else:			
			url = url
		if len(thumb) > 0:		
			add_link(name, url, 1, thumb, thumb)			
		else:			
			add_link(name, url, 1, icon, fanart)			
					
def play_video(url):
	media_url = url
	item = xbmcgui.ListItem(name, path = media_url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	return
			
def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring)>= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?', '')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0]] = splitparams[1]
	return param

def add_dir(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
		u = 'plugin://plugin.video.youtube/%s/%s/' % (url.split( '/' )[-2], url.split( '/' )[-1])
		ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
		return ok		
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
	return ok

def add_link(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)	
	liz = xbmcgui.ListItem(name, iconImage = "DefaultVideo.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	liz.setProperty('IsPlayable', 'true') 
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz)  
		
params = get_params()
url = None
name = None
mode = None
iconimage = None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode = int(params["mode"])
except:
	pass
try:
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass  

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)
print "iconimage: " + str(iconimage)		

if mode == None or url == None or len(url) < 1:
	main()


elif mode == 1:
	play_video(url)

elif mode == 111:
	m3u_log()
elif mode == 2:
	m3u_online()
	
elif mode == 3:
	m3u_filmes()
	
elif mode == 4:
	m3u_infantil()
	
elif mode == 5:
	m3u_nasa()
	
elif mode == 6:
	m3u_noticias()
	
elif mode == 7:
	m3u_pt()
	
elif mode == 8:
	m3u_ru()
	
elif mode == 9:
	m3u_desporto()
	
elif mode == 10:
	m3u_series()
	
elif mode == 11:
	m3u_uk()
	
elif mode == 12:
	m3u_praias()
	
elif mode == 13:
	m3u_pessoal()
	
elif mode == 14:
	m3u_pessoal_local()
	
elif mode == 15:
	xml_online()
	
elif mode == 16:
	xml_local()

elif mode == 99:
	search()
	
xbmcplugin.endOfDirectory(plugin_handle)