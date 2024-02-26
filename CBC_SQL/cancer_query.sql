# seronetdb-Vaccine_response
with 
Cancer_visits as (
	Select Visit_Info_ID from `seronetdb-Vaccine_Response`.Cancer_Cohort as CC
	Union
	Select Visit_Info_ID from `seronetdb-Vaccine_Response`.Comorbidities_Names as CN
		where Cancer_Description_Or_ICD10_codes not in ('Not Reported')
	Union
    Select Visit_Info_ID from `seronetdb-Vaccine_Response`.Participant_Visit_Info as PVi
		where Primary_Study_Cohort = 'Cancer'
 ),
#'Cohort' as Data_location
#'Comorbidities' as Data_location
subject_level as (
	Select 

		ptVisit.Visit_Info_ID, ptVisit.Research_Participant_ID, 
		
		CASE #refernce fomr Michae Ritchie for internal org. codes
			When ptVisit.Visit_Info_ID like '14_%' then 'Mt. Sinai'
			When ptVisit.Visit_Info_ID like '41_%' then 'Feinstein'
			When ptVisit.Visit_Info_ID like '27_%' then 'UMN'
			When ptVisit.Visit_Info_ID like '32_22%' then 'Midwestern'
			When ptVisit.Visit_Info_ID like '32_%' then 'Arizona State University'
-- 			when ptVisit.Visit_Info_ID like '32_33%' then 'Dignity Health'
-- 			when ptVisit.Visit_Info_ID like '32_34%' then 'ValleyWise'
-- 			when ptVisit.Visit_Info_ID like '32_35%' then 'Columbia'
-- 			when ptVisit.Visit_Info_ID like '32_77%' then 'Phoenix Childrens Hospital'
			ELSE null
		END as CBC,

        
        ptVisit.Primary_Study_Cohort, 
		
		ptVisit.Type_Of_Visit, demo.Sunday_Prior_To_Visit_1, ptVisit.Visit_Number, ptVisit.Visit_Date_Duration_From_Index,

		demo.Age, 
		CASE #age of 5 year buckets
			When demo.Age between 0 and 5 then 'age: 0-5'
            When demo.Age between 6 and 10 then 'age: 6-10'
			When demo.Age between 11 and 15 then 'age: 11-15'
			When demo.Age between 16 and 20 then 'age: 16-20'
            When demo.Age between 21 and 25 then 'age: 21-25'
            When demo.Age between 26 and 30 then 'age: 26-30'
            When demo.Age between 31 and 35 then 'age: 31-35'
            When demo.Age between 36 and 40 then 'age: 36-40'
            When demo.Age between 41 and 45 then 'age: 41-45'
            When demo.Age between 46 and 50 then 'age: 46-50'
            When demo.Age between 51 and 55 then 'age: 51-55'
            When demo.Age between 56 and 60 then 'age: 56-60'
            When demo.Age between 61 and 65 then 'age: 61-65'
            When demo.Age between 66 and 70 then 'age: 66-70'
            When demo.Age between 71 and 75 then 'age: 71-75'
            When demo.Age between 76 and 80 then 'age: 76-80'
            When demo.Age between 81 and 85 then 'age: 81-85'
            When demo.Age between 86 and 90 then 'age: 86-90'
			When demo.Age >=90 then 'age: 90+'
			Else null 

		END as Age_bin, 
		
		demo.Race, demo.Ethnicity, demo.Sex_At_Birth, 
		comorb.Cancer_Description_Or_ICD10_codes, normNames.`Harmonized Cancer Name`,
        
		cChort.Cured,
		tHistory.Treatment,
        tHistory.Stop_Date_Duration_From_Index,
		CASE
			When cChort.In_Remission in ('Yes') then 'In_Remission'
			When cChort.In_Unspecified_Therapy in ('Yes') then 'In_Unspecified_Therapy'
			When cChort.Chemotherapy in ('Yes') then 'Chemotherapy'
			When cChort.`Radiation Therapy` in ('yes') then 'Radiation Therapy'
			When cChort.Surgery in ('Yes') then 'Surgery'
			Else 'No' 

		END as Treatment_type, 
		
		vaccStatus.Vaccination_Status, 
		vaccStatus.`SARS-CoV-2_Vaccine_Type`, 
		vaccStatus.`SARS-CoV-2_Vaccination_Date_Duration_From_Index`, 

		covidHis.Breakthrough_COVID,covidHis.PCR_Test_Date_Duration_From_Index, 
		covidHis.Rapid_Antigen_Test_Date_Duration_From_Index, 
		covidHis.Antibody_Test_Date_Duration_From_Index,
		
		CASE
			WHEN EXISTS (select *
						 from `seronetdb-Vaccine_Response`.Cancer_Cohort as B
						 where B.Visit_Info_ID = Cancer_visits.Visit_Info_ID)
			THEN 'Cancer Cohort table'
			ELSE 'Comorbidity Table'
		END as mysql_db_location
		

		
	 --    CASE
	-- 	WHEN SOMETHING.`Original Cancer Name` like 'Condition Not Described' then 'Comobidity' as data_origin
	-- 	END


	From Cancer_visits
		left join `seronetdb-Vaccine_Response`.Cancer_Cohort as cChort ON
			Cancer_visits.Visit_Info_ID = cChort.Visit_Info_ID
		left join `seronetdb-Vaccine_Response`.Participant_Visit_Info as ptVisit ON 
			Cancer_visits.Visit_Info_ID = ptVisit.Visit_Info_ID
		left join `seronetdb-Vaccine_Response`.Covid_Vaccination_Status as vaccStatus ON
			Cancer_visits.Visit_Info_ID = vaccStatus.Visit_Info_ID
		left join `seronetdb-Vaccine_Response`.Covid_History as covidHis ON
			Cancer_visits.Visit_Info_ID = covidHis.Visit_Info_ID
		left join `seronetdb-Vaccine_Response`.Normalized_Cancer_Names_v2 as normNames ON
			Cancer_visits.Visit_Info_ID = normNames.Visit_Info_ID
		left join `seronetdb-Vaccine_Response`.Comorbidities_Names as comorb ON
			Cancer_visits.Visit_Info_ID=comorb.Visit_Info_ID
		left join `seronetdb-Vaccine_Response`.Treatment_History as tHistory ON
			ptVisit.Visit_Info_ID=tHistory.Visit_Info_ID
		left join `seronetdb-Vaccine_Response`.Accrual_Participant_Info as demo ON
			ptVisit.Research_Participant_ID=demo.Research_Participant_ID
),

