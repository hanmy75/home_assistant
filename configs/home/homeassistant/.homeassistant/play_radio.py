#!/usr/bin/python3

import requests, re, json
import subprocess, sys
import os, signal


# Get items
def SafeGetItems(dct, *keys):
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
    return dct

def get_url(url, hh):
    resp = requests.get(url, headers=hh)
    data = resp.content.decode("utf-8")

    return data

def check_valid_url(url):
	try:
		resp = requests.get(url)
	except requests.exceptions.RequestException as e:
		return 0
	return 1

def kbs_func(code):
    url = ""
    hh = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36', 'Accept-Language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7', 'Accept-Encoding' : 'gzip, deflate'}
    request_url = "https://onair.kbs.co.kr/index.html?sname=onair&stype=live&ch_code=" + code

    WebHTML = get_url(request_url, hh)
    for line in WebHTML.split("\n"):
        if "service_url" in line:
            subLines = line.split("'")
            data = json.loads(subLines[1].replace("\\", ""))
            channelInfos = SafeGetItems(data, "channel_item")
            if channelInfos:
                for channelInfo in channelInfos:
                    # Find Radio channel
                    if channelInfo["media_type"] == "radio":
                        url = channelInfo["service_url"]

    return url

def mbc_func(code):

    hh = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36', 'Referer' : 'http://mini.imbc.com/', 'Accept-Language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7', 'Accept-Encoding' : 'gzip, deflate'}
    request_url = 'http://miniplay.imbc.com/WebHLS.ashx?channel=' + code + '&protocol=M3U8&agent=ios&nocash=0.4'
    url = get_url(request_url, hh)

    return url

def sbs_func(code):

    sbs_ch = {'powerfm' : 'powerpc', 'lovefm': 'lovepc'}
    SBS_URL = 'https://apis.sbs.co.kr/play-api/1.0/livestream/{}/{}?protocol=hls&ssl=Y'
    sbsheader = {
        'Host': 'apis.sbs.co.kr',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) GOREALRA/1.2.1 Chrome/85.0.4183.121 Electron/10.1.3 Safari/537.36',
        'Accept': '*/*',
        'Origin': 'https://gorealraplayer.radio.sbs.co.kr',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://gorealraplayer.radio.sbs.co.kr/main.html?v=1.2.1',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko',
        'If-None-Match': 'W/"134-0OoLHiGF4IrBKYLjJQzxNs0/11M"'
    }

    url = get_url(SBS_URL.format(sbs_ch[code], code), sbsheader)

    return url

def ch_func(ch):

    channelCodes = {
        "KBS 1FM" : "24",
        "KBS 2FM" : "25",
        "KBS 1R"  : "21",
        "KBS 2R"  : "22",
        "KBS 3R"  : "23",
        "MBC FM4U"  : "mfm",
        "MBC FM"    : "sfm",
        "MBC ALL"   : "chm",
        "SBS Power FM" : "powerfm",
        "SBS Love FM"  : "lovefm",
    }

    if "KBS" in ch:
        url = kbs_func(channelCodes[ch])
    elif "MBC" in ch:
        url = mbc_func(channelCodes[ch])
    elif "SBS" in ch:
        url = sbs_func(channelCodes[ch])
    else:
        print("Argument(%s) is missing or invalid!" % ch)
        quit()

    return url

def check_kill_process(pstring):
    for line in os.popen("ps ax | grep " + pstring + " | grep -v grep"):
        fields = line.split()
        pid = fields[0]
        os.kill(int(pid), signal.SIGKILL)

def play_func(url):
    FFMPEG_CMD = "ffmpeg -i {}{}{} -f alsa default 2>/dev/null &".format("\'", url, "\'")
    subprocess.call(FFMPEG_CMD, shell=True)

def run_mkchromecast(device):
    CAST_CMD = "mkchromecast -n {}{}{} 2>/dev/null &".format("\'" ,device, "\'")
    subprocess.call(CAST_CMD, shell=True)

def run_pulseaudio():
    PULSEAUDIO_CMD = "pulseaudio -D"
    subprocess.call(PULSEAUDIO_CMD, shell=True)

# Main
# Kill ffmpeg & mkchromecast is it is already running
check_kill_process('pulseaudio')
check_kill_process('mkchromecast')
check_kill_process('ffmpeg')

# Run mkchromecast
run_pulseaudio()
run_mkchromecast("MY Mini")

# Get Radio URL
url = ch_func(sys.argv[1])

# Play URL
play_func(url)
