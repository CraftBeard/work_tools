/*
------------------------- Info -------------------------
Last Modified: Dec 5, 2019
Author: Alex
Version: 0.1

Continuous Variable Discretization
temp_in_data: input dataset name
temp_out_data: output dataset name
temp_option: column name1:min1:max1:groups1:describtion name1@column name2:min2:max2:groups2:describtion name2
------------------------- Info -------------------------

*/

/*
------------------------- Log -------------------------
Modified Date: Dec 5, 2019
Author: Alex
Version: 0.1
Modification: Continuous Variable Discretization
------------------------- Log -------------------------

*/

%macro discretization(temp_in_data, temp_out_data, temp_option);

%put temp_in_data: &temp_in_data.;
%put temp_out_data: &temp_out_data.;
%put temp_option: &temp_option.;

%let temp_desc=;
%do opt_cnt=1 %to %sysfunc(count(&temp_option.,@))+1;
	%let option=%scan(&temp_option.,&opt_cnt.,@); %put Option &opt_cnt.: &option.;	
	%let opt_col=%scan(&option.,1,:); %put opt_col: &opt_col.;
	%let opt_min=%scan(&option.,2,:); %put opt_min: &opt_min.;
	%let opt_max=%scan(&option.,3,:); %put opt_max: &opt_max.;
	%let opt_groups=%scan(&option.,4,:); %put opt_groups: &opt_groups.;
	%let opt_interval=%eval((&opt_max.-&opt_min.)/&opt_groups.); %put opt_interval: &opt_interval.;
	%let opt_label=%scan(&option.,5,:); %put opt_label: &opt_label.;
	%let temp_desc=&temp_desc. &opt_label.;

	proc format;
		value fmt_&opt_label.
			low-<&opt_min.="00.(-Inf,&opt_min.)"
			%do grp_cnt=1 %to &opt_groups.;
				%eval(&opt_min.+(&grp_cnt.-1)*&opt_interval.)-<%eval(&opt_min.+&grp_cnt.*&opt_interval.)="%sysfunc(putn(&grp_cnt.,z2.)).[%eval(&opt_min.+(&grp_cnt.-1)*&opt_interval.),%eval(&opt_min.+&grp_cnt.*&opt_interval.))"
			%end;
			%eval(&opt_min.+(&grp_cnt.-1)*&opt_interval.)-high="%sysfunc(putn(&grp_cnt.,z2.)).[%eval(&opt_min.+(&grp_cnt.-1)*&opt_interval.),+Inf)"
		;
	quit;
%end;

%put temp_desc: &temp_desc.;

data &temp_out_data.;
	set &temp_in_data.;
	length &temp_desc. $30.;
	%do opt_cnt=1 %to %sysfunc(count(&temp_option.,@))+1;
		%let option=%scan(&temp_option.,&opt_cnt.,@);
		%let opt_label=%scan(&option.,5,:); 
		%let opt_col=%scan(&option.,1,:); 
		%put &opt_label.=put(&opt_col.,fmt_&opt_label..);
		&opt_label.=put(&opt_col.,fmt_&opt_label..);
	%end;
run;

%mend discretization;

/*%discretization(*/
/*	temp_in_data=cars, */
/*	temp_out_data=cars, */
/*	temp_option=%nrstr(length:100:200:10:desc_length@horsepower:200:300:10:desc_horsepower)*/
/*);*/
