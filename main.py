import vk_api
import json
from bot import bot_longpoll

with open ("config.json") as f:
	config = json.load(f)

if __name__=="__main__":
	group_api = vk_api.VkApi(token=config["token_bot"])
	bot_longpoll(group_api, config)
