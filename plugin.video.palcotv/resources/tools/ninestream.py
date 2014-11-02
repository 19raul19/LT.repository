# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV Regex de 9straem
# Version 0.2 (02.11.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re
import shutil
import zipfile
import time

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import re,urllib,urllib2,sys
import plugintools,ioncube

home = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv-wip/', ''))
tools = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv-wip/resources/tools', ''))
addons = xbmc.translatePath(os.path.join('special://home/addons/', ''))
resources = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv-wip/resources', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv-wip/art', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv-wip/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/playlists', ''))

icon = art + 'icon.png'
fanart = 'fanart.jpg'



# Función que guía el proceso de elaboración de la URL original
def ninestreams(params):
    plugintools.log("[PalcoTV-0.3.0].ninestreams "+repr(params))
    url_user = {}
    
    # Construimos diccionario...
    url = params.get("url")
    url_extracted = url.split(" ")
    for entry in url_extracted:
        if entry.startswith("rtmp"):
            entry = entry.replace("rtmp=", "")         
            url_user["rtmp"]=entry
        elif entry.startswith("playpath"):
            entry = entry.replace("playpath=", "")
            url_user["playpath"]=entry            
        elif entry.startswith("swfUrl"):
            entry = entry.replace("swfUrl=", "")
            url_user["swfurl"]=entry
        elif entry.startswith("pageUrl"):
            entry = entry.replace("pageUrl=", "")
            url_user["pageurl"]=entry          
        elif entry.startswith("token"):
            entry = entry.replace("token=", "")
            url_user["token"]=entry
        elif entry.startswith("referer"):
            entry = entry.replace("referer=", "")
            url_user["referer"]=entry

    plugintools.log("URL_user dict= "+repr(url_user))

    # Ejecutamos nuevo regex de Quequino...
    pageurl = url_user.get("pageurl")
    ref = url_user.get("referer")    
    nstr(url,ref,pageurl)
    

def nstr(url,ref,pageurl):
    p1 = re.compile(ur'channel=?\'?"?([^\'"\&,;]+)')
    p2 = re.compile(ur'width=?\'?"?([^\'"\&,;]+)')
    p3 = re.compile(ur'height=?\'?"?([^\'"\&,;]+)')
    f1=re.findall(p1, pageurl);f2=re.findall(p2, pageurl);f3=re.findall(p3, pageurl);#res=list(set(f));
    c=f1[0];w=f2[0];h=f3[0]
    url='http://www.9stream.com/embedplayer.php?width='+w+'&height='+h+'&channel='+c+'&autoplay=true';body='';#
    plugintools.log("url= "+url)
    plugintools.log("referer= "+ref)
    bodi=curl_frame(url,ref,body)
    print "\nURLXXX = "+url+"\nREFXXX = "+ref#+"\n"+bodi
    tkserv='';strmr='';plpath='';swf='';vala='';
    vals=ioncube.ioncube1(bodi)
    print "URL = "+url;print "REF = "+ref;
    tkserv=vals[0][1];strmr=vals[1][1].replace("\/","/");plpath=vals[2][1].replace(".flv","");swf=vals[3][1];
    ref=url;url=tkserv;bodi=curl_frame(url,ref,body);
    p='token":"([^"]+)';token=plugintools.find_single_match(bodi,p);#print token
    media_url = strmr+'/'+plpath+' swfUrl='+swf+' token='+token+' live=1 timeout=15 swfVfy=1 pageUrl='+ref
    plugintools.play_resolved_url(media_url)
    print media_url    

		
def curl_frame(url,ref,body):
	request_headers=[];
	request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
	request_headers.append(["Referer",ref])
	body,response_headers=plugintools.read_body_and_headers(url, headers=request_headers);
	return body
    
