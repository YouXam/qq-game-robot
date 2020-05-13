class RankPerson(object):
    def __init__(self, uid):
        self.uid = uid  # QQ号
        self.coin = 0  # 金币数量
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


class WiuPerson(object):
    def __init__(self, tid, uid, gid, name):
        '''
        Args
            tid     :游戏中座位号
            uid     :QQ号
            gid     :游戏所在群号
            name    :群昵称或昵称
            isu     :是否为卧底
        '''
        self.tid = tid
        self.uid = uid
        self.gid = gid
        self.name = name
        self.isu = False
