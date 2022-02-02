from typing import Optional, List, Dict, Union
from fastapi import FastAPI, Header, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from models import *
from config import *
from datetime import datetime, timedelta
from secrets import token_urlsafe
from routes import EndPoints
import bcrypt

app = FastAPI(
    title='DR_NEXT',
    description = 'All apis are working on drnext app',
    version = '1.0.0',
    contact={},
    license_info={}
)

pwd_context = CryptContext(schemes=['bcrypt',], deprecated="auto")

def db_connect():
    try:
        db = DatabaseConnection(Env_Variables.enroll_establishment)
        yield db
    finally:
        db.connection.close()



@app.post(EndPoints.masterData.value)
async def create_record_masterdata(data: MasterData,root_user: Optional[str]=Header(None), db_connect = Depends(db_connect)):
    # db_connect = DatabaseConnection(Env_Variables.enroll_establishment)
    if db_connect.connection.cursor():
        result = db_connect.createItems(StoredProcedures.masterData, 'create', data.dict())
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=result) if result.get('success') else JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED, content='data not modified')
    raise HTTPException(status_code=500, detail='ServerError')

@app.get(EndPoints.masterDataInfo.value)
async def get_record_masterdata(item_id: int, db_connect = Depends(db_connect)):
    if db_connect.connection.cursor():
        result = db_connect.getItems(StoredProcedures.masterData, 'get', {'id': item_id})
        return JSONResponse(status_code=status.HTTP_200_OK, content=MasterData(**result[0]).dict()) if len(result) else JSONResponse(status_code=status.HTTP_404_NOT_FOUND)
    raise HTTPException(status_code=500, detail='ServerError')

@app.put(EndPoints.masterDataUpdate.value)
async def update_record_masterdata(data: MasterData, db_connect = Depends(db_connect)):
    # db_connect = DatabaseConnection(Env_Variables.enroll_establishment)
    if db_connect.connection.cursor():
        existing = db_connect.getItems(StoredProcedures.masterData, 'get', {'id': data.id})[0]
        existing.update(data.dict())
        result = db_connect.updateItems(StoredProcedures.masterData, 'update', MasterData(**existing).dict())
        return JSONResponse(status_code=status.HTTP_200_OK, content=result) if result.get('success') else JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED, content='data not modified')
    raise HTTPException(status_code=500, detail='ServerError')

@app.post(EndPoints.userEnrollment.value)
async def create_user(user_details: UserEnrollment, root_user: Optional[str]=Header(None), db_connect = Depends(db_connect)):
    # db_connect = DatabaseConnection(Env_Variables.enroll_establishment)
    user_details.enrollment_id = str(user_details.member_type[:3]).upper()+str(abs(hash(token_urlsafe(5))))
    if user_details.member_type in ('member', 'admin'):
        user_details.created_by = user_details.modified_by = user_details.enrollment_id
    else:
        user_details.created_by = user_details.modified_by = root_user
    user_details.mobile_auth_pin = pwd_context.hash(user_details.mobile_auth_pin)
    if db_connect.connection.cursor():
        result = db_connect.createItems(StoredProcedures.userEnrollment, 'create', user_details.dict())
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=result) if result.get('success') else JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED, content='data not modified')
    raise HTTPException(status_code=500, detail='ServerError')

@app.put(EndPoints.updateProfile.value)
async def create_user(user_details: UserEnrollment, root_user: Optional[str]=Header(None), db_connect = Depends(db_connect)):
    # db_connect = DatabaseConnection(Env_Variables.enroll_establishment)
    if db_connect.connection.cursor():
        existing = db_connect.getItems(StoredProcedures.userEnrollment, 'get', {'enrollment_id': user_details.enrollment_id})[0]
        existing.update(user_details.dict())
        result = db_connect.updateItems(StoredProcedures.userEnrollment, 'update', UserEnrollment(**existing).dict())
        return JSONResponse(status_code=status.HTTP_200_OK, content=result) if result.get('success') else JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED, content='data not modified')
    raise HTTPException(status_code=500, detail='ServerError')

@app.get(EndPoints.getUserInformation.value)
async def get_user_information(enrollment_id: str, db_connect = Depends(db_connect)):
    # db_connect = DatabaseConnection(Env_Variables.enroll_establishment)
    if db_connect.connection.cursor():
        result = db_connect.getItems(StoredProcedures.userEnrollment, 'get', {'enrollment_id': enrollment_id})
        return JSONResponse(status_code=status.HTTP_200_OK, content=UserEnrollment(**result[0]).dict()) if len(result) else JSONResponse(status_code=status.HTTP_404_NOT_FOUND)
    raise HTTPException(status_code=500, detail='ServerError')


@app.post(EndPoints.hospitalEnrollment.value)
async def create_hsp(data: HospitalDetails, root_user: Optional[str]=Header(None), db_connect = Depends(db_connect)):
    # db_connect = DatabaseConnection(Env_Variables.enroll_establishment)
    if db_connect.connection.cursor():
        data.br_enroll_id = 'HSP'+str(abs(hash(token_urlsafe(5))))
        data.created_by = data.modified_by = root_user
        result = db_connect.createItems(StoredProcedures.hspEnrollment, 'create', data.dict())
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=result) if result.get('success') else JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED, content='data not modified')
    raise HTTPException(status_code=500, detail='ServerError')

@app.put(EndPoints.updateHospital.value)
async def update_hsp(data: HospitalDetails, root_user: Optional[str]=Header(None), db_connect = Depends(db_connect)):
    # db_connect = DatabaseConnection(Env_Variables.enroll_establishment)
    if db_connect.connection.cursor():
        data.modified_by = root_user
        result = db_connect.updateItems(StoredProcedures.updateHspBranch, 'update', data.dict())
        return JSONResponse(status_code=status.HTTP_200_OK, content=result) if result.get('success') else JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED, content='data not modified')
    raise HTTPException(status_code=500, detail='ServerError')


