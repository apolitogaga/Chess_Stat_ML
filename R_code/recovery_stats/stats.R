library(data.table)
FOLDER = "recovery_stats/"
FILE = paste(FOLDER,"competitors_stats2.csv",sep="")

competitors = fread(FILE)
colnames(competitors) =  c("name","avg_elo","number_elo_entries")
summary(competitors$number_elo_entries)
elos =  competitors$number_elo_entries
summary(elos)
avgs = competitors$avg_elo

avgs[avgs=="None"] = 0
avgs = as.numeric(avgs)
hist(avgs)
summary(avgs)

table(elos==0)
#FALSE   TRUE 
#100383  91543 
elos =  order(elos, decreasing=T)
elos.factor = as.factor(elos)
plot(elos.factor)
summary(elos.factor)
hist(elos[elos>2])
table(elos==0)
summary(avgs)

table(elos)

View(elos)

hist(as.factor(elos))
summary(elos)

head(elos)
summary(competitors$number_elo_entries)
