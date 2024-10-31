import os
def message( payload):
    try:
        volume = int(payload)
        os.system(f"amixer sset 'Master' {volume}%")
        print(f"Volume set to {volume}%")
    except ValueError:
        print("Invalid volume value received")





# def toggle_device(command):
#     try:
#         if command == "wifi:off":
#             result = os.system("nmcli radio wifi off")
#             if result == 0:
#                 print("Wi-Fi turned off successfully")
#             else:
#                 print("Failed to turn off Wi-Fi")
#         elif command == "wifi:on":
#             result = os.system("nmcli radio wifi on")
#             if result == 0:
#                 print("Wi-Fi turned on successfully")
#             else:
#                 print("Failed to turn on Wi-Fi")
#         elif command == "bluetooth:off":
#             result = os.system("rfkill block bluetooth")
#             print("Bluetooth turned off" if result == 0 else "Failed to turn off Bluetooth")
#         elif command == "bluetooth:on":
#             result = os.system("rfkill unblock bluetooth")
#             print("Bluetooth turned on" if result == 0 else "Failed to turn on Bluetooth")
#         else:
#             print("Unknown command.")
#     except Exception as e:
#         print(f"An error occurred: {e}")


# toggle_device("bluetooth:on")