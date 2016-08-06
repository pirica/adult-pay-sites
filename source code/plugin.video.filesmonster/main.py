#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------
# filesmonster - KODI Plugin
# Addon for filesmonster.com
# http://github.com/spaniard1978/filesmonster
#------------------------------------------------------------



    
import sys
import urllib
import urllib2
import urlparse
import xbmcgui
import xbmcplugin
import re
import os
import xbmc
import xbmcaddon
import time
import datetime
import threading



		

#addon values for dialogs
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
addonid   = addon.getAddonInfo('id')

#Absolute path to icons
addonPath = xbmcaddon.Addon().getAddonInfo("path")
latest_icon = os.path.join(addonPath, 'resources', 'images', 'latest_folder_menu_main.png')
search_icon = os.path.join(addonPath, 'resources', 'images', 'search_folder_menu_main.png')
favorites_icon = os.path.join(addonPath, 'resources', 'images', 'favorites_folder_menu_main.png')
settings_icon = os.path.join(addonPath, 'resources', 'images', 'settings_folder_menu_main.png')
categories_icon = os.path.join(addonPath, 'resources', 'images', 'categories_folder_menu_main.png')
downloads_icon = os.path.join(addonPath, 'resources', 'images', 'my_downloads_folder_menu_main.png')
fanart_main = os.path.join(addonPath,  'resources', 'images','fanart_main.jpg')


#get language and change menus
my_addon = xbmcaddon.Addon()
language = my_addon.getSetting('language')

if language=="Español (España)":
	text_latest_videos='Úlimos vídeos'
	text_categories='Categorías'
	text_search_content="Buscar"
	text_my_favorites='Mis favoritos'
	text_my_downloads="Mis descargas"
	text_settings="Preferencias"
	text_login="acceso (login)"
	text_add_to_my_favorites="Añadir a favoritos en filesmoster"
	text_download_video="Descargar el vídeo"
	text_user="usuario"
	text_login_with_your="Accede con tu"
	text_filesmonster_acount="cuenta de filesmonster.com"
	text_not_logged="No se podido acceder con tu usuario y contraseña "
	text_reason="Causa: "
	text_file_downloaded_yesno="¿Quieres descargar este vídeo?"
	text_file_delete_yesno="¿Estás seguro de que quieres borrar este vídeo?"
	text_file_downloaded="El vídeo se está descargando en la ruta de descarga (puedes cambiarla en preferencias). Puedes controlar el proceso de descarga desde 'Mis descargas' en el menú principal"
	text_video_info="Información del vídeo"
	text_added_favorites="El vídeo se añadido a tus favoritos de filesmonster.com. Puedes verlo desde el menú principal"
	text_name_download="Se descargará con este nombre"
	text_cancel_download="¿Cancelar la descarga?"
	text_remove_record_download="Borrar este registro"
	text_remove_download="Borrar este vídeo"
	text_file_canceled="Para cancelar las descargas tienes que salir de Kodi y volver a entrar, entonces podrás borrar el archivo"
	text_file_deleted="Vídeo borrado de la carpeta de descargas"
	text_refresh_download="Actualizar datos de descargas"
	text_no_premium="Necesitas acceder con una cuenta premium activa de filesmonster.com para poder ver este vídeo, introduce tus datos en preferencias"
	text_file_exist="Un archivo con este nombre ya existe o se está descargando en tu carpeta de descargas"
	
else:
	text_latest_videos='Latest videos'
	text_categories='Categories'
	text_search_content="Search"
	text_my_favorites='My favorites'
	text_my_downloads="My Downloads"
	text_settings="Settings"
	text_login="login"
	text_add_to_my_favorites="Add to my filesmoster favorites"
	text_download_video="Download video"
	text_user="user"
	text_login_with_your="Login with your"
	text_filesmonster_acount="filesmonster.com acount"
	text_not_logged="Not Logged with your useranme and password "
	text_reason="Reason: "
	text_file_downloaded_yesno="Do you want to download this video?"
	text_file_delete_yesno="Do you really want to delete this video?"
	text_file_downloaded="Video is being downloading in the download path (you can change it in your settings). You can control the download process from 'My downloads' in the main menu"
	text_video_info="Video info"
	text_added_favorites="Video added to your favorites in filesmonter.com. Watch it from the main menu"
	text_name_download="Filename for downloaded video"
	text_cancel_download="Cancel download?"
	text_remove_record_download="Remove this record"
	text_remove_download="Delete this video"
	text_file_canceled="To cancel downloads you must exit Kodi and enter again. Then you can delete it without problems"
	text_file_deleted="Video deleted from download folder"
	text_refresh_download="Refresh download data"
	text_no_premium="You need to use an active premium account of filesmonster.com to watch this video, add it in settings"
	text_file_exist="A file with the same filename already exists in your download folder or it's downloading"


