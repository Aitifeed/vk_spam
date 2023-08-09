from vk_api.keyboard import VkKeyboard,VkKeyboardColor

def keyboards():
	keyboard = VkKeyboard()
	keyboard.add_button('Начать работу', VkKeyboardColor.NEGATIVE)	
	keyboard.add_button('Активировать/деактивировать группу', VkKeyboardColor.NEGATIVE)
	keyboard.add_line()
	keyboard.add_button('Посмотреть спам текст групп', VkKeyboardColor.PRIMARY)
	keyboard.add_line()
	keyboard.add_button('Посмотреть данные спам аккаунтов', VkKeyboardColor.PRIMARY)
	keyboard.add_line()
	keyboard.add_button('Проверить статус спам аккаунтов', VkKeyboardColor.PRIMARY)
	keyboard.add_line()
	keyboard.add_button('Загрузить группу', VkKeyboardColor.PRIMARY)
	keyboard.add_button('Удалить группу', VkKeyboardColor.PRIMARY)
	keyboard.add_line()
	keyboard.add_button('Добавить или обновить спам текст', VkKeyboardColor.PRIMARY)
	keyboard.add_line()
	keyboard.add_button('Загрузить спам аккаунт', VkKeyboardColor.PRIMARY)
	keyboard.add_button('Удалить спам аккаунт', VkKeyboardColor.PRIMARY)

	return keyboard
