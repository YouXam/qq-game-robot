def geti(session):
    return session.ctx['sender']['user_id'], session.ctx['group_id'], (session.ctx['sender']['card'] if session.ctx['sender']['card'] else session.ctx['sender']['nickname'])
