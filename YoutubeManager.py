
# youtube-dl --get-url https://www.youtube.com/watch?v=d-GQq792pWI

import yt_dlp as youtube
import json

ydl_opts = {'quiet': True}
ydl = youtube.YoutubeDL(ydl_opts)


qualities = ['144', '240', '360','480','720','1080','2160']
thumbResolution = ['640x480', '1280x720', '480x360', '1920x1080', '336x188']


def getVideoDetails(url = ''):

    with ydl:
        info_dict = ydl.extract_info(url, download = False)

        videoDetail = VideoDetail()
        videoDetail.title = info_dict.get('title', '')
        videoDetail.likes = info_dict.get('like_count', 0)
        videoDetail.dislikes = info_dict.get('dislike_count', 0)
        videoDetail.thumbnail = info_dict.get('thumbnail', '')
        videoDetail.duration = info_dict.get('duration', 0)
        videoDetail.youtubeUrl = url
        videoDetail.uploadAt = info_dict.get('upload_date', '')

        # getting video download urls
        formats = info_dict.get('formats', [])
        
        for format in formats:
            videoFormat = VideoFormat()

            # extracting details
            videoFormat.url = format.get('url', '')
            videoFormat.quality = format.get('format_note', '')
            videoFormat.format = format.get('ext', '')
            videoFormat.size = format.get('filesize', 0)

            # adding download and filtering biased on qualities
            for quality in qualities:
                if videoFormat.quality.find(quality) != -1 and videoFormat.size != 0 :
                    videoDetail.downloads.append(videoFormat)
                    break
            

        print(json.dumps(videoDetail.toDict()))


def getPlaylist(url = ''):
    with ydl:
        info_dict = ydl.extract_info(url, download=False)

        playlist = Playlist()
        playlist.title = info_dict.get('title', '')

        for item in info_dict.get('entries', []):
            playlistVideo = PlaylistVideo()

            playlistVideo.title = item.get('title', '')
            playlistVideo.views = item.get('view_count', 0)
            playlistVideo.likes = item.get('like_count', 0)
            playlistVideo.dislikes = item.get('dislike_count', 0)
            playlistVideo.url = item.get('webpage_url', '')

            
            # selecting thumbnail
            thumbnails = item.get('thumbnails', [])
            isThumbnailFound = False

            for index in range(len(thumbnails), 0, -1):
                thumbnail = thumbnails[index - 1]
                resolution = thumbnail.get('resolution', '')

                for res in thumbResolution:
                    if(res == resolution):
                        playlistVideo.thumbnail = thumbnail.get('url', '')
                        isThumbnailFound = True
                        break
                
                if isThumbnailFound == True:
                    break

            playlist.videos.append(playlistVideo)
        
        print(json.dumps(playlist.toDict())) 






class VideoDetail:
    title = ''
    likes = 0
    dislikes = 0
    views = 0
    thumbnail = ''
    duration = 0
    youtubeUrl = ''
    uploadAt = ''
    downloads = list()

    def toDict(self):
        dic = {
            "title" : self.title,
            "likes" : self.likes,
            "dislikes" : self.dislikes,
            "views" : self.views,
            "thumbnail" : self.thumbnail,
            "duration" : self.duration,
            "youtubeUrl" : self.youtubeUrl,
            "uploadAt" : self.uploadAt,
            "downloads" : []
        }

        downloadDic = []
        # loop through all downloads
        for item in self.downloads:
            downloadDic.append(item.toDict())

        dic['downloads'] = downloadDic

        return dic


class VideoFormat:
    url = ''
    quality = ''
    format = ''
    size = 0

    def toDict(self):
        dic = {
            "url" : self.url,
            "quality" : self.quality,
            "format" : self.format,
            "size" : self.size
        }

        return dic

class Playlist:
    title = ''
    videos = []

    def toDict(self):
        dic = {
            "title" : self.title,
            "videos" : []
        }

        videoDic = []

        # loop through all videos
        for item in self.videos:
            videoDic.append(item.toDict())

        dic['videos'] = videoDic
        return dic



class PlaylistVideo:
    title = ''
    likes = 0
    dislikes = 0
    views = 0
    thumbnail = ''
    url = ''

    def toDict(self):
        dic = {
            "title" : self.title,
            "likes" : self.likes,
            "dislikes" : self.dislikes,
            "views" : self.views,
            "thumbnail" : self.thumbnail,
            "url": self.url
        }

        return dic

# getVideoDetails('https://www.youtube.com/watch?v=d-GQq792pWI')
# getVideoDetails('https://www.youtube.com/watch?v=7PIji8OubXU')
getPlaylist('https://www.youtube.com/playlist?list=PLPwpWyfm6JADGP7TZF-FzCtP9Nm-g5B8v')

