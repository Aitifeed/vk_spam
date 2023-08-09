import vk_api
from keyboard import keyboards
from vk_api.longpoll import VkLongPoll,VkEventType
from vk_api.keyboard import VkKeyboard,VkKeyboardColor
from db import Database
from button_callback import ButtonAction
from threading import Thread

def bot_longpoll(group_api, config):
	try:
		db = Database(config['host'], config['user'], config['password'], config['name_db'])
		action = ButtonAction(group_api, config)
		while True:
			for event in VkLongPoll(group_api).listen():
				if event.type == VkEventType.MESSAGE_NEW and event.to_me:
					if event.user_id == config["admin_id"]:
						text = event.text
						if text == 'start' or text == 'Главное меню':
							#Создаем главные кнопки
							action.send_message(group_api,event.user_id,
									    'Привет я твой спам бот,что ты хочешь сделать?',
									    keyboards())

						if text == 'Активировать/деактивировать группу':
							#Кнопка отвечает за активацию или деактивацию группы которая будет работать для получения новых юзеров и отсылки им спам текста.
							keyboard= VkKeyboard()
							keyboard.add_button('Главное меню', VkKeyboardColor.PRIMARY)

							groups=db.get_groups()

							if len(groups['id']) == 0:
								action.send_message(group_api, event.user_id,
										'У вас нет ни одной загруженной группы!')
							else:
								#Получаем статуст активированых или деактивированных групп.
								for i in groups['id']:
									if groups['id'][i]['status'] == False:
										action.send_message(group_api, event.user_id,
												    'id-' + str(i) + ',группа-' + groups['id'][i]['name'] + ',статус деактивированна!')
									else:
										action.send_message(group_api, event.user_id, 
												    'id-'+str(i)+',группа-'+groups['id'][i]['name']+',статус активированна!')

								action.send_message(group_api, event.user_id,
										    'Отправьте id группы,чтобы активировать/деактивировать её!',
										    keyboard)				
								action.activate_deactivate(groups)

						if text == 'Посмотреть данные спам аккаунтов':
							#Выводит логин и пароль загруженых спам аккаунтов.
							accounts = db.get_spam_account()
						
							if len(accounts['id']) == 0:
								action.send_message(group_api, event.user_id,
										    'У вас нет ни одного спам аккаунта!')
							else:
								for id_acc in accounts['id']:
									action.send_message(group_api, event.user_id,
											    f'логин:%s,пароль:%s'% (accounts['id'][id_acc]['login'],accounts['id'][id_acc]['password']))

						if text == 'Удалить группу':
							keyboard = VkKeyboard()
							keyboard.add_button('Главное меню', VkKeyboardColor.PRIMARY)

							groups = db.get_groups()

							if len(groups['id']) == 0:
								action.send_message(group_api, event.user_id,
										    'У вас нет ни одной группы,чтобы удалить её.\nСначала загрузите группу!')
							else:
								for i in groups['id']:
									action.send_message(group_api, event.user_id,
											    'id-' + str(i) + ', ' + groups['id'][i]['name'])

								action.send_message(group_api, event.user_id,
										    'Отправь мне id группы из списка которую будем удалять.\nОтправлять нужно только цифры без других символов!',
										    keyboard)
								action.delete_group(groups)

						if text == 'Посмотреть спам текст групп':
							keyboard = VkKeyboard()
							keyboard.add_button('Главное меню', VkKeyboardColor.PRIMARY)

							groups = db.get_groups()

							if len(groups['id']) == 0:
								action.send_message(group_api, event.user_id,
										    'У вас нет ни одной группы,чтобы посмотреть спам текст.\nСначала загрузите группу.')
							else:
								for i in groups['id']:
									action.send_message(group_api, event.user_id,
											    'id-' + str(i) + ', ' + groups['id'][i]['name'])

								action.send_message(group_api, event.user_id,
										    'Отправь мне id группы из списка для которой будем смотреть спам текст.\nОтправлять нужно только цифры без других символов!',
										    keyboard)
								action.see_spam_text(groups)
											
						if text == 'Добавить или обновить спам текст':
							keyboard = VkKeyboard()
							keyboard.add_button('Главное меню', VkKeyboardColor.PRIMARY)
						
							groups = db.get_groups()
					
							if len(groups['id']) == 0:
								action.send_message(group_api, event.user_id,
										    'У вас нет ни одной группы,чтобы добавить/обновить спам текст.Сначала загрузите группу.')
							else:
								for i in groups['id']:
									action.send_message(group_api, event.user_id,
											    'id-' + str(i) + ', ' +groups['id'][i]['name'])

								action.send_message(group_api, event.user_id,
										    'Отправь мне id группы из списка для которой будем добавлять/обновлять спам текст.\nОтправлять нужно только цифры без других символов!',
										    keyboard)
								action.add_update_spam_text(groups)

						if text == 'Загрузить группу':
							keyboard = VkKeyboard()
							keyboard.add_button('Главное меню', VkKeyboardColor.PRIMARY)
							
							action.send_message(group_api, event.user_id,
									    'Отправь мне токен группы.',keyboard)
							action.load_group()
											
						if text == 'Загрузить спам аккаунт':
							keyboard = VkKeyboard()
							keyboard.add_button('Главное меню', VkKeyboardColor.PRIMARY)
							action.send_message(group_api, event.user_id,
									    'Отправь мне логин,пароль и токен аккаунта без пробелов в формате - log:логин,pass:пароль,token:токен.\n\nЧтобы прекратить процедуру нажмите "Главное меню".',
									    keyboard)
							action.load_spam_ac()

									
						if text == 'Проверить статус спам аккаунтов':
							#Просмотр в каком состоянии спам аккаунт,если аккаунт в бане то он автоматичеки удалеться из бд
							keyboard = VkKeyboard()
							keyboard.add_button('Главное меню', VkKeyboardColor.PRIMARY)
						
							accounts = db.get_spam_account()
						
							if len(accounts['id']) == 0:
								action.send_message(group_api, event.user_id,
										    'У вас нет ни одного спам аккаунта!Сначала загрузите их.')
							else:
								for id_acc in accounts['id']:
									try:
										vk = vk_api.VkApi(token=accounts['id'][id_acc]['token'])
										vk = vk.get_api()
										vk.account.getInfo()
										action.send_message(group_api, event.user_id,
												    'id-'+str(id_acc)+',логин:%s,пароль:%s.Состояние-ЗДОРОВ!'% (accounts['id'][id_acc]['login'],accounts['id'][id_acc]['password'])
										)
									except Exception as error:
										print(error)
										if 'invalid access_token' in str(error):
									
											action.send_message(group_api, event.user_id,
													    'id-'+str(id_acc)+',логин:%s,пароль:%s.Состояние-НЕПРАВИЛЬНЫЙ ТОКЕН!'% (accounts['id'][id_acc]['login'],accounts['id'][id_acc]['password'])
											)
							
										if 'user is blocked' in str(error):
											db.del_spam_account(id_acc)

										if 'Captcha needed' in str(error):
											action.send_message(group_api, event.user_id,
													    'id-'+str(id_acc)+',логин:%s,пароль:%s.Состояние-НУЖНО ВВЕСТИ КАПЧУ!'% (accounts['id'][id_acc]['login'],accounts['id'][id_acc]['password'])
											)

						if text == 'Удалить спам аккаунт':
							keyboard = VkKeyboard()
							keyboard.add_button('Главное меню', VkKeyboardColor.PRIMARY)
						
							accounts = db.get_spam_account()
						
							if len(accounts['id']) == 0:
								action.send_message(group_api, event.user_id,
										    'У вас нет ни одного спам аккаунта,чтобы его удалить!')
							else:
								for id_acc in accounts['id']:
									action.send_message(group_api, event.user_id,
											    'id-{str(id_acc)},логин:%s,пароль:%s.'% (accounts['id'][id_acc]['login'],accounts['id'][id_acc]['password']))

								action.send_message(group_api, event.user_id,
										    'Отправь id аккаунта,чтобы его удалить.Чтобы прекратить процедуру нажмите "Главное меню".',
										    keyboard)
								action.download_spam_ac(accounts)

											
						if text == 'Начать работу':
							#Считываем активированные группы для работы и запускам функцию spam для этих групп через потоки
							keyboard = VkKeyboard()
							keyboard.add_button('Главное меню', VkKeyboardColor.PRIMARY)
							groups = db.get_active_groups()

							if len(groups['id']) == 0:
								action.send_message(group_api, event.user_id,
										    'Нет активированных груп!Пожалуйста активруйте группы и повторите процедуру!')
							else:
								for i in groups['id']:
			 						Thread(target=ButtonAction.spam,
									       args=(i, groups['id'][i]['token'], 
										     groups['id'][i]['group_id'], 
										config)).start()
		 						
			 						action.send_message(group_api, event.user_id,
											    'Работа рассылок в группе - ' + groups['id'][i]['name'] + ' началась!')
	except Exception as error:
		print(error)
		bot_longpoll(group_api, config)
