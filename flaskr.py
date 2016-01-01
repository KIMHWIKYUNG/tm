#-*-coding:utf-8-*-

# all the import
from sqlalchemy import create_engine, desc, asc, func
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import Flask, request, redirect, url_for, abort, render_template, flash, jsonify
from flask import session as login_session
from json import dumps, loads
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.cors import CORS

import sys
import sqlalchemy.exc
import telepot as tp


# DB fils import
from isp_final import Base, Department, Dept_obj, Object

#configuration
# DEBUG = True
# SECRET_KEY = '1234'
# USERNAME = 'adminJ'
# PASSWORD = 'wjdtnsgud1!'

#create our little application
app=Flask(__name__)
CORS(app)
app.config.from_object(__name__)
reload(sys)
sys.setdefaultencoding('utf-8')


#wjdtnsgud1!
#Connect to Database and create database session
engine = create_engine("mysql://root:wjdtnsgud1!@localhost/isp", encoding='utf8', echo=False)
Base.metadata.bind = engine
DBSession=scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
session = DBSession()


######deportment
# @app.route('/')
# def show_deportment():
# 	# entries=session.query(Entries).order_by(desc(Entries.id)).all()
# 	# session.close()
# 	return jsonify(greeting= 'Hello ISP!')
######Deportment
# @app.route('/department')
# def show_department():
# 	query = session.query(Department)
# 	query_list =  query.all()
# 	converted_list = []
# 	for i in query_list:
# 		individual_object = i.__dict__.copy()
# 		del individual_object['_sa_instance_state']
# 		converted_list.append(individual_object)
# 	return jsonify(results = converted_list)

#Telegram Module
def message_me(message):
	bot = tp.Bot('155578772:AAGngKO2rPtjzC2_P3CM7FSsL-FIAfzRk8A')
	bot.sendMessage(33612976,str(message))


#Some Module
class InvalidUsage(Exception):
	status_code = 400

	def __init__(self, message, status_code=None, payload=None):
		Exception.__init__(self)
		self.message = message
		if status_code is not None:
			self.status_code = status_code
		self.payload = payload

	def to_dict(self):
		rv = dict(self.payload or ())
		rv['message'] = self.message
		return rv



#main page
@app.route('/')
def main_page():
	query = session.query(Department)
	allList = query.all()
	for i in allList:
		result = dumps(str(i))
	return result

# @app.route('/board1/<int:page_number>')
# def board1(page_number):
# 	#총 글의 갯수를 구함
# 	total_number_writings=int(session.query(func.count('*')).select_from(Board1).scalar())
# 	# 왜 +2를 해야 하지?? 총 페이지 수를 도출
# 	total_page_number=int(total_number_writings/10)+2
# 	if page_number>=total_page_number:
# 		flash('그 페이지는 존재하지 않습니다')
# 		return redirect(url_for('board1', page_number=1))
# 	# count number of writings
# 	# session.query(Entries.id).order_by(desc(Entries.id)).first()
# 	if page_number==None:
# 		page_number=1
# 	writings1=session.query(Board1).order_by(desc(Board1.id)).limit(10).offset((page_number-1)*10).all()
# 	session.close()
# 	return render_template('board1.html', writings1=writings1, page_number=page_number, total_page_number=total_page_number)

# #object get
# @app.route('/object/<obj_code>/<obj_desc>', methods=['GET'])
# def get_object(obj_code, obj_desc):
# 	if obj_code == "":
# 		if 

