import vk_api
from config import admin_id,host,user,name_db,password
from vk_api.bot_longpoll import VkBotLongPoll,VkBotEventType

def spam(id,token,group_id):
	from db import Database
	
	db=Database(host,user,password,name_db)
	group_api = vk_api.VkApi(token=token)
	
	while True:
		#Ловим нового юзера которому будем отсылать спам
		for event in VkBotLongPoll(group_api,group_id).listen():
			status=db.get_status(id)
			if status==False:
				print('return')
				return

			if event.type == VkBotEventType.GROUP_JOIN:
				#Получаем все айди спам аккаунтов из бд
				id_acc=db.get_all_id_sa()
				if len(id_acc)==0:
					continue
					print('Нету айди')
				#Запускаем цикл по всем айди наших спам аккаунтов и пытаемся отослать новому юзеру спам сообщение 
				for i in id_acc:
					#Пытаемся отослать новому юзеру спам,если это удалось завершаем цикл,если нет проходимся по всем спам акаунтом пока это не удасться
					try:
						data_group=db.get_groups(id)
						data_acc=db.get_spam_account(i)

						vk = vk_api.VkApi(token=data_acc['token'])
						vk = vk.get_api()
						vk.messages.send(user_id=event.object.user_id,random_id=0,
										message=data_group['spam_text'])
						break
					except Exception as error:
						if 'Captcha needed' in str(error):
							#Если вылезла капчы,записываем ее в бд чтобы пользователь потом мог ее снять
							db.set_captcha(data_acc['id'],True)

						if "Can't send messages for users without permission" in str(error):
							break
						
						if "Can't send messages to this user due to their privacy settings" in str(error):
							break
						continue
				'''
				Здесь будет код в случае если не смогли отправить сообщение по какой то причине!
				'''