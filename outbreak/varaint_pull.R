library(dplyr)
library(outbreakinfo)
authenticateUser()
# "Arizona", "Minnesota", "New York", "Iowa", "Michigan","North Dakota", "New Jersey", "Oklahoma", "pennsylvania", "Rhode Island", "Wisconsin", "South Dakota"
states = c("Arizona","Iowa", "Michigan","North Dakota", "New Jersey", "Oklahoma", "pennsylvania", "Rhode Island", "Wisconsin", "South Dakota")
states="New York"


#################################

for (state in states){
  print(state)

  df = getAllLineagesByLocation(location = state,other_threshold=0.01, nday_threshold=5, ndays = 100, cumulative = F)
  
  write.csv(df, paste("./",state,"_DATA.csv", sep = ''))
}

