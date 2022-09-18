#!/usr/local/bin/python3.8

import requests, re, json
import subprocess, sys
import os, signal
import psutil
from zlib import crc32

# DASH folder
DASH_FOLDER = "/var/www/html/dash/"
# FFMPEG process
FFMPEG = "ffmpeg"


# Get items
def SafeGetItems(dct, *keys):
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
    return dct

def getUrl(url, hh):
    resp = requests.get(url, headers=hh)
    data = resp.content.decode("utf-8")

    return data

def GetKBSUrl(code):
    url = ""
    hh = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36', 'Accept-Language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7', 'Accept-Encoding' : 'gzip, deflate'}
    request_url = "https://onair.kbs.co.kr/index.html?sname=onair&stype=live&ch_code=" + code

    WebHTML = getUrl(request_url, hh)
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

def GetMBCUrl(code):

    hh = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36', 'Referer' : 'http://mini.imbc.com/', 'Accept-Language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7', 'Accept-Encoding' : 'gzip, deflate'}
    request_url = 'http://miniplay.imbc.com/WebHLS.ashx?channel=' + code + '&protocol=M3U8&agent=ios&nocash=0.4'
    url = getUrl(request_url, hh)

    return url

def GetSBSUrl(code):

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

    url = getUrl(SBS_URL.format(sbs_ch[code], code), sbsheader)

    return url

def GetRadioUrl(ch):

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
        url = GetKBSUrl(channelCodes[ch])
    elif "MBC" in ch:
        url = GetMBCUrl(channelCodes[ch])
    elif "SBS" in ch:
        url = GetSBSUrl(channelCodes[ch])
    else:
        print("Argument(%s) is missing or invalid!" % ch)
        quit()

    return url

def findProcessIdByName(processName, argument = None):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''
    listOfProcessObjects = []
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            isMatchedProcess = False
            pinfo = proc.as_dict(attrs=['pid', 'name', 'cmdline'])
            # Check if process name contains the given name string.
            if processName.lower() in pinfo['name'].lower():
                isMatchedProcess = True

            if argument:
                findArgument = False
                # argument should be includes in pinfo['cmdline']
                for cmd in pinfo['cmdline']:
                    if argument in cmd:
                        findArgument = True
                        break
                if findArgument == False:
                    isMatchedProcess = False

            if isMatchedProcess == True:
                listOfProcessObjects.append(pinfo)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return listOfProcessObjects;

def KillProcess(process):

    listOfProcessIds  = findProcessIdByName(process)
    if len(listOfProcessIds) > 0:
        for elemt in listOfProcessIds:
            pid = elemt['pid']
            print ("Kill %s(%d)" % (process, pid))
            os.kill(pid, signal.SIGKILL)

def TranscodeUrl(url, index):

    FFMPEG_CMD = "ffmpeg -re  -i \"{}\" -c:a copy -bsf:a aac_adtstoasc -f flv rtmp://localhost/live/{} 2> /dev/null &".format(url, index)
    print (FFMPEG_CMD)
    subprocess.call(FFMPEG_CMD, shell=True)

def GetMpdCrc(mpdFilename):

    crc = 0
    try:
        fmpd = open(mpdFilename, mode='rb')
        crc = crc32(fmpd.read())
        fmpd.close()
    except:
        pass

    return str(crc)

def UpdateCRC(mpdFilename, crcFilename):

    crc = GetMpdCrc(mpdFilename)
    fcrc = open(crcFilename, mode='w')
    fcrc.write(crc)
    fcrc.close()

def isEqualCRC(mpdFilename, crcFilename):

    crc1 = GetMpdCrc(mpdFilename)
    crc2 = 0
    try:
        fcrc = open(crcFilename, mode='r')
        crc2 = fcrc.read()
        fcrc.close()
    except:
        pass

    return True if crc1 == crc2 else False


#######################################
# Main
#######################################
channelMap = {
    "mbc" : "MBC FM4U",
    "sbs" : "SBS Power FM",    
    "kbs" : "KBS 2FM"
}

# Get Command
command = sys.argv[1]

if command == "start":
    for index, item in channelMap.items():
        # Check CRC32 value
        isEqual = isEqualCRC(DASH_FOLDER + index + ".mpd", DASH_FOLDER + index + ".crc")
        if isEqual == True:
            print ("%s MPD CRC does not updated" % index)

        # Check process is running
        listOfProcessIds  = findProcessIdByName(FFMPEG, index)
        if len(listOfProcessIds) == 0 or isEqual == True:
            # Process is not runing properly
            if len(listOfProcessIds) > 0:
                pid = listOfProcessIds[0]['pid']
                print ("Kill %d" % pid)
                os.kill(pid, signal.SIGKILL)            

            # Get Radio URL
            url = GetRadioUrl(item)
            
            # Transcode URL
            print ("Start %s transcoding" % item)
            TranscodeUrl(url, index)

        # Update CRC32 value for mpd file
        UpdateCRC(DASH_FOLDER + index + ".mpd", DASH_FOLDER + index + ".crc")

else:
    "Stop Transcoding"
    KillProcess(FFMPEG)
