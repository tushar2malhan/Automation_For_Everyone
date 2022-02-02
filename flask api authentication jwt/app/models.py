from pydantic import BaseModel, ValidationError, root_validator
from typing import List, Optional, Dict
from enum import Enum
import re

class MemberTypes(Enum):
    hospital = 'hospital'
    member = 'member'
    pharmacy = 'pharmacy'
    diagnostics = 'diagnostics'
    clinic = 'clinic'
    doctor = 'doctor'
    PharmacyDealer = 'PharmacyDealer'
    DiagnosticDealer = 'DiagnosticDealer'
    insurance = 'insurance'


class CountryDetails(BaseModel):
    country_code: int
    country_name: str
    currency: str

class StateDetails(BaseModel):
    country_code: int
    state_code: int
    state_name: str

class CityDetails(BaseModel):
    country_code: int
    state_code: int
    city_code: int
    city_name: str
    
class FreeSubscriptionDetails(BaseModel):
    free_doctors_limit: int
    free_diagnostics_limit: int
    free_pharmacy_limit: int
    free_braches_limit: int
    free_duration: int
    cost = 0

class PlatinumSubscriptionDetails(BaseModel):
    platinum_doctors_limit: int
    platinum_diagnostics_limit: int
    platinum_pharmacy_limit: int
    platinum_braches_limit: int
    platinum_duration: int
    cost: int
    
class SilverSubscriptionDetails(BaseModel):
    silver_doctors_limit: int
    silver_diagnostics_limit: int
    silver_pharmacy_limit: int
    silver_braches_limit: int
    silver_duration: int
    cost: int

class GoldSubscriptionDetails(BaseModel):
    gold_doctors_limit: int
    gold_diagnostics_limit: int
    gold_pharmacy_limit: int
    gold_braches_limit: int
    gold_duration: int
    cost: int
    
class PremiumSubscriptionDetails(BaseModel):
    premium_doctors_limit: int
    premium_diagnostics_limit: int
    premium_pharmacy_limit: int
    premium_braches_limit: int
    premium_duration: int
    cost: int

class MasterData(BaseModel):
    id: Optional[int] = 0
    country: CountryDetails
    state: Optional[List[StateDetails]] = []
    city: Optional[List[CityDetails]] = []
    enrollment: Optional[List[str]] = ['hospital', 'member', 'pharmacy', 'diagnostics', 'clinic', 'doctor', 'PharmacyDealer', 'DiagnosticDealer', 'insurance']
    mem_assigned_role: Optional[List[str]] = ['admin', 'hospital-admin', 'employee'] 
    specalisation: Optional[List[str]] = []
    br_consultation_type: Optional[List[str]] = ['online', 'walkin', 'emergency']
    br_status: Optional[List[str]] = ['active', 'disabled', 'inactive', 'onhold']
    relationship: Optional[List[str]] = ['son', 'daughter', 'wife', 'father', 'mother', 'other']
    mode_of_payment: Optional[List[str]] = ['cash', 'online', 'card']
    payment_status: Optional[List[str]] = ['paid', 'declined', 'paid', 'onhold']
    subscription_status: Optional[List[str]] = ['active', 'inactive']
    terms_conditions_enrollment: Optional[List[str]] = []
    terms_conditions_pharmacy: Optional[List[str]] = []
    terms_conditions_diagnostics: Optional[List[str]] = []
    terms_conditions_branches: Optional[List[str]] = []
    subscription_type: Optional[List[str]] = ['free', 'platinum', 'silver', 'gold', 'premieum']
    free_subscription_details: Optional[FreeSubscriptionDetails] = FreeSubscriptionDetails(free_doctors_limit=0, free_braches_limit=0 ,free_duration=0, cost=0, free_pharmacy_limit=0, free_diagnostics_limit=0).dict()
    platinum_subscription_details: Optional[PlatinumSubscriptionDetails] = PlatinumSubscriptionDetails(platinum_doctors_limit=0,platinum_diagnostics_limit=0, platinum_pharmacy_limit=0, platinum_duration=0, cost=0, platinum_braches_limit=0).dict()
    silver_subscription_details: Optional[SilverSubscriptionDetails] = SilverSubscriptionDetails(silver_doctors_limit=0,silver_diagnostics_limit=0, silver_pharmacy_limit=0, silver_duration=0, cost=0, silver_braches_limit=0).dict()
    gold_subscription_details: Optional[GoldSubscriptionDetails] = GoldSubscriptionDetails(gold_doctors_limit=0,gold_diagnostics_limit=0, gold_pharmacy_limit=0, gold_duration=0, cost=0, gold_braches_limit=0).dict()
    premium_subscription_details: Optional[PremiumSubscriptionDetails] = PremiumSubscriptionDetails(premium_doctors_limit=0,premium_diagnostics_limit=0, premium_pharmacy_limit=0, premium_duration=0, cost=0, premium_braches_limit=0).dict()
    mem_login_type: Optional[List[str]] = ['mpin', 'face_id', 'finger_print', 'voice']
    
