# IdentityV-login-helper(绕过注册时间限制-一键法)
![Language](https://img.shields.io/badge/language-python-blue.svg)
![GitHub License](https://img.shields.io/github/license/MeiHuaGuangShuo/idv-login)
![GitHub Release](https://img.shields.io/github/v/release/MeiHuaGuangShuo/idv-login)
![Gitea Last Commit](https://img.shields.io/github/commits-since/MeiHuaGuangShuo/idv-login/latest)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/MeiHuaGuangShuo/idv-login/build-stable.yaml)


原项目仓库：[click](https://github.com/Alexander-Porter/idv-login)
QQ群：[click](https://www.bilibili.com/opus/920131433914171416)
视频教程（已过时）：[click](https://www.bilibili.com/video/BV1qM4m1Q7i8)

## 改变的函数 / 特点
1. logger全部采用loguru
2. 自动登录支持
3. 自动启动游戏支持

### 如何自动登录？
启动程序加上 -a 或者在程序目录创建 AutoLogin 空文件或者在 `config.json` (随程序首次启动后创建) 中的 `AutoLogin` 选项改为 true

### 如何取消自动扫描？
在 `config.json` (随程序首次启动后创建) 中的 `GamePath` 选项改为 "disabled"

### 自定义启动游戏位置
在 `config.json` (随程序首次启动后创建) 中的 `GamePath` 选项填入游戏文件的**绝对路径**


## 1. 使用方式

### 特别注意
1. 如果遇到账号二次验证界面白屏的问题，请自行百度*打开TLS 1.2 教程*

### 使用预编译版本
1. 从本仓库的``release`` / ``action`` 页下载最新版本的可执行文件(*.exe)
- **注:如果你使用的是`Windows7`，请下载带有`Py3.8`后缀的版本；如果你使用的是`Windows8`及以上版本，两者均可，推荐下载带有`Py3.12`后缀的版本**)
- 下载完成后，**强烈建议**校验其``sha256``是否与 ``release``中``.sha256``的值相同。
    如果``sha256``不同，那么您下载的文件是不安全的，可能存在盗号风险，请检查您的网络环境并重新在**官方仓库**下载文件。
2. 您可以使用 ``Windows Powershell`` 的 ``Get-FileHash`` 命令来获取文件的``sha256``值，例如，计算v5.0.0-beta版本的`sha256`可以使用以下命令：
    ```bash
    PS D:\> Get-FileHash idv-login-v5.0.0-beta.zip
    
    Algorithm       Hash
    ---------       ----
    SHA256          <这里会显示HASH值>
    ```
3. 将该压缩文件解压，在解压完的目录中直接右键**以管理员身份运行**下载的可执行文件，例如``idv-login-v5.0.0-beta.exe``，等观察到脚本提示``可以开启游戏``时，保持终端窗口**打开**，然后您可以打开游戏。    
   
4. 打开游戏后，点击登录框**右下角的"电脑"图标**（如下图所示），即可使用账号密码登录，以绕过注册时间限制。

![图1](assets/image1.png)

5. 当你成功登录进入游戏大厅后，你可以在本程序界面中使用``Ctrl+C``关闭本程序。

### 手动构建（Optional）

* 在 Python 官网下载 Python [Python.org](https://www.python.org/downloads/release/python-3123/)
* 例：64 位电脑 [Windows installer (64-bit)](https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe)
* 安装Python时要**使用管理员权限**，自定义(Custom)安装，**添加到Path**、**为所有用户安装**和**pip**。
* 由于新版本的Python **不支持** Windows7，如需在Windows7上构建本程序，可能需要借助**Anaconda**之类的软件安装支持Windows7的python（如 python 3.8）进行构建，具体教程请自行百度。
* 下载[代码](https://github.com/Alexander-Porter/idv-login/archive/refs/heads/one-key.zip)到本地，解压
* 进入解压后的目录，shift+鼠标右键，选择打开Powershell或终端
* 输入以下代码并回车
```bash
pip install -r requirements.txt
pyinstaller -F src/main.py -n idv-login-v10beta.exe -i assets/icon.ico --version-file assets/version.txt --uac-admin
```
* dist文件夹中的`idv-login-v10beta.exe`就是成品

### 渠道服登录

* 在扫码界面以对应渠道扫码一次
* 下次需要登录该区服时，点击扫码登录二维码下方的游戏图标，进入一个浏览器界面
* 在该界面内管理账号登录信息

* 特别地，小米、华为账号登录需要使用手动导入的方式，需要在渠道服管理界面按照提示操作。对于华为账号，每次登录均需要在浏览器中验证，建议在第一次登录华为账号时，使用账号密码登录，信任浏览器并记住密码。

### 如果程序意外退出导致开游戏后无法登录
* 在文件资源管理器里输入`%windir%\System32\drivers\etc`并回车，删除`hosts`文件，即可解除工具对网易登录的劫持。

### 网易第五人格PC端下载
* 大陆 [下载游戏](https://adl.netease.com/d/g/id5/c/gw?type=pc)
* 海外 [下载游戏](https://h55na.gdl.easebar.com/identityv_setup_release_oversea_0112.exe)


## 2. 开源协议
本仓库使用 ``GNU General Public License 3`` 进行开源，请使用/分发本仓库的软件或源代码或衍生产品时请遵守该开源协议，并保留原始项目地址。**需要特别注意的是，根据``GPLv3``许可证的要求，如果你使用了本仓库的代码进行二次开发，那么您的代码也必须使用`GPLv3`协议开源。**

## 3. Bug 反馈
如果您在使用过程中遇到了 ``Bug``, 可以在本仓库提交 `issue` 或者加入QQ群进行反馈。

## 4. 参与本项目

### 贡献渠道服登录方式
以下渠道由于Token过期较快，需要本工具存储渠道服的session（而不是扫码时能接触到的Token）进行刷新。涉及模拟手机端SDK的行为。
| 渠道 | 描述 |
|------|------|
| 应用宝(微信) | Token过期很快，难度较大 |
| vivo账号 | Token过期时间一小时，难度较低，保存Cookie即可 |
| 九游 | Token过期很快，难度?? |

一个渠道服登录实现的类模板在[这里](src/channelHandler/miChannelHandler.py)。

如果你愿意参与本项目的开发，无论是否涉及新渠道服支持，很简单，提交一个Pull request即可。如果有意长期参与开发，请联系我。

## 5. 免责声明
- 一旦您使用本软件，便代表您同意以下所有条款。
- 截至北京时间2024年8月5日，没有**第五人格**用户因使用本程序导致封号，但本软件开发组成员**不保证**使用该软件不会导致封号，您的账号的最终解释权归网易所有，请自行甄别是否使用!**一旦您使用本软件，那么意味着您愿意自行承担使用该软件可能带来的任何风险和后果**
- 由于本软件为开源软件，非官方的二次开发版本有不可控的特性，如果您使用任何非官方版本导致任何后果的，由使用者独自承担全部责任！
- 如有将该软件用于非法目的或造成不良影响后果的，由使用者独自承担全部责任！
- 如果该软件侵犯了网易公司的相关权益，请相关人员及时与我们取得联系，我们将第一时做出处理。
