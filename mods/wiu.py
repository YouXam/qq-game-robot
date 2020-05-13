from nonebot import CommandSession
import views


class WiuPerson(object):
    def __init__(self, tid, uid, gid, name, nickname):
        '''
        Args
            tid     :游戏中座位号
            uid     :QQ号
            gid     :游戏所在群号
            name    :群昵称或昵称
            nickname:昵称
            isu     :是否为卧底
        '''
        self.tid = tid
        self.uid = uid
        self.gid = gid
        self.name = name
        self.isu = False


class Wiu(object):
    def __init__(self):
        self.name = "谁是卧底"
        self.limit = 1
        self.person = WiuPerson

    async def main(self, session: CommandSession, bot_game: views.BotGame):
        await session.send("这里是谁是卧底游戏")


mod = Wiu()
