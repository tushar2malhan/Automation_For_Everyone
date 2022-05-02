select p.* from prescriptions pp, 
json_table(prescription_details, "$.prescription[*]"
 columns (tablet_details json path "$")) as p;
 
 select * from prescriptions;
