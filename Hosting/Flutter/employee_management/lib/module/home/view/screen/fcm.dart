import "package:firebase_messaging/firebase_messaging.dart";
import 'package:firebase_core/firebase_core.dart';
import "package:dio/dio.dart";


final FirebaseMessaging message = FirebaseMessaging.instance;

Future<void> initFcm() async{

  //token
  

  //request permission
  NotificationSettings settings = await message.requestPermission(
  alert: true,
  announcement: false,
  badge: true,
  carPlay: false,
  criticalAlert: false,
  provisional: false,
  sound: true,
);
  if (settings.authorizationStatus == AuthorizationStatus.authorized) {
  print('User granted permission');
} else if (settings.authorizationStatus == AuthorizationStatus.provisional) {
  print('User granted provisional permission');
} else {
  print('User declined or has not accepted permission');
}
  @pragma('vm:entry-point')
  Future<void> _firebaseMessagingBackgroundHandler(RemoteMessage message) async {
  // If you're going to use other Firebase services in the background, such as Firestore,
  // make sure you call `initializeApp` before using other Firebase services.
  await Firebase.initializeApp();
  FirebaseMessaging.onBackgroundMessage(_firebaseMessagingBackgroundHandler);

  print("Handling a background message: ${message.messageId}");
}




FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
  print("onMessageOpenedApp: $message");});


late String? fcm_token;

  await FirebaseMessaging.instance.getToken().then((token) async {
      fcm_token = token!;
      
    }).catchError((e) {
      print('eroare e');
      print(e);
    });
    print('tokenul e');
    print(fcm_token);

  //adaugata ulterior
  FirebaseMessaging.instance.isAutoInitEnabled ;
  //
  await FirebaseMessaging.instance.getToken();
  FirebaseMessaging.onMessage.listen(_firebaseMessagingBackgroundHandler);

  FirebaseMessaging.onMessage.listen((RemoteMessage message) {
  print('Got a message whilst in the foreground!');
  print('Message data: ${message.data}');

  if (message.notification != null) {
    print('Message also contained a notification: ${message.notification}');
  }
});

  


  //hit the API
  //final urlpath =  'https://fcm.googleapis.com/fcm/send';
  /*
  final data = {
    "registration_id": fcm_token,
    "type": "android",

  };
  */
  //var dio = Dio();
  //final resp = await dio.post(urlpath, data:data);

  print("response e");
  

  
}

  

