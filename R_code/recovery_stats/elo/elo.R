# try to analise the elo's
library(data.table)
library(ggplot2)
library(RColorBrewer)

setwd("/Volumes/DOCS/DOCS/OneDrive/DEV/TestSis/data/stats/elo")
lib = fread("ELOS.csv")
colnames(lib)  =  c("White", "Black", "white_elo", "black_elo","white_avg_elo", "black_avg_elo", "Result","len_fen")
max(lib$len_fen) # 457
lib2= lib[1:100000]
summary(lib)
plot(lib2$white_elo~lib2$black_elo, col=lib2$Result+3)
legend(7,4.3,unique(lib2$Result),col=1:length(lib2$Result),pch=1)
lin = lm(lib2$white_elo~lib2$black_elo)
plot(lin)

data.lib = as.data.frame(lib)
head(data.lib[5:6])
elos = data.lib[5:6]
welo =  elos$white_avg_elo



## order the grid, by whites.
n <-100 

qual_col_pals = brewer.pal.info[brewer.pal.info$category == 'qual',]
col_vector = unlist(mapply(brewer.pal, qual_col_pals$maxcolors, rownames(qual_col_pals)))
pie(rep(1,n), col=sample(col_vector, n))
##
N=10
elos = split(elos$white_avg_elo, sample(1:N, nrow(elos$white_avg_elo), replace=T))

n = 10
chunk <- cut_number(welo,10, label=F)-1
table(chunk)
test = elos
test[3]=0
table(test[3])
test[3] = chunk*10
table(test[3])
result = as.data.frame(matrix(ncol=3))
names(result) = names(test)
result = result[-1,]
result
i=0
for(i in 0:9){
    new_test = test[test[3]==i*10,]
    new_chunk <- cut_number(new_test$black_avg_elo,10,labels=F)
    new_test[3] = new_chunk+(i*10)
    result <- rbind(result,new_test)
}
(table(result[3]))
i=1
for(i in 1:100){
    grid = result[result[3]==i,]
    print(paste(i," ",nrow(grid)," >  ",min(grid$white_avg_elo),max(grid$white_avg_elo),",",min(grid$black_avg_elo),max(grid$black_avg_elo)))
}


sub_result = result[sample(nrow(result),1000), ]
head(sub_result)
table(sub_result$V3)
plot(sub_result$white_avg_elo,sub_result$black_avg_elo,col = floor(sub_result$V3/10))



?subset
min(var)
max(var)

# 1      2      3      4      5      6      7      8      9     10 
# 205503 203946 204215 207548 200144 206152 208122 201741 202703 202507 
# [1] "100 2043"
# [1] "2044 2160"
# [1] "2161 2235"
# [1] "2236 2293"
# [1] "2294 2347"
# [1] "2348 2397"
# [1] "2398 2448"
# [1] "2449 2498"
# [1] "2499 2558"
# [1] "2559 2875"

length(welo.split[[i]])



#####

plot(data$Sepal.Length, data$Sepal.Width, col=data$Species)
legend(7,4.3,unique(data$Species),col=1:length(data$Species),pch=1)


plot(density(lib[lib$Result==-1]$white_elo-lib[lib$Result==-1]$black_elo),
     ylim=c(0,.003),xlim=c(-1000,1000))
lines(density(lib[lib$Result==1]$white_elo-lib[lib$Result==1]$black_elo),col=4)
lines(density(lib[lib$Result==0]$white_elo-lib[lib$Result==0]$black_elo),col=2)

hist(lib$len_fen,br=500)


head(lib)

hist(round(.5*(lib$len_fen+1),0),br=500)
head(sort(table(lib$White),decreasing=TRUE),40)
head(sort(table(lib$White),decreasing=TRUE),200)
plot(sort(table(lib$White),decreasing=TRUE),type="b")
plot(sort(table(lib$White),decreasing=TRUE),type="h")
plot(log(sort(table(lib$White),decreasing=TRUE)),type="h")
plot(log(sort(table(lib$White),decreasing=TRUE)))
plot(log(sort(table(lib$Black),decreasing=TRUE)))
