import numpy as np

def lms_filter(input_signal, reference_signal, filter_len, mu):
    # Khởi tạo trọng số với giá trị bằng 0
    weights = np.zeros(filter_len)
    
    # Tạo mảng để lưu kết quả
    output_signal = np.zeros_like(input_signal)
    
    # Duyệt qua tất cả các mẫu của tín hiệu
    for n in range(len(input_signal)):
        # Tính toán đầu ra của bộ lọc
        y = 0.0
        for k in range(filter_len):
            if n >= k:
                y += weights[k] * reference_signal[n - k]
        
        # Tính toán sai số
        error = input_signal[n] - y
        output_signal[n] = error  # Lưu sai số vào mảng đầu ra
        
        # Cập nhật trọng số
        for k in range(filter_len):
            if n >= k:
                weights[k] += 2 * mu * error * reference_signal[n - k]
    
    return output_signal, weights

# Ví dụ sử dụng
input_signal = np.array([1, 2, 3, 4, 5])
reference_signal = np.array([1, 1, 1, 1, 1])
filter_len = 3
mu = 0.01

output, weights = lms_filter(input_signal, reference_signal, filter_len, mu)
print("Output Signal:", output)
print("Weights:", weights)
