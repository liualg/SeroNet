# seronetdb-Vaccine_response
with vaccr as (select 
	ptVisit.Research_Participant_ID, ptVisit.Primary_Study_Cohort, ptVisit.CBC, count(Distinct ptVisit.Visit_Info_ID) as number_of_visits,
    cChort.Cancer, normNames.`Harmonized Cancer Name`,GROUP_CONCAT(vaccStatus.Vaccination_Status SEPARATOR ', ') as raw_status,
Max(
CASE 
	When vaccStatus.Vaccination_Status not in ('No vaccination event reported', 'Unvaccinated') then True
    Else False
END) as Vaccinated,

# Obtaining Treatment - 0 if false, otherwise will provide the treatment type
GROUP_CONCAT(Distinct(
CASE
	When cChort.In_Remission in ('Yes') then 'In_Remission'
    When cChort.In_Unspecified_Therapy in ('Yes') then 'In_Unspecified_Therapy'
    When cChort.Chemotherapy in ('Yes') then 'Chemotherapy'
    When cChort.`Radiation Therapy` in ('yes') then 'Radiation Therapy'
    When cChort.Surgery in ('Yes') then 'Surgery'
    Else 'No' 

END) SEPARATOR ' ,') as treatment_type,

MAX(
CASE
	When covidHis.Breakthrough_COVID in ('Yes') then True
    Else False
END) as COVID_Breakthrough

from `seronetdb-Vaccine_Response`.Cancer_Cohort as cChort
left join `seronetdb-Vaccine_Response`.Participant_Visit_Date_Normalized_Duration_View as ptVisit ON 
	cChort.Visit_Info_ID = ptVisit.Visit_Info_ID
left join `seronetdb-Vaccine_Response`.Covid_Vaccination_Status as vaccStatus ON
	cChort.Visit_Info_ID=vaccStatus.Visit_Info_ID
left join `seronetdb-Vaccine_Response`.Covid_History as covidHis ON
	cChort.Visit_Info_ID = covidHis.Visit_Info_ID
left join `seronetdb-Vaccine_Response`.Normalized_Cancer_Names_v2 as normNames ON
	cChort.Visit_Info_ID = normNames.Visit_Info_ID

group by Research_Participant_ID)

select vaccr.cbc as CBC, count(vaccr.Research_Participant_ID) as participants, 
	sum(vaccr.number_of_visits) as number_of_visits,
	GROUP_CONCAT(DISTINCT vaccr.`Harmonized Cancer Name` separator ', ') as cancer_types,
	GROUP_CONCAT(DISTINCT replace(vaccr.treatment_type,' ','')separator ', ') as treatment, 
    sum(vaccr.vaccinated) as total_participants_vaccinated
from vaccr
group by vaccr.CBC
