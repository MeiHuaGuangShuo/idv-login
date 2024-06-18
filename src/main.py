# coding=UTF-8
"""
 Copyright (c) 2024 Alexander-Porter & fwilliamhe

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program. If not, see <https://www.gnu.org/licenses/>.
 """

import json
import random
import string
from gevent import monkey
import gevent

monkey.patch_all()
import os
import sys
import time
import ctypes
import atexit
import signal
import psutil
import argparse
import win32api
import win32file
import win32con
import requests
import requests.packages
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from certmgr import certmgr
from hostmgr import hostmgr
from proxymgr import proxymgr
from channelmgr import ChannelManager
from envmgr import genv
from logger import logger

m_certmgr = None
m_hostmgr = None
m_proxy = None
on_exit = False


def handle_exit(*_):
    global on_exit
    if on_exit:
        return True
    on_exit = True
    logger.info("程序关闭，正在清理 hosts ！")
    if m_hostmgr is not None:
        m_hostmgr.remove(genv.get("DOMAIN_TARGET"))  # 无论如何退出都应该进行清理
    logger.info("再见!")
    sys.exit(0)


def ctrl_handler(ctrl_type):
    if ctrl_type == 2:  # 对应CTRL_CLOSE_EVENT
        handle_exit()
        return False
    return True


def initialize():
    # if we don't have enough privileges, relaunch as administrator
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        logger.error(f"没有管理员权限，已经启动新的程序，本程序将自动退出")
        sys.exit(1)

    # initialize the global vars at first
    genv.set("DOMAIN_TARGET", "service.mkey.163.com")
    genv.set("FP_WEBCERT", os.path.join(genv.get("FP_WORKDIR"), "domain_cert_2.pem"))
    genv.set("FP_CONFIG", os.path.join(genv.get("FP_WORKDIR"), "config.json"))
    genv.set("FP_FAKE_DEVICE", os.path.join(genv.get("FP_WORKDIR"), "fakeDevice.json"))
    genv.set("FP_WEBKEY", os.path.join(genv.get("FP_WORKDIR"), "domain_key_2.pem"))
    genv.set("FP_CACERT", os.path.join(genv.get("FP_WORKDIR"), "root_ca.pem"))
    genv.set("FP_CHANNEL_RECORD", os.path.join(genv.get("FP_WORKDIR"), "channels.json"))
    genv.set("CHANNEL_ACCOUNT_SELECTED", "")
    

    # handle exit
    atexit.register(handle_exit)

    # initialize object
    global m_certmgr, m_hostmgr, m_proxy
    m_certmgr = certmgr()
    m_hostmgr = hostmgr()
    m_proxy = proxymgr()

    # initialize workpath
    if not os.path.exists(genv.get("FP_WORKDIR")):
        os.mkdir(genv.get("FP_WORKDIR"))

    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4|0x80|0x20|0x2|0x10|0x1|0x00|0x100))
    # (Can't) copy web assets! Have trouble using pyinstaller = =
    # shutil.copytree( "web_assets", genv.get("FP_WORKDIR"), dirs_exist_ok=True)

    os.chdir(os.path.join(genv.get("FP_WORKDIR")))

    # 关于线程安全：谁？
    genv.set("CHANNELS_HELPER", ChannelManager())

    # disable warnings for requests
    requests.packages.urllib3.disable_warnings()

    if not os.path.exists(genv.get("FP_FAKE_DEVICE")):
        udid = "".join(random.choices(string.hexdigits, k=16))
        sdkDevice = {
            "device_model": "M2102K1AC",
            "os_name": "android",
            "os_ver": "12",
            "udid": udid,
            "app_ver": "157",
            "imei": "".join(random.choices(string.digits, k=15)),
            "country_code": "CN",
            "is_emulator": 0,
            "is_root": 0,
            "oaid": "",
        }
        with open(genv.get("FP_FAKE_DEVICE"), "w") as f:
            json.dump(sdkDevice, f)
    else:
        with open(genv.get("FP_FAKE_DEVICE"), "r") as f:
            sdkDevice = json.load(f)
    genv.set("FAKE_DEVICE", sdkDevice)

    if not os.path.exists(genv.get("FP_CONFIG")):
        with open(genv.get("FP_CONFIG"), "w") as f:
            json.dump({}, f)
            genv.set("CONFIG", {})
    else:
        with open(genv.get("FP_CONFIG"), "r") as f:
            genv.set("CONFIG", json.load(f))


def welcome():
    print("[+] 欢迎使用第五人格登陆助手 version 5.2.2-beta")
    print(" - 官方项目地址 : https://github.com/Alexander-Porter/idv-login/")
    print(" - 本项目地址 : https://github.com/MeiHuaGuangShuo/idv-login/")
    print(" - 如果你的这个工具不能用了，请前往仓库检查是否有新版本发布或加群询问！")
    print(" - 本程序使用GNU GPLv3协议开源， 严禁将本程序用于任何商业行为！")
    print(" - This program is free software: you can redistribute it and/or modify")
    print(" - it under the terms of the GNU General Public License as published by")
    print(" - the Free Software Foundation, either version 3 of the License, or")
    print(" - (at your option) any later version.")


def get_drives():
    drives = [i for i in win32api.GetLogicalDriveStrings().split('\x00') if i]
    rdrives = [d for d in drives if win32file.GetDriveType(d) == win32file.DRIVE_FIXED]
    return rdrives