class UserInformation(BaseModel):
    first_name: str
    last_name: Optional[str] = ''
    gender: str
    member_pic: Optional[str] = ''
    member_status: str = 'active'
    member_login_type: Optional[str] = ''
    member_assigned_role: str
    mem_assigned_role_with: Optional[List[str]] = []
    dr_reg_no: Optional[str] = ''
    specialization: Optional[str] = ''
    qualification: Optional[str] = ''
    doctor_type: Optional[str] = ''
    total_exp: Optional[int] = 0
    dr_consultation_type: Optional[List[str]] = []
    previous_hospital: Optional[str] = ''
    current_hospital: Optional[str] = ''
    comm_ddress: Optional[str] = ''
    profile_is_sharable: Optional[int] = 0
    shared_with_drs: Optional[int] = 0
    my_doctors: Optional[List[str]] = []
    comments: Optional[str] = ''
    notify_SMS: Optional[int] = 0
    notify_whatsapp: Optional[int] = 0
    remind_me: Optional[int] = 0
    mem_has_pharmacy: Optional[int] = 0
    mem_has_diagnostic: Optional[int] = 0
    mem_has_appointments: Optional[int] = 0
    mem_has_prescription: Optional[int] = 0
    location: Optional[str] = ''
    city: Optional[str] = ''
    state: Optional[str] = ''
    pincode: Optional[str] = ''
    country: Optional[str] = ''
    Insurance_Details: Optional[str] = ''
    is_terms_condtions_checked: Optional[int] = 0
    check_terms_conditions: Optional[int] = 0
    terms_and_conditions_info: Optional[int] = 0
    youtub_url: Optional[str] = ''
    facebook_account: Optional[str] = ''
    linked_account: Optional[str] = ''
    twitter_account: Optional[str] = ''
    is_connected_now: Optional[int] = 0

    @root_validator(pre=True)
    def validation(cls, values):
        assert re.search(r'^[a-zA-Z]+$', values.get('first_name')), 'First name should be alphabets only'
        assert re.search(r'^[a-zA-Z]+$', values.get('last_name')), 'First name should be alphabets only'

class UserEnrollment(BaseModel):
    id: Optional[int] = 0
    enrollment_id: Optional[str] = ''
    mobile_number: str
    mobile_auth_pin: str
    user_login: str
    member_type: str
    last_login: Optional[str] = ''
    is_connected_now: Optional[int] = 0
    user_information: UserInformation
    created: Optional[str]
    created_by: Optional[str]
    modified: Optional[str]
    modified_by: Optional[str]
    
    @root_validator(pre=True)
    def validation(cls, values):
        assert values.get('mobile_number').isdigit() and len(values.get('mobile_number')) == 10, 'Mobile number must be 10 digits'
        assert values.get('member_type') in MemberTypes.__dict__.get('_member_names_'), 'Members should be with in domain'
        return values
        
