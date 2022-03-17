import os 
# Looping through each section in the Registy template
for section_number in range(len(sp)-1):
    temp_wb = Workbook()
    temp_ws = temp_wb.active

    #making a temp workbook to store each section. This will be turned into df
    for i in registry.iter_rows(values_only = True,
                                min_row = sp[section_number]+1,
                                max_row = sp[section_number+1]-1):
        temp_ws.append(i)
        
    max_row = temp_ws.max_row
    max_col = temp_ws.max_column
    seroFxn.remove_excess(temp_ws)
#     print("Rows:", max_row, "->", temp_ws.max_row)
#     print("Columns:", max_col, "->", temp_ws.max_column)
    
    df = pd.DataFrame(temp_ws.values)
    sub_section = registry.cell(row=sp[section_number], column = 1).value
#     print(sub_section)

    if sub_section == 'study':
        df = seroFxn.edit_df(df)
        
        STUDY = seroClass.study(
            df['Study Identifier'][1],
            df['Study Name'][1],
            df['Publication Title'][1],
            df['Study Objective'][1],
            df['Study Description'][1],
            df['Primary Institution Name'][1]
            )
    
    elif sub_section == 'study_pubmed':
        df = seroFxn.edit_df(df)
        
        STUDY_PERSONNEL = seroClass.study_pubmed(
            df['Pubmed ID'],
            df['Keyword']
        )
        
    elif sub_section == 'study_personnel':
        df = seroFxn.edit_df(df)

        STUDY_PERSONNEL = seroClass.study_personnel(
            df['Personnel ID'],
            df['Honorific'],
            df['Last Name'],
            df['First Name'],
            df['Suffixes'],
            df['Organization'],
            df['ORCID ID'],
            df['Email'],
            df['Title In Study'],
            df['Role In Study'],
            df['Site Name']
        )


    elif sub_section == 'study_file':
        df = seroFxn.edit_df(df)

        STUDY_FILE = seroClass.study_file(
            df['Study File Name'],
            df['Study File Description'],
            df['Study File Type']  
        )
        
    
    elif sub_section == 'study_link':
        df = seroFxn.edit_df(df)

        STUDY_LINK = seroClass.study_link(
            df['Link Name'],
            df['Value']
        )
             
        
    elif sub_section == 'study_categorization':
        df = seroFxn.edit_df(df)

        STUDY_CATEGORIZATION = seroClass.study_categorization(
            df['Research Focus *'][1],
            df['Study Type'][1],
            df['Keywords'][1],
        )
    
    elif sub_section == 'study_design':
        df = seroFxn.edit_df(df)

        if (df.shape != (2,0)): # checking size. There has to be a better way to do this

            STUDY_DESIGN = seroClass.study_design(
                df['Clinical Study Design'],
                df['in silico Model Type']
            )
        else:
            study_des = study_design()

    elif sub_section == 'protocol':
        df = seroFxn.edit_df(df)

        PROTOCOLS = seroClass.protocols(
            df['Protocol ID'],
            df['Protocol File Name'],
            df['Protocol Name'],
            df['Protocol Description'],
            df['Protocol Type'],
        )
        
    elif sub_section == 'condition_or_disease':
        df = seroFxn.edit_df(df)

        COD = seroClass.condition_or_disease(
            df['Reported Health Condition* ']
        )
        
    elif sub_section == 'Intervention Agent':
        df = seroFxn.edit_df(df)

        INTERVENTION_AGENT = seroClass.Intervention_Agent(
            df['SARS-CoV-2 Vaccine Type *'][1]
        )

    elif sub_section == 'study_details':
        df = seroFxn.edit_df(df)

        STUDY_DETAILS = seroClass.study_details(
            df['Clinical Outcome Measure'],
            df['Enrollment Start Date'],
            df['Enrollment End Date'],
            df['Number of Study Subjects'],
            df['Age Unit'],
            df['Minimum Age'],
            df['Maximum Age']
            )

    elif sub_section == 'arm_cohort':
        df = seroFxn.edit_df(df)

        AOC = seroClass.arm_or_cohort(
            df['Arm ID'],
            df['Arm Name'],
            df['Study Population Description'],
            df['Arm Type']
        )


    elif sub_section == 'inclusion_exclusion':
        df = seroFxn.edit_df(df)

        INCLUSION_EXCLUSION = seroClass.inclusion_exclusion(
            df['Inclusion ID'],
            df['Inclusion Criterion'],
            df['Inclusion Criterion Category']  
        )

    elif sub_section == 'subject':
        df = seroFxn.edit_df(df)

        STUDY_DETAILS = seroClass.subject(
            df['Subject ID'][1],
            df['Sex at Birth*'][1],
            df['Age Event'][1],
            df['Subject Phenotype'][1],
            df['Study Location'][1]
            )
        
    elif sub_section == 'Subject Type: human':
        df = seroFxn.edit_df(df)

        STUDY_DETAILS = seroClass.subject_type_human(
            df['Ethnicity'],
            df['Race'],
            df['Race Specify'],
            df['Description']
            )

    elif sub_section == 'Subject Type: model organism':
        df = seroFxn.edit_df(df)

        STUDY_DETAILS = seroClass.subject_type_mode_organism(
            df['Species'],
            df['Biosample Types'],
            df['Strain Characteristics']
            )
        
    elif sub_section == 'immuneExposure':
        df = seroFxn.edit_df(df)

        STUDY_DETAILS = seroClass.immuneExposure(
            df['SARS-CoV2 History'][1],
            df['SARS-CoV-2 Vaccine Type'][1],
            df['COVID-19 Disease Severity'][1]
            )
    
    elif sub_section == 'planned_visit':
        df = seroFxn.edit_df(df)

        PLANNED_VISIT = seroClass.planned_visit(
            df['Visit ID'],
            df['Visit Name'],
            df['Visit Order Number'],
            df['Visit Min Start Day'],
            df['Visit Max Start Day'],
            df['Visit Start Rule']                                
    )
    
    elif sub_section == 'Assessment':
        df = seroFxn.edit_df(df)

        PLANNED_VISIT = seroClass.assessment(
            df['Assessment ID'],
            df['Assessment Name'],
            df['Measured Behavioral or Psychological Factor'],
            df['Measured Social Factor'],
            df['SARS-CoV-2 Symptoms'],
            df['Assessment_Clinical  and Demographic Data Provenance'],
            df['Assessment_Demographic Data Types Collected']                                
    )
    
    elif sub_section == 'Study Experiment Samples':
        df = seroFxn.edit_df(df)

        PLANNED_VISIT = seroClass.study_experiment_samples(
            df['Expt Sample User Defined ID'],
            df['Expt Sample Biospecimen Type'],
            df['Expt Sample Biospecimen Collection Point']                             
    )
    
    elif sub_section == 'Study Experiments':
        df = seroFxn.edit_df(df)

        PLANNED_VISIT = seroClass.study_experiment(
            df['Experiment ID'],
            df['Experiment Name'],
            df['Experiment Assay Type'],
            df['Experiment Results File Name']
    )
        
    elif sub_section == 'Reagent per Experiment-Assay Type':
        df = seroFxn.edit_df(df)

        PLANNED_VISIT = seroClass.reagent_per_experiment(
            df['Expt Sample User Defined ID'],
            df['Expt Sample Biospecimen Type'],
            df['Expt Sample Biospecimen Collection Point']                             
    )  
        
    elif sub_section == 'Results':
        df = seroFxn.edit_df(df)

        PLANNED_VISIT = seroClass.results(
            df['Results Virus Target'],
            df['Results Antibody Isotype'],
            df['Results Reporting Units'],
            df['Results Reporting Format']
    )  
        
    else:
        print(sub_section, ': does not exist')
