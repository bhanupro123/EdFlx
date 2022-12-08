

from ast import And
from email import message
from reg import db
from reg import users
import random
import string
def createUser(name=None,email=None,password=None):
    try:
        if name is None:
                return responseHandler(False,{},"name field required")
        elif email is None:
                return responseHandler(False,{},"email field required")
        elif password is None:
                return responseHandler(False,{},"password field required")
        elif len(email)<5 or len(email)>40:
                return responseHandler(False,{},"email should be 5 to 45 char")
        elif len(name)<5 or len(name)>25:
                return responseHandler(False,{},"name should be 5 to 25 char")
        elif len(password)<5 or len(password)>25:
                return responseHandler(False,{},"password should be 5 to 25 char")
        
        user_to_create = users(name=name,
                            email=email,
                            password=password)
        db.create_all()                            
        db.session.add(user_to_create)
        db.session.commit()
        return responseHandler(True,{},"User creatation is done")
    except Exception as e:
        print(str(e))
        if (str(e.__cause__)=="UNIQUE constraint failed: users.email"):
            return responseHandler(False,{},"Email already existed") 
        else : 
            return responseHandler(False,{},str(e))

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def responseHandler(status=None,data=None,message=None) :
    return { "status":status,"data":data,"message":message}

def checkUserCredentials(email=None,password=None) :
     try:
        return db.session.query(db.exists().where(users.email ==email , users.password==password)).scalar() 
     except Exception as e: 
        return responseHandler(False,{},str(e))

def getUserDataByEmail(email=None) :
     return users.query.filter(users.email==email).first()

