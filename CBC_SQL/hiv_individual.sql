With 
hiv_visits_ud as (
	Select Visit_Info_ID from `seronetdb-Vaccine_Response`.HIV_Cohort as HC
		Union
		Select Visit_Info_ID from `seronetdb-Vaccine_Response`.Comorbidities_Names as CN
			where Autoimmune_Disorder_Description_Or_ICD10_codes in ('HIV')
		union 
        select Visit_Info_ID from `seronetdb-Vaccine_Response`.Participant_Visit_Info as PVi
			where Primary_Study_Cohort = 'HIV'
),

hiv_visits as (
	select distinct Visit_Info_ID from hiv_visits_ud
),

subject_level as (

select 
hiv_visits.Visit_Info_ID, 

ptVisit.Research_Participant_ID,
		
		CASE #refernce fomr Michae Ritchie for internal org. codes
			When hiv_visits.Visit_Info_ID like '14_%' then 'Mt. Sinai'
			When hiv_visits.Visit_Info_ID like '41_%' then 'Feinstein'
			When hiv_visits.Visit_Info_ID like '27_%' then 'UMN'
			When hiv_visits.Visit_Info_ID like '32_22%' then 'Midwestern'
			When hiv_visits.Visit_Info_ID like '32_%' then 'Arizona State University'
-- 			when ptVisit.Visit_Info_ID like '32_33%' then 'Dignity Health'
-- 			when ptVisit.Visit_Info_ID like '32_34%' then 'ValleyWise'
-- 			when ptVisit.Visit_Info_ID like '32_35%' then 'Columbia'
-- 			when ptVisit.Visit_Info_ID like '32_77%' then 'Phoenix Childrens Hospital'
			ELSE null
		END as CBC,

		CASE 
			WHEN CNames.Autoimmune_Disorder_Description_Or_ICD10_codes like '%B20%' then 'EMR'
            ELSE 'Self Reported'
		END as Provanance,
        
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
        
        hiv.Viral_RNA_Load, hiv.Viral_RNA_Load_Reporting_Date_Duration_From_Index,
        hiv.CD4_Count, hiv.CD4_Count_Reporting_Date_Duration_From_Index, 
        hiv.Opportunistic_Infection_History, hiv.OI_Status_Reporting_Date_Duration_From_Index, 
        
        
        covidHis.Breakthrough_COVID,covidHis.PCR_Test_Date_Duration_From_Index, 
		covidHis.Rapid_Antigen_Test_Date_Duration_From_Index, 
		covidHis.Antibody_Test_Date_Duration_From_Index,
        CNames.Autoimmune_Disorder_Description_Or_ICD10_codes as auto_ICD10



from hiv_visits

left join `seronetdb-Vaccine_Response`.Participant_Visit_Info as ptVisit ON 
	hiv_visits.Visit_Info_ID = ptVisit.Visit_Info_ID
left join `seronetdb-Vaccine_Response`.Covid_Vaccination_Status as vaccStatus ON
	hiv_visits.Visit_Info_ID = vaccStatus.Visit_Info_ID
left join `seronetdb-Vaccine_Response`.Covid_History as covidHis ON
	hiv_visits.Visit_Info_ID = covidHis.Visit_Info_ID
left join `seronetdb-Vaccine_Response`.Treatment_History as tHistory ON
	hiv_visits.Visit_Info_ID=tHistory.Visit_Info_ID
left join `seronetdb-Vaccine_Response`.Accrual_Participant_Info as demo ON
	ptVisit.Research_Participant_ID=demo.Research_Participant_ID
left join `seronetdb-Vaccine_Response`.HIV_Cohort as hiv ON
	hiv_visits.Visit_Info_ID=hiv.Visit_Info_ID
left join `seronetdb-Vaccine_Response`.Comorbidities_Names as CNames ON
	hiv_visits.Visit_Info_ID = CNames.Visit_Info_ID

)

select * from subject_level
	inner join
    (
		Select max(Visit_Number) as LatestDate, Research_Participant_ID
        from subject_level
        group by Research_Participant_ID
    ) SubMax
    on subject_level.Visit_Number = SubMax.LatestDate
    and subject_level.Research_Participant_ID = SubMax.Research_Participant_ID
    
	group by subject_level.Research_Participant_ID



