import 'package:flutter/material.dart';
// import 'package:flutter_application_1/widgets/color_button.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class SpeakerControlScreen extends StatefulWidget {
  @override
  _SpeakerControlScreenState createState() => _SpeakerControlScreenState();
}

class _SpeakerControlScreenState extends State<SpeakerControlScreen> {
  bool isLightOn = false;
  bool isLoading = true;
  double brightness = 35.0;
  double volume = 50.0;
  Color selectedColor = Colors.white;

  final String username = dotenv.env['USERNAME'] ?? "";
  final String apiKey = dotenv.env['API_KEY'] ?? "";
  final String volumeFeed = "volume";

  @override
  void initState() {
    super.initState();
    _loadLocalStatus();
    _getVolumeStatus();
  }

  Future<void> _loadLocalStatus() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      isLightOn = prefs.getBool('isLightOn') ?? false;
    });
  }

  Future<void> _saveLocalStatus(bool status) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('isLightOn', status);
  }

  Future<void> _getVolumeStatus() async {
    final url = Uri.parse(
        "https://io.adafruit.com/api/v2/$username/feeds/$volumeFeed/data/last");

    try {
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
          volume = double.parse(data["value"]);
        });
      } else {
        print("Lấy trạng thái âm lượng thất bại: ${response.body}");
      }
    } catch (e) {
      print("Lỗi khi lấy trạng thái âm lượng: $e");
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  Future<void> _setVolume(double value) async {
    final url = Uri.parse(
        "https://io.adafruit.com/api/v2/$username/feeds/$volumeFeed/data");

    try {
      final response = await http.post(
        url,
        headers: {
          "Content-Type": "application/json",
          "X-AIO-Key": apiKey,
        },
        body: jsonEncode({"value": value.toString()}),
      );

      if (response.statusCode == 200) {
        print("Đã gửi dữ liệu âm lượng thành công đến Adafruit IO");
      } else {
        print("Gửi dữ liệu âm lượng thất bại: ${response.body}");
      }
    } catch (e) {
      print("Lỗi khi gửi dữ liệu âm lượng: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
          title: const Text("Điều Khiển Speaker",
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
          centerTitle: true),
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
                          await _saveLocalStatus(value);
                        },
                      ),
                    ],
                  ),
                  const SizedBox(height: 50),
                  const Text("Độ Lớn Loa",
                      style:
                          TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                  Slider(
                    value: volume,
                    min: 0,
                    max: 100,
                    divisions: 10,
                    label: "${volume.round()}",
                    onChanged: (value) async {
                      setState(() => volume = value);
                      await _setVolume(value);
                    },
                  ),
                ],
              ),
            ),
    );
  }
}
