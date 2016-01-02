#-*-coding:utf-8-*-

# all the import
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import Flask, request, jsonify
from json import dumps, loads
#from sqlalchemy.ext.declarative import declarative_base
from flask.ext.cors import CORS

import sys
import sqlalchemy.exc



# DB fils import
from tm import Base, Time

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
engine = create_engine("mysql://root:1127@52.192.89.97/timeManagement", encoding='utf8', echo=False)
Base.metadata.bind = engine
DBSession=scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
session = DBSession()


#main page
@app.route('/<int:datetime>', methods=['GET'])
#int:datetime = 20150102.. int형
def main_page(datetime):
#2016-01-02필요 -> datime 슬라이싱 필요
#datime은 int형이므로 슬라이싱하기 위해 int -> str변환
	datetime = str(datetime)
	year = datetime[:4]
	month = datetime[4:6]
	day = datetime[6:8]

#session.query의 return형은 object이다.
	query = session.query(Time)

#eTime : 2016-01-02 13:00:00
	matched_query = query.from_statement("SELECT * FROM time WHERE eTime LIKE :dateT").params(dateT = year+'-'+month+'-'+day+'%')

	converted_list = []
	for i in matched_query:
		time_object = i.__dict__.copy()
		del time_object['_sa_instance_state']
		converted_list.append(time_object)
	session.close()
	return jsonify(result=converted_list)

	#result는 query의 결과인 리스트의 키 부분이다.
	#query는 [{키:값}{키:값}..]
	#result:query
	#result:[{behavior: "test",eTime: "Sat, 02 Jan 2016 13:00:00 GMT", timeCode: "1"},{..},{...}]

	#flask.jsonify()는 ()를 json타입으로 바꿔줌
	#result를 키로 리스트형인 query를 값으로하는 json타입(딕셔너리형)이 된다.
	#{result:query}
	#{result:[{키:값}{..}]}




