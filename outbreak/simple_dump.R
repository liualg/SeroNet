library(dplyr)
library(Dict)
library(outbreakinfo)
authenticateUser()

#states=c("New York","Arizona", "Minnesota") #THESE STATES, 
states=c("Connecticut","Iowa","Minnesota","Michigan","North Dakota", "New Jersey", "Oklahoma", "Pennsylvania", "Rhode Island", "Wisconsin","New York","Arizona","South Dakota")
#states=c("Minnesota","Michigan","North Dakota", "New Jersey", "Oklahoma", "Pennsylvania", "Rhode Island", "Wisconsin","New York","Arizona","South Dakota")

RAW_DIR='/Users/liualg/Documents/GitHub/SeroNet/outbreak/_raw/'
PANGO_DIR='/Users/liualg/Documents/GitHub/SeroNet/outbreak/_output/'

states=c("Connecticut")
length(states)

sh1=c()
#Pulling lineages for each of the states above. 
for (state in states){
  print(state)
  df = getAllLineagesByLocation(location = state, other_threshold=.00001, nday_threshold=1, ndays = 1500, cumulative = F)
  write.csv(df, paste(RAW_DIR,state,"_raw-03.csv", sep = ''))
}





#other_threshold=0.00001, nday_threshold=50, ndays = 1500: 20017
#other_threshold=0.00001, nday_threshold=50, ndays = 300: 2729
#other_threshold=0.00001, nday_threshold=50, ndays = 1: 1432

#other_threshold=0.00001, nday_threshold=5, ndays = 1500: 55546
#other_threshold=0.00001, nday_threshold=180, ndays = 1500: 3663
#other_threshold=0.00001, nday_threshold=500, ndays = 1500: 1432


#other_threshold=0.1, nday_threshold=1, ndays = 1500: 37397
#other_threshold=0.001, nday_threshold=1, ndays = 1500: 63920
#other_threshold=0.00001, nday_threshold=1, ndays = 1500: 63920
