# !/usr/bin/env python
# coding=utf-8
import requests
import pytz
import datetime
from io import StringIO
import time

# 初始化信息
SCKEY = 'xxxxxxxxxxxxxxxxxxxxxxxx'  # '*********复制SERVER酱的SCKEY进来*************(保留引号)'
data = {
    "wps_invite": [
        {
            "name": "水哥他爸",
            "invite_userid": 11699139251,  # "*********复制手机WPS个人信息中的用户ID进来，类似括号内容(191641526)*************(不保留双引号)",
            "sid": "xxxxxxxxxx"  # network获取wps_sid
        }
    ]
}
# 初始化日志
sio = StringIO('WPS签到日志\n\n')
sio.seek(0, 2)  # 将读写位置移动到结尾
s = requests.session()
tz = pytz.timezone('Asia/Shanghai')
nowtime = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
sio.write("--------------------------" + nowtime + "----------------------------\n\n")


# 微信推送
def pushWechat(desp, nowtime):
    ssckey = SCKEY
    send_url = 'https://sc.ftqq.com/' + ssckey + '.send'
    if '失败' in desp:
        params = {
            'text': 'WPS小程序签到失败提醒' + nowtime,
            'desp': desp
        }
    else:
        params = {
            'text': 'WPS小程序签到提醒' + nowtime,
            'desp': desp
        }
    requests.post(send_url, params=params)


# 主函数
def main():
    wps_inv = data['wps_invite']
    # 这13个账号被邀请
    invite_sid = [
        "V02StVuaNcoKrZ3BuvJQ1FcFS_xnG2k00af250d4002664c02f",
        "V02SWIvKWYijG6Rggo4m0xvDKj1m7ew00a8e26d3002508b828",
        "V02Sr3nJ9IicoHWfeyQLiXgvrRpje6E00a240b890023270f97",
        "V02SBsNOf4sJZNFo4jOHdgHg7-2Tn1s00a338776000b669579",
        "V02ScVbtm2pQD49ArcgGLv360iqQFLs014c8062e000b6c37b6",
        "V02S2oI49T-Jp0_zJKZ5U38dIUSIl8Q00aa679530026780e96",
        "V02ShotJqqiWyubCX0VWTlcbgcHqtSQ00a45564e002678124c",
        "V02SFiqdXRGnH5oAV2FmDDulZyGDL3M00a61660c0026781be1",
        "V02S7tldy5ltYcikCzJ8PJQDSy_ElEs00a327c3c0026782526",
        "V02SPoOluAnWda0dTBYTXpdetS97tyI00a16135e002684bb5c",
        "V02Sb8gxW2inr6IDYrdHK_ywJnayd6s00ab7472b0026849b17",
        "V02SwV15KQ_8n6brU98_2kLnnFUDUOw00adf3fda0026934a7f",
        "V02SC1mOHS0RiUBxeoA8NTliH2h2NGc00a803c35002693584d"

    ]
    sio.write("\n\n==========wps邀请==========\n\n")
    for item in wps_inv:
        sio.write("为{}邀请---↓\n\n".format(item['name']))
        if type(item['invite_userid']) == int:
            wps_invite(invite_sid, item['invite_userid'])
        else:
            sio.write("邀请失败：用户ID错误，请重新复制手机WPS个人信息中的用户ID并修改'invite_userid'项,注意不保留双引号\n\n")
    desp = sio.getvalue()
    pushWechat(desp, nowtime)
    print(desp)
    return desp


# wps接受邀请
def wps_invite(sid: list, invite_userid: int) -> None:
    invite_url = 'http://zt.wps.cn/2018/clock_in/api/invite'
    for index, i in enumerate(sid):
        headers = {
            'sid': i
        }
        time.sleep(10)
        r = s.post(invite_url, headers=headers, data={
            'invite_userid': invite_userid})
        sio.write("ID={}, 状态码: {}, \n\n ".format(str(index + 1).zfill(2), r.status_code))


def main_handler(event, context):
    return main()


if __name__ == '__main__':
    main()
