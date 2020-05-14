from nonebot import CommandSession
import views
import asyncio


class WiuPerson(object):
    '''谁是卧底 玩家类'''

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
        self.isdie = False

        self.score = 0
        self.iswin = False


class Wiu(object):
    '''谁是卧底 游戏类'''

    def __init__(self):
        self.name = "谁是卧底"
        self.limit = 1
        self.person = WiuPerson

    async def main(self, session: CommandSession, bot_game: views.BotGame, msg_queue: asyncio.Queue):
        '''游戏逻辑 主函数'''
        await session.send(f"这里是{self.name}游戏")


mod = Wiu()
