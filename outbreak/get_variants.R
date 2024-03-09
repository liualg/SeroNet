library(dplyr)
library(Dict)
library(outbreakinfo)
# library(setTxtProgressBar)
authenticateUser()

states=c("Connecticut","Iowa","Minnesota","Michigan","North Dakota", "New Jersey", "Oklahoma", "Pennsylvania", "Rhode Island", "Wisconsin","New York","Arizona","South Dakota")

RAW_DIR='/Users/liualg/Documents/GitHub/SeroNet/outbreak/_raw/'
PANGO_DIR='/Users/liualg/Documents/GitHub/SeroNet/outbreak/_output/'

length(states)

lineage_dat_dic = getCuratedLineages()

`%like%` <- function (x, pattern) { 
  pattern_fix <-paste0('\\b',pattern,'\\b')
  grepl(pattern_fix, x, ignore.case=TRUE)
}

dd <- list()



## Adding WHO names to each of the variants see in pull above. 
for (state in states){
  print(paste("##############",state,"##############"))
  # pb = txtProgressBar(min = 0, max = length(df$lineage), initial = 0) 
  # icount=0
  temp = read.csv(paste(RAW_DIR,state,"_raw-01.csv", sep = ''))
  aa<-c()
  for (i in trimws(temp$lineage)){
  	# setTxtProgressBar(pb,icount)
    i = tolower(i)
    for (n in seq_len(nrow(lineage_dat_dic))){
      if (i %in% tolower(lineage_dat_dic$reportQuery$pango[[n]])){
        term=lineage_dat_dic$label[n]
        dd[i] <- term
        aa = append(aa,term)
        # print(paste(i,term, sep=' - '))
      }
      else{
        aa = append(aa,NA)
      }
    }
    
    # icount = icount+1
    # close(pb)

  }
  
temp$term <- aa
write.csv(temp, paste(PANGO_DIR,state,"_data-pangoterms.csv", sep = ''))

}


