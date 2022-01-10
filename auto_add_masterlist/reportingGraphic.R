install.packages("ggplot2")
install.packages('reshape2')
library('ggplot2')
library('dplyr')
library('reshape2')

setwd("/Users/liualg/Documents/GitHub/SeroNet/auto_add_masterlist/Jira")
df <- read.csv("./reporting_test.csv")


df_subset = subset(df, select=-c(Percent.done))
df_subset['A'] = c(range(1:length(PMID, df_subset)))
df_subset['Vivie'] = c(1:106)
rownames(df_subset) <- df_subset$PMID


df_subset

melted_data <- melt(df)
melted_data

#[PMID, DATE, STATUS]

ggplot(melted_data, aes(fill=condition, y=value, x=specie)) + 
  geom_bar(position="stack", stat="identity")

specie <- c(rep("sorgho" , 3) , rep("poacee" , 3) , rep("banana" , 3) , rep("triticum" , 3) )
condition <- rep(c("normal" , "stress" , "Nitrogen") , 4)
value <- abs(rnorm(12 , 0 , 15))
data <- data.frame(specie,condition,value)
data