#Object post, put, delete
@app.route('/object', methods=['GET','POST'])
def show_object():
	if request.method == "POST":
	 	#Get Request
	 	data = request.get_json(force=True)
		#the request object already has a method get_json which can give you the json regardless of the content-type if you execute it with force=True
	 	#get data from requested
	 	idf = data['a'].encode('utf-8')

		# if idf == 'ShowObject':
		#   	query = session.query(Object)
		# #session = stream의 일종
		# #sqlalchemy의 Object클레스
		#   	#Select * from where obj_code == obj_code or obj_desc == %obj_desc% or obj_priority == obj_priority
		#   	# query_list = query.filter(Object.obj_code == obj_code, Object.obj_desc.like("%"+obj_desc+"%"), Object.obj_priority == obj_priority).all()

		#   	#This is needs to be converted complex 'where' condition.
		#   	# query_list = query.filter("obj_code =:obj_code").params(obj_code=obj_code).all()
		#   	query_list = query.from_statement("select * from object where obj_code=:obj_code OR obj_priority=:obj_priority").params(obj_code=obj_code, obj_priority=obj_priority).like('%'+obj_desc+'%').all()
		# 	#query_list = query.filter("obj_code=:obj_code OR obj_priority=:obj_priority").params(obj_code=obj_code, obj_priority=obj_priority).filter(Object.obj_desc.like(''%'+obj_desc+'%').all()
		# 	#obj_desc=obj_desc의 쿼리 일부분만 검색, 일부 내용 검색 해도 가능하도록 정규표현식화, sql, sqlalchemy에서 검색, like는 factory pattern

		# 	# query_list = query.filter(Object.obj_code=obj_code).all()

		#   	#Check if there a queried list exists
		#   	if query_list is not None:
		#   		converted_list = []
		#   		for i in query_list:
		#   			individual_object = i.__dict__.copy()
		#   			del individual_object['_sa_instance_state']
		#   			converted_list.append(individual_object)
		#   		session.close()
		#   		return jsonify(results = converted_list)
		#   	else:
		#   		return jsonify(results = "0")

		if idf == 'CreateObject':
			obj_code = data['obj_code'].encode('utf-8')
	 		obj_desc = data['obj_desc'].encode('utf-8')
	 		obj_priority = data['obj_priority'].encode('utf-8')

			newObj=Object(obj_code = obj_code, obj_desc = obj_desc, obj_priority = obj_priority)
			
			session.add(newObj)
			session.commit()
			session.close()
			return jsonify(results = "1")


		elif idf == 'UpdateObject':
			obj_code = data['obj_code'].encode('utf-8')
	 		obj_desc = data['obj_desc'].encode('utf-8')
	 		obj_priority = data['obj_priority'].encode('utf-8')

			#데이터베이스에서 업데이트 하고자 하는 객체를 불러옴
			query = session.query(Object)
		  	query_row = query.from_statement("select * from object where obj_code=:obj_code").params(obj_code=obj_code).first()
			#만약 객체가 조회되지 않을 경우 0을 반환
			if query_row is None :
				return jsonify(results = "0")
			#조회된 객체안에 컬럼에 접근하여 사용자가 요청한 데이터를 입력해줌
			query_row.obj_desc = obj_desc
			query_row.obj_priority = obj_priority
			#세션 커밋 믿 닫음
			session.commit()
			session.close()
			return jsonify(results = "1")

		elif idf == 'DeleteObject':
			obj_code = data['obj_code'].encode('utf-8')

		  	query = session.query(Object)
		  	deleted_row = query.from_statement("select * from object where obj_code=:obj_code").params(obj_code=obj_code).first()
			session.delete(deleted_row)
			session.commit()
			session.close()
			return jsonify(results = "1")

		elif type(idf) == type("") :
		  	return jsonify(results = "0")


	# elif request.method == "PUT":
	#  	#Get Request
	#  	data = request.get_json(force=True)
	#  	#get data from requested
	#  	idf = data['a'].encode('utf-8')
	#  	obj_code = data['obj_code'].encode('utf-8')
	#  	obj_desc = data['obj_desc'].encode('utf-8')
	#  	obj_priority = data['obj_priority'].encode('utf-8')

	# 	if idf == 'UpdateObject':
	# 		#데이터베이스에서 업데이트 하고자 하는 객체를 불러옴
	# 		query = session.query(Object)
	# 	  	query_row = query.from_statement("select * from object where obj_code=:obj_code").params(obj_code=obj_code).first()
	# 		#만약 객체가 조회되지 않을 경우 0을 반환
	# 		if query_row is None :
	# 			return jsonify(results = "0")
	# 		#조회된 객체안에 컬럼에 접근하여 사용자가 요청한 데이터를 입력해줌
	# 		query_row.obj_desc = obj_desc
	# 		query_row.obj_priority = obj_priority
	# 		#세션 커밋 믿 닫음
	# 		session.commit()
	# 		session.close()
	# 		return jsonify(results = "1")

	# 	elif type(idf) == type("") :
	# 	  	return jsonify(results = "0")

	# elif request.method == "DELETE":
	#  	#Get Request
	#  	data = request.get_json(force=True)
	#  	#get data from requested
	#  	idf = data['a'].encode('utf-8')
	#  	obj_code = data['obj_code'].encode('utf-8')

	# 	if idf == 'DeleteObject':
	# 	  	query = session.query(Object)
	# 	  	deleted_row = query.from_statement("select * from object where obj_code=:obj_code").params(obj_code=obj_code).first()
	# 		session.delete(deleted_row)
	# 		session.commit()
	# 		session.close()
	# 		return jsonify(results = "1")

	# 	elif type(idf) == type("") :
	# 	  	return jsonify(results = "0")