#Get active value
my_addon = xbmcaddon.Addon()
username = my_addon.getSetting('username')
password = my_addon.getSetting('password')
if (username==''):my_addon.setSetting('active', "not active")
active = my_addon.getSetting('active')
if (active=='active'):
	status_login=text_settings+" | [COLOR brown]"+text_user+": "+username+"[/COLOR]"
	my_addon.setSetting('premium', "xxx")
if (active!='active'): 
	video_value0=(text_video_info, ' XBMC.Action(Info)' )
	video_value=(text_login_with_your,  ' XBMC.Action(Info)')
	video_value2=(text_filesmonster_acount, ' XBMC.Action(Info)')
	status_login=text_settings+" | [COLOR brown] "+text_login+"[/COLOR]"
	my_addon.setSetting('premium', "Not logged")


#set default downloadpath int settings.xml file
download_path = my_addon.getSetting('download_path')
__addon__       = xbmcaddon.Addon(id='plugin.video.filesmonster')
__addondir__    = xbmc.translatePath( __addon__.getAddonInfo('profile') ) 
if (download_path==''): my_addon.setSetting('download_path', __addondir__ +"download/")





def open_settings():
	#xbmc.executebuiltin('Addon.OpenSettings(plugin.video.filesmonster)')
	xbmcaddon.Addon().openSettings()
	makelogin()
	return
	


	
def makelogin():
	username = addon.getSetting('username')
	password = addon.getSetting('password')
	xbmc.executebuiltin("ActivateWindow(busydialog)")
	#test if login is correct (if it's not remove the value in settings)
	post2 = urllib.urlencode({ 'username':  username,'password': password }  )
	login_url="http://filesmonster.com/api/public/login"
	request = urllib2.Request(login_url, post2)
	response = urllib2.urlopen(request)
	data=response.read()
	partes1=data.split('"')
	status=partes1[3]
	if status!='success': 
		reason=partes1[7]
		xbmcgui.Dialog().ok(addonname, text_not_logged,text_reason+reason)
		addon.setSetting('active', reason)
		xbmc.executebuiltin("Dialog.Close(busydialog)")
		xbmc.executebuiltin('Container.Refresh')
	if status=='success': 
		addon.setSetting('active', "active")
		xbmc.executebuiltin("Dialog.Close(busydialog)")
		xbmc.executebuiltin('Container.Refresh')
	return


	
#dowload progress
def progress(count, blockSize, totalSize):
	percent = int(count*blockSize*100/totalSize)
	if percent<0:percent=''
	downloaded=str(((count*blockSize)*0.0009765625)*0.001)
	total_size=round((totalSize*0.0009765625)*0.001,3)
	totalmb=str(total_size)

	directory=download_path
	file_txt=directory+"/"+new_filename+".txt"
	f=open(file_txt, "a+")
	if percent<101:f.write(str(percent)+"% | "+str(downloaded)+"Mb/"+str(totalmb)+"Mb | \n")
	if percent>=101:f.write("Error \n")
	f.close()
	return






base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')




def build_url(query):
    return base_url + '?' + urllib.urlencode(query)
    
    
   
	

    

setting_value=(text_settings, 'Addon.OpenSettings(plugin.video.filesmonster)')

mode = args.get('mode', None)


 
def refresh():
	if mode[0]=='my_downloads':xbmc.executebuiltin('Container.Refresh')

