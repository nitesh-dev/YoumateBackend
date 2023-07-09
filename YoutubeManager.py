
# youtube-dl --get-url https://www.youtube.com/watch?v=d-GQq792pWI

import yt_dlp as youtube
import json

ydl_opts = {'quiet': True}
ydl = youtube.YoutubeDL(ydl_opts)

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
        qualities = ['144', '240', '360','480','720','1080','2160']
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



# getVideoDetails('https://www.youtube.com/watch?v=d-GQq792pWI')
getVideoDetails('https://www.youtube.com/watch?v=7PIji8OubXU')

