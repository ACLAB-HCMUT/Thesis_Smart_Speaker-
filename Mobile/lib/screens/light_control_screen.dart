import 'package:flutter/material.dart';
import 'package:flutter_application_1/widgets/color_button.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class LightControlScreen extends StatefulWidget {
  @override
  _LightControlScreenState createState() => _LightControlScreenState();
}

class _LightControlScreenState extends State<LightControlScreen> {
  bool isLightOn = false;
  bool isLoading = true;
  double brightness = 35.0;
  Color selectedColor = Colors.white;

  // Thông tin tài khoản Adafruit IO
  final String username = dotenv.env['USERNAME'] ?? "";
  final String apiKey = dotenv.env['API_KEY'] ?? "";
  final String feed = "led1";

  @override
  void initState() {
    super.initState();
    _loadLocalStatus();
    _getLightStatus(); // Lấy trạng thái từ Adafruit IO
  }

  // Hàm lấy trạng thái lưu trữ cục bộ
  Future<void> _loadLocalStatus() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      isLightOn = prefs.getBool('isLightOn') ?? false;
    });
  }

  // Hàm lưu trạng thái cục bộ
  Future<void> _saveLocalStatus(bool status) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('isLightOn', status);
  }

  // Hàm lấy trạng thái hiện tại từ Adafruit IO
  Future<void> _getLightStatus() async {
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
        isLightOn = data["value"] == "ON";
        isLoading = false; // Tắt chế độ tải sau khi hoàn thành
      });
      _saveLocalStatus(isLightOn); // Cập nhật trạng thái cục bộ
    } else {
      print("Lấy trạng thái đèn thất bại: ${response.body}");
      setState(() {
        isLoading = false; // Tắt chế độ tải nếu thất bại
      });
    }
  }

  // Hàm gửi dữ liệu đến Adafruit IO
  Future<void> _toggleLight(bool status) async {
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
      print("Đã gửi dữ liệu thành công đến Adafruit IO");
      _saveLocalStatus(status); // Lưu trạng thái cục bộ khi có thay đổi
    } else {
      print("Gửi dữ liệu thất bại: ${response.body}");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Điều Khiển Đèn",
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
        centerTitle: true,
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text("Bật/Tắt", style: TextStyle(fontSize: 18)),
                      Switch(
                        value: isLightOn,
                        onChanged: (value) async {
                          setState(() => isLightOn = value);
                          await _toggleLight(
                              value); // Gọi hàm gửi dữ liệu đến Adafruit
                        },
                      ),
                    ],
                  ),
                  Slider(
                    value: brightness,
                    min: 0,
                    max: 100,
                    divisions: 10,
                    label: "${brightness.round()}%",
                    onChanged: (value) => setState(() => brightness = value),
                  ),
                  const Text("Màu Sắc", style: TextStyle(fontSize: 18)),
                  Row(
                    children: [
                      ColorButton(
                          color: Colors.white,
                          onTap: () =>
                              setState(() => selectedColor = Colors.white)),
                      ColorButton(
                          color: Colors.blue,
                          onTap: () =>
                              setState(() => selectedColor = Colors.blue)),
                      ColorButton(
                          color: Colors.red,
                          onTap: () =>
                              setState(() => selectedColor = Colors.red)),
                    ],
                  ),
                ],
              ),
            ),
    );
  }
}
