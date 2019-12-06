/*
------------------------- Info -------------------------
Last Modified: Dec 4, 2019
Author: Alex
Version: 0.1

Output data cols
------------------------- Info -------------------------

*/

/*
------------------------- Log -------------------------
Modified Date: Dec 4, 2019
Author: Alex
Version: 0.1
Modification: Output data cols
------------------------- Log -------------------------

*/

%macro data_dictionary(temp_data, dict_name, dict_path=);

proc contents noprint 
	data=&temp_data. out=temp_data;
run;

data temp_data2;
	set temp_data(
		keep=libname memname name length format label formatl
	);
	name=upcase(name);
run;

proc export data=temp_data2
     outfile="&dict_path.\&dict_name..csv"
     dbms=csv 
     label replace;
run;

%mend data_dictionary;

/*libname cacs "" access=readonly;*/
%data_dictionary(temp_data=, dict_name=);
