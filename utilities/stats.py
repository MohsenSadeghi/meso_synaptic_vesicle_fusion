import numpy as np

def crop_arrays_to_min_size(arrays, axis=0):
    """
    Crop a list of NumPy arrays along the specified axis to the minimal size.
    
    Parameters:
        arrays (list of np.ndarray): List of arrays to crop.
        axis (int): Axis along which to crop.
    
    Returns:
        list of np.ndarray: List of cropped arrays.
    """
    # Step 1: Find the minimal size along the specified axis
    min_size = min(arr.shape[axis] for arr in arrays)
    
    # Step 2: Create slicing objects for each array
    slices = [tuple(
        slice(0, min_size) if i == axis else slice(None)
        for i in range(arr.ndim)
    ) for arr in arrays]
    
    # Step 3: Crop each array using the slicing objects
    cropped_arrays = [arr[s] for arr, s in zip(arrays, slices)]
    
    return cropped_arrays


def conv_smooth(x, window_len=11, window='hanning'):

    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise ValueError("conv_smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window_len < 3:
        return x

    if window not in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s = np.r_[x[window_len // 2 - 1:0:-1], x, x[-1:-window_len//2 - 1:-1]]

    # print(len(s))
    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.' + window + '(window_len)')

    y = np.convolve(w / w.sum(), s, mode='valid')

    return y
