/*Import Part*/
libname x excelcs "c:\temp\test.xls";
proc import out=test_data
	dbms=xls
	datafile="c:\temp\test.xls"
	replace;
	getnames=yes;
	guessingrows=1024;
run;

/*Export Part 1*/
proc export data=sashelp.cars
	outfile="c:\temp\test.xls"
	dbms=xls replace label;
	sheet="cars";
run;

proc export data=sashelp.zipcode
	outfile="c:\temp\test.xls"
	dbms=xls replace label;
	sheet="zipcode";
run;

/*Export Part 2*/
proc export data=sashelp.cars
	outfile="c:\temp\test"
	dbms=xls replace label;
	sheet="cars";
run;

proc export data=sashelp.zipcode
	outfile="c:\temp\test"
	dbms=xls replace label;
	sheet="zipcode";
run;

/*Export Part 3*/
proc export data=sashelp.cars
	outfile="c:\temp\test.xls"
	dbms=excelcs replace label;
	sheet="cars";
run;

/*Label seems to have length limit*/
proc export data=sashelp.zipcode
	outfile="c:\temp\test.xls"
	dbms=excelcs replace;
	sheet="zipcode";
run;
