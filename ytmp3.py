import youtube_dl
def downloadMp3(video_url, destination_folder_path):
    # video_url = input("please enter youtube video url:")
  
    video_info = youtube_dl.YoutubeDL().extract_info(
        url = video_url,download=False
    )
    filename = f"{destination_folder_path}{video_info['title']}.mp3"
    options={
        'format':'bestaudio/best',
        'keepvideo':False,
        'outtmpl':filename,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    return filename
    # print("Download complete... {}".format(filename))

if __name__=='__main__':
    downloadMp3(input("yt video url: "), "./downloads/")


  
# from pytube import YouTube
# import os

# # "https://www.youtube.com/watch?v=jNQXAC9IVRw"
# def run():
#   # downloadMp3(str(input("url:\n>> ")), "downloads/")
#   downloadMp3("https://www.youtube.com/watch?v=jNQXAC9IVRw", "./downloads/")

# # returns file path
# def downloadMp3(url, destination_folder_path):

#     yt = YouTube(url)
#     #str(url))
  
#     # extract only audio
#     video = yt.streams.filter(only_audio=True).first()
  
#     # hardcode download destination
#     destination =  destination_folder_path#"./downloads/"
  
#     # download the file
#     out_file = video.download(output_path=destination)
  
#     # save the file
#     base, ext = os.path.splitext(out_file)

#     # base is file path (str)
    
#     # cap filename at 30 chars
#     if len(yt.title) > 30:
#       vidname = yt.title[0:30]
#       last_slash = base.rfind("/")
#       base = base[0: (last_slash + 1)] + vidname
      
    
#     new_file = base + '.mp3'
#     os.rename(out_file, new_file)

#     # result of success
#     print("'" + yt.title + "' download done.")

#     return new_file


# if __name__ == "__main__":
#     run()