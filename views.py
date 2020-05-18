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
    '''保存整个游戏游戏框架的类

    应该只实例化一次
    '''

    def __init__(self):
        self.games = []  # 游戏列表
        self.groups = {}  # 保存玩家列表
        self.persons = {}  # 保存玩家当前游戏信息
        self.limit = {}  # 每个游戏的最小参加人数
        self.games_func = {}  # 游戏逻辑函数
        self.person = {}  # 每个游戏对应的玩家类
        self.queue = {}  # 每个群聊对应的消息队列, 可以多个群聊对应一个消息队列
        self.is_start = {}  # 游戏是否开始
        self.on_func = {}  # 监听函数
        self.private_default_func = {}  # 私聊默认监听函数
        self.group_default_func = {}  # 群聊默认监听函数

    def add(self, module):
        '''加载mod
        Args:
            module: mod
        '''
        name = module.mod.name  # 游戏名称
        self.games.append(name)
        self.groups[name] = {}
        self.limit[name] = module.mod.limit
        self.games_func[name] = module.mod.main
        self.person[name] = module.mod.person
        self.is_start[name] = {}
        self.on_func[name] = module.cm.func
        self.private_default_func[name] = module.cm.private_default_func
        self.group_default_func[name] = module.cm.group_default_func
        logger.info(f"[BotGame.{name}] mod has been load.")


class CustomizeMethod(object):
    def __init__(self):
        self.func = {}
        self.private_default_func = None
        self.group_default_func = None

    def on(self, command, is_private=False, is_start=True):
        def decorator(func):
            self.func[command] = {"is_private": is_private, "is_start": is_start, "func": func}
            return func
        return decorator

    def default(self, is_private=False):
        def decorator(func):
            if is_private:
                self.private_default_func = func
            else:
                self.group_default_func = func
            return func
        return decorator


class RankPerson(object):
    '''排行榜上保存玩家信息的类'''

    def __init__(self, uid):
        self.uid = uid  # QQ号
        self.coin = 0  # 金币数量
        self.charm = 0  # 魅力
        self.won = {}  # 赢场计数
        self.all = {}  # 总场计数
        self.is_id_public = False  # 是否公开QQ号

    def __eq__(self, other):
        return self.uid == other.uid

    def settle(self, game, gid, iswin, coin):
        '''游戏结算'''
        if not self.all[game].get(gid):
            self.all[game][gid] = 1
            self.won[game][gid] = 1 if iswin else 0
        else:
            self.all[game][gid] += 1
            self.won[game][gid] += 1 if iswin else 0
        self.coin += coin
