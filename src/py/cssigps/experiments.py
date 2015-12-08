# Module:  experiment
# Purpose: contain set of experiments that make use of classifiers
#          and features.
#
from matplotlib import pyplot as plt

from offlineclassifier import *
from get_dropbox_path import *
from dataset import *
from feature import *

def run_experiment_0(path=get_dropbox_path()+"old-test/"):
    """
    Run Experiment 0.
    Use the old simple vowel sample collection (only A and E present).
    Use a single class classifier (for A).
    Run the offline version of the Template Classifier.

    Parameters:
    -----------
    path - string
        the path to search for the Templates and TestRecordings.
    """
    print('Running Experiment 0')
    print('Running template matching')
    classifier = TemplateClassifier()

    # train classifier
    templates = find_templates(path)
    if len(templates) < 1:
        raise ValueError('No templates found! aborting')

    print("Training on template: "+str(templates[0]))
    # train on a single template for now
    classifier.train(templates[0])

    # test a single recording with classifier
    recordings = find_testrecordings(get_dropbox_path())

    classifier.test_recording(recordings[0].path)
    print "Test: "+str(recordings[0])

    # plot results
    plt.plot(classifier._get_raw_result())
    plt.show()

    print 'Classifier test times: '+str(classifier._get_raw_test_times())
    print 'Classifier read times: '+str(classifier._get_raw_read_times())

MultiTemplateLoader([])

def feature_factory(sample):
    return FBankFeature(sample).feature

def class_factory(sample):
    return class_to_num(sample.y)

def single_class_factory(sample,sample_class):
    if extract_gen_class(sample.y) == sample_class:
        return 1
    return 0

def run_experiment_1(include_none=False,path=get_dropbox_path()+"yes-no-test/"):
    """
    Run Experiment 1.
    Use the Yes/No sample collection.
    Use a single class classifier (for Yes).
    Run the offline version of the SVM classifier.

    Parameters:
    -----------
    include_none - bool
        whether or not to include the "NONE" class samples
    path - string
        the path to search for the samples
    """
    print('Running Experiment 1')
    # return a list of the audio test samples
    samples = find_testsamples(path)

    classes=["Y","N"]
    if include_none:
        classes.append("NONE")

    sample_set = SampleSet(samples,classes=classes)
    sample_set.stats()
    (train,test) = sample_set.sample()

    # generate features and classes from TestSamples
    train_features = []
    train_classes = []
    for sample in train:
        train_features.append(feature_factory(sample))
        train_classes.append(class_factory(sample))
        print('class: '+str(class_factory(sample)))

    # train the classifier
    classifier = SVMClassifier()
    classifier.train(train_features,train_classes)

    # generate features and classes from TestSamples
    test_features = []
    test_classes = []
    for sample in test:
        test_features.append(feature_factory(sample))
        test_classes.append(class_factory(sample))

    # test the classifier
    classifier.test(test_features,test_classes)

def run_experiment_2(path=get_dropbox_path()+"yes-no-test/"):
    """
    Run Experiment 2.
    Use the Yes/No sample collection, but only the "Y" and "NONE" samples.
    Use a single class classifier (for Yes).
    Run the offline version of the SVM classifier.

    Parameters:
    -----------
    path - string
        the path to search for the samples
    """
    print('Running Experiment 2')
    # return a list of the audio test samples
    samples = find_testsamples(path)

    classes=["Y","NONE"]
    sample_set = SampleSet(samples,classes=classes)
    sample_set.stats()
    (train,test) = sample_set.sample()

    # generate features and classes from TestSamples
    train_features = []
    train_classes = []
    for sample in train:
        train_features.append(feature_factory(sample))
        train_classes.append(single_class_factory(sample,"Y"))
        #print(str(sample))
        #print('class: '+str(single_class_factory(sample,"Y")))

    # train the classifier
    print("Training classifier...")
    classifier = SVMClassifier()
    classifier.train(train_features,train_classes)

    print("Testing classifier...")
    # Test samples one by one
    score = 0
    for sample in test:
        prediction = classifier.predict(feature_factory(sample))
        test_class = single_class_factory(sample,"Y")
        if prediction != test_class:
            print(str(sample))
            print("incorrect classification (prediction: "+str(prediction)+", class: "+str(test_class)+")")
            print("feature: "+str(feature_factory(sample)))
        else:
            print("correct classification")
            score=score+1
    print('Classification score: '+str(score)+'/'+str(len(test)))
    print('Classification score: '+str(float(score)/float(len(test))))

