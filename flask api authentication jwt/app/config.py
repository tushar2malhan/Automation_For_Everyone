from os import getenv
from dotenv import load_dotenv
import pymysql
from json import dumps, loads

    
class Env_Variables:
    load_dotenv()
    enroll_establishment = getenv('MYSQL_ENROLLMENT_DB')
    
class StoredProcedures:
    masterData = 'sp_create_master'
    userEnrollment = 'sp_user_enrollment'
    hspEnrollment = 'SP_enroll_branch'
    getHspBranch = 'SP_get_branch'
    updateHspBranch = 'SP_Update_branch'
    addMember = 'sp_add_member'
    updateMember = 'sp_update_member'
    getMember = 'sp_get_member'
    addBilling = 'SP_create_billing'
    updateBilling = 'SP_Update_Billing'
    getBilling = 'SP_GetBilling'
    loginHistory = 'SP_Log_access'
        
class DatabaseConnection:
    load_dotenv()

    def __init__(self, database=None):
        self.connection = pymysql.connect(
            user=getenv('MYSQL_USER'),
            password=getenv('MYSQL_PASSWORD'),
            host=getenv('MYSQL_HOST'),
            database=database
        )
        self.cursor = self.connection.cursor()

    def createItems(self, stored_procedure=None, user_action=None, data=None):
        try:
            self.cursor.callproc(stored_procedure, (dumps(data), user_action))
            self.connection.commit()
            self.database_response = loads(self.cursor.fetchone()[0])
            return self.database_response
        except pymysql.err.OperationalError as e:
            print(e)
            return {'success': 0, 'message': 'Server Error', 'description': str(e)}

    def updateItems(self, stored_procedure=None, user_action=None, data=None):
        try:
            self.cursor.callproc(stored_procedure, (dumps(data), user_action))
            self.connection.commit()
            self.database_response = loads(self.cursor.fetchone()[0])
            return self.database_response
        except pymysql.err.OperationalError as e:
            return {'success': 0, 'message': 'Server Error', 'description': str(e)}
        
    def deleteItems(self, stored_procedure=None, user_action=None, data=None):
        try:
            self.cursor.callproc(stored_procedure, (dumps(data), user_action))
            self.connection.commit()
            self.database_response = loads(self.cursor.fetchone()[0])
            return self.database_response
        except pymysql.err.OperationalError as e:
            return {'success': 0, 'message': 'Server Error', 'description': str(e)}
        
    def getItem(self, stored_procedure=None, user_action=None, data=None):  
        try:
            self.cursor.callproc(stored_procedure, (dumps(data), user_action))
            self.database_response = [loads(i[0]) for i in self.cursor.fetchall()]
            return self.database_response[0] if len(self.database_response) else {}
        except pymysql.err.OperationalError as e:
            return {'success': 0, 'message': 'Server Error', 'description': str(e)}
        
    def getItems(self, stored_procedure=None, user_action=None, data=None):
        self.cursor.callproc(stored_procedure, (dumps(data), user_action))
        self.database_response = [loads(i[0]) for i in self.cursor.fetchall()]
        return self.database_response