class BranchDetails(BaseModel):
    br_name: str
    br_location: str
    br_city: str
    br_state: str
    br_country: str
    br_address: str
    br_logo_image: Optional[str]
    br_image: Optional[str]
    br_contact_no: str
    br_email: str
    br_specialization: Optional[str]
    br_consultation_type: Optional[List[str]] = ['online', 'walkin', 'emergency']
    br_enrolled_date: Optional[str]
    br_deactivatedOn: Optional[str]
    has_home_collection: Optional[int] = 0
    br_help_desk: Optional[str]
    br_services: Optional[List[str]] = []
    br_transport_service: Optional[List[str]] = []
    pharma_doctors: Optional[List[str]] = []
    pharma_dealers: Optional[List[str]] = []
    diagno_dealers: Optional[List[str]] = []
    help_desk: Optional[str] = ''
    has_online_bed_booking: Optional[int] = 0
    has_online_patient_visit: Optional[int] = 0
    web_site: Optional[str] = ''
    youtube: Optional[str] = ''
    facebook_id: Optional[str] = ''
    twitter_id: Optional[str] = ''
    share_data_outside: Optional[int] = 0
    has_online_payment: Optional[int] = 0
    timings: Optional[str] = ''
    holiday_info: Optional[str] = ''
    reports_available: Optional[int] = 0
    has_pharmacy: Optional[int] = 0
    has_diagnostic: Optional[int] = 0
    has_branch: Optional[int] = 0
    has_24X7: Optional[int] = 0
    guideline: Optional[List[str]]
    delete_history: Optional[int] = 0
    delete_history_phamacy: Optional[int] = 0
    delete_history_diagnostics: Optional[int] = 0
    delete_history_appointments: Optional[int] = 0
    delete_history_prescriptions: Optional[int] = 0
    delete_history_useraccess: Optional[int] = 0
    currency: Optional[str] = ''
    walkin_fee: Optional[int] = 0
    online_fee: Optional[int] = 0
    consultation_fee: Optional[int] = 0    

    # @root_validator(pre=True)
    # def validation(cls, values):
    #     br_name
    #     br_location: str
    #     br_city: str
    #     br_state: str
    #     br_country: str
    #     br_address: str
    #     br_logo_image: Optional[str]
    #     br_image: Optional[str]
    #     br_contact_no: str
    #     br_email: str
    #     br_specialization: Optional[str]

class HospitalDetails(BaseModel):
    id: Optional[int] = 0
    br_enroll_id: Optional[str]
    master_reg_no: str
    br_reg_Id: str
    br_status: str = 'active'
    branch_details: BranchDetails
    created: Optional[str]
    modified: Optional[str]
    created_by: Optional[str]
    modified_by: Optional[str]
    
class MemberInfo(BaseModel):
    first_name: str
    last_name: str
    gender: str
    relationship: str
    member_type: Optional[str] = 'member'
    
class MemberDetails(BaseModel):
    id: Optional[int] = 0
    enrollment_id: str
    member_enrollment_id: Optional[str] = ''
    members: MemberInfo
    created: Optional[str]
    modified: Optional[str]
    created_by: Optional[str]
    modified_by: Optional[str]
    
    
class BillingInformation(BaseModel):
    start_date: str
    end_date: str
    total_amount: float
    payment_status: str
    mode_of_payment: str
    transaction_id: str
    payment_date: str
    bank_name: str
    paid_by: str
    purchased_date: str
    activation_date: str
    doctors_limit: int
    pharmacy_limit: int
    diagnostics_limit: int
    branches_limit: int
    braches_count: int
    pharmacy_count: int
    diagnostics_count: int
    doctors_count: int
    subscription_status: str
    comments: str
    subscription_start_date: str
    subscription_end_date: str
    last_notification: str
    
class BillingSubscritpion(BaseModel):
    id: Optional[int]
    enrollment_id: str
    billing_information: BillingInformation
    created: Optional[str]
    created_by: Optional[str]
    modified: Optional[str]
    modified_by: Optional[str]
    
class LoginHistory(BaseModel):
    id: Optional[int] = 0
    enrollment_id: str
    device: str
    location: str
    ipaddress: str
    address: str
    log_date: Optional[str]
    created: Optional[str]
    modified: Optional[str]
    created_by: Optional[str]
    modified_by: Optional[str]
    
class UserLogin(BaseModel):
    mobile_number: str
    mobile_auth_pin: str
    device: str
    location: str
    ipaddress: str
    address: str
    enrollment_id: Optional[str]
    
    @root_validator(pre=True)
    def validate(cls, values):	
        assert values.get('mobile_number').isdigit() and len(values.get('mobile_number')) == 10, 'Mobile number must be 10 digits'
        return values