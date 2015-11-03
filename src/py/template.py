
# python lib imports
# external imports
from scipy import signal

# project specific imports
from get_dropbox_path import get_dropbox_path

def template_match(template, audio):
    # convolution
    match = signal.fftconvolve(audio, template)

    # scale and take absolute value
    match = match ** 2

    # low-pass filter
    a = 1
    b = signal.firwin(999, cutoff = 1e-9, window = 'hamming')
    match = signal.lfilter(b, a, match, axis = 0)

    return match

if __name__ == '__main__':
    from matplotlib import pyplot as plt
    import scipy.io.wavfile as wavfile

    DROPBOX_PATH = get_dropbox_path()

    template_rate, template = wavfile.read(DROPBOX_PATH + 'raw_samples/distinct_sounds/eee_sound.wav')
    #audio_rate, audio = wavfile.read(DROPBOX_PATH + 'test/distinct_sounds/song-audio-eee-present.wav')
    audio_rate, audio = wavfile.read(DROPBOX_PATH + 'test/distinct_sounds/ad-audio-eee-present.wav')
    assert template_rate == audio_rate
    print('performing template match...')
    result = template_match(template, audio)
    print('done')

    plt.plot(result)
    plt.show()
