
library(gdata)
library(kernlab)
library(randomForest)
source("functions.R")


file_train = "/Volumes/DOCS/thesData/final_csv_train/train_0.csv"
file_test = "/Volumes/DOCS/thesData/final_csv_test/test_0.csv"
dat = fread(file_test)
?randomForest
names(train)

var = get_file_pairs(99)
n=99

# res = predict_svm(, FALSE)

train = var$train[n]

var=get_list_files(2)
var

(r = predict_svm(get_file_pairs(i),TRUE))
r = sapply(fin, predict_svm)



test = load_file(file_test)
train = load_file(file_train)
testt = get_data(test, TRUE)
trainn = get_data(train, TRUE)
tr = data.frame(trainn$x, trainn$y)

mod = randomForest(trainn.y~., data=tr, ntree=1000, proximity=TRUE)

save(mod, file="mod.rdata")
pred.rf <- predict (mod, testt$x, type="class")

(ct <- table(Truth=testt$y, Pred=pred.rf))



process_all_files <-function(){
    file_paths = get_list_files()
    r =  lapply(file_paths, predict_svm, TRUE)
    r2 =  lapply(file_paths, predict_svm, FALSE)
}

predict_svm <- function(var, del_draw=FALSE)
{
    test = load_file(var$test)
    train = load_file(var$train)
    test.list = get_data(test, del_draw)
    train.list = get_data(train, del_draw)
    
    head(train.list$x)
    head(train.list$y)
    
    ker =  rbfdot(sigma = .1)
    svp <- ksvm(train.list$x,train.list$y,kernel=ker,C=10, cross=3)
    
    pred = predict(svp, test.list$x)
    n <- length(test.list$y)
    (err2 <- table(pred,test.list$y))
    (err <- (n-sum(diag(err2)))/n)
    return(list("err" = err,"table" = err2))
}
