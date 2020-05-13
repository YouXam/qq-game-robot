from nonebot.log import logger
from nonebot import CommandSession


def geti(session: CommandSession):
    '''根据 session 获取 QQ号, 群号和昵称

    Args:
        session     :当前 session

    Returns:
        (uid, gid, name)

        uid     :QQ号
        gid     :群号
        name    :群名片或昵称
    '''
    return session.ctx['sender']['user_id'], session.ctx['group_id'], (session.ctx['sender']['card'] if session.ctx['sender']['card'] else session.ctx['sender']['nickname'])


class BotGame(object):
    def __init__(self):
        self.groups = {}  # 保存玩家列表
        self.persons = {}  # 保存玩家当前游戏信息
        self.limit = {}  # 每个游戏的最小参加人数
        self.games = {}  # 游戏逻辑函数
        self.person = {}  # 每个游戏对应的玩家类

    def add(self, module):
        '''加载mod
        Args:
            module: mod
        '''
        name = module.mod.name  # 游戏名称
        self.groups[name] = {}
        self.limit[name] = module.mod.limit
        self.games[name] = module.mod.main
        self.person[name] = module.mod.person
        logger.info(f"[BotGame.{name}] mod has been load.")


class RankPerson(object):
    def __init__(self, uid):
        self.uid = uid  # QQ号
        self.coin = 0  # 金币数量
        self.charm = 0  # 魅力
        self.won = {"wiu": {}}  # 赢场计数
        self.all = {"wiu": {}}  # 总场计数
        self.if_id_public = False  # 是否公开QQ号

    def __eq__(self, other):
        return self.uid == other.uid

    def played_wiu(self, gid, ifwin, coin):
        if not self.all["wiu"].get(gid):
            self.all["wiu"][gid] = 1
            self.won["wiu"][gid] = 1 if ifwin else 0
        else:
            self.all["wiu"][gid] += 1
            self.won["wiu"][gid] += 1 if ifwin else 0
