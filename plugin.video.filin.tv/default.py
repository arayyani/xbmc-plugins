#!/usr/bin/python
# Writer (c) 2012, MrStealth
# Rev. 1.0.0
# -*- coding: utf-8 -*-

#import urllib2, sys, os, time
import urllib, re
import xbmc, xbmcplugin,xbmcgui,xbmcaddon
import HTMLParser
import CommonFunctions

common = CommonFunctions
common.plugin = "Youfreetv.net"
common.dbg = False # Default (True)
common.dbglevel = 3 # Default

pluginhandle = int(sys.argv[1])
__addon__    = xbmcaddon.Addon(id='plugin.video.filin.tv')

URL         = 'http://www.filin.tv'

# TODO: find a better way of html decoding
#def format(text):
#    return re.sub(r'^(&.*;)$', '', text)

def unescape(entity, encoding):
  if encoding == 'utf-8':
    return HTMLParser.HTMLParser().unescape(entity).encode(encoding)
  elif encoding == 'cp1251':
    return entity.decode(encoding).encode('utf-8')

def get_url(string):
  return re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+.xml', string)[0]

def next(url):
  if url[-1] == 'v':
    return URL+'/page/2'
  else:
    return URL+'/page/' + str(int(url[-1])+1)


# (xbmc.getSkinDir() == "skin.quartz")

#def menu():
#    name="Categories"
#    item = xbmcgui.ListItem(name)
#    uri = sys.argv[0] + '?mode=CATEGORIES'
#    xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

#    name='Latest income'
#    item = xbmcgui.ListItem(name)
#    uri = sys.argv[0] + '?mode=RECENT'
#    xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

#    xbmcplugin.endOfDirectory(pluginhandle)

#def categories(url):
#    page = ''
#    result = common.fetchPage({"link": url})

#    if result["status"] == 200:
#        content = common.parseDOM(result["content"], "div", attrs = { "class":"mcont" })
#        categories = common.parseDOM(content, "option", ret="value")
#        descriptions = common.parseDOM(content, "option")

#        if len(categories):
#            for i, categorie in enumerate(categories):
#                uri = sys.argv[0] + '?mode=RECENT&url=' + URL + '/x.php?onlyjanr=' + categorie
#                title = unescape(descriptions[i], 'cp1251')
#                print uri

#                item = xbmcgui.ListItem(title)
#                xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

    xbmcplugin.endOfDirectory(pluginhandle, True)

def recent(url):
    page = ''
    result = common.fetchPage({"link": url})

    if result["status"] == 200:
        content = common.parseDOM(result["content"], "div", attrs = { "id":"dle-content" })
        mainf = common.parseDOM(content, "div", attrs = { "class":"mainf" })
        block = common.parseDOM(content, "div", attrs = { "class":"block_text" })

        descriptions = common.parseDOM(result["content"], "div", attrs = { "style":"display:inline;" })

        if len(mainf):
            for i, div in enumerate(mainf):
                href = common.parseDOM(div, "a", ret="href")[0]
                thumbnail = common.parseDOM(block[i], "img", ret = "src")[0]
                if thumbnail[0] == '/': thumbnail = URL+thumbnail

                # TODO: parse encoding from html meta tag
                title = unescape(common.parseDOM(div, "a")[0], 'cp1251')
                uri = sys.argv[0] + '?mode=SHOW&url=' + href + '&thumbnail=' + thumbnail

                item = xbmcgui.ListItem(title, thumbnailImage=thumbnail)
                item.setProperty( "Fanart_Image", thumbnail )

                item.setInfo( type='Video', infoLabels={'title': title, 'plot': unescape(descriptions[i], 'cp1251')})
                xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

    uri = sys.argv[0] + '?mode=NEXT&url=' + next(url)
    xbmcplugin.addDirectoryItem(pluginhandle, uri, xbmcgui.ListItem(">>"), True)
    xbmc.executebuiltin('Container.SetViewMode(52)')
    xbmcplugin.endOfDirectory(pluginhandle, True)

def show(url,thumbnail):
    result = common.fetchPage({"link": url})
    flashvars = common.parseDOM(result["content"], "embed", ret="flashvars")[0]
    url = get_url(flashvars)

    #TODO: parse <creator> tag and create groups
    #http://filin.tv/208950482a70e02fad0e82e9a7db82c2/play/srochnoeuvedomlenie.xml


    xml = common.fetchPage({"link": url})["content"]
    locations = common.parseDOM(xml, "location")
    titles = common.parseDOM(xml, "title")

    t = common.parseDOM(xml, "title")
    creators = common.parseDOM(xml, "creator")

    print type(creators)
    for i in range(0, len(creators)):
        print unescape(creators[i], 'utf-8')

#        uri = sys.argv[0] + '?mode=PLAY&url=%s'%locations[i]
#        item = xbmcgui.ListItem(unescape(titles[i], 'utf-8'), thumbnailImage=thumbnail)
#        xbmcplugin.addDirectoryItem(pluginhandle, uri, item)
#        item.setProperty('IsPlayable', 'true')

    for i in range(0, len(locations)):
        uri = sys.argv[0] + '?mode=PLAY&url=%s'%locations[i]
        item = xbmcgui.ListItem(unescape(titles[i], 'utf-8'), thumbnailImage=thumbnail)
        xbmcplugin.addDirectoryItem(pluginhandle, uri, item)
        item.setProperty('IsPlayable', 'true')
    xbmcplugin.endOfDirectory(pluginhandle, True)

