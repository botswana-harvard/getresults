import pyodbc

cnxn = pyodbc.connect("DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;DATABASE=BHPLAB")
cursor = cnxn.cursor()

def fetch_receiving(sample_id):
	sql = """select l.pid as sample_id, 
					l.datecreated as sample_date_received, 
					l.pat_id,
					l.sample_date_drawn, 
					case 
						when patindex('[0-9]:[0-5][0-9]', 
						l.sample_time_drawn)=0 and patindex('[012][0-9]:[0-5][0-9]',
						l.sample_time_drawn)=0 then '06:00' else
						l.sample_time_drawn end as sample_time_drawn, 
					case when patindex('[0-9]:[0-5][0-9]', 
						l.sample_time_drawn)=0 and patindex('[012][0-9]:[0-5][0-9]',
						l.sample_time_drawn)=0 then 'Time of sample draw unknown.'
							else '' end as sample_time_drawn_warning,	
						l.sample_protocolnumber, 
						l.sample_visitid as sample_visit_id, 
						l.sample_site_id, 				
						l.sample_condition, 
					case when bid.gender='M' or bid.gender='F' 
						then bid.gender else l.gender 
					end as gender, 
					case when isDate(bid.dob)=1 and bid.dob<=getdate()           
						then bid.dob
						else 
               case when isDate(l.dob)<>1 or l.dob>getdate() 
               	then dateadd(yy, -18, getdate()) 
               	else 
                   	convert(datetime, l.dob, 121)
               	end
               end as dob, 
               case when isDate(bid.dob)=1 and bid.dob<=getdate() 
               then '' 
               else 
               case when isDate(l.dob)<>1 or l.dob>getdate()
               then 'assuming 18yrs.'
               else '' end
               end as dob_warning,
               case l.other_pat_ref 
               	when '-9' then '--' 
               	when '-3' then '--'  else l.other_pat_ref end as other_pat_ref,
               case when patindex('%[A-Z]%', l.cinitials)<>0 then cinitials 
				 	when patindex('%[A-Z]%', 
				 	l.sample_clinician_initials)<>0 then sample_clinician_initials 
				 	else '--' end as sample_clinician_initials,
				 	l.sample_billingcode as sample_billing_code,
				 	case l.sample_comment 
				 	when '-9' then '' else l.sample_comment end as sample_comment,
				 	l.batch_id
				 from bhplab.dbo.lab01response as l
				left join bhp.dbo._bid as bid on bid.pid=l.pat_id 
 				where l.pid='%s'"""
 	sql = sql % sample_id

 	# print sql
 	cursor.execute(sql)
 	row = cursor.fetchone()
	return row

def fetch_orders():
	return ""

def fetch_results(sample_id, lab21_id):
	sql = """select l21.id as lab21_id,
				l21.pid as sample_id,
				l21.headerdate as report_date,
				l21.panel_id,
				rtrim(ltrim(lower(l21d.utestid))) as utestid, l21d.result,l21d.result_quantifier,
				l21d.status, l21d.flag, 
				case when l21d.comment is null then '' when l21d.comment='-3' then '' when l21d.comment='-9' then '' else l21d.comment end as result_comment,
				isNull(utest.LONGNAME, 'UNDEF (ref F0110)') as utestid_description,
				case when utest.utestid_units is null then ''  when utest.utestid_units = '-9' then '' else utest.utestid_units end as utestid_units,
				utestid_dec as utestid_decimal,
				'' as utestid_range_low,
				'' as utestid_range_high,
				l21d.validation_ref, 
				l21d.sample_assay_date,
				isCalculated as is_utestid_calculated,
				lower(utestid_formula) as utestid_formula,
				lower(utestid_valuetype) as utestid_value_type,
				l21d.keyopcreated as operator,
				l21d.keyoplastmodified as validator,
				l21d.datelastmodified as validation_date,
				'auto' as validation_method
				from BHPLAB.DBO.LAB21Response as L21
				left join BHPLAB.DBO.LAB21ResponseQ001X0 as L21D on L21.Q001X0=L21D.QID1X0
				left join BHPLAB.DBO.F0110Response as UTEST on UTEST.UTESTID=L21D.UTESTID
				where L21.PID='{$this->sample_id}'
				and L21.ID = {$this->lab21_id}
				and L21D.STATUS='F'""";
	return ""


def fetch_audit_trail():
	return ''


def is_valid_sample_id():
	return ''



