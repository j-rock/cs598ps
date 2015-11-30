#! /bin/bash
# Install the required python packages

pip install sounddevice

# Sphinx not needed at this time
#pip install Sphinx # double check this command

# install the scikit lib for SVM implementation
# Successfully installed scikit-learn-0.17
pip install -U scikit-learn #http://scikit-learn.org/stable/install.html

# install the "features" module to get MEL MFCC, and FeatureBin Features
git clone https://github.com/jameslyons/python_speech_features
cd python_speech_features
python setup.py install
