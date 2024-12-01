import numpy as np

def lms_filter(input_signal, reference_signal, filter_len, mu):
    weights = np.zeros(filter_len)
    
    output_signal = np.zeros_like(input_signal)
    
    for n in range(len(input_signal)):
        y = 0.0
        for k in range(filter_len):
            if n >= k:
                y += weights[k] * reference_signal[n - k]
        
        error = input_signal[n] - y
        output_signal[n] = error 
        
        for k in range(filter_len):
            if n >= k:
                weights[k] += 2 * mu * error * reference_signal[n - k]
    
    return output_signal, weights
