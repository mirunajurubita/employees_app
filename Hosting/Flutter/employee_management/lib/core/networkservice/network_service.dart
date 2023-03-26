import 'dart:convert';
import 'package:http/http.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:http/http.dart' as http;


class NetworkService {
  ///Base Url
  //final baseUrlApi = "http://10.0.2.2:8000";
  final baseUrlApi = "http://192.168.0.100:8000";
  ///SignIn Function
  Future signIn(username, password) async {
   
    late String? fcm_token;
  
    await FirebaseMessaging.instance.getToken().then((token) async {
      fcm_token = token!;
      
    }).catchError((e) {
      print('eroare e');
      print(e);
    });
    print('tokenul e');
    print(fcm_token);
    
    final response = await post(
      Uri.parse('$baseUrlApi/employee-api/signin/'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, dynamic>{
        'username': username,
        'password': password.toString(),
        'token' : fcm_token
      }),
    );

    if (response.statusCode == 200) {
      // If the server did return a 201 CREATED response,
      // then parse the JSON.
      return [true, jsonDecode(response.body)];
    } else {
      // If the server did not return a 201 CREATED response,
      // then throw an exception.
      return [false, jsonDecode(response.body)];
    }
  }
  
  ///GetDashboardItems function
  Future<List> getDashboardItems() async {
    
  
    

     AndroidNotificationChannel channel = AndroidNotificationChannel(
    'high_importance_channel', // id
    'High Importance Notifications', // title
    importance: Importance.high,
    enableVibration: true,
    playSound: true,
  );
  /// Initalize the [FlutterLocalNotificationsPlugin] package.
  final FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin =
      FlutterLocalNotificationsPlugin();

  int _messageCount = 0;

/// The API endpoint here accepts a raw FCM payload for demonstration purposes.
String constructFCMPayload(String token) {
  _messageCount++;
  return jsonEncode({
    'token': token,
    'data': {
      'via': 'FlutterFire Cloud Messaging!!!',
      'count': _messageCount.toString(),
    },
    'notification': {
      'title': 'Hello FlutterFire!',
      'body': 'This notification (#$_messageCount) was created via FCM!',
    },
  });
}
    
    SharedPreferences prefs = await SharedPreferences.getInstance();
    var accessToken = "Token ${prefs.getString("accessToken")!}";
    final response = await get(
      Uri.parse('$baseUrlApi/employee-api/dashboard/'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': accessToken,
      },
    );

    if (response.statusCode == 200) {
      // If the server did return a 201 CREATED response,
      // then parse the JSON.
      return [true, jsonDecode(response.body)];
    } else {
      // If the server did not return a 201 CREATED response,
      // then throw an exception.
      return [false, jsonDecode(response.body)];
    }
  }

  ///startTask function
  Future startTask(id) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    var accessToken = "Token ${prefs.getString("accessToken")!}";
    final response = await put(
      Uri.parse('$baseUrlApi/employee-api/start/$id/'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': accessToken,
      },
    );

    if (response.statusCode == 201) {
      // If the server did return a 201 CREATED response,
      // then parse the JSON.
      return [true, jsonDecode(response.body)];
    } else {
      // If the server did not return a 201 CREATED response,
      // then throw an exception.
      return [false, jsonDecode(response.body)];
    }
  }



  ///MarkedAsCompleted function
  Future markAsCompleted(id) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    var accessToken = "Token ${prefs.getString("accessToken")!}";
    final response = await put(
      Uri.parse('$baseUrlApi/employee-api/completed/$id/'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': accessToken,
      },
    );

    if (response.statusCode == 201) {
      // If the server did return a 201 CREATED response,
      // then parse the JSON.
      return [true, jsonDecode(response.body)];
    } else {
      // If the server did not return a 201 CREATED response,
      // then throw an exception.
      return [false, jsonDecode(response.body)];
    }
  }



  ///startpause function
  Future startPause(id) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    var accessToken = "Token ${prefs.getString("accessToken")!}";
    final response = await put(
      Uri.parse('$baseUrlApi/employee-api/startpause/$id/'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': accessToken,
      },
    );

    if (response.statusCode == 201) {
      // If the server did return a 201 CREATED response,
      // then parse the JSON.
      return [true, jsonDecode(response.body)];
    } else {
      // If the server did not return a 201 CREATED response,
      // then throw an exception.
      return [false, jsonDecode(response.body)];
    }
  }

  ///stoppause function
  Future stopPause(id) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    var accessToken = "Token ${prefs.getString("accessToken")!}";
    final response = await put(
      Uri.parse('$baseUrlApi/employee-api/stoppause/$id/'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': accessToken,
      },
    );

    if (response.statusCode == 201) {
      // If the server did return a 201 CREATED response,
      // then parse the JSON.
      return [true, jsonDecode(response.body)];
    } else {
      // If the server did not return a 201 CREATED response,
      // then throw an exception.
      return [false, jsonDecode(response.body)];
    }
  }
}