#GET방식
	query = session.query(Object)
	query_list = query.all()
	converted_list = []
	for i in query_list:
		individual_object = i.__dict__.copy()
		del individual_object['_sa_instance_state']
		converted_list.append(individual_object)
	session.close()
	return jsonify(results = converted_list)


#Department Read
@app.route('/department', methods=['GET','POST'])
def show_department():
	if request.method == "POST":
	 	#Get Request
	 	data = request.get_json(force=True)
	 	#get data from requested
	 	idf = data['a'].encode('utf-8')

	 	# dept_code = data['dept_code'].encode('utf-8')
	 	# dept_desc = data['dept_desc'].encode('utf-8')

		if idf == 'ShowDepartment':

			dept_code = data['dept_code'].encode('utf-8')
	 		dept_desc = data['dept_desc'].encode('utf-8')

		  	query = session.query(Department)
			query_list = query.from_statement("select * from department where dept_code=:dept_code OR dept_desc=:dept_desc").params(dept_code=dept_code, dept_desc=dept_desc).all()
			if query_list is not None:
		  		converted_list = []
		  		for i in query_list:
		  			individual_department = i.__dict__.copy()
		  			del individual_department['_sa_instance_state']
		  			converted_list.append(individual_department)
		  		session.close()
		  		return jsonify(results = converted_list)
		  	else:
		  		return jsonify(results = "0")
		
		elif idf == 'CreateDepartment':

			dept_code = data['dept_code'].encode('utf-8')
	 		dept_desc = data['dept_desc'].encode('utf-8')

			newDept=Department(dept_code = dept_code, dept_desc = dept_desc)
			session.add(newDept)
			session.commit()
			session.close()
			return jsonify(results = "1")

		if idf =='UpdateDepartment':

			dept_code = data['dept_code'].encode('utf-8')
	 		dept_desc = data['dept_desc'].encode('utf-8')

			query = session.query(Department)
			query_updated = query.from_statement("select * from department where dept_code=:dept_code").params(dept_code=dept_code).first() ##
			if query_updated is None:
				return jsonify(results="0")
			query_updated.dept_code = dept_code
			query_updated.dept_desc = dept_desc
			# 세션 커밋
			session.commit()
			session.close()
			return jsonify(results = "1")

		if idf=='DeleteDepartment':

			dept_code = data['dept_code'].encode('utf-8')

			query = session.query(Department)
			query_deleted = query.from_statement("SELECT * FROM department WHERE dept_code=:dept_code").params(dept_code=dept_code).first()#
			session.delete(query_deleted)
			session.commit()
			session.close()
			return jsonify(results = "1")

		elif type(idf) == type("") :
		  	return jsonify(results = 0)


	###
	# elif request.method==['POST']:
	# 	#Get Request
	#  	data = request.get_json(force=True)
	#  	#get data from requested
	#  	idf = data['a'].encode('utf-8')
	#  	dept_code = data['dept_code'].encode('utf-8')
	#  	dept_desc = data['dept_desc'].encode('utf-8')

	# 	if idf == 'AddDepartment':
	# 		query = session.query(Department)
	# 		query_list = query.form_statement("insert into table Department values('dept_code=:dept_code','dept_desc=:dept_desc').params(dept_code=dept_code,dept_desc=dept_desc).first()")
	# 		if query_update in None:
	# 			return jsonify(results="0")
	# 		query_update.dept_code = dept_code
	# 		query_update.dept_desc = dept_desc
	# 		# 세션 커밋
	# 		session.commit()
	# 		session.close()
	# 		return jsonify(results = "1")



	# elif request.method== 'PUT' :
	# 	data = request.get_json(force=True)
	# 	idf = data['a'].encode('utf-8')
	# 	dept_code = data['dept_code'].encode('utf-8')
	#  	dept_desc = data['dept_desc'].encode('utf-8')

	# 	if idf =='UpdateDepartment':
	# 		query = session.query(Department)
	# 		query_updated = query.from_statement("select * from department where dept_code=:dept_code").params(dept_code=dept_code).first() ##
	# 		if query_updated is None:
	# 			return jsonify(results="0")
	# 		query_updated.dept_code = dept_code
	# 		query_updated.dept_desc = dept_desc
	# 		# 세션 커밋
	# 		session.commit()
	# 		session.close()
	# 		return jsonify(results = "1")

	# elif request.method=='DELETE':
	# 	data = request.get_json(force=True)
	# 	idf = data['a'].encode('utf-8')
	# 	dept_code = data['dept_code'].encode('utf-8')
	#  	#dept_desc = data['dept_desc'].encode('utf-8')#

	# 	if idf=='DeleteDepartment':
	# 		query = session.query(Department)
	# 		query_deleted = query.from_statement("SELECT * FROM department WHERE dept_code=:dept_code").params(dept_code=dept_code).first()#
	# 		session.delete(query_deleted)
	# 		session.commit()
	# 		session.close()
	# 		return jsonify(results = "1")

	query = session.query(Department)
	query_list = query.all()
	converted_list = []
	for i in query_list:
		individual_department = i.__dict__.copy()
		del individual_department['_sa_instance_state']
		converted_list.append(individual_department)
	session.close()
	return jsonify(results = converted_list)

