select * from appointments;


select * from user_member_info;

select * from appointments a  inner join user_member_info u
 on a.patient_id = u.enrollment_id where appointment_date = CURDATE()

DELIMITER $$
CREATE PROCEDURE user_dates()
BEGIN
	 select a.id,a.appointment_date,a.appointments, a.appointment_status,u.mobile_number  
     from appointments a  inner join user_member_info u
	 on a.patient_id = u.enrollment_id where appointment_date = CURDATE();
END $$
DELIMITER ;

CALL user_dates();

DROP PROCEDURE IF EXISTS user_dates;


