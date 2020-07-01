import random
import numpy as np
from sklearn.model_selection import train_test_split
from collections import OrderedDict
from sklearn import svm



def train(classifier):
    train_samples, test_samples, train_labels, test_labels = train_test_split(
        samples,
        labels,
        test_size=classifier.seed,
        random_state=classifier
    )
    classifier._clf = svm.SVC()
    classifier._clf.fit(train_samples, train_labels)
  
    predicted_labels = classifier._clf.predict(test_samples)
    classifier._accuracy = sum([ expected == returned for expected, returned in zip(test_labels, predicted_labels)])
    classifier.save() 
    return classifier.tag

