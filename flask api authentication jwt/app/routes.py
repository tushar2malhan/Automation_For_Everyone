from enum import Enum

class EndPoints(Enum):
    masterData = '/masterData'
    masterDataInfo = '/masterDataInfo/{item_id}'
    masterDataUpdate = '/masterDataUpdate'
    userEnrollment = '/UserEnrollment'
    updateProfile = '/UpdateProfile'
    getUserInformation = '/GetUserInformation/{enrollment_id}'
    hospitalEnrollment = '/HospitalEnrollment'
    updateHospital = '/UpdateHospital'
    getHospitalInfo = '/GetHospitalInfo/{br_enroll_id}'
    addMember = '/AddMember'
    updateMember = '/UpdateMember'
    getMember = '/GetMember/{enrollment_id}'
    addBilling = '/AddBillingData'
    updateBilling = '/UpdateBilling'
    getBillingInfo = '/GetBillingInfo/{id}'
    authenticate = '/Authenticate'