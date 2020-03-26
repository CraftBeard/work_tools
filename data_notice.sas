options noxwait;

/*Time Parameters*/
* 
%let my_date = 15Mar2020;
%put &sysdate.; 
%let my_date = &sysdate.; 

data _null_;
	call symput("mmyyyy", compress(put("&my_date."d-1, mmyy7.), "M"));
	call symput("yymmdd", put("&my_date."d-1, yymmdd6.));
run;

%put mmyyyy=&mmyyyy.;
%put yymmdd=&yymmdd.;

/*Path Parameters*/
%let output_path = C:\Users\1615066\Desktop\temp\Daily_Notice;

%macro unzip_file(zip_file, zip_path, unzip_path, file_psw);
%put zip_file=&zip_file.;
%put zip_path=&zip_path.;
%put unzip_path=&unzip_path.;
%put file_psw=&file_psw.;

%put ---Step1: xcopy /y "&zip_path.\&zip_file." "&unzip_path.";
x xcopy /y "&zip_path.\&zip_file." "&unzip_path.";

%put ---Step2: cd "&unzip_path.";
x cd "&unzip_path.";

%put ---Step3: "C:\progra~1\7-Zip\7zg.exe x &zip_file. &file_psw.";
x "C:\progra~1\7-Zip\7zg.exe x &zip_file. &file_psw.";
%mend unzip_file;

/*Card Delinquent List*/
%unzip_file(
	zip_file=daily_delq_Card_&yymmdd..zip, 
	zip_path=\\CNWPIPFIL18\CA_Share\CAR\Daily Delinquent Account List\CCMS,
	unzip_path=&output_path.,
	file_psw=-pCollhk&mmyyyy.#
);

/*Loan Delinquent List*/
%unzip_file(
	zip_file=daily_delq_rls_&yymmdd..zip, 
	zip_path=\\CNWPIPFIL18\CA_Share\CAR\Daily Delinquent Account List\RLS,
	unzip_path=&output_path.,
	file_psw=-pCollhk&mmyyyy.#
);

/*COLIST*/
x xcopy /y "\\hksctfil104\dat\wkgrps\SZ\PPQ_Sharing\Daily\COLIST.xlsx" "&output_path.";

/*rsmcds*/
x xcopy /y "\\HKSCTFIL100\3905dat\data\Collect\Upload\rsmcds.txt" "&output_path.";

/*open msg*/
x "H:\Harry\Daily Batch Log\Data Ready Notice 24Mar20  Internal .msg";