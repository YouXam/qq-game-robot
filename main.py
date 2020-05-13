from nonebot import on_command, CommandSession
import views

import mods.wiu

bot_game = views.BotGame()
bot_game.add(mods.wiu)


@on_command('加入', only_to_me=False)
async def join(session: CommandSession):
    if session.ctx['message_type'] != "group":
        await session.send(f'此命令只在群聊中可用')
        return
    uid, gid, name = views.geti(session)
    game = session.get('game', prompt=f"[CQ:at,qq={uid}] 请输入你要加入的游戏:")
    if bot_game.groups.get(game, -1) == -1:
        await session.send(f'[CQ:at,qq={uid}] 找不到此游戏: {game}')
        return
    if bot_game.persons.get(uid):
        if bot_game.persons[uid][0] == gid:
            await session.send(f"[CQ:at,qq={uid}] 你已经加入了 “{bot_game.persons[uid][1]}” 游戏，请退出后重新加入")
        else:
            await session.send(f"[CQ:at,qq={uid}] 你已经在其他群加入了 “{bot_game.persons[uid][1]}” 游戏，请退出后重新加入")
        return
    if not bot_game.groups[game].get(gid):
        bot_game.groups[game][gid] = []
    p = bot_game.person[game](len(bot_game.groups[game][gid])+1,
                              uid, gid, name, session.ctx['sender']['nickname'])
    bot_game.groups[game][gid].append(p)
    # TODO: 游戏结束删除这一项
    bot_game.persons[uid] = (gid, game, p)
    await session.send(f"[CQ:at,qq={uid}] 加入 {game}")
    await sendlist(session, game)


@on_command('开始', only_to_me=False)
async def start(session: CommandSession):
    if session.ctx['message_type'] != "group":
        await session.send(f'此命令只在群聊中可用')
        return
    uid, gid, name = views.geti(session)
    game = session.get('game', prompt=f"[CQ:at,qq={uid}] 请输入你要开始的游戏:")
    if bot_game.groups.get(game, -1) == -1:
        await session.send(f'[CQ:at,qq={uid}] 找不到此游戏: “{game}”')
        return
    if bot_game.groups[game].get(gid, -1) == -1:
        bot_game.groups[game][gid] = []
    if not bot_game.persons.get(uid) or bot_game.persons[uid][0] != gid:
        await session.send(f'[CQ:at,qq={uid}] 你当前未在此群加入 “{game}” 游戏')
        return
    persons_length = len(bot_game.groups[game][gid])
    if persons_length < bot_game.limit[game]:
        await session.send(f'[CQ:at,qq={uid}] 人数不足， 无法开始 “{game}” 游戏')
        await sendlist(session, game)
        return
    await session.send(f'{game} 开始游戏')
    await bot_game.games[game](session, bot_game)
    await session.send(f'{game} 游戏结束')


@on_command('退出', only_to_me=False)
async def exit_game(session: CommandSession):
    if session.ctx['message_type'] != "group":
        await session.send(f'此命令只在群聊中可用')
        return
    uid, gid, name = views.geti(session)
    if not bot_game.persons.get(uid):
        await session.send(f'[CQ:at,qq={uid}] 你没有加入任何游戏')
        return
    game = bot_game.persons[uid][1]
    if gid != bot_game.persons[uid][0]:
        await session.send(f'[CQ:at,qq={uid}] 你没有在此群加入任何游戏，但在其它群加入了“{game}”游戏')
        return
    bot_game.groups[game][gid].remove(bot_game.persons[uid][2])
    await session.send(f"[CQ:at,qq={uid}] 退出了“{game}”游戏")
    await sendlist(session, game)
    del bot_game.persons[uid]


@on_command('玩家列表', only_to_me=False)
async def player_list(session: CommandSession):
    if session.ctx['message_type'] != "group":
        await session.send(f'此命令只在群聊中可用')
        return
    uid, gid, name = views.geti(session)
    game = session.get('game', prompt=f"[CQ:at,qq={uid}] 请输入你要查询的游戏:")
    if bot_game.groups.get(game, -1) == -1:
        await session.send(f'[CQ:at,qq={uid}] 找不到此游戏: “{game}”')
        return
    await sendlist(session, game)


@on_command('帮助', only_to_me=False)
async def game_help(session: CommandSession):
    game_list = list(bot_game.games.keys())
    game_list_str = "\n".join(
        f"    {i+1}.{game_list[i]}" for i in range(len(game_list)))
    await session.send(f'''帮助

命令列表

    所有命令前需加前缀 "." 或 "\\" 或 "/"

    .帮助\t\t\t:显示帮助
    .加入 <游戏>\t:加入某游戏
    .退出 <游戏>\t:退出某游戏
    .开始 <游戏>\t:开始某游戏

游戏列表

{game_list_str}
''')


@exit_game.args_parser
@join.args_parser
@start.args_parser
@player_list.args_parser
async def _parser(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['game'] = stripped_arg
        return
    session.state[session.current_key] = stripped_arg


async def sendlist(session: CommandSession, game):
    _, gid, _ = views.geti(session)
    plist = ''
    if bot_game.groups[game].get(gid, -1) == -1:
        bot_game.groups[game][gid] = []
    persons_length = len(bot_game.groups[game][gid])
    if persons_length:
        plist = "玩家列表:\n" + \
            "\n".join(
                f"  {i.tid}.{i.name}" for i in bot_game.groups[game][gid])
    await session.send(f"“{game}” 游戏\n当前共 {len(bot_game.groups[game][gid])} 人加入\n{plist}")