def carga():
	directory=download_path
	if not os.path.exists(directory):os.makedirs(directory)
	records=os.listdir(directory)
	for record in records:
		extension=".txt"
		if extension in record:
			f=open(directory+record, 'r')
			data = f.readlines()
			f.close()
			last='downloading...'
			last=data[len(data)-1]
			file_name=record.replace(".txt" , "")
			url2 = build_url({'mode':'cancel_download', 'foldername': file_name})
			cancel_download=(text_cancel_download, 'XBMC.RunPlugin('+url2+')')
			url2 = build_url({'mode':'remove_download', 'foldername': file_name})
			remove_download=(text_remove_download, 'XBMC.RunPlugin('+url2+')')  
			url2 = build_url({'mode':'refresh_download', 'foldername': file_name})
			refresh_download=(text_refresh_download, 'XBMC.RunPlugin('+url2+')') 
			info_show=(text_video_info, ' XBMC.Action(Info)' )
			url = download_path+file_name
			li = xbmcgui.ListItem("[COLOR brown]"+file_name+"[/COLOR]  "+last, iconImage=downloads_icon)
			li.setArt({'fanart':fanart_main})
			info = {'title': file_name, 'plot':last}
			li.setInfo('video', info)
			li.setProperty('IsPlayable', 'true')
			li.addContextMenuItems([cancel_download, remove_download,refresh_download, info_show] ,replaceItems=True)
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
	threading.Timer(3, refresh).start()

   

   

    
if mode is None:
 
	
    url = build_url({'mode': 'folder', 'foldername': 'latest'})
    li = xbmcgui.ListItem(text_latest_videos, iconImage=latest_icon)
    li.setArt({'fanart':fanart_main,})
    url2 = build_url({'mode':'settings', 'foldername': 'settings'})
    settings=(status_login, 'XBMC.RunPlugin('+url2+')')  
    li.addContextMenuItems([settings] ,replaceItems=True)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'mode': 'folder', 'foldername': 'categories'})
    li = xbmcgui.ListItem(text_categories, iconImage=categories_icon)
    li.setArt({'fanart':fanart_main,})
    url2 = build_url({'mode':'settings', 'foldername': 'settings'})
    settings=(status_login, 'XBMC.RunPlugin('+url2+')')  
    li.addContextMenuItems([settings] ,replaceItems=True)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'mode': 'folder', 'foldername': 'search'})
    li = xbmcgui.ListItem(text_search_content, iconImage=search_icon)
    li.setArt({'fanart':fanart_main,})
    url2 = build_url({'mode':'settings', 'foldername': 'settings'})
    settings=(status_login, 'XBMC.RunPlugin('+url2+')')  
    li.addContextMenuItems([settings] ,replaceItems=True)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    
    url = build_url({'mode': 'folder', 'foldername': 'favorites'})
    li = xbmcgui.ListItem(text_my_favorites, iconImage=favorites_icon)
    li.setArt({'fanart':fanart_main,})
    url2 = build_url({'mode':'settings', 'foldername': 'settings'})
    settings=(status_login, 'XBMC.RunPlugin('+url2+')')  
    li.addContextMenuItems([settings] ,replaceItems=True)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
   
    url = build_url({'mode': 'my_downloads', 'foldername': 'my_downloads'})
    li = xbmcgui.ListItem(text_my_downloads, iconImage=downloads_icon)
    li.setArt({'fanart':fanart_main,})
    url2 = build_url({'mode':'settings', 'foldername': 'settings'})
    settings=(status_login, 'XBMC.RunPlugin('+url2+')')  
    li.addContextMenuItems([settings] ,replaceItems=True)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
   
    url = build_url({'mode':'settings', 'foldername': 'settings'})
    li = xbmcgui.ListItem(status_login, iconImage=settings_icon)
    li.setArt({'fanart':fanart_main,})
    url2 = build_url({'mode':'settings', 'foldername': 'settings'})
    settings=(status_login, 'XBMC.RunPlugin('+url2+')')  
    li.addContextMenuItems([settings] ,replaceItems=True)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False) 
    
    

       

                          
    	
	                           
elif mode[0] == 'settings': 
	open_settings()	


        

