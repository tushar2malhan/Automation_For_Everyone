DELIMITER $$
create  procedure member_info(id int , name varchar(255) )
BEGIN 
	select * from user_member_info where user_name = name and mobile_number = id;
END $$
DELIMITER ;

call member_info(1212121212,'patu dgg');
DROP PROCEDURE IF EXISTS GetAllc;
-- IN PYTHON
-- 		self.cursor.callproc('member_info', [1212121212,'patu dgg'])
          # for r in self.cursor.stored_results():
--                result = r.fetchall()
--                print(result)
DELIMITER &
CREATE PROCEDURE app()
BEGIN select * from appointments;
END &s
DELIMITER ;

call app()