def play(url):
    item = xbmcgui.ListItem(path = url)
    xbmc.Player().play(url)



#########################################################################

# INDEX or categories section
# return array of item urls
# def getList(url)

def menu():
    name="Categories"
    item = xbmcgui.ListItem(name)
    uri = sys.argv[0] + '?mode=CATEGORIES'
    xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

    name='Latest income'
    item = xbmcgui.ListItem(name)
    uri = sys.argv[0] + '?mode=RECENT'
    xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

    xbmcplugin.endOfDirectory(pluginhandle)

# url = ROOT URL
def getCategories(url):
    page = ''
    result = common.fetchPage({"link": url})

    if result["status"] == 200:
        content = common.parseDOM(result["content"], "div", attrs = { "class":"mcont" })
        categories = common.parseDOM(content, "option", ret="value")
        descriptions = common.parseDOM(content, "option")

        if len(categories):
            for i, categorie in enumerate(categories):
                uri = sys.argv[0] + '?mode=GET&url=' + URL + '/x.php?onlyjanr=' + categorie
                title = unescape(descriptions[i], 'cp1251')
                print uri

                item = xbmcgui.ListItem(title)
                xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

def getCategoryItems(url):
    result = common.fetchPage({"link": url})

    if result["status"] == 200:
        links = common.parseDOM(content, "a", ret="href")
        titles = common.parseDOM(content, "a") # should be unescape



# Item with multiple subitems
# return array of subitem urls
def getItems(url) # == recent()
    page = ''
    result = common.fetchPage({"link": url})

    if result["status"] == 200:
        content = common.parseDOM(result["content"], "div", attrs = { "id":"dle-content" })
        mainf = common.parseDOM(content, "div", attrs = { "class":"mainf" })
        block = common.parseDOM(content, "div", attrs = { "class":"block_text" })

        descriptions = common.parseDOM(result["content"], "div", attrs = { "style":"display:inline;" })

        if len(mainf):
            for i, div in enumerate(mainf):
                href = common.parseDOM(div, "a", ret="href")[0]
                thumbnail = common.parseDOM(block[i], "img", ret = "src")[0]
                if thumbnail[0] == '/': thumbnail = URL+thumbnail

                # TODO: parse encoding from html meta tag
                title = unescape(common.parseDOM(div, "a")[0], 'cp1251')
                uri = sys.argv[0] + '?mode=SHOW&url=' + href + '&thumbnail=' + thumbnail

                item = xbmcgui.ListItem(title, thumbnailImage=thumbnail)
                item.setProperty( "Fanart_Image", thumbnail )

                item.setInfo( type='Video', infoLabels={'title': title, 'plot': unescape(descriptions[i], 'cp1251')})
                xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

    uri = sys.argv[0] + '?mode=NEXT&url=' + next(url)
    xbmcplugin.addDirectoryItem(pluginhandle, uri, xbmcgui.ListItem(">>"), True)
    xbmc.executebuiltin('Container.SetViewMode(52)')
    xbmcplugin.endOfDirectory(pluginhandle, True)


# Show item description with thumbnail
# return playable subitem url
def showItem(url, thumbnail)

    result = common.fetchPage({"link": url})
    flashvars = common.parseDOM(result["content"], "embed", ret="flashvars")[0]
    url = get_url(flashvars)

    xml = common.fetchPage({"link": url})["content"]
    locations = common.parseDOM(xml, "location")
    titles = common.parseDOM(xml, "title")

    t = common.parseDOM(xml, "title")
    creators = common.parseDOM(xml, "creator")

    for i in range(0, len(locations)):
        uri = sys.argv[0] + '?mode=PLAY&url=%s'%locations[i]
        item = xbmcgui.ListItem(unescape(titles[i], 'utf-8'), thumbnailImage=thumbnail)
        xbmcplugin.addDirectoryItem(pluginhandle, uri, item)
        item.setProperty('IsPlayable', 'true')

    xbmcplugin.endOfDirectory(pluginhandle, True)

# Play subitem url
def playItem(url)
    item = xbmcgui.ListItem(path = url)
    xbmc.Player().play(url)

#########################################################################

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param

params = get_params()

# TODO: code refactoring
url=None
mode=None
channel=None
thumbnail=None

try:
    mode=params['mode'].upper()
except: pass

try:
    url=urllib.unquote_plus(params['url'])
except: pass

try:
    thumbnail=urllib.unquote_plus(params['thumbnail'])
except: pass

if mode == 'NEXT':
    recent(url)
elif mode == 'SHOW':
    show(url,thumbnail)
elif mode == 'PLAY':
    playItem(url) # play(url)
elif mode == 'CATEGORIES':
    getCategories(URL)
elif mode == 'RECENT':
    recent(URL)
elif mode == None:
    menu()
