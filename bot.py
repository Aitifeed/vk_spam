import vk_api
from vk_api.keyboard import VkKeyboard,VkKeyboardColor
from vk_api.longpoll import VkLongPoll,VkEventType
from db import Database
from threading import Thread
from action import spam,send_message
 
def bot_longpoll(group_api):
	try:
		while True:
			for event in VkLongPoll(group_api).listen():
				if event.type == VkEventType.MESSAGE_NEW and event.to_me:
					if event.user_id == admin_id:
						text = event.text
						if text == 'start' or text == 'Главное меню':
							#Создаем главные кнопки
							keyboard= VkKeyboard()
							keyboard.add_button('Начать работу',VkKeyboardColor.NEGATIVE)	
							keyboard.add_button('Активировать/деактивировать группу',VkKeyboardColor.NEGATIVE)
							keyboard.add_line()
							keyboard.add_button('Посмотреть спам текст групп',VkKeyboardColor.PRIMARY)
							keyboard.add_line()
							keyboard.add_button('Посмотреть данные спам аккаунтов',VkKeyboardColor.PRIMARY)
							keyboard.add_line()
							keyboard.add_button('Проверить статус спам аккаунтов',VkKeyboardColor.PRIMARY)
							keyboard.add_line()
							keyboard.add_button('Загрузить группу',VkKeyboardColor.PRIMARY)
							keyboard.add_button('Удалить группу',VkKeyboardColor.PRIMARY)
							keyboard.add_line()
							keyboard.add_button('Добавить или обновить спам текст',VkKeyboardColor.PRIMARY)
							keyboard.add_line()
							keyboard.add_button('Загрузить спам аккаунт',VkKeyboardColor.PRIMARY)
							keyboard.add_button('Удалить спам аккаунт',VkKeyboardColor.PRIMARY)

							send_message(group_api,event.user_id,'Привет я твой спам бот,что ты хочешь сделать?',keyboard)

						if text=='Активировать/деактивировать группу':
							#Кнопка отвечает за активацию или деактивацию группы которая будет работать для получения новых юзеров и отсылки им спам текста.
							keyboard= VkKeyboard()
							keyboard.add_button('Главное меню',VkKeyboardColor.PRIMARY)

							db=Database(host,user,password,name_db)
							groups=db.get_groups()

							if len(groups['id'])==0:
								send_message(group_api,event.user_id,'У вас нет ни одной загруженной группы!')
							else:
								#Получаем статуст активированых или деактивированных групп.
								for i in groups['id']:
									if groups['id'][i]['status']==False:
										send_message(group_api,event.user_id,'id-'+str(i)+',группа-'+groups['id'][i]['name']+',статус деактивированна!')
									else:
										send_message(group_api,event.user_id,'id-'+str(i)+',группа-'+groups['id'][i]['name']+',статус активированна!')

								send_message(group_api,event.user_id,'Отправьте id группы,чтобы активировать/деактивировать её!',keyboard)				

								for event in VkLongPoll(group_api).listen():
									if event.type == VkEventType.MESSAGE_NEW and event.to_me:
										if event.user_id == admin_id:
											text = event.text
											if text == 'start' or text == 'Главное меню':
												keyboard= VkKeyboard()
												keyboard.add_button('Начать спам',VkKeyboardColor.NEGATIVE)	
												keyboard.add_line()
												keyboard.add_button('Посмотреть спам текст групп',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Посмотреть данные спам аккаунтов',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Проверить статус спам аккаунтов',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Загрузить группу',VkKeyboardColor.PRIMARY)
												keyboard.add_button('Удалить группу',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Добавить или обновить спам текст',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Загрузить спам аккаунт',VkKeyboardColor.PRIMARY)
												keyboard.add_button('Удалить спам аккаунт',VkKeyboardColor.PRIMARY)

												break
											else:
												try:
													id_group=int(text)

													if id_group not in groups['id']:
														send_message(group_api,event.user_id,'Такого айди нет!\nПожалуйста внимательно посмотрите на id в списке групп и отправьте правильный id!')
													else:
														#Меняем статус группы в бд и отправляем сообещние о статусе группы
														db.change_status(id_group)
														name_group=groups['id'][id_group]['name']
														data_group=db.get_groups()
														status=db.get_status(id_group)

														if status==True:
															send_message(group_api,event.user_id,'Группа - '+name_group+',успешно активированна!\nМожете дальше отправлять id,чтобы активировать/деактивировать группы или нажать "Главное меню",чтобы прекратить процедуру.')
														
														else:
															send_message(group_api,event.user_id,'Группа - '+name_group+',успешно деактивированна!\nМожете дальше отправлять id,чтобы активировать/деактивировать группы или нажать "Главное меню",чтобы прекратить процедуру.')
												
												except:
													send_message(group_api,event.user_id,'Неправильный формат айди,нужно отправлять только цифры без символов!')
					
						if text=='Посмотреть данные спам аккаунтов':
							#Выводит логин и пароль загруженых спам аккаунтов.
							db=Database(host,user,password,name_db)
							accounts=db.get_spam_account()
						
							if len(accounts['id'])==0:
								send_message(group_api,event.user_id,'У вас нет ни одного спам аккаунта!')
							else:
								for id_acc in accounts['id']:
									send_message(group_api,event.user_id,
												f'логин:%s,пароль:%s'% (accounts['id'][id_acc]['login'],accounts['id'][id_acc]['password'])
									)

						if text=='Удалить группу':
							keyboard= VkKeyboard()
							keyboard.add_button('Главное меню',VkKeyboardColor.PRIMARY)

							db=Database(host,user,password,name_db)
							groups=db.get_groups()

							if len(groups['id'])==0:
								send_message(group_api,event.user_id,'У вас нет ни одной группы,чтобы удалить её.\nСначала загрузите группу!')
							else:
								for i in groups['id']:
									send_message(group_api,event.user_id,'id-'+str(i)+', '+groups['id'][i]['name'])

								send_message(group_api,event.user_id,'Отправь мне id группы из списка которую будем удалять.\nОтправлять нужно только цифры без других символов!',keyboard)

								for event in VkLongPoll(group_api).listen():
									if event.type == VkEventType.MESSAGE_NEW and event.to_me:
										if event.user_id == admin_id:
											text = event.text
											if text == 'start' or text == 'Главное меню':
												keyboard= VkKeyboard()
												keyboard.add_button('Начать спам',VkKeyboardColor.NEGATIVE)	
												keyboard.add_line()
												keyboard.add_button('Посмотреть спам текст групп',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Посмотреть данные спам аккаунтов',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Проверить статус спам аккаунтов',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Загрузить группу',VkKeyboardColor.PRIMARY)
												keyboard.add_button('Удалить группу',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Добавить или обновить спам текст',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Загрузить спам аккаунт',VkKeyboardColor.PRIMARY)
												keyboard.add_button('Удалить спам аккаунт',VkKeyboardColor.PRIMARY)

												break
											else:
												try:
													id_group=int(text)
													if id_group not in groups['id']:
														send_message(group_api,event.user_id,'Такого айди нет!\nПожалуйста внимательно посмотрите на id в списке групп и отправьте правильный id!')
													else:
														db.del_group(id_group)
														name_group=groups['id'][id_group]['name']
														data_group=db.get_groups()
														if len(data_group['id'])==0:
															send_message(group_api,event.user_id,'Группа - '+name_group+',успешно удалена!',keyboard)
															break
														else:
															send_message(group_api,event.user_id,'Группа - '+name_group+',успешно удалена!\nМожете дальше отправлять id,чтобы удалять группы или нажать "Главное меню",чтобы прекратить процедуру удаления.')
												
												except:
													send_message(group_api,event.user_id,'Неправильный формат айди,нужно отправлять только цифры без символов!')

						if text=='Посмотреть спам текст групп':
							keyboard= VkKeyboard()
							keyboard.add_button('Главное меню',VkKeyboardColor.PRIMARY)

							db=Database(host,user,password,name_db)
							groups=db.get_groups()

							if len(groups['id'])==0:
								send_message(group_api,event.user_id,'У вас нет ни одной группы,чтобы посмотреть спам текст.\nСначала загрузите группу.')
							else:
								for i in groups['id']:
									send_message(group_api,event.user_id,f'id-'+str(i)+', '+groups['id'][i]['name'])

								send_message(group_api,event.user_id,'Отправь мне id группы из списка для которой будем смотреть спам текст.\nОтправлять нужно только цифры без других символов!',keyboard)

								for event in VkLongPoll(group_api).listen():
									if event.type == VkEventType.MESSAGE_NEW and event.to_me:
										if event.user_id == admin_id:
											text = event.text
											if text == 'start' or text == 'Главное меню':
												keyboard= VkKeyboard()
												keyboard.add_button('Начать спам',VkKeyboardColor.NEGATIVE)	
												keyboard.add_line()
												keyboard.add_button('Посмотреть спам текст групп',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Посмотреть данные спам аккаунтов',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Проверить статус спам аккаунтов',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Загрузить группу',VkKeyboardColor.PRIMARY)
												keyboard.add_button('Удалить группу',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Добавить или обновить спам текст',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Загрузить спам аккаунт',VkKeyboardColor.PRIMARY)
												keyboard.add_button('Удалить спам аккаунт',VkKeyboardColor.PRIMARY)

												break
											else:
												try:
													id_group=int(text)
													if id_group not in groups['id']:
														send_message(group_api,event.user_id,'Такого айди нет!\nПожалуйста внимательно посмотрите на id в списке групп и отправьте правильный id!')
										
													else:
														spam_text=groups['id'][id_group]['spam_text']
														name_group=groups['id'][id_group]['name']
														if spam_text==None:
															send_message(group_api,event.user_id,'Для группы '+name_group+' нет спам текста!\n\nВы можите дальше отправлять id группы или нажать кнопку "Главное меню",чтобы вернуться.' )
														else:
															send_message(group_api,event.user_id,'Cпам текст для группы - '+name_group+':\n\n'+spam_text)
											
												except Exception as error:
													send_message(group_api,event.user_id,'Неправильный формат айди,нужно отправлять только цифры без символов!')
											
						if text== 'Добавить или обновить спам текст':
							keyboard= VkKeyboard()
							keyboard.add_button('Главное меню',VkKeyboardColor.PRIMARY)
						
							db=Database(host,user,password,name_db)
							groups=db.get_groups()
					
							if len(groups['id'])==0:
								send_message(group_api,event.user_id,'У вас нет ни одной группы,чтобы добавить/обновить спам текст.Сначала загрузите группу.')
							else:
								for i in groups['id']:
									send_message(group_api,event.user_id,'id-'+str(i)+', '+groups['id'][i]['name'])

								send_message(group_api,event.user_id,'Отправь мне id группы из списка для которой будем добавлять/обновлять спам текст.\nОтправлять нужно только цифры без других символов!',keyboard)

								for event in VkLongPoll(group_api).listen():
									if event.type == VkEventType.MESSAGE_NEW and event.to_me:
										if event.user_id == admin_id:
											if event.text == 'start' or event.text == 'Главное меню':
												keyboard= VkKeyboard()
												keyboard.add_button('Начать спам',VkKeyboardColor.NEGATIVE)	
												keyboard.add_line()
												keyboard.add_button('Посмотреть спам текст групп',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Посмотреть данные спам аккаунтов',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Проверить статус спам аккаунтов',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Загрузить группу',VkKeyboardColor.PRIMARY)
												keyboard.add_button('Удалить группу',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Добавить или обновить спам текст',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Загрузить спам аккаунт',VkKeyboardColor.PRIMARY)
												keyboard.add_button('Удалить спам аккаунт',VkKeyboardColor.PRIMARY)

												break
											else:
												try:
													text = event.text
													if spam_text==text:
														continue
												except:
													text = event.text
										
												try:
													id_group=int(text)
													if id_group not in groups['id']:
														send_message(group_api,event.user_id,'Такого айди нет!\nПожалуйста внимательно посмотрите на id в списке групп и отправьте правильный id.')
												
													else:
														name_group=groups['id'][id_group]['name']
														send_message(group_api,event.user_id,'Отправь спам текст для группы - '+name_group)
														for event in VkLongPoll(group_api).listen():
															if event.type == VkEventType.MESSAGE_NEW and event.to_me:
																if event.user_id == admin_id:
																	spam_text = event.text
																	if event.text == 'start' or event.text == 'Главное меню':
																		keyboard= VkKeyboard()
																		keyboard.add_button('Начать спам',VkKeyboardColor.NEGATIVE)	
																		keyboard.add_line()
																		keyboard.add_button('Посмотреть спам текст групп',VkKeyboardColor.PRIMARY)
																		keyboard.add_line()
																		keyboard.add_button('Посмотреть данные спам аккаунтов',VkKeyboardColor.PRIMARY)
																		keyboard.add_line()
																		keyboard.add_button('Проверить статус спам аккаунтов',VkKeyboardColor.PRIMARY)
																		keyboard.add_line()
																		keyboard.add_button('Загрузить группу',VkKeyboardColor.PRIMARY)
																		keyboard.add_button('Удалить группу',VkKeyboardColor.PRIMARY)
																		keyboard.add_line()
																		keyboard.add_button('Добавить или обновить спам текст',VkKeyboardColor.PRIMARY)
																		keyboard.add_line()
																		keyboard.add_button('Загрузить спам аккаунт',VkKeyboardColor.PRIMARY)
																		keyboard.add_button('Удалить спам аккаунт',VkKeyboardColor.PRIMARY)

																		break
																	else:
																		db.add_spam_text(id_group,spam_text)
																		send_message(group_api,event.user_id,'Спам текст для группы "'+name_group+'",успешно добавлен/обновлен!\n\nМожете дальше отправлять id группы,чтобы добавить спам текст или нажать кнопку "Главное меню",чтобы прекратить эту процедуру.')
						
																		break

												except:
													send_message(group_api,event.user_id,'Неправильный формат айди,нужно отправлять только цифры без символов!')


						if text== 'Загрузить группу':
							keyboard= VkKeyboard()
							keyboard.add_button('Главное меню',VkKeyboardColor.PRIMARY)
							
							send_message(group_api,event.user_id,'Отправь мне токен группы.',keyboard)

							for event in VkLongPoll(group_api).listen():
								if event.type == VkEventType.MESSAGE_NEW and event.to_me:
									if event.user_id == admin_id:
										if event.text == 'Главное меню' or event.text=='start':
											keyboard= VkKeyboard()
											keyboard.add_button('Начать спам',VkKeyboardColor.NEGATIVE)	
											keyboard.add_line()
											keyboard.add_button('Посмотреть спам текст групп',VkKeyboardColor.PRIMARY)
											keyboard.add_line()
											keyboard.add_button('Посмотреть данные спам аккаунтов',VkKeyboardColor.PRIMARY)
											keyboard.add_line()
											keyboard.add_button('Проверить статус спам аккаунтов',VkKeyboardColor.PRIMARY)
											keyboard.add_line()
											keyboard.add_button('Загрузить группу',VkKeyboardColor.PRIMARY)
											keyboard.add_button('Удалить группу',VkKeyboardColor.PRIMARY)
											keyboard.add_line()
											keyboard.add_button('Добавить или обновить спам текст',VkKeyboardColor.PRIMARY)
											keyboard.add_line()
											keyboard.add_button('Загрузить спам аккаунт',VkKeyboardColor.PRIMARY)
											keyboard.add_button('Удалить спам аккаунт',VkKeyboardColor.PRIMARY)

											break

										else:
											try:
												#Проверяем валидность токена и загружаем токен группы в бд
												group=vk_api.VkApi(token=event.text)
												group=group.get_api()
												data=group.groups.getById()
									
												db=Database(host,user,password,name_db)
												db.add_group_spam(data[0]['id'],data[0]['name'],event.text)

												send_message(group_api,event.user_id,'Группа:'+data[0]['name']+' успешно загружена!\n\nМожете дальше отправлять токен другой группы,чтобы ее загрузить или нажать "Главное меню",чтобы отменить процедуру загрузки групп.')

											except Exception as error:
										 		print(error)
										 		send_message(group_api,event.user_id,'Неправильный токен!Возможно вы допустили ошибку добавив какой-нибудь символ или проблел.\n\nПожалуйста отправьте коректный токен!\n\nЧтобы прекратить процедуру загрузки групп,нажмите на кнопку "Главное меню".')
											
						if text=='Загрузить спам аккаунт':
							keyboard= VkKeyboard()
							keyboard.add_button('Главное меню',VkKeyboardColor.PRIMARY)
							send_message(group_api,event.user_id,'Отправь мне логин,пароль и токен аккаунта без пробелов в формате - log:логин,pass:пароль,token:токен.\n\nЧтобы прекратить процедуру нажмите "Главное меню".',keyboard)

							for event in VkLongPoll(group_api).listen():
								if event.type == VkEventType.MESSAGE_NEW and event.to_me:
									if event.user_id == admin_id:								
										if event.text == 'Главное меню' or event.text=='start':
											keyboard= VkKeyboard()
											keyboard.add_button('Начать спам',VkKeyboardColor.NEGATIVE)	
											keyboard.add_line()
											keyboard.add_button('Посмотреть спам текст групп',VkKeyboardColor.PRIMARY)
											keyboard.add_line()
											keyboard.add_button('Посмотреть данные спам аккаунтов',VkKeyboardColor.PRIMARY)
											keyboard.add_line()
											keyboard.add_button('Проверить статус спам аккаунтов',VkKeyboardColor.PRIMARY)
											keyboard.add_line()
											keyboard.add_button('Загрузить группу',VkKeyboardColor.PRIMARY)
											keyboard.add_button('Удалить группу',VkKeyboardColor.PRIMARY)
											keyboard.add_line()
											keyboard.add_button('Добавить или обновить спам текст',VkKeyboardColor.PRIMARY)
											keyboard.add_line()
											keyboard.add_button('Загрузить спам аккаунт',VkKeyboardColor.PRIMARY)
											keyboard.add_button('Удалить спам аккаунт',VkKeyboardColor.PRIMARY)
							
											break
										else:
											data=event.text
											log=data.find('log')
											pas=data.find('pass')
											token=data.find('token')
											
											if log==-1 or pas==-1 or token==-1:
												keyboard= VkKeyboard()
												keyboard.add_button('Начать спам',VkKeyboardColor.NEGATIVE)	
												keyboard.add_line()
												keyboard.add_button('Посмотреть спам текст групп',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Посмотреть данные спам аккаунтов',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Проверить статус спам аккаунтов',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Загрузить группу',VkKeyboardColor.PRIMARY)
												keyboard.add_button('Удалить группу',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Добавить или обновить спам текст',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Загрузить спам аккаунт',VkKeyboardColor.PRIMARY)
												keyboard.add_button('Удалить спам аккаунт',VkKeyboardColor.PRIMARY)

												send_message(group_api,event.user_id,'Неправильный формат для загрузки данных!Возможно вы где то ошиблись.\nФормат данных должен быть без пробелов в такой форме - log:логин,pass:пароль,token:токен',keyboard)

												continue

											log=data[log+4:pas-1]
											pas=data[pas+5:token-1]
											token=data[token+6:]

											try:	
												#Пробуем войти в спам аккаунт,если все ок загружаем акк в бд и переносим пользователя в главное меню,если нет отправялем ошибку того почему не можем загрузить спам аккаунт 
												vk = vk_api.VkApi(token=token)
												vk = vk.get_api()
												vk.account.getInfo()
											
												db=Database(host,user,password,name_db)
												db.add_spam_account(log,pas,token)
										
												keyboard= VkKeyboard()
												keyboard.add_button('Начать спам',VkKeyboardColor.NEGATIVE)	
												keyboard.add_line()
												keyboard.add_button('Посмотреть спам текст групп',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Посмотреть данные спам аккаунтов',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Проверить статус спам аккаунтов',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Загрузить группу',VkKeyboardColor.PRIMARY)
												keyboard.add_button('Удалить группу',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Добавить или обновить спам текст',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Загрузить спам аккаунт',VkKeyboardColor.PRIMARY)
												keyboard.add_button('Удалить спам аккаунт',VkKeyboardColor.PRIMARY)

												send_message(group_api,event.user_id,'Данные аккаунта успешно загружены\\n Можете дальше отправлять данные аккаунта.Чтобы прекратить процедуру нажмите "Главное меню"',keyboard)

											except Exception as error:
												print(error)
												if 'invalid access_token' in str(error):
													keyboard= VkKeyboard()
													keyboard.add_button('Начать спам',VkKeyboardColor.NEGATIVE)	
													keyboard.add_line()
													keyboard.add_button('Посмотреть спам текст групп',VkKeyboardColor.PRIMARY)
													keyboard.add_line()
													keyboard.add_button('Посмотреть данные спам аккаунтов',VkKeyboardColor.PRIMARY)
													keyboard.add_line()
													keyboard.add_button('Проверить статус спам аккаунтов',VkKeyboardColor.PRIMARY)
													keyboard.add_line()
													keyboard.add_button('Загрузить группу',VkKeyboardColor.PRIMARY)
													keyboard.add_button('Удалить группу',VkKeyboardColor.PRIMARY)
													keyboard.add_line()
													keyboard.add_button('Добавить или обновить спам текст',VkKeyboardColor.PRIMARY)
													keyboard.add_line()
													keyboard.add_button('Загрузить спам аккаунт',VkKeyboardColor.PRIMARY)
													keyboard.add_button('Удалить спам аккаунт',VkKeyboardColor.PRIMARY)

													send_message(group_api,event.user_id,'Неправильный токен! Пожалуйста проверьте правльность токена и повторить процедуру!',keyboard)
												
												if 'user is blocked' in str(error):
													keyboard= VkKeyboard()
													keyboard.add_button('Начать спам',VkKeyboardColor.NEGATIVE)	
													keyboard.add_line()
													keyboard.add_button('Посмотреть спам текст групп',VkKeyboardColor.PRIMARY)
													keyboard.add_line()
													keyboard.add_button('Посмотреть данные спам аккаунтов',VkKeyboardColor.PRIMARY)
													keyboard.add_line()
													keyboard.add_button('Проверить статус спам аккаунтов',VkKeyboardColor.PRIMARY)
													keyboard.add_line()
													keyboard.add_button('Загрузить группу',VkKeyboardColor.PRIMARY)
													keyboard.add_button('Удалить группу',VkKeyboardColor.PRIMARY)
													keyboard.add_line()
													keyboard.add_button('Добавить или обновить спам текст',VkKeyboardColor.PRIMARY)
													keyboard.add_line()
													keyboard.add_button('Загрузить спам аккаунт',VkKeyboardColor.PRIMARY)
													keyboard.add_button('Удалить спам аккаунт',VkKeyboardColor.PRIMARY)
												
													send_message(group_api,event.user_id,'Данный аккаунт заблокирован!',keyboard)

									
						if text=='Проверить статус спам аккаунтов':
							#Просмотр в каком состоянии спам аккаунт,если аккаунт в бане то он автоматичеки удалеться из бд
							keyboard= VkKeyboard()
							keyboard.add_button('Главное меню',VkKeyboardColor.PRIMARY)
						
							db=Database(host,user,password,name_db)
							accounts=db.get_spam_account()
						
							if len(accounts['id'])==0:
								send_message(group_api,event.user_id,'У вас нет ни одного спам аккаунта!Сначала загрузите их.')
							else:
								for id_acc in accounts['id']:
									try:
										vk = vk_api.VkApi(token=accounts['id'][id_acc]['token'])
										vk = vk.get_api()
										vk.account.getInfo()
										send_message(group_api,event.user_id,
													'id-'+str(id_acc)+',логин:%s,пароль:%s.Состояние-ЗДОРОВ!'% (accounts['id'][id_acc]['login'],accounts['id'][id_acc]['password'])
										)
									except Exception as error:
										print(error)
										if 'invalid access_token' in str(error):
									
											send_message(group_api,event.user_id,
													'id-'+str(id_acc)+',логин:%s,пароль:%s.Состояние-НЕПРАВИЛЬНЫЙ ТОКЕН!'% (accounts['id'][id_acc]['login'],accounts['id'][id_acc]['password'])
											)
							
										if 'user is blocked' in str(error):
											db.del_spam_account(id_acc)

										if 'Captcha needed' in str(error):
											send_message(group_api,event.user_id,
														'id-'+str(id_acc)+',логин:%s,пароль:%s.Состояние-НУЖНО ВВЕСТИ КАПЧУ!'% (accounts['id'][id_acc]['login'],accounts['id'][id_acc]['password'])
											)

						if text=='Удалить спам аккаунт':
							keyboard= VkKeyboard()
							keyboard.add_button('Главное меню',VkKeyboardColor.PRIMARY)
						
							db=Database(host,user,password,name_db)
							accounts=db.get_spam_account()
						
							if len(accounts['id'])==0:
								send_message(group_api,event.user_id,'У вас нет ни одного спам аккаунта,чтобы его удалить!')
							else:
								for id_acc in accounts['id']:
									send_message(group_api,event.user_id,
												f'id-{str(id_acc)},логин:%s,пароль:%s.'% (accounts['id'][id_acc]['login'],accounts['id'][id_acc]['password'])
									)

								send_message(group_api,event.user_id,'Отправь id аккаунта,чтобы его удалить.Чтобы прекратить процедуру нажмите "Главное меню".',keyboard)

								for event in VkLongPoll(group_api).listen():
									if event.type == VkEventType.MESSAGE_NEW and event.to_me:
										if event.user_id == admin_id:
											if event.text == 'Главное меню' or event.text=='start':
												keyboard= VkKeyboard()
												keyboard.add_button('Начать спам',VkKeyboardColor.NEGATIVE)	
												keyboard.add_line()
												keyboard.add_button('Посмотреть спам текст групп',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Посмотреть данные спам аккаунтов',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Проверить статус спам аккаунтов',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Загрузить группу',VkKeyboardColor.PRIMARY)
												keyboard.add_button('Удалить группу',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Добавить или обновить спам текст',VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Загрузить спам аккаунт',VkKeyboardColor.PRIMARY)
												keyboard.add_button('Удалить спам аккаунт',VkKeyboardColor.PRIMARY)

												break
											else:
												try:
													id_acc=int(event.text)
													if id_acc not in accounts['id']:
														send_message(group_api,event.user_id,'Аккаунтов под id-'+str(id_acc)+' нет!Внимательно смотрите на список id спам аккаунтов!')
													else:
														db.del_spam_account(id_acc)
														send_message(group_api,event.user_id,'Аккаунт под id-'+str(id_acc)+' успешно удален!')

												except:
													send_message(group_api,event.user_id,'Не могу найти такой id,возможно вы ошиблись.\nОтправьте коректный id!',keyboard)
											

						if text=='Начать работу':
							#Считываем активированные группы для работы и запускам функцию spam для этих групп через потоки
							keyboard= VkKeyboard()
							keyboard.add_button('Главное меню',VkKeyboardColor.PRIMARY)
							db=Database(host,user,password,name_db)
							groups=db.get_active_groups()

							if len(groups['id'])==0:
								send_message(group_api,event.user_id,'Нет активированных груп!Пожалуйста активруйте группы и повторите процедуру!')
							else:
								for i in groups['id']:
			 						Thread(target=spam,args=(i,groups['id'][i]['token'],groups['id'][i]['group_id'])).start()
		 						
			 						send_message(group_api,event.user_id,'Работа рассылок в группе - '+groups['id'][i]['name']+' началась!')
	except:
		bot_longpoll(group_api)