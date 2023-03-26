import 'package:employee_management/module/auth/signin/view/screen/signin.dart';
import 'package:employee_management/utils/theme/color_const.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get_navigation/src/root/get_material_app.dart';
import 'module/splash/view/screen/splash.dart';
import 'dart:convert';
import "package:firebase_messaging/firebase_messaging.dart";
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:timezone/data/latest_all.dart' as tz;
import 'package:timezone/timezone.dart' as tz;

void main() async {

  
  
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(MyApp());
}
/*
  Future<void> _firebaseMessagingBackgroundHandler(RemoteMessage message) async {
    final fcmToken = await FirebaseMessaging.instance.getToken();

  debugPrint("Firebase Messaging firebase is initialized");
}
*/

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);




  @override
  Widget build(BuildContext context) {
    return ScreenUtilInit(

      designSize: const Size(428, 919),
      minTextAdapt: true,
      splitScreenMode: true,
      builder: (context, child) {
        return GetMaterialApp(
          debugShowCheckedModeBanner: false,
          title: 'Flutter Demo',
          theme: ThemeData(
            fontFamily: 'Roboto',
            textTheme: const TextTheme().copyWith(
              bodyText2: TextStyle(
                color: MyColors.whiteColor,
              ),
            ),
            iconTheme: IconThemeData(color: MyColors.whiteColor),
            useMaterial3: true,
            primarySwatch: Colors.blue,
          ),
          home: const Splash(),

          routes: {'/signIn': (context) => const SignIn()},
        );
      },
    );
  }
}
