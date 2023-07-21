SELECT
	PVI.Research_Participant_ID, PVI.Visit_Info_ID, CH.COVID_Status, PVI.Primary_Study_Cohort, 
    PVI.Visit_Number, PVI.Submission_Index, NVI.Duration_From_Visit_1,
    CV.`SARS-CoV-2_Vaccine_Type`, CV.Vaccination_Status, NVI.Duration_Between_Vaccine_and_Visit,
    CH.Long_COVID_symptoms, CH.Other_Long_COVID_symptoms

FROM `seronetdb-Vaccine_Response`.Covid_History as CH
	Left join `seronetdb-Vaccine_Response`.Participant_Visit_Info as PVI On CH.Visit_Info_ID=PVI.Visit_Info_ID
	left join `seronetdb-Vaccine_Response`.Normalized_Visit_Vaccination as NVI On PVI.Visit_Info_ID=NVI.Visit_Info_ID
	left join `seronetdb-Vaccine_Response`.Covid_Vaccination_Status as CV on CH.Visit_Info_ID=CV.Visit_Info_ID
where (
	CH.Long_COVID_symptoms not like "no symp%" or
	(
		CH.Other_Long_COVID_symptoms is not null and  
		CH.Other_Long_COVID_symptoms not like ("NA") 
    )
)

;