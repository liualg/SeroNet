library(dplyr)
library(outbreakinfo)
authenticateUser()
# "Arizona", "Minnesota", "New York", "Iowa", "Michigan","North Dakota", "New Jersey", "Oklahoma", "pennsylvania", "Rhode Island", "Wisconsin", "South Dakota"
states = c("Arizona","Iowa", "Michigan","North Dakota", "New Jersey", "Oklahoma", "pennsylvania", "Rhode Island", "Wisconsin", "South Dakota")
states="New York"
my_function1<-function(Names,VVV) {
  
  name1 <-paste0('\\b',Names,'\\b')
  VVV$Index<-apply(VVV[1:8],1, function(x) sum(grepl(name1,x,ignore.case = T)))
  VVV.sub<-subset(VVV,Index>=1)
  
  a = VVV.sub$variantType[1]
  b = VVV.sub$label[1]
  c = VVV.sub$pangolin_lineage[1]
  return(c(a, b, c))
  
}

function2<-function(outer) {
  #  print(length(outer))
  if (length(outer) == 0) {
    outa = NA
  }
  else if (outer %in% c(NULL, NA, 'Other', 'other'," ","")) {
    outa = NA
  }
  else{
    outa = outer
  }
  return(outa)
}

#################################

for (state in states){
  print(state)

  df = getAllLineagesByLocation(location = state,other_threshold=0.00001, nday_threshold=5, ndays = 1300, cumulative = F)
  colnames(df)
  
  
  curated = getCuratedLineages()
  
  
  colnames(curated)
  # Pull out the curated lineages which are WHO-desginated
  variant_status = c('Variant of Interest', 'Variant under Monitoring', 'Previously Circulating Variant of Concern')
  VOC = filter(curated, variantType %in% variant_status)
  
  VOC = VOC %>% select(variantType,who_name,short_name,pangolin_lineage,pango_descendants, pango_sublineages,
                     label, searchTerms)
  
  # I want variantType and WHO name 
  #my_function1("jn.1")[[3]]
  
  
  isVariant=list()
  isWHO=list()
  isPangolin=list()
  
  pb = txtProgressBar(min = 0, max = length(df$lineage), initial = 0) 
  icount=0
  for (i in df$lineage){
    setTxtProgressBar(pb,icount)
    if (length(i) == 0) {
      outputa = NA
      outputb = NA
      outputc = NA
      
      isVariant = append(isVariant,outputa)
      isWHO = append(isWHO,outputb)
      isPangolin = append(isPangolin,outputc)
    }
    else if (!( i %in% c(NULL, NA, 'Other', 'other'," ","")))
    {
      output <- my_function1(i, VOC)
  #    print(paste(i, "-",output[[3]]))
      
      outputa = function2(trimws(output[[1]]))
      outputb = function2(trimws(output[[2]]))
      outputc = function2(trimws(output[[3]]))
      
      
      
      isVariant = append(isVariant,outputa)
      isWHO = append(isWHO,outputb)
      isPangolin = append(isPangolin,outputc)
    }
    else {
      isVariant = append(isVariant, NA)
      isWHO = append(isWHO, NA)
      isPangolin = append(isPangolin, NA)
    }
    icount = icount+1
    close(pb)
    
  }
  
  temp <- df
  temp$VOC <- as.character(isVariant)
  temp$WHO <- as.character(isWHO)
  temp$Pangolin <- as.character(isPangolin)
  temp
  #temp <- apply(temp,2,as.character)
  write.csv(temp, paste("./",state,"_DATA.csv", sep = ''))
}

