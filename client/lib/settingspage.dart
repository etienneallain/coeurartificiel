import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  _SettingsPageState createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  String ia1Difficulty = 'Easy';
  String ia1Type = 'MCTS';

  String ia2Difficulty = 'Easy';
  String ia2Type = 'MCTS';

  String ia3Difficulty = 'Easy';
  String ia3Type = 'MCTS';

  void sendInitializationRequest() async {
    final Map<String, dynamic> requestBody = {
      "ia_players": [
        {"id": 1, "type": ia1Type},
        {"id": 2, "type": ia2Type},
        {"id": 3, "type": ia3Type},
      ]
    };

    final String requestBodyJson = json.encode(requestBody);

    try {
      final response = await http.post(
        Uri.parse('http://localhost:5000/initialisation'),
        headers: <String, String>{
          'Content-Type': 'application/json',
        },
        body: requestBodyJson,
      );

      if (response.statusCode == 200) {
        Navigator.pushNamed(context, "/game");
      } else {
        print(
            "Erreur lors de la requête d'initialisation : ${response.statusCode}");
      }
    } catch (e) {
      print("Erreur lors de la requête d'initialisation : $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("SETTINGS"),
        backgroundColor: Colors.red[700],
        centerTitle: true,
      ),
      body: Stack(
        fit: StackFit.expand,
        children: [
          Image.asset(
            'assets/5120953.jpg',
            fit: BoxFit.cover,
          ),
          SingleChildScrollView(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                children: [
                  SizedBox(height: 40),
                  buildIaSection(1),
                  SizedBox(height: 20),
                  buildIaSection(2),
                  SizedBox(height: 20),
                  buildIaSection(3),
                  SizedBox(height: 80),
                  ElevatedButton(
                    child: Text("Start the game !"),
                    onPressed: sendInitializationRequest,
                    style: ElevatedButton.styleFrom(primary: Colors.red[700]),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget buildIaSection(int number) {
    String iaDifficulty;
    String iaType;

    switch (number) {
      case 1:
        iaDifficulty = ia1Difficulty;
        iaType = ia1Type;
        break;
      case 2:
        iaDifficulty = ia2Difficulty;
        iaType = ia2Type;
        break;
      case 3:
        iaDifficulty = ia3Difficulty;
        iaType = ia3Type;
        break;
      default:
        return Container();
    }

    return Container(
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.8),
        borderRadius: BorderRadius.circular(15.0),
      ),
      padding: EdgeInsets.all(16.0),
      child: Column(
        children: [
          Text(
            'Intelligence Artificielle $number',
            style: TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 18.0,
            ),
          ),
          SizedBox(height: 10),
          DropdownButton<String>(
            value: iaDifficulty,
            onChanged: (String? newValue) {
              setState(() {
                switch (number) {
                  case 1:
                    ia1Difficulty = newValue!;
                    break;
                  case 2:
                    ia2Difficulty = newValue!;
                    break;
                  case 3:
                    ia3Difficulty = newValue!;
                    break;
                }
              });
            },
            items: <String>['Easy', 'Medium', 'Hard'].map((String value) {
              return DropdownMenuItem<String>(
                value: value,
                child: Text(value),
              );
            }).toList(),
          ),
          SizedBox(height: 20),
          DropdownButton<String>(
            value: iaType,
            onChanged: (String? newValue) {
              setState(() {
                switch (number) {
                  case 1:
                    ia1Type = newValue!;
                    break;
                  case 2:
                    ia2Type = newValue!;
                    break;
                  case 3:
                    ia3Type = newValue!;
                    break;
                }
              });
            },
            items: <String>['MCTS', 'Neural Network'].map((String value) {
              return DropdownMenuItem<String>(
                value: value,
                child: Text(value),
              );
            }).toList(),
          ),
        ],
      ),
    );
  }
}
