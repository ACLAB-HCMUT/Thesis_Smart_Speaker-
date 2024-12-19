import bluetooth
import subprocess
from time import sleep

# Tìm kiếm thiết bị Bluetooth gần đó
def discover_devices():
    print("Đang tìm kiếm thiết bị Bluetooth...")
    devices = bluetooth.discover_devices(duration=8, lookup_names=True)
    for addr, name in devices:
        print(f"Tìm thấy thiết bị: {name} - {addr}")
    return devices

# Kết nối tới thiết bị Bluetooth
def connect_device(address):
    print(f"Kết nối tới thiết bị: {address}")
    try:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((address, 1))
        print("Kết nối thành công!")
        return sock
    except Exception as e:
        print(f"Lỗi khi kết nối: {e}")
        return None

# Gửi lệnh gọi qua Bluetooth
def make_call(sock, phone_number):
    print(f"Thực hiện cuộc gọi tới: {phone_number}")
    try:
        # Lệnh giả định (tùy theo thiết bị hỗ trợ HFP)
        command = f"ATD{phone_number};\n"  # Lệnh AT để quay số
        sock.send(command.encode())
        print("Đang gọi...")
    except Exception as e:
        print(f"Lỗi khi gọi: {e}")

# Ngắt cuộc gọi
def end_call(sock):
    print("Kết thúc cuộc gọi...")
    try:
        sock.send("ATH\n".encode())  # Lệnh AT để ngắt cuộc gọi
        print("Đã kết thúc cuộc gọi.")
    except Exception as e:
        print(f"Lỗi khi kết thúc cuộc gọi: {e}")

# Chương trình chính
if __name__ == "__main__":
    devices = discover_devices()
    if not devices:
        print("Không tìm thấy thiết bị Bluetooth nào.")
        exit()

    # Chọn thiết bị
    target_device = devices[0]  # Chọn thiết bị đầu tiên (có thể sửa thành logic khác)
    address = target_device[0]

    # Kết nối tới thiết bị
    sock = connect_device(address)
    if sock:
        phone_number = input("Nhập số điện thoại cần gọi: ")
        make_call(sock, phone_number)
        sleep(10)  # Gọi trong 10 giây (có thể thay đổi)
        end_call(sock)
        sock.close()