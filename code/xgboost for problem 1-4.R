library(xgboost)
library(ROCR)
# Data<-subset(task_info,select = -c(task,alt,longt,`16km_renshu`,`7km_renshu`,`8km_renshu`,`15km_renshu`,
#                                    `5km_renshu`,`9km_renshu`,`17km_renshu`,`4km_renshu`,`1km_renshu`, 
#                                    `10km_renshu`,`11km_renshu`,`6km_renshu`,`20km_renshu`,`3km_renshu`,
#                                    `2km_average`,`8km_renshu`,`3km_renshu`,`7km_renshu`,`10km_renshu`,
#                                    `11km_renshu`,`4km_renshu`,`9km_renshu`,`6km_renshu`,`1km_renshu`,
#                                    `5km_renshu`,`17km_renshu`,`20km_renshu`,`12km_renshu`,`12km_average`,
#                                    `3km_average`,`15km_average`,`13km_average`,`1km_average`,`11km_average`,
#                                    `4km_average`,`14km_renshu`,`19km_renshu`,`2km_renshu`))


Data<-subset(task_info,select = c(task,price,`7km_renshu`,`7km_average`,outcomes))

# for (i in 1:835){
#   Data$`7km_renshu`[i]<-log(1+Data$`7km_renshu`[i])
#   Data$`7km_average`[i]<-log(1+Data$`7km_average`[i])
#   Data$price[i]<-(Data$price[i]-65)^5
# }
##5-fold cv for xgboost
index = sample(1:835,835)
cut = c(1,168,335,502,669,835)
accu.xgb<-rep(0,5)
auc.xgb<-rep(0,5)
for(i in 1:5){
  Data.train<-Data[-index[cut[i]:(cut[i+1]-1)],]
  Data.test<-Data[index[cut[i]:(cut[i+1]-1)],]
  
  train_x <- model.matrix(outcomes~price+`7km_renshu`+`7km_average`,Data.train)
  head(train_x[,1])
  xgb <- xgboost(data=data.matrix(train_x[,-1]),
                 label=Data.train$outcomes,
                 eta=0.2,
                 max_depth=20,
                 colsample_bytree=0.8,
                 nrounds=110,
                 seed=1,
                 eval_metrix="error",
                 objective="binary:logistic",
                 nthread=7)
  
  Test <- model.matrix(outcomes~price+`7km_renshu`+`7km_average`,Data.test)
  pred_xgb <- predict(xgb,Test[,-1])
  prediction_xgb <- prediction(pred_xgb,Data.test$outcomes)
  perf_xgb <- performance(prediction_xgb,"tpr","fpr")
  plot(perf_xgb,colorize=T)
  auc_xgb <- performance(prediction_xgb, measure = "auc")
  auc_xgb <- auc_xgb@y.values[[1]]
  auc.xgb[i]=auc_xgb
  ##
  names <- colnames(train_x[,-1])
  importance_matrix <- xgb.importance(names,model=xgb)
  ##
  threshold <- 0.5
  result = vector(length=nrow(Data.test))
  result[pred_xgb < threshold] <- 0
  result[pred_xgb >= threshold] <- 1
  ##
  TP = sum(result==1&Data.test$outcomes==1)
  FN = sum(result==0&Data.test$outcomes==1)
  FP = sum(result==1&Data.test$outcomes==0)
  TN = sum(result==0&Data.test$outcomes==0)
  ##
  P=TP/(TP+FP)
  R=TP/(TP+FN)
  ##
  accu <- (TP+TN)/nrow(Data.test)
  accu.xgb[i] = accu
}
mean(accu.xgb)
mean(auc.xgb)
  
##train model with full set
train_x <- model.matrix(outcomes~price+`7km_renshu`+`7km_average`,Data)
head(train_x[,1])
xgb <- xgboost(data=data.matrix(train_x[,-1]),
               label=Data$outcomes,
               eta=0.2,
               #min_child_weight=0.5,
               max_depth=10,
               colsample_bytree=0.8,
               nrounds=100,
               seed=1,
               eval_metrix="error",
               objective="binary:logistic",
               nthread=7)
Test <- model.matrix(outcomes~price+`7km_renshu`+`7km_average`,Data)
Data$pred_xgb <- predict(xgb,Test[,-1])


###########################solving problem 2
##sort data
Data1<- Data[order(-Data$pred_xgb),]

##adjust price
# lm.sol<-lm(price~log(1+`7km_renshu`)+log(1+`7km_average`),Data)
# lm.sol<-lm(price~.,Data)
# summary(lm.sol)


##decrease price of pred_xgb>0.5
i=1
total=0
while(i<836){
  #record price
  price<-Data1[i,]$price
  ##decline 0.5 price
  while(Data1[i,]$pred_xgb>0.7){
    Data1[i,]$price<-Data1[i,]$price-0.5
    #test the try of adjust price
    Test <- model.matrix(outcomes~price+`7km_renshu`+`7km_average`,Data1)
    pred_xgb <- predict(xgb,Test[,-1])
    if(pred_xgb[i]<0.7|Data1[i,]$price<65|price-Data1[i,]$price>5) {
      Data1$price[i]<-Data1$price[i]+0.5
      total<-total+price-Data1$price[i]
      break
    }
    Data1[i,]$pred_xgb<-pred_xgb[i]
  }
  i<-i+1
}

##add price for pred_xgb<0.5

