import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class FanControlScreen extends StatefulWidget {
  @override
  _FanControlScreenState createState() => _FanControlScreenState();
}

class _FanControlScreenState extends State<FanControlScreen> {
  bool isAcOn = false;
  bool isLoading = true;

  // Thông tin tài khoản Adafruit IO

  final String username = dotenv.env['USERNAME'] ?? "";
  final String apiKey = dotenv.env['API_KEY'] ?? "";
  final String feed = "fan";

  @override
  void initState() {
    super.initState();
    _loadLocalStatus();
    _getACStatus(); // Lấy trạng thái từ Adafruit IO
  }

  // Hàm lấy trạng thái lưu trữ cục bộ
  Future<void> _loadLocalStatus() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      isAcOn = prefs.getBool('isAcOn') ??
          false; // Lấy trạng thái đã lưu hoặc mặc định là false
    });
  }

  // Hàm lưu trạng thái cục bộ
  Future<void> _saveLocalStatus(bool status) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('isAcOn', status);
  }

  // Hàm lấy trạng thái hiện tại từ Adafruit IO
  Future<void> _getACStatus() async {
    final url = Uri.parse(
        "https://io.adafruit.com/api/v2/$username/feeds/$feed/data/last");

    final response = await http.get(
      url,
      headers: {
        "Content-Type": "application/json",
        "X-AIO-Key": apiKey,
      },
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      setState(() {
        isAcOn = data["value"] == "ON";
        isLoading = false; // Tắt chế độ tải sau khi hoàn thành
      });
      _saveLocalStatus(isAcOn); // Cập nhật trạng thái cục bộ
    } else {
      print("Lấy trạng thái điều hòa thất bại: ${response.body}");
      setState(() {
        isLoading = false; // Tắt chế độ tải nếu thất bại
      });
    }
  }

  // Hàm gửi dữ liệu đến Adafruit IO
  Future<void> _toggleAC(bool status) async {
    final url =
        Uri.parse("https://io.adafruit.com/api/v2/$username/feeds/$feed/data");

    final response = await http.post(
      url,
      headers: {
        "Content-Type": "application/json",
        "X-AIO-Key": apiKey,
      },
      body: jsonEncode({"value": status ? "ON" : "OFF"}),
    );

    if (response.statusCode == 200) {
      print("Đã gửi dữ liệu điều hòa thành công đến Adafruit IO");
      _saveLocalStatus(status); // Lưu trạng thái cục bộ khi có thay đổi
    } else {
      print("Gửi dữ liệu điều hòa thất bại: ${response.body}");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
          title: const Text("Điều khiển quạt",
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
          centerTitle: true),
      body: isLoading
          ? const Center(
              child:
                  CircularProgressIndicator()) // Hiển thị biểu tượng tải khi chờ dữ liệu
          : Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text(
                    "Điều Khiển Điều Hòa",
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 20),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text("Bật/Tắt", style: TextStyle(fontSize: 18)),
                      Switch(
                        value: isAcOn,
                        onChanged: (value) async {
                          setState(() => isAcOn = value);
                          await _toggleAC(
                              value); // Gửi trạng thái mới lên Adafruit IO
                        },
                      ),
                    ],
                  ),
                  // Thêm các thành phần điều khiển khác cho AC ở đây nếu cần
                ],
              ),
            ),
    );
  }
}