@app.get(EndPoints.getHospitalInfo.value)
async def get_hsp(br_enroll_id: str, root_user: Optional[str]=Header(None), db_connect = Depends(db_connect)):
    # db_connect = DatabaseConnection(Env_Variables.enroll_establishment)
    if db_connect.connection.cursor():
        result = db_connect.getItems(StoredProcedures.getHspBranch, 'get', {"br_enroll_id": br_enroll_id})
        return JSONResponse(status_code=status.HTTP_200_OK, content=HospitalDetails(**result[0]).dict()) if len(result) else JSONResponse(status_code=status.HTTP_404_NOT_FOUND)
    raise HTTPException(status_code=500, detail='ServerError')

# column mapping class: "MemberDetails"
# field mapping: {"member_enrollment_id"}
# stored procedure: "sp_add_member"
@app.post(EndPoints.addMember.value)
async def add_member(data: MemberDetails, root_user: Optional[str]=Header(None), db_connect = Depends(db_connect)):
    # db_connect = DatabaseConnection(Env_Variables.enroll_establishment)
    if db_connect.connection.cursor():
        data.member_enrollment_id = 'UMEM'+str(abs(hash(token_urlsafe(5))))
        data.created_by = data.modified_by = data.enrollment_id
        result = db_connect.createItems(StoredProcedures.addMember, 'create', data.dict())
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=result) if result.get('success') else JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED, content='data not modified')
    raise HTTPException(status_code=500, detail='ServerError')  

@app.put(EndPoints.updateMember.value)
async def update_member(data: MemberDetails, root_user: Optional[str]=Header(None), db_connect = Depends(db_connect)):
    # db_connect = DatabaseConnection(Env_Variables.enroll_establishment)
    if db_connect.connection.cursor():
        data.modified_by = root_user
        result = db_connect.updateItems(StoredProcedures.updateMember, 'update', data.dict())
        return JSONResponse(status_code=status.HTTP_200_OK, content=result) if result.get('success') else JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED, content='data not modified')
    raise HTTPException(status_code=500, detail='ServerError') 


@app.get(EndPoints.getMember.value)
async def getMembers(enrollment_id: str, root_user: Optional[str]=Header(None), db_connect = Depends(db_connect)):
    # db_connect = DatabaseConnection(Env_Variables.enroll_establishment)
    if db_connect.connection.cursor():
        result = db_connect.getItems(StoredProcedures.getMember, 'get', {'enrollment_id': enrollment_id})
        return JSONResponse(status_code=status.HTTP_200_OK, content=result) if len(result) else JSONResponse(status_code=status.HTTP_404_NOT_FOUND)
    raise HTTPException(status_code=500, detail='ServerError')

                        
@app.post(EndPoints.addBilling.value)
async def add_billing(data: BillingSubscritpion, root_user: Optional[str]=Header(None), db_connect = Depends(db_connect)):
    # db_connect = DatabaseConnection(Env_Variables.enroll_establishment)
    if db_connect.connection.cursor():
        data.created_by = data.modified_by = root_user
        result = db_connect.createItems(StoredProcedures.addBilling, 'create', data.dict())
        return JSONResponse(status.HTTP_201_CREATED, content=result) if result.get('success') else JSONResponse(status.HTTP_304_NOT_MODIFIED)
    return HTTPException(status_code=500, detail='ServerError')

@app.put(EndPoints.updateBilling.value)
async def update_billing(data: BillingSubscritpion, root_user: Optional[str]=Header(None), db_connect = Depends(db_connect)):
    # db_connect = DatabaseConnection(Env_Variables.enroll_establishment)
    if db_connect.connection.cursor():
        data.modified_by = root_user
        result = db_connect.createItems(StoredProcedures.updateBilling, 'update', data.dict())
        return JSONResponse(status_code=status.HTTP_200_OK, content=result) if result.get('success') else JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED, content='data not modified')
    raise HTTPException(status_code=500, detail='ServerError')

@app.get(EndPoints.getBillingInfo.value)
async def get_billing_info(id: str, root_user: Optional[str]=Header(None), db_connect = Depends(db_connect)):    
    # db_connect = DatabaseConnection(Env_Variables.enroll_establishment)
    if db_connect.connection.cursor():
        result = db_connect.getItems(StoredProcedures.getBilling, 'get', {'id': id})
        return JSONResponse(status_code=status.HTTP_200_OK, content=result) if len(result) else JSONResponse(status_code=status.HTTP_404_NOT_FOUND)
    raise HTTPException(status_code=500, detail='ServerError')

@app.post(EndPoints.authenticate.value)
async def login(data: UserLogin, db_connect = Depends(db_connect)):
    # db_connect = DatabaseConnection(Env_Variables.enroll_establishment)
    result = db_connect.getItems(StoredProcedures.userEnrollment, 'get', {'mobile_number': data.mobile_number})
    if db_connect.connection.cursor():
        if len(result): 
            user = UserEnrollment(**(result[0]))
            if not pwd_context.verify(data.mobile_auth_pin, user.mobile_auth_pin): return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'message': 'password mismatch'})
            data.enrollment_id = user.enrollment_id
            logging_user = db_connect.createItems(StoredProcedures.loginHistory, 'create', data.dict())
            if logging_user.get('success'):
                return JSONResponse(status_code=status.HTTP_200_OK, content={'jwt_token': 'niubnn;kninikbbj'})
            else: return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED)
        else: return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED)
    raise HTTPException(status_code=500, detail='ServerError')
        