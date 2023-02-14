-- 4)	Co-morbidities. How does a patients co-morbidity Influence their antibody measurements?
-- 5)	Compare within the group of patients with comorbidities and look at what comorbidity is ‘the worst’ to have antibody titer wise. 
-- 6)	Is there a correlation between (low) antibody titer and alcohol/smoking/drug use? 

-- Vaccine_Response
Select * from `seronetdb-Vaccine_Response`.Participant_Visit_Info as PVI
left join `seronetdb-Vaccine_Response`.AutoImmune_Cohort as AIC ON PVI.Visit_Info_ID = AIC.Visit_Info_ID
left join `seronetdb-Vaccine_Response`.Cancer_Cohort as CC ON PVI.Visit_Info_ID = CC.Visit_Info_ID
left join `seronetdb-Vaccine_Response`.Participant_Comorbidities as PC ON PVI.Visit_Info_ID = PC.Visit_Info_ID
left join `seronetdb-Vaccine_Response`.Drugs_And_Alcohol_Use as DAAU ON PVI.Visit_Info_ID = DAAU.Visit_Info_ID
left join `seronetdb-Vaccine_Response`.Participant_Other_Conditions as POC ON PVI.Visit_Info_ID = POC.Visit_Info_ID;
-- group by PVI.Visit_Info_ID;
-- Q5: Comorbidity + antibody + autoimmune
Select * from `seronetdb-Vaccine_Response`.Drugs_And_Alcohol_Use as DAAU
left join `seronetdb-Vaccine_Response`.Assay_Target as ATa ON DAAU.Visit_Info_ID = ATa.Assay_ID
left join `seronetdb-Vaccine_Response`.Assay_Target as ATa ON DAAU.Visit_Info_ID = ATa.Visit_Info_ID;


-- Q6: Drugs + antibody
Select * from `seronetdb-Vaccine_Response`.Participant_Visit_Info as PVI
left join `seronetdb-Vaccine_Response`.Drugs_And_Alcohol_Use as DAAU ON PVI.Visit_Info_ID = DAAU.Visit_Info_ID
left join `seronetdb-Vaccine_Response`.Assay_Target as ATa ON PVI.Visit_Info_ID = ATa.Visit_Info_ID;


-- Validated
Select * from `seronetdb-Validated`.Participant as P
left join `seronetdb-Validated`.Participant_Comorbidity_Reported as PCR ON P.Research_Participant_ID = PCR.Research_Participant_ID
left join `seronetdb-Validated`.Participant_Covid_Symptom_Reported as PCSR ON P.Research_Participant_ID = PCSR.Research_Participant_ID
left join `seronetdb-Validated`.Participant_Prior_Infection_Reported as PRIR ON P.Research_Participant_ID = PRIR.Research_Participant_ID
left join `seronetdb-Validated`.Participant_Prior_SARS_CoV2_PCR as PPSCP ON P.Research_Participant_ID = PPSCP.Research_Participant_ID
left join `seronetdb-Validated`.Participant_Prior_Test_Result as PPTR ON P.Research_Participant_ID = PPTR.Research_Participant_ID
left join `seronetdb-Validated`.Prior_Covid_Outcome as PCO ON P.Research_Participant_ID = PCO.Research_Participant_ID;
-- group by PVI.Visit_Info_ID;