# DEPT_OBJ
@app.route('/dept-obj', methods=['GET','POST'])
def show_deptobj():
	if request.method == "POST":
	 	#Get Request
	 	data = request.get_json(force=True)
	 	#get data from requested
	 	idf = data['a'].encode('utf-8')
# 	 	dept_code = data['dept_code'].encode('utf-8')
# 		obj_code = data['obj_code'].encode('utf-8')

# ############문제해결 // org = {'a': 'ShowDeptObj', 'dept_code':'2', 'obj_code':'2', 'dept_obj_resp':'0', 'dept_obj_auth':'0', 'dept_obj_exp':'1','dept_obj_work':'1','dept_obj_ref':'0'}
# 	 	dept_obj_resp = data['dept_obj_resp'].encode('utf-8') #책임여부
# 		dept_obj_auth = data['dept_obj_auth'].encode('utf-8') #권한여부
# 		dept_obj_exp = data['dept_obj_exp'].encode('utf-8') #경험여부
# 		dept_obj_work = data['dept_obj_work'].encode('utf-8') #작업여부
# 		dept_obj_ref = data['dept_obj_ref'].encode('utf-8') #참조여부

		# if idf == 'ShowDeptObj':
		#   	query = session.query(Dept_obj)
		# 	query_list = query.from_statement("select * from dept_obj where dept_code=:dept_code AND obj_code=:obj_code").params(dept_code=dept_code, obj_code=obj_code).all()
		# 	if query_list is not None:
		# 		converted_list = []
		#   		for i in query_list:
		#   			individual_dep_obj = i.__dict__.copy()
		#   			del individual_dep_obj['_sa_instance_state']
		#   			converted_list.append(individual_dep_obj)
		#   		session.close()
		#   		return jsonify(results = converted_list)
		#   	else:
		#   		return jsonify(results = "0")

		if idf == 'CreateDeptObj':
			dept_code = data['dept_code'].encode('utf-8')
			obj_code = data['obj_code'].encode('utf-8')
		 	dept_obj_resp = data['dept_obj_resp'].encode('utf-8') #책임여부
			dept_obj_auth = data['dept_obj_auth'].encode('utf-8') #권한여부
			dept_obj_exp = data['dept_obj_exp'].encode('utf-8') #경험여부
			dept_obj_work = data['dept_obj_work'].encode('utf-8') #작업여부
			dept_obj_ref = data['dept_obj_ref'].encode('utf-8') #참조여부

			newDept_obj = Dept_obj(dept_code = dept_code, obj_code = obj_code, dept_obj_resp =dept_obj_resp ,dept_obj_auth = dept_obj_auth,dept_obj_exp=dept_obj_exp ,dept_obj_work=dept_obj_work ,dept_obj_ref=dept_obj_ref)
			session.add(newDept_obj)
			session.commit()
			session.close()
			return jsonify(results = "1")

		elif idf=='UpdateDeptObj':

			dept_code = data['dept_code'].encode('utf-8')
			obj_code = data['obj_code'].encode('utf-8')
		 	dept_obj_resp = data['dept_obj_resp'].encode('utf-8') #책임여부
			dept_obj_auth = data['dept_obj_auth'].encode('utf-8') #권한여부
			dept_obj_exp = data['dept_obj_exp'].encode('utf-8') #경험여부
			dept_obj_work = data['dept_obj_work'].encode('utf-8') #작업여부
			dept_obj_ref = data['dept_obj_ref'].encode('utf-8') #참조여부

			query = session.query(Dept_obj)
			query_list = query.from_statement("SELECT * FROM dept_obj WHERE dept_code=:dept_code AND obj_code=:obj_code").params(dept_code=dept_code, obj_code=obj_code).first()

			if query_list is None:
				return jsonify(results="0")
