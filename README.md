#CS598PS UIUC Final Project

##Members

* Sean Bartell (smbarte2)
* Evan Bowling (ebowlin2)
* Joseph Rock (jwrock2)

##Summary

Supervised learning task that detects pre-recorded audio samples (training) within other audio inputs (testing). The audio inputs will consist of multiple environments including on-going human conversations. We will be constructing our own dataset of human-made sounds (not words, more like simple noises you might make to a pet):

* click noise
* kissy noise
* popping noise
* whistle noise
* etc

##Motivation

Audio voice inputs such as Siri and Cortana have grown in popularity and common usage. This is in part due to the ability for these systems to operate without any additional training by the user (they just "work" out of the box). While they provide rich speech detection capabilities, a "conversation" with these systems requires that one user speak at a time. This constraint is likely necessary right now as these systems are considered to be state of the art, but complete voice detection is not always necessary for conversations. By detecting a simple pre-defined click or pop while emitting speech, an audio voice input could react faster like a human being. If Siri was going to announce "I'm sorry but I can't connect to the internet right now", a user could quickly interrupt it with a click or pop to indicate impatience or dismissal and the phone would resume its previous task e.g. playing a song.

###Objective 1

First task will be working on multi-template audio detection (need to identify which template occurred, if any) in Matlab code and ramping up on a Python library to perform the same task. Aligning with the goals of the class, we aim to solve practical problems and develop code that we can run in more diverse environments.

###Objective 2

Enhance the robustness of the template detection by introducing altered test datasets (added echo, reverb, distortion, etc).

###Objective 3

Run the detection algorithm live. See if templates can be detected on a per/person basis. Investigate what other attributes can be derived about a detection event (loud vs soft event, close vs distant, aggrevated vs relaxed).

##Installation

Python 2.X is required. The codebase must be downloaded from Github. This can be done with the following command:

    git clone https://github.com/j-rock/cs598ps.git

Additional libraries must be installed as well including:
* numpy
* scipy
* python_speech_features library that provides MFCC and Filter Bank features

Reference the `install.sh` file.

##Run Instructions

There are two primary methods of running the python codebase: experiment mode and listening mode. The experiments can be started in the following way:

    run.sh
  
This will require user input for determinging which experiment to run. This can be specified from the command line as well:

    run.sh 0  # run experiment 0
    
    run.sh 1  # run experiment 1

Listening mode addresses Objective 3 by training a classifier offline and then testing against live input.

##Testing

A set of unit tests have been created for the python codebase. These can be run from the command line with the following command:

    test.sh

##Datasets

All of the datasets used for this project were created using:
* iPhone 5s microphone
* MacBook Pro microphone
* Ableton Live audio processing software

Each dataset is summarized in the table below:

Dataset Name  | Description | Number of Classes
------------- | -------------|---------------
old-test  | simple collection of vowel sounds and silence| ?
simple-yes-no-test | collection of "yes" and "no" sound samples where each "yes" and "no" are nearly identical. | 3 ("Y","N","NONE")
yes-no-test  | collection of "yes" and "no" sound samples. Each "yes" and "no" are a different utterance. | 3 ("Y","N","NONE")
vowels-test  | collection of English vowel sounds. 5 instances of each vowel are used to produce the different samples. | 6 ("A","E","I","O","U")

##Experiments

Multiple experiments were devised to test the accuracy and practicality of the audio classifiers. They are summarized in the table below.

Experiment Number  | Dataset Name  | Description
------------- | ------------- | -----------
0  | old-test | 
1  | yes-no-test | Multi-class classification for all 3 classes.
2  | yes-no-test | Single class classification (Y vs NONE).
3  | simple-yes-no-test | Single class classification for trivial dataset. Expectation is nearly 100% accuracy on this experiment.
