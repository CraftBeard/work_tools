/*
------------------------- Info -------------------------
Last Modified: Dec 4, 2019
Author: Alex
Version: 0.1

Set time parameters
------------------------- Info -------------------------

*/

/*
------------------------- Log -------------------------
Modified Date: Dec 4, 2019
Author: Alex
Version: 0.1
Modification: Set time parameters
------------------------- Log -------------------------

*/

%macro time_parameters(macro_date, mth_cnt=12);

	%put macro_date=&macro_date.;

	%global sub_date;

	data _null_;
		call symput("sub_date", substr(put(intnx("day", input(put(&macro_date., z8.), yymmdd8.), -1), yymmddn8.), 3, 6));
		call symput("yesterday", put(intnx("day", input(put(&macro_date., z8.), yymmdd8.), -1), yymmddn8.));
	run;
	%put sub_date=&sub_date.;
	%put yesterday=&yesterday.;

	/*First & Last date of months*/
	%do cnt=0 %to &mth_cnt.;
		%global temp_date&cnt. temp_mth&cnt. temp_mth_beg&cnt. temp_mth_end&cnt.;

		data _null_;
			call symput("temp_date&cnt.", put(intnx("month", input(put(&macro_date., z8.), yymmdd8.), -&cnt., "b"), yymmddn8.));
			call symput("temp_mth&cnt.", put(intnx("month", input(put(&macro_date., z8.), yymmdd8.), -&cnt., "b"), yymmn6.));
			call symput("temp_mth_beg&cnt.", put(intnx("month", input(put(&macro_date., z8.), yymmdd8.), -&cnt., "b"), yymmddn8.));
			call symput("temp_mth_end&cnt.", put(intnx("month", input(put(&macro_date., z8.), yymmdd8.), -&cnt., "e"), yymmddn8.));
		run;

		%put temp_date&cnt.=&&temp_date&cnt.;		
		%put temp_mth&cnt.=&&temp_mth&cnt.;
		%put temp_mth_beg&cnt.=&&temp_mth_beg&cnt.;
		%put temp_mth_end&cnt.=&&temp_mth_end&cnt.;
	%end;

%mend time_parameters;

/*%time_parameters(macro_date=20191201, mth_cnt=12);*/

%macro time_stamp(para_name);

	%global &para_name.;

	data _null_;
		call symput("&para_name.", datetime());
	run;
	%put &para_name.=&&&para_name..;

%mend time_stamp;

/*%time_stamp(para_name=start_time);*/
/*%time_stamp(para_name=end_time);*/

%macro time_diff(start_time, end_time);

	data _null_;
		call symput("min_diff", compress(intck("minute", &start_time., &end_time.)));
		call symput("sec_diff", compress(intck("second", &start_time., &end_time.)));
	run;
	%put Duration: &min_diff.mins &sec_diff.s;

%mend time_diff;

/*%time_diff(start_time=&start_time., end_time=&end_time.);*/