############문제해결 org = {'a': 'UpdateDeptObj', 'dept_code':'2', 'obj_code':'2', 'dept_obj_resp':'0', 'dept_obj_auth':'0', 'dept_obj_exp':'1','dept_obj_work':'1','dept_obj_ref':'0'}
			query_list.dept_code = dept_code
			query_list.obj_code = obj_code
			query_list.dept_obj_resp = dept_obj_resp
			query_list.dept_obj_auth = dept_obj_auth
			query_list.dept_obj_exp = dept_obj_exp
			query_list.dept_obj_work = dept_obj_work
			query_list.dept_obj_ref = dept_obj_ref
			session.commit()
			session.close()
			return jsonify(results ="1")

		elif idf=='DeleteDeptObj':  # 키값 = a
			dept_code = data['dept_code'].encode('utf-8')
			obj_code = data['obj_code'].encode('utf-8')

			query = session.query(Dept_obj)
			query_list = query.from_statement("SELECT * FROM dept_obj WHERE dept_code=:dept_code AND obj_code=:obj_code").params(dept_code=dept_code, obj_code=obj_code).first()
			if query_list is None:
				return jsonify(results="0")
			session.delete(query_list)
			session.commit()
			session.close()
			return jsonify(results="1")

		elif type(idf) == type("") :
		  	return jsonify(results = 0)

	 #중복된 코드임
	# elif request.method == "POST":
	#  	#Get Request
	#  	data = request.get_json(force=True)
	#  	#get data from requested
	#  	idf = data['a'].encode('utf-8')
	#  	dept_code = data['dept_code'].encode('utf-8')
	# 	obj_code = data['obj_code'].encode('utf-8')
	#  	dept_obj_resp = data['dept_obj_resp'].encode('utf-8') #책임여부
	# 	dept_obj_auth = data['dept_obj_auth'].encode('utf-8') # 권한여부
	# 	dept_obj_exp = data['dept_obj_exp'].encode('utf-8') # 경험여부
	# 	dept_obj_work = data['dept_obj_work'].encode('utf-8') # 작업여부
	# 	dept_obj_ref = data['dept_obj_ref'].encode('utf-8') #참조여부
	#
	# 	if idf == 'CreateDeptObj':
	# 		insertObj = object(dept_code=dept_code,obj_code=obj_code,dept_obj_resp=dept_obj_resp,dept_obj_auth=dept_obj_auth,dept_obj_exp=dept_obj_exp,dept_obj_work=dept_obj_work,dept_obj_ref=dept_obj_ref)
	# 		session.add(insertObj)
	# 		session.commit()
	# 		session.close()
	# 		return jasonify(results="1")
	#
	# 		if query_list in None:
	# 			return jsonify(results="0")
	# 		query_list.dept_code = dept_code
	# 		query_list.obj_code = obj_code
	# 		query_list.dept_obj_resp = dept_obj_resp
	# 		query_list.dept_obj_auth = dept_obj_auth
	# 		query_list.dept_obj_exp = dept_obj_exp
	# 		query_list.dept_obj_work = dept_obj_work
	# 		query_list.dept_obj_ref = dept_obj_ref
	# 		# 세션 커밋
	# 		session.commit()
	# 		session.close()
	# 		return jsonify(results = "1")
		

	# elif request.method =="DELETE":
	# 	#Get Request
	#  	data = request.get_json(force=True)
	#  	#get data from requested
	#  	idf = data['a'].encode('utf-8')
	#  	dept_code = data['dept_code'].encode('utf-8')
	# 	obj_code = data['obj_code'].encode('utf-8')
	# 	# dept_obj_resp = data['dept_obj_resp'].encode('utf-8') #책임여부
	# 	# dept_obj_auth = data['dept_obj_auth'].encode('utf-8') # 권한여부
	# 	# dept_obj_exp = data['dept_obj_exp'].encode('utf-8') # 경험여부
	# 	# dept_obj_work = data['dept_obj_work'].encode('utf-8') # 작업여부
	# 	# dept_obj_ref = data['dept_obj_ref'].encode('utf-8') #참조여부

	# 	if idf=='DeleteDeptObj':  # 키값 = a
	# 		query = session.query(Dept_obj)
	# 		query_list = query.from_statement("SELECT * FROM dept_obj WHERE dept_code=:dept_code AND obj_code=:obj_code").params(dept_code=dept_code, obj_code=obj_code).first()
	# 		if query_list is None:
	# 			return jsonify(results="0")
	# 		session.delete(query_list)
	# 		session.commit()
	# 		session.close()
	# 		return jsonify(results="1")


	query = session.query(Dept_obj)
	query_list = query.all()
	converted_list = []
	for i in query_list:
		individual_DeptObj = i.__dict__.copy()
		del individual_DeptObj['_sa_instance_state']
		converted_list.append(individual_DeptObj)
	session.close()
	return jsonify(results = converted_list)





