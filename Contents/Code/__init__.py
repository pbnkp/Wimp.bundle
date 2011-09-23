import urllib2, httplib, re

VIDEO_PREFIX = "/video/wimp"

NAME = L('Title')

ART  = 'art-default.jpg'
ICON = 'icon-default.png'

WIMP_URL = 'http://wimp.com'
####################################################################################################

def Start():

    Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, NAME, ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    
    ObjectContainer.title1 = NAME
    ObjectContainer.view_group = "List"
    ObjectContainer.art = R(ART)
    DirectoryObject.thumb = R(ICON)
    VideoItem.thumb = R(ICON)
    
    HTTP.CacheTime = CACHE_1HOUR

 

def VideoMainMenu():

    oc = ObjectContainer(view_group="InfoList")
    #oc.add(DirectoryObject(key=Callback(TodaysVideos, title="Today's Videos"), title="Today's Videos", summary="Videos uploaded today on Wimp.com"))
    oc.add(DirectoryObject(key=Callback(NewestVideos, title="Newest Videos"), title="Newest Videos", summary="Most Recent Videos uploaded on Wimp.com"))
    oc.add(DirectoryObject(key=Callback(OlderVideos, title="Older Videos"), title="Older Videos", summary="Videos previously uploaded on Wimp.com"))
    oc.add(VideoClipObject(key=Callback(RandomUrl), title="Random Video", summary="Play a random Wimp.com video", thumb=R(ICON)))

    return oc

def NewestVideos(title):
    
    oc = ObjectContainer(title1=title, view_group="InfoList")
    data = HTML.ElementFromURL(WIMP_URL)
    
    for video in data.xpath('//span[@class="video_date"]'):
        #Log(video.text)
        theDate = Datetime.ParseDate(video.text)
        delta = Datetime.Now() - theDate
        if delta.days <= 1:
            title = video.xpath('./following-sibling::a')[0].text
            #Log(title)
            url = video.xpath('./following-sibling::a')[0].get('href')
            #Log(url)
            oc.add(VideoClipObject(url=(WIMP_URL + url), title=title, thumb=R(ICON)))
        else:
            pass
    
    return oc  

def OlderVideos(title):
    
    oc = ObjectContainer(title1=title, view_group="InfoList")
    data = HTML.ElementFromURL(WIMP_URL)
    
    for video in data.xpath('//span[@class="video_date"]'):
        #Log(video.text)
        theDate = Datetime.ParseDate(video.text)
        delta = Datetime.Now() - theDate
        if delta.days > 1:
            title = video.xpath('./following-sibling::a')[0].text
            #Log(title)
            url = video.xpath('./following-sibling::a')[0].get('href')
            #Log(url)
            oc.add(VideoClipObject(url=(WIMP_URL + url), title=title, thumb=R(ICON)))
        else:
            pass
    
    return oc

@indirect
def RandomUrl():
    oc = ObjectContainer()
    
    url = WIMP_URL + '/random/'
    request = urllib2.Request(url)
    opener = urllib2.build_opener(SmartRedirectHandler)
    f = opener.open(request)
    if f.status == 301 or f.status == 302:
        Log(f.url)
        #URLService.MediaObjectsForURL(f.url)
        #return Redirect(f.url)
        oc.add(VideoClipObject(url=f.url))
    
    #return URLService.MediaObjectsForURL(url)
    #return Redirect(url)
    else:
        oc.add(VideoClipObject(url=url))
    
    return oc

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):     
  def http_error_301(self, req, fp, code, msg, headers):
    result = urllib2.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers)              
    result.status = code
    return result                                       

  def http_error_302(self, req, fp, code, msg, headers):   
    result = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)              
    result.status = code                                
    return result