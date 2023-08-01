import psycopg2

class Database:
	def __init__(self,host,user,password,name_db):
		try:
			self.connect = psycopg2.connect(host=host,
											user=user,
											password=password,
											database=name_db)
			self.cursor=self.connect.cursor()
		except Exception as error: 
			if f'database "{name_db}" does not exist' in str(error):
				self.__create_database(host,user,password,name_db)
			else:
				print(error)

	@classmethod
	def __create_database(cls,host,user,password,name_db):
		cls.connect = psycopg2.connect(host=host,
										user=user,
										password=password)
		cls.cursor=cls.connect.cursor()
		cls.connect.autocommit = True
		cls.cursor.execute(f'CREATE database {name_db}')
		cls.connect.commit()
		cls.cursor.close()

		cls.connect = psycopg2.connect(
				host=host,
				user=user,
				password=password,
				database=name_db
			)
		cls.cursor=cls.connect.cursor()
		cls.cursor.execute('CREATE TABLE "spam_accounts" ('
							"id			BIGSERIAL,"
							"login 		TEXT,"
							"password 	TEXT,"
							"token 		TEXT,"
							"captcha	BOOLEAN DEFAULT False,"
							"is_banned	BOOLEAN DEFAULT False);")
		
		cls.cursor.execute('CREATE TABLE "group_spam" ('
							"id			BIGSERIAL,"
							"group_id 	INTEGER,"
							"name 		TEXT,"
							"token 		TEXT,"
							"spam_text 	TEXT,"
							"status 	BOOLEAN DEFAULT False);")
		
		cls.connect.commit()


	def set_status(self,id):
		self.cursor.execute('SELECT status FROM group_spam WHERE id=%s',(id,))
		status=self.cursor.fetchall()
		
		if status[0][0]==True:	
			self.cursor.execute('UPDATE group_spam SET status=%s WHERE id=%s',(False,id,))
			self.connect.commit()

			return False
		else:
			self.cursor.execute('UPDATE group_spam SET status=%s WHERE id=%s',(True,id,))
			self.connect.commit()

			return True
			
	def get_status(self,id):
		self.cursor.execute('SELECT status FROM group_spam WHERE id=%s',(id,))
		status=self.cursor.fetchall()

		return status[0][0]

	def add_spam_account(self,login,password,token):
		self.cursor.execute('INSERT INTO spam_accounts (login,password,token) VALUES (%s,%s,%s)',(login,password,token,))
		self.connect.commit()
	
	def add_group_spam(self,group_id,name,token):
		self.cursor.execute('INSERT INTO group_spam (group_id,name,token) VALUES (%s,%s,%s)',(group_id,name,token,))
		self.connect.commit()

	
	def get_active_groups(self):
		self.cursor.execute('SELECT * FROM group_spam WHERE status=True')
		data_db=self.cursor.fetchall()

		data_js={'id':{}}
		for i in data_db:
			data_js['id'][i[0]]={
				'group_id':i[1],
				'name':i[2],
				'token':i[3],
				'spam_text':i[4],
			}

		return data_js

		
	def get_groups(self,id=None):
		if id==None:
			self.cursor.execute('SELECT * FROM group_spam')
			data_db=self.cursor.fetchall()

			data_js={'id':{}}
			for i in data_db:
				data_js['id'][i[0]]={
					'group_id':i[1],
					'name':i[2],
					'token':i[3],
					'spam_text':i[4],
					'status':i[5],
				}

			return data_js
		else:
			self.cursor.execute('SELECT * FROM group_spam WHERE id=%s',(id,))
			data_db=self.cursor.fetchall()

			for i in data_db:
				data_js={
					'id':[i[0]],
					'group_id':i[1],
					'name':i[2],
					'token':i[3],
					'spam_text':i[4],
				}

			return data_js


	def del_group(self,id_group):
		self.cursor.execute('DELETE FROM group_spam WHERE id=%s',(id_group,))
		self.connect.commit()
		
	def add_spam_text(self,id_group,text):
		self.cursor.execute('UPDATE group_spam SET spam_text=%s WHERE id=%s',(text,id_group,))
		self.connect.commit()
		
	def get_all_id_sa(self):
		self.cursor.execute('SELECT id FROM spam_accounts WHERE captcha = False AND is_banned = False')
		id_db=self.cursor.fetchall()
		
		id_acc=[]
		for i in range(len(id_db)):
			id_acc.append(id_db[0][i])
		
		return id_acc

	def get_spam_account(self,id_acc=None):
		if id_acc==None:
			self.cursor.execute('SELECT * FROM spam_accounts')
			data_db=self.cursor.fetchall()
			
			data_js={'id':{}}
			for i in data_db:
				data_js['id'][i[0]]={
					'login':i[1],
					'password':i[2],
					'token':i[3],
					'captcha':i[4],
				}

			return data_js
		else:
			self.cursor.execute('SELECT * FROM spam_accounts WHERE id=%s AND captcha = False AND is_banned = False',(id_acc,))
			data_db=self.cursor.fetchall()
		
			data_js={
				'id':data_db[0][0],
				'login':data_db[0][1],
				'password':data_db[0][2],
				'token':data_db[0][3],
				'captcha':data_db[0][4],
			}

			return data_js

	def del_spam_account(self,id_acc):
		self.cursor.execute('DELETE FROM spam_accounts WHERE id=%s',(id_acc,))
		self.connect.commit()


	def set_captcha(self,id_acc,status):
		self.cursor.execute('UPDATE spam_accounts SET captcha=%s WHERE id=%s',(status,id_acc,))
		self.connect.commit()