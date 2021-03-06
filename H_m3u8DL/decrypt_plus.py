import re
import requests
import base64,json
from Crypto.Cipher import AES

class Decrypt_plus:
    def __init__(self):
        pass

    def xiaoetong(self,m3u8url):
        replace_header = ['encrypt-k-vod.xet.tech']
        true_header = '1252524126.vod2.myqcloud.com'
        for i in replace_header:
            if i in m3u8url:
                m3u8url = m3u8url.replace(i, true_header).split('?')[0]
                if m3u8url[-3:] == '.ts':
                    m3u8url = re.sub('_\d+', '', m3u8url).replace('.ts', '.m3u8')
        return m3u8url

    def DecodeHuke88Key(self,m3u8url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71'
        }
        # m3u8url = 'https://video-tx.huke88.com/cb3d3408vodtransgzp1256517420/363a46cd5285890808736808030/voddrm.token.eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9~eyJ0eXBlIjoiRHJtVG9rZW4iLCJhcHBJZCI6MTI1NjUxNzQyMCwiZmlsZUlkIjoiNTI4NTg5MDgwODczNjgwODAzMCIsImN1cnJlbnRUaW1lU3RhbXAiOjE2MjcwNTEwOTksImV4cGlyZVRpbWVTdGFtcCI6MjE0NzQ4MzY0NywicmFuZG9tIjoyNzU2NzE4MjQzLCJvdmVybGF5S2V5IjoiNzVkNmVlYWUzZGUxNDgwNWQ5NDdhODU4NmU3ZjE0YzQiLCJvdmVybGF5SXYiOiI0NjcxZGIwYWE3ZWI0YTIzNWJlN2EzMmJmNzE3ZmZkOSIsImNpcGhlcmVkT3ZlcmxheUtleSI6IiIsImNpcGhlcmVkT3ZlcmxheUl2IjoiIiwia2V5SWQiOjAsInN0cmljdE1vZGUiOjB9~g698PBwoPK5mSkIaN9XgeqVzVMtbnwnwTKzcV5rJtSg.video_12_2.m3u8?rlimit=3&sign=b22838015362871788c40f616acef1b3&t=60fafe87&us=1627051095'
        text = m3u8url.split('~')[1]
        if text[-2:] != '==':
            text += '=='
        enc = base64.b64decode(text).decode()

        jObject = json.loads(enc)

        overlayKey = jObject['overlayKey']
        overlayIv = jObject['overlayIv']

        # 得到 key
        m3u8text = requests.get(m3u8url, headers=headers).text
        keyurl = re.findall('URI="(.+?)"', m3u8text)[0]
        encryptkey = requests.get(keyurl).content
        cryptor = AES.new(key=bytes.fromhex(overlayKey), mode=AES.MODE_CBC, iv=bytes.fromhex(overlayIv))

        decryptkey = cryptor.decrypt(encryptkey)
        # base64编码的解密key
        decryptkey = base64.b64encode(decryptkey).decode()
        return (m3u8url, decryptkey)

    """
    http://cd11-ccd1-2.play.bokecc.com/flvs/78665FEF083498AB/2019-03-05/4D4D230A187CBA929C33DC5901307461-20.m3u8?t=1651246391&key=F34B8C88C7051F72DA0531248765D000&tpl=10&tpt=112
    https://s1-cloud.bokecc.com/flvs/78665FEF083498AB/2019-03-05/4D4D230A187CBA929C33DC5901307461.avi?t=1651283541&key=2996C00B0CA0416505E2CDE0F428E7C6
    """
    def DecodeBokeccKey(self,m3u8url):
        invSBoxArray = [
            'Uglq1TA2pTi/QKOegfPX+3zjOYKbL/+HNI5DRMTe6ctUe5QypsIjPe5MlQtC+sNOCC6hZijZJLJ2W6JJbYvRJXL49mSGaJgW1KRczF1ltpJscEhQ/e252l4VRlenjZ2EkNirAIy80wr35FgFuLNFBtAsHo/KPw8Cwa+9AwETims6kRFBT2fc6pfyz87wtOZzlqx0IuetNYXi+TfoHHXfbkfxGnEdKcWJb7diDqoYvhv8Vj5LxtJ5IJrbwP54zVr0H92oM4gHxzGxEhBZJ4DsX2BRf6kZtUoNLeV6n5PJnO+g4DtNrir1sMjruzyDU5lhFysEfrp31ibhaRRjVSEMfQ==',
            'Y1UhDH1SCWrVMDalOL9Ao56B89f7fOM5gpsv/4c0jkNExN7py1R7lDKmwiM97kyVC0L6w04ILqFmKNkksnZboklti9Elcvj2ZIZomBbUpFzMXWW2kmxwSFD97bnaXhVGV6eNnYSQ2KsAjLzTCvfkWAW4s0UG0Cwej8o/DwLBr70DAROKazqREUFPZ9zql/LPzvC05nOWrHQi5601heL5N+gcdd9uR/EacR0pxYlvt2IOqhi+G/xWPkvG0nkgmtvA/njNWvQf3agziAfHMbESEFkngOxfYFF/qRm1Sg0t5Xqfk8mc76DgO02uKvWwyOu7PINTmWEXKwR+unfWJuFpFA==',
        ]

        def decryptBokeccKey(key, info):
            if len(key) <= 16:
                return bytes(key)

            version = key[0]
            key = key[1:]
            invSBox = base64.b64decode(invSBoxArray[version])

            if version == 0:
                for i, v in enumerate(key):
                    if v < 0:
                        v = 255 & v
                    key[i] = invSBox[v]
            if version == 1:
                r = [255 & ord(i) for i in info]
                for n, s in enumerate(key):
                    s ^= r[n % len(info)]
                    if s < 0:
                        s = 255 & s
                    key[n] = invSBox[s]

            return bytes(key)

        if 'play.bokecc.com' not in m3u8url:
            return (m3u8url, '')
        info = re.findall('&key=(.+?)&', m3u8url)[0]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62'
        }
        m3u8text = requests.get(m3u8url, headers=headers).text
        keyurl = re.findall('URI="([^"]+)"', m3u8text)[0]
        key = requests.get(url=keyurl, headers=headers).content

        m3u8key = list(key)
        m3u8key = decryptBokeccKey(m3u8key, info)
        m3u8key = base64.b64encode(m3u8key[0:16]).decode()
        return (m3u8url, m3u8key)
