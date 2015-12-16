import sys
import time

from cssigps.offlineclassifier import *
from cssigps.dataset import *
from cssigps.feature import *
from cssigps.experiments import *
from get_dropbox_path import *

def print_usage():
    """
    Print the usage for the main script.
    """
    print("USAGE: use the run.sh or the main.py directly.")
    print("")
    print("  run.sh <EXPERIMENT_NUMBER>")
    print("  python main.py <EXPERIMENT_NUMBER>")


if __name__ == '__main__':

    # decide which experiment to run based on the command line or user-input
    response = ""
    if len(sys.argv) >= 2:
        response=sys.argv[1]
        if response in ["-h","--help"]:
             print_usage()
             quit()
    else:
        prompt = "Which experiment would you like to run? [0-2]"
        response = raw_input(prompt)

    # run experiment
    if response == "0":
        path=get_dropbox_path()+"old-test/"
        run_experiment_0(path)
    elif response == "1":
        run_experiment_1(include_none=True)
    elif response == "2":
        run_experiment_2()
    elif response == "3":
        run_experiment_3()
    elif response == "4":
        run_experiment_4()
    elif response == "5":
        path=get_dropbox_path()+"vowels-test/"
        run_offline_svm(path)
    elif response == "S":
        # run single class classifier
        c = sys.argv[2]
        f = sys.argv[3]
        classes=["NONE"]
        path=get_dropbox_path()+"yes-no-test/"
        factory = FBankFeature()

        # select the class
        if c == "Y":
            path=get_dropbox_path()+"yes-no-test/"
            classes.append("Y")
        elif c=="N":
            path=get_dropbox_path()+"yes-no-test/"
            classes.append("N")
        elif c=="A":
            path=get_dropbox_path()+"vowels-test/"
            classes=["A","NONE"]
        elif c=="E":
            path=get_dropbox_path()+"vowels-test/"
            classes=["E","NONE"]
        elif c=="I":
            path=get_dropbox_path()+"vowels-test/"
            classes=["I","NONE"]
        elif c=="O":
            path=get_dropbox_path()+"vowels-test/"
            classes=["O","NONE"]
        elif c=="U":
            path=get_dropbox_path()+"vowels-test/"
            classes=["U","NONE"]
        else:
            print("class argument invalid")
            quit()

        # select the feature
        if f == "fbank":
            factory=FBankFeature()
        elif f == "m" or f == "magnitude":
            factory=MagnitudeFeature()
        elif f == "t" or f == "template":
            factory=MultiTemplateFeature(SampleSet(find_testsamples(path),classes=classes).class_rep())
        else:
            print("feature argument invalid")


        samples = find_testsamples(path)
        sample_set = SampleSet(samples,classes=classes)
        sample_set.stats()
        run_sample_experiment(sample_set,feat_factory=factory)
    elif response == "M":
        # run multi class classifier
        c = sys.argv[2]
        f = sys.argv[3]
        classes=["NONE"]
        path=get_dropbox_path()+"yes-no-test/"
        factory = FBankFeature()

        # select the class
        if c == "Y":
            path=get_dropbox_path()+"yes-no-test/"
            classes=["Y","N","NONE"]
        elif c=="A":
            path=get_dropbox_path()+"vowels-test/"
            classes=["A","E","I","O","U","NONE"]
        else:
            print("class argument invalid")
            quit()

        samples = find_testsamples(path)
        sample_set = SampleSet(samples,classes=classes)
        sample_set.stats()

        # select the feature
        if f == "fbank":
            factory=FBankFeature()
        elif f == "m" or f == "magnitude":
            factory=MagnitudeFeature()
        elif f == "t" or f == "template":
            factory=MultiTemplateFeature(SampleSet(find_testsamples(path),classes=classes).class_rep())
        else:
            print("feature argument invalid")

        run_sample_experiment(sample_set,feat_factory=factory)
    else:
        print("Invalid option. Aborting..")