#first decrease to 65
for (i in 1:835){
  if(Data1[i,]$pred_xgb<0.5){
    total<-total+Data1[i,]$price-65
    Data1[i,]$price<-65
  }
}


#then incease as for the largest pred_xgb's price
i=1
while(i<836){
  ##add 0.5 price each turn
  while(Data1[i,]$pred_xgb<0.5){
    Data1[i,]$price<-Data1[i,]$price+0.5
    #test the try of adjust price
    Test <- model.matrix(outcomes~price+`7km_renshu`+`7km_average`,Data1)
    pred_xgb <- predict(xgb,Test[,-1])
    Data1[i,]$pred_xgb<-min(pred_xgb[i]*1)  
    if(Data1[i,]$pred_xgb>=0.5|Data1[i,]$price>=85) {
      total<-total+65-Data1$price[i]
      break
    }
  }
  if (Data1[i,]$pred_xgb<0.5){
    total<-total+Data1[i,]$price-65
    Data1[i,]$price<-65
    
  }
  if (total<0) {
    total<-total-65+Data1[i,]$price
    Data1[i,]$price<-65
    break
  }
  
  i<-i+1
}

for (i in 1:835){
  if(Data1[i,]$pred_xgb>=0.5){
    Data1[i,]$outcomes<-1
  }
  
}
##export data to csv
write.csv(Data,file="C://Users//24732//Desktop//B//Data.csv",quote=F,row.names = T)
write.csv(Data1,file="C://Users//24732//Desktop//B//Data1.csv",quote=F,row.names = T)

###############################################

##problem 3

library(readr)
problem_3 <- read_csv("C:/Users/24732/Desktop/B/problem 3.csv")
Data<-subset(problem_3,select = c(task,price,`7km_renshu`,`7km_average`,pairs,task_pair_count,outcomes))
Data<-subset(Data,select=-c(pairs))
# ##compute real renshu in area
# for (i in 1:835){
#   Data[i,]$`7km_renshu`<-Data[i,]$`7km_renshu`*Data[i,]$task_pair_count
# }

##use xgboost
Test <- model.matrix(outcomes~price+`7km_renshu`+`7km_average`,Data)
Data$pred_xgb <- predict(xgb,Test[,-1])




##export data to csv
write.csv(Data,file="C://Users//24732//Desktop//B//Data_in_problem_3.csv",quote=F,row.names = T)









#################################################
##problem 4
library(readr)
problem_4 <- read_csv("C:/Users/24732/Desktop/B/problem_4_Phase_I.csv")
Data2<-subset(problem_4,select = c(task,price,`7km_renshu`,`7km_average`,outcomes))

Test <- model.matrix(outcomes~price+`7km_renshu`+`7km_average`,Data2)
Data2$pred_xgb <- predict(xgb,Test[,-1])

for (i in 1:2066){
  if(Data2[i,]$pred_xgb>=0.5){
    Data2[i,]$outcomes<-1
  }
}

write.csv(Data2,file="C://Users//24732//Desktop//B//Data_problem_4_Phase_I.csv",quote=F,row.names = T)


##construct Data1
Data1<- Data2[order(-Data2$pred_xgb),]

##decrease price of pred_xgb>0.5
i=1
total=0
while(i<2067){
  #record price
  price<-Data1[i,]$price
  ##decline 0.5 price
  while(Data1[i,]$pred_xgb>0.7){
    Data1[i,]$price<-Data1[i,]$price-0.5
    #test the try of adjust price
    Test <- model.matrix(outcomes~price+`7km_renshu`+`7km_average`,Data1)
    pred_xgb <- predict(xgb,Test[,-1])
    if(pred_xgb[i]<0.7|Data1[i,]$price<65|price-Data1[i,]$price>5) {
      Data1$price[i]<-Data1$price[i]+0.5
      total<-total+price-Data1$price[i]
      break
    }
    Data1[i,]$pred_xgb<-pred_xgb[i]
  }
  i<-i+1
}

##add price for pred_xgb<0.5

#first decrease to 65
for (i in 1:2066){
  if(Data1[i,]$pred_xgb<0.5){
    total<-total+Data1[i,]$price-65
    Data1[i,]$price<-65
  }
}


#then incease as for the largest pred_xgb's price
i=1
while(i<2067){
  ##add 0.5 price each turn
  while(Data1[i,]$pred_xgb<0.5){
    Data1[i,]$price<-Data1[i,]$price+0.5
    #test the try of adjust price
    Test <- model.matrix(outcomes~price+`7km_renshu`+`7km_average`,Data1)
    pred_xgb <- predict(xgb,Test[,-1])
    Data1[i,]$pred_xgb<-min(pred_xgb[i]*1)  
    if(Data1[i,]$pred_xgb>=0.5|Data1[i,]$price>=85) {
      total<-total+65-Data1$price[i]
      break
    }
  }
  if (Data1[i,]$pred_xgb<0.5){
    total<-total+Data1[i,]$price-65
    Data1[i,]$price<-65
    
  }
  if (total<0) {
    total<-total-65+Data1[i,]$price
    Data1[i,]$price<-65
    break
  }
  i<-i+1
}


for (i in 1:2066){
  if(Data1[i,]$pred_xgb>=0.5){
    Data1[i,]$outcomes<-1
  }
}

##export to Data2_final price
write.csv(Data1,file="C://Users//24732//Desktop//B//Data_problem_4_Phase_II.csv.csv",quote=F,row.names = T)