def run_experiment_3(path=get_dropbox_path()+"simple-yes-no-test/"):
    """
    Run Experiment 3.
    Use the simple Yes/No sample collection, but only the "Y" and "NONE" samples.
    Use a single class classifier (for Yes).
    Run the offline version of the SVM classifier.

    Parameters:
    -----------
    path - string
        the path to search for the samples
    """
    print('Running Experiment 3')
    # return a list of the audio test samples
    samples = find_testsamples(path)

    classes=["Y","NONE"]
    sample_set = SampleSet(samples,classes=classes)
    sample_set.stats()
    (train,test) = sample_set.sample()

    # generate features and classes from TestSamples
    train_features = []
    train_classes = []
    for sample in train:
        train_features.append(feature_factory(sample))
        train_classes.append(single_class_factory(sample,"Y"))

    # train the classifier
    print("Training classifier...")
    classifier = SVMClassifier()
    classifier.train(train_features,train_classes)

    print("Testing classifier...")
    # Test samples one by one
    score = 0
    for sample in test:
        prediction = classifier.predict(feature_factory(sample))
        test_class = single_class_factory(sample,"Y")
        if prediction != test_class:
            print(str(sample))
            print("incorrect classification (prediction: "+str(prediction)+", class: "+str(test_class)+")")
            print("feature: "+str(feature_factory(sample)))
        else:
            print("correct classification")
            score=score+1
    print('Classification score: '+str(score)+'/'+str(len(test)))
    print('Classification score: '+str(float(score)/float(len(test))))

def run_experiment_4(path=get_dropbox_path()+"simple-yes-no-test/"):
    """
    Run Experiment 4.
    Use the simple Yes/No sample collection and all samples.
    Use multi-class classifier ("Y","N","NONE").
    Run the offline version of the SVM classifier.

    Parameters:
    -----------
    path - string
        the path to search for the samples
    """
    print('Running Experiment 4')
    # return a list of the audio test samples
    samples = find_testsamples(path)

    sample_set = SampleSet(samples)
    sample_set.stats()
    (train,test) = sample_set.sample()

    # generate features and classes from TestSamples
    train_features = []
    train_classes = []
    for sample in train:
        train_features.append(feature_factory(sample))
        train_classes.append(class_factory(sample))

    # train the classifier
    print("Training classifier...")
    classifier = SVMClassifier()
    classifier.train(train_features,train_classes)

    print("Testing classifier...")
    # Test samples one by one
    score = 0
    for sample in test:
        prediction = classifier.predict(feature_factory(sample))
        test_class = single_class_factory(sample,"Y")
        if prediction != test_class:
            print(str(sample))
            print("incorrect classification (prediction: "+str(prediction)+", class: "+str(test_class)+")")
            print("feature: "+str(feature_factory(sample)))
        else:
            print("correct classification")
            score=score+1
    print('Classification score: '+str(score)+'/'+str(len(test)))
    print('Classification score: '+str(float(score)/float(len(test))))

def run_sample_experiment(sampleset,ratio=0.5,feat_factory=feature_factory):
    """
    Run Sample Experiment.

    Parameters:
    -----------
    sampleset - SampleSet object
        object containing the list of samples for training/testing
    ratio - float
        the training/testing ratio
    feat_factory - function
        the function to generate features for each sample from
    """
    (train,test) = sampleset.sample(ratio=ratio)

    # generate features and classes from TestSamples
    train_features = []
    train_classes = []
    for sample in train:
        train_features.append(feat_factory(sample))
        train_classes.append(class_factory(sample))

    # train the classifier
    print("Training classifier...")
    classifier = SVMClassifier()
    classifier.train(train_features,train_classes)

    # train the baseline classifier for comparison
    baseline = BestGuessClassifier()
    baseline.train(train_features,train_classes)

    print("Testing classifier...")
    # Test samples one by one
    score = 0
    test_features=[]
    test_classes=[]
    for sample in test:
        prediction = classifier.predict(feat_factory(sample))
        test_class = class_factory(sample)
        test_features.append(feat_factory(sample))
        test_classes.append(test_class)
        if prediction != test_class:
            print(str(sample))
            print("incorrect classification (prediction: "+str(prediction)+", class: "+str(test_class)+")")
            print("feature: "+str(feat_factory(sample)))
        else:
            print("correct classification")
            score=score+1
    print('Classification score: '+str(score)+'/'+str(len(test)))
    print('Classification score: '+str(float(score)/float(len(test))))

    baseline.test(test_features,test_classes)
