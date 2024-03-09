library(dplyr)
library(Dict)
library(outbreakinfo)
# authenticateUser()
# states=c("Oklahoma","New York")
states=c("Connecticut")

#states=c("Oklahoma","New York", "Connecticut","Iowa","Minnesota","Michigan","North Dakota", "New Jersey", "Pennsylvania", "Rhode Island", "Wisconsin","Arizona","South Dakota")

RAW_DIR='/Users/liualg/Documents/GitHub/SeroNet/outbreak/_raw/'
PANGO_DIR='/Users/liualg/Documents/GitHub/SeroNet/outbreak/_output-fast/'

length(states)

lineage_dat_dic = getCuratedLineages()
# print(length(lineage_dat_dic))
  #matrix(unlist(lineage_dat_dic),ncol = length(lineage_dat_dic)[0], byrow = TRUE  ))
# write.csv(lineage_dat_dic,'/Users/liualg/Documents/GitHub/SeroNet/outbreak/data_dic.csv')

`%like%` <- function (x, pattern) { 
  pattern_fix <-paste0('\\b',pattern,'\\b')
  grepl(pattern_fix, x, ignore.case=TRUE)
}

#Create readable dict
dd <- list()

for (i in c(1:length(lineage_dat_dic$reportQuery$pango))){
  for (n in lineage_dat_dic$reportQuery$pango[[i]]){
    dd[tolower(n)] <- lineage_dat_dic$label[[i]]
  }
}

write.csv(t(as.data.frame(dd)), '/Users/liualg/Documents/GitHub/SeroNet/outbreak/key.csv')

# Adding WHO names to each of the variants see in pull above. 
for (state in states){
  print(paste("##############",state,"##############"))
  
  stepi = 0
  temp = read.csv(paste(RAW_DIR,state,"_raw-03.csv", sep = ''))
  pb = txtProgressBar(min = 0, max = length(temp$lineage), initial = 0) 
  aa<-c()

  for (variant in trimws(temp$lineage)){
    setTxtProgressBar(pb,stepi)
    variant = tolower(variant)

    if (is.null(dd[[variant]])){
      aa = append(aa, NA)
    }
    else{
      aa = append(aa, dd[[variant]])
    }
  stepi = stepi + 1
  

  }
  close(pb)
  
temp$term <- aa
write.csv(temp[,-1], paste(PANGO_DIR,state,"_data-pangoterms.csv", sep = ''), row.names = FALSE)

}


