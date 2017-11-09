import requests
import json
import string
import random
import sys
import os
import time
from Crypto.Hash import SHA,MD5

class PyDMTQ(object):
    #This is MethodID/MethodName Table
    IDMethodTable={56:"game.getPatternUrl",
                   69:"game.getFirstResourceSongList",
                   28:"shop.getUnlockedProductList",
                   34:"game.getOwnPatternScore",
                   14:"user.getOwnRecomInfo",
                   49:"game.getOwnQuestList",
                   46:"game.getOwnAchievementList",
                   24:"shop.getOwnItemList",
                   41:"game.getOwnSongList",
                   35:"game.getUserAsset",
                   10:"user.updateInfo",
                   6:"memo.getMemoList",
                   2:"board.getNoticeList",
                   51:"game.getLineTopRank",
                   33:"game.getResourceList",
                   39:"game.getSongList",
                   55:"game.getSongUrl",
                   9:"user.loginV2",
                   0:"service.getInfo",
                   53:"game.getLineScoreRange",
                   48:"game.getPreviewPlayInfo",
                   42:"game.savePlayResult",
                   77:"game.getLineScoreRangeWithLevel",
                   37:"shop.buyMultiProductByQPoint",
                   94:"game.getAdTicketRequest"

    }
    #Functions are named as MethodName.replace(".","_") for dynamic method dispatching
    app_key='c6a0fad2ef3ab45068ba95fdc059e2bf'
    app_secret='ODY0NmM0ZjBjZTI5ZTQ2NzFkMTVmOTE2YjU1YzY3MmY'
    def __init__(self, email=None, password=None,udid=None):
        #PMang Login
        epoch=str(time.time())
        HTTPHeaders = {"User-Agent": "PmangPlus SDK 1.8 170414 (iPhone OS,9.3.3,iPad5,3,Apple,(null),(null))",
                       "X-PmangPlus-Platform": 'iOS',
                       'fp': self.SHA1(str(epoch+PyDMTQ.app_secret).encode('utf-8')),
                       'locale': "en_US",
                       'ts': str(epoch),
                       'ver': '5'}
        Body = {'app_id': '576',
                'app_key':PyDMTQ.app_key,
                'locale': 'en_US',
                'device_cd': 'IPAD',
                'app_secret': PyDMTQ.app_secret,
                'local_cd': 'ENG',
                'os_ver': '9.3.3',
                'app_ver': '1.0',
                "privacy_yn":"Y",
                "ad_yn":"Y",
                "provider":"",
                "ad_night_yn":"N",
                "jailbreak_yn": 'N',
                "old_udid":"",
                "mob_svc_yn":"Y",
                'udid': udid}
        if udid!=None:
            Body["old_udid"]=udid
            Body["udid"]=udid
        else:
            Body["old_udid"]=self.CalculateNce()
            Body["udid"]=Body["old_udid"]
        if email!=None and password!=None:
            Body["passwd"]=password
            Body["email"]=email
        RawRequest=requests.post("https://pmangplus.com/accounts/v3/global/login_dmq",params=Body, headers=HTTPHeaders)
        foo=json.loads(RawRequest.content)
        self.access_token=foo['value']['access_token']
        self.member_id=foo['value']['member']['member_id']
        self.secretkey=""
        self.secretkeyver="1"
        self.apitoken=""
        if email==None and password==None:
            self.nickname=" "
            self.profileimageurl=""
        else:
            #Untested. Should be wrong
            self.nickname=foo['value']['member']['nickname']
            self.profileimageurl=foo['value']['member']['profile_img_url']
    def SHA1(self,String):
        x=SHA.new()
        x.update(String)
        return x.hexdigest()
    def CalculateFp(self, PostData):
        h = MD5.new()
        h.update(bytearray(str(self.secretkey + PostData), 'utf8'))
        return h.hexdigest()
    def APIPost(self,id,Params):
        HTTPBody=[
        	{
        		"id": id,
        		"method": PyDMTQ.IDMethodTable[id],
        		"params": Params
        	}
        ]
        HTTPBody=json.dumps(HTTPBody)
        HTTPHeader={
        	                "Api-Token" :self.apitoken,
        	                "Fp" : self.CalculateFp(HTTPBody),
        	                "Nce" : self.CalculateNce(),
        	                "Secret-Key" : self.secretkey,
        	                "Secret-Ver" : self.secretkeyver,
        	                "X-Unity-Version" : "5.5.2f1"
        }
        return requests.post("https://dmqglb.mb.pmang.com/DMQ/rpc",data=HTTPBody, headers=HTTPHeader)
    def CalculateNce(self, size=32, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    def user_loginV2(self):
        foo2=json.loads(self.APIPost(9,[self.access_token,self.nickname,self.profileimageurl,"1.0.11","iOS","CN"]).content)

        self.LoginInfo=foo2[0]
        self.apitoken=foo2[0]['result']['API_TOKEN']
        self.secretkey=str(foo2[0]['result']['SECRET_KEY'])
        self.secretkeyver=str(foo2[0]['result']['SECRET_VER'])
        self.guid=str(foo2[0]['result']['guid'])
        print("Logged in with API Token:"+self.apitoken)
    def game_getPatternUrl(self,PatternId,EarphoneMode=True,DeviceType="P"):
        EM=""
        if EarphoneMode==True:
            EM="e"

        return json.loads(self.APIPost(56,[self.guid,PatternId,EM,DeviceType]).content)[0]["result"]
    def game_getSongList(self):
        return json.loads(self.APIPost(39,[]).content)[0]["result"]
    def game_getResourceList(self,version,ClientOS):
        return json.loads(self.APIPost(33,[version,ClientOS]).content)[0]["result"]
    def game_getUserAsset(self):
        return json.loads(self.APIPost(35,[self.guid]).content)[0]["result"]
    def game_getFirstResourceSongList(self):
        return json.loads(self.APIPost(69,[]).content)[0]["result"]
    def service_getInfo(self,Version,ClientOS):
        return json.loads(self.APIPost(0,[Version,ClientOS]).content)[0]["result"]
    def game_savePlayResult(self,PatternId,JudgementStat,MaxCombo,LuckyBonus,Effector,IngameItem,GameToken):
        '''
        JudgementStat: list(none, breakCount, max1Count, max10Count, max20Count, max30Count, max40Count, max50Count, max60Count, max70Count, max80Count, max90Count, max100Count)
        Effector: list(effectFade,effectTimeLine,effectBlink)
        IngameItem: list(feverCount, gaugeRefillCount, breakShieldCount),
        '''
        return json.loads(self.APIPost(42,[self.guid,PatternId,JudgementStat,MaxCombo,LuckyBonus,Effector,IngameItem,GameToken]).content)[0]["result"]
    def game_getLineScoreRange(self,SongId,Line,FromRank,Range):
        '''
        Range is 20 in game
        '''
        return json.loads(self.APIPost(53,[SongId,Line,FromRank,Range]).content)[0]["result"]
    def game_getAdTicketRequest(self,SongId):
        '''
        Fake a AdTicketRequest
        '''
        return json.loads(self.APIPost(94,[self.guid,SongId]).content)[0]["result"]
    def game_getSongUrl(self,SongID,ClientOS,Version):
        '''
            ClientOS: IOS or ANDROID
            Version: 1.0.0
        '''
        return json.loads(self.APIPost(55,[self.guid,SongID,ClientOS,Version]).content)[0]["result"]
    def game_getPreviewPlayInfo(self,PatternID):
        return json.loads(self.APIPost(48,[self.guid,PatternID]).content)[0]["result"]
    def shop_buyMultiProductByQPoint(self,ProductIDs):
        '''
        ProductIDs: A list of ProductIDs
        '''
        return json.loads(self.APIPost(37,[self.guid,json.dumps({"product_id":ProductIDs})]).content)[0]["result"]