# #board2 page
# @app.route('/board2/<int:page_number>')
# def board2(page_number):
# 	#총 글의 갯수를 구함
# 	total_number_writings=int(session.query(func.count('*')).select_from(Board2).scalar())
# 	# 왜 +2를 해야 하지?? 총 페이지 수를 도출
# 	total_page_number=int(total_number_writings/10)+2
# 	if page_number>=total_page_number:
# 		flash('그 페이지는 존재하지 않습니다')
# 		return redirect(url_for('board2', page_number=1))
# 	# count number of writings
# 	# session.query(Entries.id).order_by(desc(Entries.id)).first()
# 	if page_number==None:
# 		page_number=1
# 	writings2=session.query(Board2).order_by(desc(Board2.id)).limit(10).offset((page_number-1)*10).all()
# 	session.close()
# 	return render_template('board2.html', writings2=writings2, page_number=page_number, total_page_number=total_page_number)

# #add new notice
# @app.route('/add', methods=['POST'])
# def add_entry():

# 	newEntry=Entries(title=request.form['title'].encode('utf-8'), text=request.form['text'].encode('utf-8'))
# 	session.add(newEntry)
# 	session.commit()
# 	flash('글이 게시되었어!')
# 	session.close()
# 	return redirect(url_for('show_entries'))

# #add new post in board1
# @app.route('/add1', methods=['POST'])
# def add1():
# 	newBoard1=Board1(title=request.form['title'].encode('utf-8'), text=request.form['text'].encode('utf-8'))
# 	session.add(newBoard1)
# 	session.commit()
# 	flash('글이 게시되었어!')
# 	session.close()
# 	return redirect(url_for('board1',page_number=1))

# #add new post in board2
# @app.route('/add2', methods=['POST'])
# def add2():
# 	newBoard2=Board2(title=request.form['title'].encode('utf-8'), text=request.form['text'].encode('utf-8'))
# 	session.add(newBoard2)
# 	session.commit()
# 	flash('글이 게시되었어!')
# 	session.close()
# 	return redirect(url_for('board2',page_number=1))

# #admin login page
# @app.route('/login', methods=['GET','POST'])
# def login():
# 	error=None
# 	if request.method=='POST':
# 		if request.form['username'] != app.config['USERNAME']:
# 			error='invalid username'
# 		elif request.form['password'] != app.config['PASSWORD']:
# 			error='invalid password'
# 		else:
# 			login_session['logged_in']=True
# 			flash('로그인 되었습니다.')
# 			return redirect(url_for('show_entries'))
# 	return render_template('login.html', error=error)

# #admin logout
# @app.route('/logout')
# def logout():
# 	login_session.pop('logged_in', None)
# 	flash('로그아웃되었습니다.')
# 	return redirect(url_for('show_entries'))

# @app.teardown_request
# def shutdown_session(exception=None):
# 	DBSession.remove()

#Error Handler
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
	# response = jsonify(error.to_dict())
	# response.status_code = error.status_code
	# return responset
	# print jsonify(error.to_dict())
	message_me(error.to_dict())
	return jsonify(results=0)

if __name__=='__main__':
	app.run(host='0.0.0.0', debug=True)
	app.debug=True
