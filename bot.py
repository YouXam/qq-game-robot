import nonebot
import config
if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugin('main')
    nonebot.run(host='172.18.0.1', port=8080)
