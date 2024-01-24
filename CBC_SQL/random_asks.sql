# Looking for the convalescent reported health condition
with 
con as (
	Select * from `seronetdb-Vaccine_Response`.Participant_Visit_Info
	where Primary_Study_Cohort like '%conva%' or Primary_Study_Cohort like '%Chronic%'
),


subby as (
	select 
		con.Visit_Info_ID, 
        Research_Participant_ID, 
        CBC_Classification, Type_Of_Visit, Visit_Number,
        Primary_Study_Cohort, 
        Diabetes, Hypertension, Obesity, Cardiovascular_Disease, Chronic_Lung_Disease,
        Chronic_Kidney_Disease, Chronic_Liver_Disease, Acute_Liver_Disease,
        Immunosuppressive_Condition, Autoimmune_Disorder, Chronic_Neurological_Condition,
        Chronic_Oxygen_Requirement, Inflammatory_Disease, Viral_Infection,
        Bacterial_Infection, Cancer, Substance_Abuse_Disorder_Description_Or_ICD10_codes,
        Organ_Transplant_Description_Or_ICD10_codes,
        Other_Health_Condition_Description_Or_ICD10_codes, 
        Health_Condition_Or_Disease
		
	from con
    
left join `seronetdb-Vaccine_Response`.Participant_Other_Condition_Names as PCN
	ON PCN.Visit_Info_ID = con.Visit_Info_ID
left join `seronetdb-Vaccine_Response`.Treatment_History as TH
	ON TH.Visit_Info_ID = con.Visit_Info_ID
left join `seronetdb-Vaccine_Response`.Participant_Comorbidities as PC
	ON PC.Visit_Info_ID = con.Visit_Info_ID
),

chronic_condition_qq as (
	select Research_Participant_ID, 
		concat_ws(', ', 
		CASE WHEN Diabetes like '%yes%' then 'Diabetes' END,
		CASE WHEN Hypertension in ('yes') then 'Hypertension' END,
		CASE WHEN Obesity like '%overweight%' or Obesity like '%obesity%' then 'Obesity'END,
		CASE WHEN Cardiovascular_Disease in ('yes') then 'Cardiovascular_Disease'  END,
		CASE WHEN Chronic_Lung_Disease in ('yes') then 'Chronic_Lung_Disease' END,
		CASE WHEN Chronic_Kidney_Disease in ('yes') then 'Chronic_Kidney_Disease'  END,
		CASE WHEN Chronic_Liver_Disease in ('yes') then 'Chronic_Liver_Disease' END,
		CASE WHEN Acute_Liver_Disease in ('yes') then 'Acute_Liver_Disease'  END,
		CASE WHEN Immunosuppressive_Condition in ('yes') then 'Immunosuppressive_Condition' END,
		CASE WHEN Autoimmune_Disorder in ('yes') then 'Autoimmune_Disorder'  END,
		CASE WHEN Chronic_Neurological_Condition in ('yes') then 'Chronic_Neurological_Condition' END,
		CASE WHEN Chronic_Oxygen_Requirement in ('yes') then 'Chronic_Oxygen_Requirement'  END,
		CASE WHEN Inflammatory_Disease in ('yes') then 'Inflammatory_Disease' END,
		CASE WHEN Viral_Infection like '%yes%' or Viral_Infection like '%new%' then 'Viral_Infection'  END,
		CASE WHEN Bacterial_Infection like '%yes%' or Bacterial_Infection like '%new%' then 'Bacterial_Infection' END,
		CASE WHEN Cancer in ('yes') then 'Cancer' END,
		CASE WHEN Substance_Abuse_Disorder_Description_Or_ICD10_codes in ('yes') then 'Substance_Abuse_Disorder_Description_Or_ICD10_codes'  END,
		CASE WHEN Organ_Transplant_Description_Or_ICD10_codes like '%yes%' or Organ_Transplant_Description_Or_ICD10_codes like '%bone%' then 'Organ_Transplant_Description_Or_ICD10_codes' END,
		CASE WHEN 
			Other_Health_Condition_Description_Or_ICD10_codes like '%Episodic%' or 
            Other_Health_Condition_Description_Or_ICD10_codes like '%APDS%' or
            Other_Health_Condition_Description_Or_ICD10_codes like '%Chronic%' or
            Other_Health_Condition_Description_Or_ICD10_codes like '%Gene%' then 'Other_Health_Condition_Description_Or_ICD10_codes' END,
		CASE WHEN Health_Condition_Or_Disease like '%HIV%' then 'Health_Condition_Or_Disease' END
		) as chronic_condition
    
    from subby
    group by Research_Participant_ID
)

Select 
	ccqq.Research_Participant_ID, subby.CBC_Classification, subby.Type_Of_Visit, subby.Primary_Study_Cohort, ccqq.chronic_condition


from chronic_condition_qq as ccqq
left join subby 
	ON subby.Research_Participant_ID = ccqq.Research_Participant_ID;
	
    
--     Research_Participant_ID, CBC_Classification, Type_Of_Visit,
--     max(Visit_Number), Primary_Study_Cohort,

--     
-- 	from subby
-- group by Research_Participant_ID
;



# ----------
with hiv_visits as (
	Select Visit_Info_ID from `seronetdb-Vaccine_Response`.HIV_Cohort as HC
		Union
		Select Visit_Info_ID from `seronetdb-Vaccine_Response`.Comorbidities_Names as CN
			where Autoimmune_Disorder_Description_Or_ICD10_codes in ('HIV')
)

select 

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

count(distinct ptVisit.Research_Participant_ID)

from hiv_visits 
left join `seronetdb-Vaccine_Response`.Participant_Visit_Info as ptVisit 
	ON hiv_visits.Visit_Info_ID = ptVisit.Visit_Info_ID
    
    
group by CBC;