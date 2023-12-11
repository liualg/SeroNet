# seronetdb-Vaccine_response
select 
	ptVisit.Research_Participant_ID, ptVisit.Primary_Study_Cohort, ptVisit.CBC,
    cChort.Cancer, vaccStatus.Vaccination_Status as raw_status,
    
CASE 
	When vaccStatus.Vaccination_Status not like 'No vaccination event reported' then True
    Else False
END as Vaccinated 

from `seronetdb-Vaccine_Response`.Cancer_Cohort as cChort
left join `seronetdb-Vaccine_Response`.Participant_Visit_Date_Normalized_Duration_View as ptVisit ON 
	cChort.Visit_Info_ID = ptVisit.Visit_Info_ID
left join `seronetdb-Vaccine_Response`.Covid_Vaccination_Status as vaccStatus ON
	cChort.Visit_Info_ID=vaccStatus.Visit_Info_ID
    
where ptVisit.CBC in ('Icahn School Of  Medicine At Mount Sinai')
;
## ---------------------------------------------------------------------------------- ##
## ---------------------------------------------------------------------------------- ##
# group by command 
# seronetdb-Vaccine_response
select 
	ptVisit.Research_Participant_ID, ptVisit.Primary_Study_Cohort, ptVisit.CBC,
   --  GROUP_CONCAT(DISTINCT replace(cChort.Cancer,' Cancer','') SEPARATOR ', ') as 'Cancer Types', vaccStatus.Vaccination_Status as raw_status,
    
CASE 
	When vaccStatus.Vaccination_Status not like 'No vaccination event reported' then True
    Else False
END as Vaccinated 

from `seronetdb-Vaccine_Response`.Cancer_Cohort as cChort
left join `seronetdb-Vaccine_Response`.Participant_Visit_Date_Normalized_Duration_View as ptVisit ON 
	cChort.Visit_Info_ID = ptVisit.Visit_Info_ID
left join `seronetdb-Vaccine_Response`.Covid_Vaccination_Status as vaccStatus ON
	cChort.Visit_Info_ID=vaccStatus.Visit_Info_ID
    
-- Group By Research_Participant_ID
;
## ---------------------------------------------------------------------------------- ##
## ---------------------------------------------------------------------------------- ##
# Only the Cancer Types Group by 
# seronetdb-Vaccine_response
# group by command 
# seronetdb-Vaccine_response
select 
	cChort.Cancer, count(Distinct ptVisit.Research_Participant_ID) as 'Number of unique pt'

from `seronetdb-Vaccine_Response`.Cancer_Cohort as cChort
left join `seronetdb-Vaccine_Response`.Participant_Visit_Date_Normalized_Duration_View as ptVisit ON 
	cChort.Visit_Info_ID = ptVisit.Visit_Info_ID
-- left join `seronetdb-Vaccine_Response`.Covid_Vaccination_Status as vaccStatus ON
-- 	cChort.Visit_Info_ID=vaccStatus.Visit_Info_ID
    
Group By cChort.Cancer
;  
## ---------------------------------------------------------------------------------- ##
## ---------------------------------------------------------------------------------- ##
select count(distinct(left(Visit_Info_ID , 10))) from `seronetdb-Vaccine_Response`.Cancer_Cohort; #14_M10017 : B01, take the first 1/2


select Visit_Info_ID from `seronetdb-Vaccine_Response`.Cancer_Cohort; #14_M10017 : B01, take the first 1/2


