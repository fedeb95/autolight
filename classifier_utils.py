from sklearn.model_selection import train_test_split

def accuracy(clf,data,test_size=0.2):
    train, test = train_test_split(data, test_size=test_size)
    values_train = train[['distance','light','time']]
    labels_train = train['switch']
    values_test = test[['distance','light','time']]
    labels_test = test['switch']
    clf=clf.fit(values_train,labels_train)
    pred=clf.predict(values_test)
    ok=len(labels_test[labels_test == pred])
    nk=len(labels_test[labels_test != pred])
    return ok,nk

