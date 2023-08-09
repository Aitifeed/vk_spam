from db import Database
import vk_api
from vk_api.longpoll import VkLongPoll,VkEventType
from vk_api.keyboard import VkKeyboard,VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll,VkBotEventType

class ButtonAction:

	def __init__(self, group_api,config):
		self.group_api = group_api
		self.config = config
		self.db = Database(config['host'], config['user'], config['password'], config['name_db'])

	@staticmethod 
	def send_message(group_api, user_id, message,keyboard=None):
		post={
			"user_id":user_id,
			"message":message,
			"random_id":0,
		}
	
		if keyboard != None:
			post['keyboard'] = keyboard.get_keyboard()


		group_api.method("messages.send",post)

	@staticmethod
	def spam(id, token, group_id, config):
		group_api = vk_api.VkApi(token=token)
		db = Database(config['host'], config['user'], config['password'], config['name_db'])
		while True:
			#Ловим нового юзера которому будем отсылать спам
			for event in VkBotLongPoll(group_api,group_id).listen():
				status=db.get_status(id)
				#Если группа деактивирована выходим из потока.
				if status == False:
					return
				if event.type == VkBotEventType.GROUP_JOIN:
					#Получаем все айди спам аккаунтов из бд
					id_acc = db.get_all_id_sa()
					if len(id_acc) == 0:
						continue
					#Запускаем цикл по всем айди наших спам аккаунтов и пытаемся отослать новому юзеру спам сообщение 
					for i in id_acc:
						#Пытаемся отослать новому юзеру спам,если это удалось завершаем цикл,если нет проходимся по всем спам акаунтом пока это не удасться
						try:
							data_group = db.get_groups(id)
							data_acc = db.get_spam_account(i)

							vk = vk_api.VkApi(token=data_acc['token'])
							vk = vk.get_api()
							vk.messages.send(user_id=event.object.user_id, random_id=0,
											message=data_group['spam_text'])
							break
						except Exception as error:
							if 'Captcha needed' in str(error):
								#Если вылезла капча,записываем ее в бд чтобы пользователь потом мог ее снять
								db.set_captcha(data_acc['id'], True)

							if "Can't send messages for users without permission" in str(error):
								break
						
							if "Can't send messages to this user due to their privacy settings" in str(error):
								break
							continue

	def activate_deactivate(self,groups):
		for event in VkLongPoll(self.group_api).listen():
			if event.type == VkEventType.MESSAGE_NEW and event.to_me:
				if event.user_id == self.config["admin_id"]:
					text = event.text
					if text == 'start' or text == 'Главное меню':					
						return
					else:
						try:
							id_group = int(text)
							if id_group not in groups['id']:
								ButtonAction.send_message(self.group_api, event.user_id, 
											  'Такого айди нет!\nПожалуйста внимательно посмотрите на id в списке групп и отправьте правильный id!')
							else:
								#Меняем статус группы в бд и отправляем сообещние о статусе группы
								self.db.change_status(id_group)
								name_group = groups['id'][id_group]['name']
								data_group = self.db.get_groups()
								status = self.db.get_status(id_group)

								if status == True:
									ButtonAction.send_message(self.group_api, event.user_id, 
												  'Группа - ' + name_group + ',успешно активированна!\nМожете дальше отправлять id,чтобы активировать/деактивировать группы или нажать "Главное меню",чтобы прекратить процедуру.')						
								else:
									ButtonAction.send_message(self.group_api, event.user_id, 
												  'Группа - ' + name_group + ',успешно деактивированна!\nМожете дальше отправлять id,чтобы активировать/деактивировать группы или нажать "Главное меню",чтобы прекратить процедуру.')						
						except:
							ButtonAction.send_message(self.group_api, event.user_id, 
										  'Неправильный формат айди,нужно отправлять только цифры без символов!')

	def delete_group(self,groups):
		for event in VkLongPoll(self.group_api).listen():
			if event.type == VkEventType.MESSAGE_NEW and event.to_me:
				if event.user_id == self.config["admin_id"]:
					text = event.text
					if text == 'start' or text == 'Главное меню':
						return
					else:
						try:
							id_group = int(text)
							if id_group not in groups['id']:
								ButtonAction.send_message(self.group_api, event.user_id, 
											  'Такого айди нет!\nПожалуйста внимательно посмотрите на id в списке групп и отправьте правильный id!')
							else:
								self.db.del_group(id_group)
								name_group = groups['id'][id_group]['name']
								data_group = self.db.get_groups()
								if len(data_group['id']) == 0:
									ButtonAction.send_message(self.group_api, event.user_id, 
												  'Группа - ' + name_group + ',успешно удалена!')
									return
								else:
									ButtonAction.send_message(self.group_api, event.user_id, 
												  'Группа - ' + name_group + ',успешно удалена!\nМожете дальше отправлять id,чтобы удалять группы или нажать "Главное меню",чтобы прекратить процедуру удаления.')
						except:
							ButtonAction.send_message(self.group_api, event.user_id, 
										  'Неправильный формат айди,нужно отправлять только цифры без символов!')

	def see_spam_text(self,groups):
		for event in VkLongPoll(self.group_api).listen():
			if event.type == VkEventType.MESSAGE_NEW and event.to_me:
				if event.user_id == self.config["admin_id"]:
					text = event.text
					if text == 'start' or text == 'Главное меню':
						return
					else:
						try:
							id_group = int(text)
							if id_group not in groups['id']:
								ButtonAction.send_message(self.group_api, event.user_id,
											  'Такого айди нет!\nПожалуйста внимательно посмотрите на id в списке групп и отправьте правильный id!')
							else:
								spam_text = groups['id'][id_group]['spam_text']
								name_group = groups['id'][id_group]['name']
								if spam_text == None:
									ButtonAction.send_message(self.group_api, event.user_id, 
												  'Для группы ' + name_group + ' нет спам текста!\n\nВы можите дальше отправлять id группы или нажать кнопку "Главное меню",чтобы вернуться.' )
								else:
									ButtonAction.send_message(self.group_api, event.user_id, 
												  'Cпам текст для группы - ' + name_group + ':\n\n'+spam_text)
						except Exception as error:
							ButtonAction.send_message(self.group_api, event.user_id, 
										  'Неправильный формат айди,нужно отправлять только цифры без символов!')

	def add_update_spam_text(self,groups):
		for event in VkLongPoll(self.group_api).listen():
			if event.type == VkEventType.MESSAGE_NEW and event.to_me:
				if event.user_id == self.config["admin_id"]:
					if event.text == 'start' or event.text == 'Главное меню':
						return
					else:
						try:
							if event.text == spam_text:
								continue
						except:
							text=event.text

						try:
							id_group = int(event.text)
							if id_group not in groups['id']:
								ButtonAction.send_message(self.group_api, event.user_id, 
											  'Такого айди нет!\nПожалуйста внимательно посмотрите на id в списке групп и отправьте правильный id.')	
							else:
								name_group = groups['id'][id_group]['name']
								ButtonAction.send_message(self.group_api, event.user_id, 
											  'Отправь спам текст для группы - '+name_group)
								
								for event in VkLongPoll(self.group_api).listen():
									if event.type == VkEventType.MESSAGE_NEW and event.to_me:
										if event.user_id == self.config["admin_id"]:
											spam_text = event.text
											if event.text == 'start' or event.text == 'Главное меню':
												return
											else:
												self.db.add_spam_text(id_group, spam_text)
												ButtonAction.send_message(self.group_api, event.user_id, 
															  'Спам текст для группы "'+name_group+'",успешно добавлен/обновлен!\n\nМожете дальше отправлять id группы,чтобы добавить спам текст или нажать кнопку "Главное меню",чтобы прекратить эту процедуру.')
												break

						except Exception as error:
							print(error)
							ButtonAction.send_message(self.group_api, event.user_id, 
										  'Неправильный формат айди,нужно отправлять только цифры без символов!')

	def load_group(self):
		for event in VkLongPoll(self.group_api).listen():
			if event.type == VkEventType.MESSAGE_NEW and event.to_me:
				if event.user_id == self.config["admin_id"]:
					if event.text == 'Главное меню' or event.text=='start':
						return
					else:
						try:
							#Проверяем валидность токена и загружаем токен группы в бд
							group = vk_api.VkApi(token=event.text)
							group = group.get_api()
							data = group.groups.getById()
									
							self.db.add_group_spam(data[0]['id'], data[0]['name'], event.text)

							ButtonAction.send_message(self.group_api, event.user_id, 
										  'Группа:' + data[0]['name'] + ' успешно загружена!\n\nМожете дальше отправлять токен другой группы,чтобы ее загрузить или нажать "Главное меню",чтобы отменить процедуру загрузки групп.')

						except Exception as error:
							print(error)
							ButtonAction.send_message(self.group_api, event.user_id, 
										  'Неправильный токен!Возможно вы допустили ошибку добавив какой-нибудь символ или проблел.\n\nПожалуйста отправьте коректный токен!\n\nЧтобы прекратить процедуру загрузки групп,нажмите на кнопку "Главное меню".')

	def load_spam_ac(self):
		for event in VkLongPoll(self.group_api).listen():
			if event.type == VkEventType.MESSAGE_NEW and event.to_me:
				if event.user_id == self.config["admin_id"]:		
					if event.text == 'Главное меню' or event.text=='start':
						return
					else:
						data = event.text
						log = data.find('log')
						pas = data.find('pass')
						token = data.find('token')
					
						if log == -1 or pas == -1 or token == -1:
							ButtonAction.send_message(self.group_api, event.user_id, 
										  'Неправильный формат для загрузки данных!Возможно вы где то ошиблись.\nФормат данных должен быть без пробелов в такой форме - log:логин,pass:пароль,token:токен')
							continue

						log = data[log+4:pas-1]
						pas = data[pas+5:token-1]
						token = data[token+6:]

						try:	
							#Пробуем войти в спам аккаунт,если все ок загружаем акк в бд и переносим пользователя в главное меню,если нет отправялем ошибку того почему не можем загрузить спам аккаунт 
							vk = vk_api.VkApi(token=token)
							vk = vk.get_api()
							vk.account.getInfo()
											
							self.db.add_spam_account(log, pas, token)
										
							ButtonAction.send_message(self.group_api, event.user_id, 
										  'Данные аккаунта успешно загружены\\n Можете дальше отправлять данные аккаунта.Чтобы прекратить процедуру нажмите "Главное меню"')
						except Exception as error:
							print(error)
							if 'invalid access_token' in str(error):				
								ButtonAction.send_message(self.group_api, event.user_id, 
											  'Неправильный токен! Пожалуйста проверьте правльность токена и повторить процедуру!')
						
							if 'user is blocked' in str(error):
								ButtonAction.send_message(self.group_api, event.user_id, 
											  'Данный аккаунт заблокирован!')

	def download_spam_ac(self,accounts):
		for event in VkLongPoll(self.group_api).listen():
			if event.type == VkEventType.MESSAGE_NEW and event.to_me:
				if event.user_id == self.config["admin_id"]:
					if event.text == 'Главное меню' or event.text=='start':
						return
					else:
						try:
							id_acc = int(event.text)
							if id_acc not in accounts['id']:
								ButtonAction.send_message(self.group_api, event.user_id, 
											  'Аккаунтов под id-' + str(id_acc) + ' нет!Внимательно смотрите на список id спам аккаунтов!')
							else:
								self.db.del_spam_account(id_acc)
								ButtonAction.send_message(self.group_api, event.user_id, 
											  'Аккаунт под id-' + str(id_acc) + ' успешно удален!')

						except:
							ButtonAction.send_message(self.group_api, event.user_id, 
										  'Не могу найти такой id,возможно вы ошиблись.\nОтправьте коректный id!')
