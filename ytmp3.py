from pytube import YouTube
import os

# https://www.youtube.com/watch?v=jNQXAC9IVRw
# def run():
    
#     downloadMp3(str(input("url:\n>> ")), "templates/")

# returns file path
def downloadMp3(url, destination_folder_path):

    yt = YouTube(url)
    #str(url))
  
    # extract only audio
    video = yt.streams.filter(only_audio=True).first()
  
    # hardcode download destination
    destination =  destination_folder_path#"./downloads/"
  
    # download the file
    out_file = video.download(output_path=destination)
  
    # save the file
    base, ext = os.path.splitext(out_file)

    # base is file path (str)
    
    # vidname = urllib.parse.quote(yt.title)
    # cap filename at 30 chars
    if len(yt.title) > 30:
      vidname = yt.title[0:30]
      last_slash = base.rfind("/")
      base = base[0: (last_slash + 1)] + vidname
      
    
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    # result of success
    print("'" + yt.title + "' download done.")

    return new_file



# if __name__ == "__main__":
#     run()