from nonebot import on_command, CommandSession
from views import WiuPerson
import funcs


# 谁是卧底 游戏逻辑
async def wiu(session: CommandSession):
    pass

groups = {"谁是卧底": {}}  # 保存玩家列表
persons = {}  # 保存玩家当前游戏信息
limit = {"谁是卧底": 1}  # 每个游戏的最小游玩人数
games = {"谁是卧底": wiu}  # 游戏逻辑函数
person = {"谁是卧底": WiuPerson}  # 每个游戏对应的玩家类


@on_command('加入游戏', only_to_me=False)
async def join(session: CommandSession):
    if session.ctx['message_type'] != "group":
        await session.send(f'此命令只在群聊中可用')
        return
    uid, gid, name = funcs.geti(session)
    game = session.get('game', prompt=f"[CQ:at,qq={uid}] 请输入你要加入的游戏:")
    if groups.get(game, -1) == -1:
        await session.send(f'[CQ:at,qq={uid}] 找不到此游戏: {game}')
        return
    if persons.get(uid):
        if persons[uid][0] == gid:
            await session.send(f"[CQ:at,qq={uid}] 你已经加入了 “{persons[uid][1]}” 游戏，请退出后重新加入")
        else:
            await session.send(f"[CQ:at,qq={uid}] 你已经在其他群加入了 “{persons[uid][1]}” 游戏，请退出后重新加入")
        return
    if not groups[game].get(gid):
        groups[game][gid] = []
    p = person[game](len(groups[game][gid])+1, uid, gid, name)
    groups[game][gid].append(p)
    # TODO: 游戏结束删除这一项
    persons[uid] = (gid, game, p)
    await session.send(f"[CQ:at,qq={uid}] 加入 {game}")
    await sendlist(session, game)


@on_command('开始游戏', only_to_me=False)
async def start(session: CommandSession):
    if session.ctx['message_type'] != "group":
        await session.send(f'此命令只在群聊中可用')
        return
    uid, gid, name = funcs.geti(session)
    game = session.get('game', prompt=f"[CQ:at,qq={uid}] 请输入你要开始的游戏:")
    if groups.get(game, -1) == -1:
        await session.send(f'[CQ:at,qq={uid}] 找不到此游戏: “{game}”')
        return
    if groups[game].get(gid, -1) == -1:
        groups[game][gid] = []
    persons_length = len(groups[game][gid])
    if persons_length < limit[game]:
        await session.send(f'[CQ:at,qq={uid}] 人数不足， 无法开始 “{game}” 游戏')
        await sendlist(session, game)
        return
    await session.send(f'{game} 开始游戏')
    await games[game](session)
    await session.send(f'{game} 游戏结束')


@on_command('退出游戏', only_to_me=False)
async def exit_game(session: CommandSession):
    if session.ctx['message_type'] != "group":
        await session.send(f'此命令只在群聊中可用')
        return
    uid, gid, name = funcs.geti(session)
    if not persons.get(uid):
        await session.send(f'[CQ:at,qq={uid}] 你没有加入任何游戏')
        return
    game = persons[uid][1]
    if gid != persons[uid][0]:
        await session.send(f'[CQ:at,qq={uid}] 你没有在此群加入任何游戏，但在其它群加入了“{game}”游戏')
        return
    groups[game][gid].remove(persons[uid][2])
    await session.send(f"[CQ:at,qq={uid}] 退出了“{game}”游戏")
    await sendlist(session, game)
    del persons[uid]


@on_command('玩家列表', only_to_me=False)
async def player_list(session: CommandSession):
    if session.ctx['message_type'] != "group":
        await session.send(f'此命令只在群聊中可用')
        return
    uid, gid, name = funcs.geti(session)
    game = session.get('game', prompt=f"[CQ:at,qq={uid}] 请输入你要查询的游戏:")
    if groups.get(game, -1) == -1:
        await session.send(f'[CQ:at,qq={uid}] 找不到此游戏: “{game}”')
        return
    await sendlist(session, game)


@exit_game.args_parser
@join.args_parser
@start.args_parser
async def _parser(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['game'] = stripped_arg
        return
    session.state[session.current_key] = stripped_arg


async def sendlist(session: CommandSession, game):
    _, gid, _ = funcs.geti(session)
    plist = ''
    if groups[game].get(gid, -1) == -1:
        groups[game][gid] = []
    persons_length = len(groups[game][gid])
    if persons_length:
        plist = "玩家列表:\n" + \
            "\n".join(f"  {i.tid}.{i.name}" for i in groups[game][gid])
    await session.send(f"“{game}” 游戏\n当前共 {len(groups[game][gid])} 人加入\n{plist}")
