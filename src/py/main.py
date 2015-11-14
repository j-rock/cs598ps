
from offlineclassifier import TemplateClassifier
from get_dropbox_path import *
from dataset import *
from matplotlib import pyplot as plt

if __name__ == '__main__':
    print('Running template matching')

    classifier = TemplateClassifier()

    # train classifier
    templates = find_templates(get_dropbox_path())
    if len(templates) < 1:
        raise ValueError('No templates found! aborting')
    classifier.train(templates[0])

    # test offline dataset with classifier
    recordings = find_testrecordings(get_dropbox_path())
    for test in recordings:
        matches = classifier.test_recording(test)
        print "Test: "+test
        print "Found "+str(len(matches))+" matches"

        # plot results
        plt.plot(classifier._get_raw_result())
        plt.show()

        print 'Classifier test times: '+str(classifier._get_raw_test_times())
        print 'Classifier read times: '+str(classifier._get_raw_read_times())
