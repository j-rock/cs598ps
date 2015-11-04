
from offlineclassifier import TemplateClassifier
from get_dropbox_path import get_dropbox_path
from matplotlib import pyplot as plt

if __name__ == '__main__':
    print('Running template matching')

    DROPBOX_PATH = get_dropbox_path()

    classifier = TemplateClassifier()

    # train classifier
    template = DROPBOX_PATH + 'raw_samples/distinct_sounds/eee_sound.wav'
    classifier.train(template)

    # test offline dataset with classifier
    matches = classifier.test(DROPBOX_PATH + 'test/distinct_sounds/ad-audio-eee-present.wav')
    for match in matches:
        print('Match found at: '+str(match))

    print('done')

    # plot results
    plt.plot(classifier._get_raw_result())
    plt.show()