# #Object post, put, delete
# @app.route('/object', methods=['GET','POST'])
# def show_object():
# 	if request.method == "POST":
# 	 	#Get Request
# 	 	data = request.get_json(force=True)
# 	 	#get data from requested
# 	 	idf = data['a'].encode('utf-8')
#
#
# 		if idf == 'CreateObject':
# 			obj_code = data['obj_code'].encode('utf-8')
# 	 		obj_desc = data['obj_desc'].encode('utf-8')
# 	 		obj_priority = data['obj_priority'].encode('utf-8')
#
# 			newObj=Object(obj_code = obj_code, obj_desc = obj_desc, obj_priority = obj_priority)
#
# 			session.add(newObj)
# 			session.commit()
# 			session.close()
# 			return jsonify(results = "1")
#
#
# 		elif idf == 'UpdateObject':
# 			obj_code = data['obj_code'].encode('utf-8')
# 	 		obj_desc = data['obj_desc'].encode('utf-8')
# 	 		obj_priority = data['obj_priority'].encode('utf-8')
#
# 			#데이터베이스에서 업데이트 하고자 하는 객체를 불러옴
# 			query = session.query(Object)
# 		  	query_row = query.from_statement("select * from object where obj_code=:obj_code").params(obj_code=obj_code).first()
# 			#만약 객체가 조회되지 않을 경우 0을 반환
# 			if query_row is None :
# 				return jsonify(results = "0")
# 			#조회된 객체안에 컬럼에 접근하여 사용자가 요청한 데이터를 입력해줌
# 			query_row.obj_desc = obj_desc
# 			query_row.obj_priority = obj_priority
# 			#세션 커밋 믿 닫음
# 			session.commit()
# 			session.close()
# 			return jsonify(results = "1")
#
# 		elif idf == 'DeleteObject':
# 			obj_code = data['obj_code'].encode('utf-8')
#
# 		  	query = session.query(Object)
# 		  	deleted_row = query.from_statement("select * from object where obj_code=:obj_code").params(obj_code=obj_code).first()
# 			session.delete(deleted_row)
# 			session.commit()
# 			session.close()
# 			return jsonify(results = "1")
#
# 		elif type(idf) == type("") :
# 		  	return jsonify(results = "0")
#
#
# #GET방식
# 	query = session.query(Object)
# 	query_list = query.all()
# 	converted_list = []
# 	for i in query_list:
# 		individual_object = i.__dict__.copy()
# 		del individual_object['_sa_instance_state']
# 		converted_list.append(individual_object)
# 	session.close()
# 	return jsonify(results = converted_list)
#
#
# #Department Read
# @app.route('/department', methods=['GET','POST'])
# def show_department():
# 	if request.method == "POST":
# 	 	#Get Request
# 	 	data = request.get_json(force=True)
# 	 	#get data from requested
# 	 	idf = data['a'].encode('utf-8')
#
# 	 	# dept_code = data['dept_code'].encode('utf-8')
# 	 	# dept_desc = data['dept_desc'].encode('utf-8')
#
# 		if idf == 'ShowDepartment':
#
# 			dept_code = data['dept_code'].encode('utf-8')
# 	 		dept_desc = data['dept_desc'].encode('utf-8')
#
# 		  	query = session.query(Department)
# 			query_list = query.from_statement("select * from department where dept_code=:dept_code OR dept_desc=:dept_desc").params(dept_code=dept_code, dept_desc=dept_desc).all()
# 			if query_list is not None:
# 		  		converted_list = []
# 		  		for i in query_list:
# 		  			individual_department = i.__dict__.copy()
# 		  			del individual_department['_sa_instance_state']
# 		  			converted_list.append(individual_department)
# 		  		session.close()
# 		  		return jsonify(results = converted_list)
# 		  	else:
# 		  		return jsonify(results = "0")
#
# 		elif idf == 'CreateDepartment':
#
# 			dept_code = data['dept_code'].encode('utf-8')
# 	 		dept_desc = data['dept_desc'].encode('utf-8')
#
# 			newDept=Department(dept_code = dept_code, dept_desc = dept_desc)
# 			session.add(newDept)
# 			session.commit()
# 			session.close()
# 			return jsonify(results = "1")
#
# 		if idf =='UpdateDepartment':
#
# 			dept_code = data['dept_code'].encode('utf-8')
# 	 		dept_desc = data['dept_desc'].encode('utf-8')
#
# 			query = session.query(Department)
# 			query_updated = query.from_statement("select * from department where dept_code=:dept_code").params(dept_code=dept_code).first() ##
# 			if query_updated is None:
# 				return jsonify(results="0")
# 			query_updated.dept_code = dept_code
# 			query_updated.dept_desc = dept_desc
# 			# 세션 커밋
# 			session.commit()
# 			session.close()
# 			return jsonify(results = "1")
#
# 		if idf=='DeleteDepartment':
#
# 			dept_code = data['dept_code'].encode('utf-8')
#
# 			query = session.query(Department)
# 			query_deleted = query.from_statement("SELECT * FROM department WHERE dept_code=:dept_code").params(dept_code=dept_code).first()#
# 			session.delete(query_deleted)
# 			session.commit()
# 			session.close()
# 			return jsonify(results = "1")
#
# 		elif type(idf) == type("") :
# 		  	return jsonify(results = 0)
#
#
#
# 	query = session.query(Department)
# 	query_list = query.all()
# 	converted_list = []
# 	for i in query_list:
# 		individual_department = i.__dict__.copy()
# 		del individual_department['_sa_instance_state']
# 		converted_list.append(individual_department)
# 	session.close()
# 	return jsonify(results = converted_list)
#
# # DEPT_OBJ
# @app.route('/dept-obj', methods=['GET','POST'])
# def show_deptobj():
# 	if request.method == "POST":
# 	 	#Get Request
# 	 	data = request.get_json(force=True)
# 	 	#get data from requested
# 	 	idf = data['a'].encode('utf-8')
# # 	 	dept_code = data['dept_code'].encode('utf-8')
# # 		obj_code = data['obj_code'].encode('utf-8')
#
# 		if idf == 'CreateDeptObj':
# 			dept_code = data['dept_code'].encode('utf-8')
# 			obj_code = data['obj_code'].encode('utf-8')
# 		 	dept_obj_resp = data['dept_obj_resp'].encode('utf-8') #책임여부
# 			dept_obj_auth = data['dept_obj_auth'].encode('utf-8') #권한여부
# 			dept_obj_exp = data['dept_obj_exp'].encode('utf-8') #경험여부
# 			dept_obj_work = data['dept_obj_work'].encode('utf-8') #작업여부
# 			dept_obj_ref = data['dept_obj_ref'].encode('utf-8') #참조여부
#
# 			newDept_obj = Dept_obj(dept_code = dept_code, obj_code = obj_code, dept_obj_resp =dept_obj_resp ,dept_obj_auth = dept_obj_auth,dept_obj_exp=dept_obj_exp ,dept_obj_work=dept_obj_work ,dept_obj_ref=dept_obj_ref)
# 			session.add(newDept_obj)
# 			session.commit()
# 			session.close()
# 			return jsonify(results = "1")
#
# 		elif idf=='UpdateDeptObj':
#
# 			dept_code = data['dept_code'].encode('utf-8')
# 			obj_code = data['obj_code'].encode('utf-8')
# 		 	dept_obj_resp = data['dept_obj_resp'].encode('utf-8') #책임여부
# 			dept_obj_auth = data['dept_obj_auth'].encode('utf-8') #권한여부
# 			dept_obj_exp = data['dept_obj_exp'].encode('utf-8') #경험여부
# 			dept_obj_work = data['dept_obj_work'].encode('utf-8') #작업여부
# 			dept_obj_ref = data['dept_obj_ref'].encode('utf-8') #참조여부
#
# 			query = session.query(Dept_obj)
# 			query_list = query.from_statement("SELECT * FROM dept_obj WHERE dept_code=:dept_code AND obj_code=:obj_code").params(dept_code=dept_code, obj_code=obj_code).first()
#
# 			if query_list is None:
# 				return jsonify(results="0")
# ############문제해결 org = {'a': 'UpdateDeptObj', 'dept_code':'2', 'obj_code':'2', 'dept_obj_resp':'0', 'dept_obj_auth':'0', 'dept_obj_exp':'1','dept_obj_work':'1','dept_obj_ref':'0'}
# 			query_list.dept_code = dept_code
# 			query_list.obj_code = obj_code
# 			query_list.dept_obj_resp = dept_obj_resp
# 			query_list.dept_obj_auth = dept_obj_auth
# 			query_list.dept_obj_exp = dept_obj_exp
# 			query_list.dept_obj_work = dept_obj_work
# 			query_list.dept_obj_ref = dept_obj_ref
# 			session.commit()
# 			session.close()
# 			return jsonify(results ="1")
#
# 		elif idf=='DeleteDeptObj':  # 키값 = a
# 			dept_code = data['dept_code'].encode('utf-8')
# 			obj_code = data['obj_code'].encode('utf-8')
#
# 			query = session.query(Dept_obj)
# 			query_list = query.from_statement("SELECT * FROM dept_obj WHERE dept_code=:dept_code AND obj_code=:obj_code").params(dept_code=dept_code, obj_code=obj_code).first()
# 			if query_list is None:
# 				return jsonify(results="0")
# 			session.delete(query_list)
# 			session.commit()
# 			session.close()
# 			return jsonify(results="1")
#
# 		elif type(idf) == type("") :
# 		  	return jsonify(results = 0)
#
#
#
# 	query = session.query(Dept_obj)
# 	query_list = query.all()
# 	converted_list = []
# 	for i in query_list:
# 		individual_DeptObj = i.__dict__.copy()
# 		del individual_DeptObj['_sa_instance_state']
# 		converted_list.append(individual_DeptObj)
# 	session.close()
# 	return jsonify(results = converted_list)



if __name__=='__main__':
	app.run(host='0.0.0.0', debug=True)
	app.debug=True
