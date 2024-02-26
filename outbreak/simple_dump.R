library(dplyr)
library(Dict)
library(outbreakinfo)
authenticateUser()

states=c("New York","Arizona", "Minnesota") #THESE STATES, 
states=c("Connecticut","Iowa","Minnesota","Michigan","North Dakota", "New Jersey", "Oklahoma", "Pennsylvania", "Rhode Island", "Wisconsin","New York","Arizona","South Dakota")
states=c("Minnesota","Michigan","North Dakota", "New Jersey", "Oklahoma", "Pennsylvania", "Rhode Island", "Wisconsin","New York","Arizona","South Dakota")

length(states)
#Pulling lineages for each of the states above. 
for (state in states){
  print(state)
  
  df = getAllLineagesByLocation(location = state, other_threshold=0.00001, nday_threshold=50, ndays = 1300, cumulative = F)
  write.csv(df, paste("./",state,"_raw-01.csv", sep = ''))
}

lineage_dat_dic = getCuratedLineages()

`%like%` <- function (x, pattern) { 
  pattern_fix <-paste0('\\b',pattern,'\\b')
  grepl(pattern_fix, x, ignore.case=TRUE)
}

dd <- list()

## Adding WHO names to each of the variants see in pull above. 
for (state in states){
  print(paste("##############",state,"##############"))
  temp = read.csv(paste("./",state,"_raw-01.csv", sep = ''))
  aa<-c()
  for (i in trimws(temp$lineage)){
    i = tolower(i)
    for (n in seq_len(nrow(lineage_dat_dic))){
      if (i %in% tolower(lineage_dat_dic$reportQuery$pango[[n]])){
        term=lineage_dat_dic$label[n]
        dd[i] <- term
        aa = append(aa,term)
        print(paste(i,term, sep=' - '))
      }
      else{
        aa = append(aa,NA)
      }
    }
    
  }
  
temp$term <- aa
write.csv(temp, paste("./",state,"_data-pangoterms.csv", sep = ''))

}


## FASTER. 
for (state in states){
  print(paste("##############",state,"##############"))
  temp = read.csv(paste("./",state,"_raw-01.csv", sep = ''))
  aa<-c()
  for (i in trimws(temp$lineage)){
    i = tolower(i)
    
    if (is.null(dd[i])) {
      for (n in seq_len(nrow(lineage_dat_dic))){
        if (i %in% tolower(lineage_dat_dic$reportQuery$pango[[n]])){
          term=lineage_dat_dic$label[n]
          dd[i] <- term
          aa = append(aa,term)
          print(paste(i,term, sep=' - '))
        }
        else{
          dd[i] <- NA
          aa = append(aa,NA)
        }
      }
    }
    else {
      aa = append(aa,dd[[i]])
    }
    
    
  }
  
  temp$term <- aa
  write.csv(temp, paste("./",state,"_data-pangoterms.csv", sep = ''))
  
}