#current status
final as (
Select  
-- 	count(distinct subject_level.Research_Participant_ID) '#ofsubjets',
-- 	count(distinct Visit_Info_ID) '#ofvisits'
	Visit_Info_ID, subject_level.Research_Participant_ID, subject_level.CBC, subject_level.Primary_Study_Cohort, 
    subject_level.Type_Of_Visit, subject_level.Sunday_Prior_To_Visit_1, subject_level.Visit_Number, subject_level.Visit_Date_Duration_From_Index, 
    subject_level.Age, subject_level.Age_bin, subject_level.Race, subject_level.Ethnicity, subject_level.Sex_At_Birth, 
    
        Case
		When subject_level.`Harmonized Cancer Name` like '%|%' or subject_level.`Cancer_Description_Or_ICD10_codes` like '%|%' then 'Multiple'
        When subject_level.`Harmonized Cancer Name` in ('Not Reported') or subject_level.`Cancer_Description_Or_ICD10_codes` in ('Not Reported') then 'Not Reported'
        When subject_level.`Harmonized Cancer Name` in ('nan') or subject_level.`Cancer_Description_Or_ICD10_codes` in ('nan') then null
        Else 'Single'
    End as Multiple_Single_Cancer,
    
    subject_level.Cancer_Description_Or_ICD10_codes, subject_level.`Harmonized Cancer Name`, subject_level.Cured, subject_level.Treatment, 
    subject_level.Stop_Date_Duration_From_Index, subject_level.Treatment_type, subject_level.Vaccination_Status, 
    subject_level.`SARS-CoV-2_Vaccine_Type`, subject_level.`SARS-CoV-2_Vaccination_Date_Duration_From_Index`, Breakthrough_COVID, subject_level.
    PCR_Test_Date_Duration_From_Index, subject_level.Rapid_Antigen_Test_Date_Duration_From_Index, subject_level.
    Antibody_Test_Date_Duration_From_Index, subject_level.mysql_db_location

From subject_level
)

select distinct *
-- *
-- Research_Participant_ID
-- count( distinct Visit_Info_ID)
-- count( distinct Research_Participant_ID)
from final
where Cancer_Description_Or_ICD10_codes like "%mul%"
 
;

-- from `seronetdb-Vaccine_Response`.Cancer_Cohort as cChort
   