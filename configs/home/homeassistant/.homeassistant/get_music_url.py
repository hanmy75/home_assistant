import sys
import pafy

url=sys.argv[1]
video = pafy.new(url)
stream_url = video.getbest()
print(stream_url.url)
