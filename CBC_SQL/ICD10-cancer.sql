with 
subject_level as (
select Visit_Info_ID,ICD_10_Code 
FROM `seronetdb-Vaccine_Response`.Cancer_Cohort as cc

union
select Visit_Info_ID,Cancer_Description_Or_ICD10_codes 
FROM `seronetdb-Vaccine_Response`.Comorbidities_Names as CN 
            
),

next_data as (
	select subject_level.Visit_Info_ID, subject_level.ICD_10_Code, Visit_Number, Visit_Date_Duration_From_Index from subject_level
    left join `seronetdb-Vaccine_Response`.Participant_Visit_Info as PVI ON
			subject_level.Visit_Info_ID = PVI.Visit_Info_ID
)

SELECT distinct Visit_Info_ID, ICD_10_Code, Visit_Number, Visit_Date_Duration_From_Index
from next_data
where Visit_Info_ID like '27_%', 
where ICD_10_Code not like '%Not Reported%';