def traverse_files(path, max_deepth: int = 255, deepth=0):
    files = []
    if deepth > max_deepth:
        # print('Out!', path)
        return []
    try:
        handle = win32file.FindFilesW(path + '\\*')
        for h in handle:
            filename = h[8]
            if filename not in ('.', '..', 'Windows', 'EFI', 'Temp'):
                fullname = path + '\\' + filename
                if win32file.GetFileAttributes(fullname) == win32file.FILE_ATTRIBUTE_DIRECTORY:
                    files.extend(traverse_files(fullname, max_deepth=max_deepth, deepth=deepth+1))
                else:
                    size = h[5]
                    files.append(fullname.replace('\\\\', '\\'))
    except:
        pass
    return files


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    pool = ThreadPoolExecutor()
    parser.add_argument('-a', '--auto-login', action='store_true')
    args = parser.parse_args()

    config_path = Path("config.json")
    if not config_path.exists():
        with open(config_path, 'w') as f:
            json.dump({
                    "AutoLogin": False,
                    "ScanDeepth": 2,
                    "GamePath": ""
                }, f, indent=4, ensure_ascii=False)
    with open(config_path, 'r') as f:
        config = json.load(f)
    def write_config():
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    is_auto_login = "True" if bool(args.auto_login) or os.path.exists("AutoLogin") or config.get("AutoLogin") else ""
    genv.set("AUTO_LOGIN", is_auto_login)
    if genv.get("AUTO_LOGIN"):
        logger.info("已经启用自动登录（仅在只有一个账号的情况下）")
    @logger.catch
    def find_game():
        logger.info(f"开始扫描游戏，扫描深度{config.get('ScanDeepth', 2)}")
        drives = get_drives()
        games = []
        for d in drives:
            files = traverse_files(d, config.get('ScanDeepth', 2))
            files = [(x, x.split("\\")[-1]) for x in files]
            files = [x[0] for x in files if x[1]=="dwrg.exe"]
            games += files
        logger.info("扫描完成")
        if len(games) == 1:
            config['GamePath'] = games[0]
            logger.info(f"查找到的游戏路径: {games[0]}")
            write_config()
            start_game()
        else:
            logger.warning(f"查找到两个游戏路径，请手动填写路径至 {config_path.absolute()} 的 GamePath 目录。游戏目录：{', '.join(games)}")

    def start_game():
        if bool(any(p.info['name'] == "dwrg.exe" for p in psutil.process_iter(['name']))):
            logger.warning("游戏已经启动，自动启动关闭")
            return False
        game_path = config.get("GamePath")
        if not isinstance(game_path, str):
            logger.error("无效的游戏路径")
        if not game_path.endswith(".exe"):
            logger.error(f"错误的游戏路径: {game_path}")
        while not genv.get("PREPARED"):
            time.sleep(0.5)
        logger.info(f"程序已经就绪，开始启动游戏 {game_path}")
        raw = os.getcwd()
        os.chdir(Path(game_path).parent)
        os.system("start " + game_path)
        os.chdir(raw)
        return True
        
            
    if not config.get("GamePath"):
        pool.submit(find_game)
    elif config.get("GamePath") == "disabled":
        pass
    else:
        pool.submit(start_game)
            

    signal.signal(signal.SIGINT, handle_exit)

    genv.set("FP_WORKDIR", os.path.join(os.environ["PROGRAMDATA"], "idv-login"))
    if not os.path.exists(genv.get("FP_WORKDIR")):
        os.mkdir(genv.get("FP_WORKDIR"))
    os.chdir(os.path.join(genv.get("FP_WORKDIR")))
    logger.info(f"已将工作目录设置为 -> {genv.get('FP_WORKDIR')}")
    try:
        welcome()
        initialize()

        if (os.path.exists(genv.get("FP_WEBCERT")) == False) or (
            os.path.exists(genv.get("FP_WEBKEY")) == False
        ):
            logger.info("正在生成必要的证书文件...")

            ca_key = m_certmgr.generate_private_key(bits=2048)
            ca_cert = m_certmgr.generate_ca(ca_key)
            m_certmgr.export_cert(genv.get("FP_CACERT"), ca_cert)

            srv_key = m_certmgr.generate_private_key(bits=2048)
            srv_cert = m_certmgr.generate_cert(
                [genv.get("DOMAIN_TARGET"), "localhost"], srv_key, ca_cert, ca_key
            )

            if m_certmgr.import_to_root(genv.get("FP_CACERT")) == False:
                logger.error("导入CA证书失败!")
                os.system("pause")
                sys.exit(-1)

            m_certmgr.export_cert(genv.get("FP_WEBCERT"), srv_cert)
            m_certmgr.export_key(genv.get("FP_WEBKEY"), srv_key)
            logger.info("初始化成功!")

        logger.info("正在重定向目标地址到本机...")
        if m_hostmgr.isExist(genv.get("DOMAIN_TARGET")) == True:
            logger.info("识别到手动定向!")
            logger.info(
                f"请确保已经将 {genv.get('DOMAIN_TARGET')} 和 localhost 指向 127.0.0.1"
            )
        else:
            m_hostmgr.add(genv.get("DOMAIN_TARGET"), "127.0.0.1")
            m_hostmgr.add("localhost", "127.0.0.1")

        logger.info("正在启动代理服务器...")

        m_proxy.run()
    except (SystemExit, gevent.exceptions.InvalidSwitchError):
        pass
    except Exception as e:
        logger.exception(
                f"发生未处理的异常:{e.__class__.__name__}: {e}.日志路径:{genv.get('FP_WORKDIR')}下的log.txt"
        )
    finally:
        handle_exit()