elif mode[0] == 'folder':
    word=''
    foldername = args['foldername'][0]
    if foldername=='search':
    	keyboard = xbmc.Keyboard("", text_search_content, False)
    	keyboard.doModal()
    	if keyboard.isConfirmed() and keyboard.getText() != "":
    		word=keyboard.getText()   
    title="Tears of Steal "+word
    
    #if it's active user or not choosse what to show
    active = my_addon.getSetting('active')
    if active=='active': 
    	url = 'http://www.libde265.org/hevc-bitstreams/tos-1720x720-cfg01.mkv'
    if (active!='active'): url = build_url({'mode': 'no_premium', 'foldername': 'no_premium'})
    
    
    video=url
    li = xbmcgui.ListItem(title, iconImage='DefaultVideo.png')
    info = {'genre': 'Porn','year': 1979,'title': title,  'plot':'argumento con ñ'+url, 'duration':9999 }
    li.setInfo('video', info)
    li.setArt({'fanart':fanart_main, 'thumb':fanart_main , 'poster':fanart_main , 'banner':fanart_main})
    li.addStreamInfo('audio', {'codec': 'dts', 'language': 'en', 'channels': 2})
    li.addStreamInfo('video', {'codec': 'xvid', 'aspect': 1.78,'width': 1280,'height': 720, 'duration':9999,})
    
    url2 = build_url({'mode':'settings', 'foldername': 'settings'})
    settings=(status_login, 'XBMC.RunPlugin('+url2+')')  
    
    if (active=='active'):
		video_value0=(text_video_info, ' XBMC.Action(Info)' )
		url2 = build_url({'mode':'favorites', 'foldername': video})
		video_value=(text_add_to_my_favorites, 'XBMC.RunPlugin('+url2+')' )
		url2 = build_url({'mode':'download', 'foldername': video})
		video_value2=(text_download_video, 'XBMC.RunPlugin('+url2+')')

    li.addContextMenuItems([video_value0, video_value, video_value2, settings ] ,replaceItems=True)
    

    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False) 
    


	

elif mode[0]=='my_downloads':
	carga()
			


		


elif mode[0]=='remove_download':
	video = args['foldername'][0]
	
	yesno =xbmcgui.Dialog().yesno(addonname, text_file_delete_yesno)
	if yesno==1:
		if os.path.exists(download_path+video): os.remove(download_path+video)
		if os.path.exists(download_path+video+".txt"):os.remove(download_path+video+".txt")
		xbmcgui.Dialog().ok(addonname, text_file_deleted)
		xbmc.executebuiltin('Container.Refresh')



elif mode[0]=='cancel_download':
	xbmcgui.Dialog().ok(addonname, text_file_canceled)
	xbmc.executebuiltin('Container.Refresh')



elif mode[0]=='refresh_download':
	xbmc.executebuiltin('Container.Refresh')






elif mode[0]=='download':
	addonPath = xbmcaddon.Addon().getAddonInfo("path")
	#test if is dowloaded or download yet
	directory=download_path
	yesno =xbmcgui.Dialog().yesno(addonname, text_file_downloaded_yesno)
	if yesno==1:
		video = args['foldername'][0]
		filename=os.path.basename(video)
		keyboard = xbmc.Keyboard(filename, text_name_download, False)
		keyboard.doModal()
		if keyboard.isConfirmed() and keyboard.getText() != "":
			new_filename=keyboard.getText()
			if os.path.isfile(directory+new_filename) :
				xbmcgui.Dialog().ok(addonname, text_file_exist)
			else:
				xbmcgui.Dialog().ok(addonname, text_file_downloaded)
				if not os.path.exists(directory):os.makedirs(directory)
				directory=download_path
				file_txt=directory+"/"+new_filename+".txt"
				f=open(file_txt, "w+")
				f.write("starting...\n")
				f.close()
				urllib.urlretrieve(video, directory+new_filename, reporthook=progress)









elif mode[0]=='favorites':
	video = args['foldername'][0]
	xbmcgui.Dialog().ok(addonname, text_added_favorites)

	           
	           
elif mode[0]=='no_premium':
	xbmcgui.Dialog().ok(addonname, text_no_premium)


xbmcplugin.endOfDirectory(addon_handle)

	