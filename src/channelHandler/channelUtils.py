import json
import random
import string
import hmac
import hashlib
import time
import requests
import pyperclip as cb
from envmgr import genv


class CustomEncoder(json.JSONEncoder):
    def encode(self, obj):
        json_str = super().encode(obj)
        return json_str.replace('/', '\\/')


LOG_KEY = "SvShWXDcmogbZJoU3YWe3Su3Ci-mCRcw"


def _get_my_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except Exception as e:
        return "127.0.0.1"


def get_sign_src(str1, str2, str3):
    str4 = ""
    replaced = str2.replace("://", "")
    if replaced.find("/") != -1:
        str4 = replaced[replaced.find("/"):]
    return str1.upper() + str4 + str3


def calcSign(url, method, data, key):
    src = get_sign_src(method, url, data)
    #sha256
    return hmac.new(key.encode(), src.encode(), hashlib.sha256).hexdigest()


def buildSAUTH(login_channel, app_channel, uid, session, game_id, sdk_version, custom_data={}):
    fakeData = genv.get("FAKE_DEVICE")
    ip = _get_my_ip()
    data = {
        "gameid"         : game_id,  # maybe works for all games
        "login_channel"  : login_channel,
        "app_channel"    : app_channel,
        "platform"       : "ad",
        "sdkuid"         : uid,
        "udid"           : fakeData["udid"],
        "sessionid"      : session,
        "sdk_version"    : sdk_version,
        "is_unisdk_guest": 0,
        "ip"             : ip,
        "aim_info"       : '{"tz":"+0800","tzid":"Asia/Shanghai","aim":"' + ip + '","country":"CN"}',
        "source_app_channel": app_channel,
        "source_platform": "ad",
        "client_login_sn": "".join(random.choices((string.hexdigits), k=16)),
        "step"           : "".join(random.choices(string.digits, k=10)),
        "step2"          : "".join(random.choices(string.digits, k=9)),
        "hostid"         : 0,
        "sdklog"         : json.dumps(fakeData),
    }
    data.update(custom_data)
    return data


def postSignedData(data, game_id, need_custom_encode=False):
    url = f"https://mgbsdk.matrix.netease.com/{game_id}/sdk/uni_sauth"
    method = "POST"
    key = genv.get("CLOUD_RES").get_by_game_id(game_id)["log_key"]
    if need_custom_encode:
        data = json.dumps(data, cls=CustomEncoder)
    else:
        data = json.dumps(data)
    headers = {"X-Client-Sign": calcSign(url, method, data, key),
               "Content-Type" : "application/json",
               "User-Agent"   : "Dalvik/2.1.0 (Linux; U; Android 12; M2102K1AC Build/V417IR)", }
    r = requests.post(url, data=data, headers=headers)
    return r.json()


def getShortGameId(game_id):
    return game_id.split("-")[-1]


def G_clipListener(verify, maxAttempt) -> str:
    cb.copy("")
    attempt = 0
    while attempt < maxAttempt:
        attempt += 1
        nowData = cb.paste()
        if verify(nowData):
            cb.copy("")
            return nowData
        else:
            time.sleep(1)
    return ""
