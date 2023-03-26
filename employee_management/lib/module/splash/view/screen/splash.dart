import 'dart:convert';

import 'package:employee_management/module/home/view/screen/home.dart';
import 'package:employee_management/utils/theme/color_const.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../../auth/signin/view/screen/signin.dart';

class Splash extends StatefulWidget {
  const Splash({Key? key}) : super(key: key);

  @override
  State<Splash> createState() => _SplashState();
}

class _SplashState extends State<Splash> {
  ///Check for accessToken in initState

  @override
  void initState() {
    Future.delayed(const Duration(milliseconds: 1500), () {
      checkForAccessToken();
      // Navigator.pushReplacement(
      //     context,
      //     MaterialPageRoute(
      //       builder: (context) => const SignIn(),
      //     ));
    });
    super.initState();
  }

  /// Check for accessToken function
  checkForAccessToken() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    final accessToken = prefs.getString("accessToken");
    if (accessToken == null) {
      ///This function will call when accessToken is not null
      gotoLoginScreen();
    } else {
      ///This function will call when accessToken is null
      gotoHomeScreen();
    }
  }

  gotoLoginScreen() {
    Navigator.pushReplacement(
        context, MaterialPageRoute(builder: (context) => const SignIn()));
  }

  gotoHomeScreen() {
    // SharedPreferences prefs = await SharedPreferences.getInstance();
    // print(jsonDecode(prefs.getString("userType")!));
    Navigator.pushReplacement(
        context, MaterialPageRoute(builder: (context) => const Home()));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: MyColors.whiteColor,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Employees Management',
              style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 32.sp,
                  color: MyColors.greenColor),
            ),
            Text(
              'App',
              style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 32.sp,
                  color: MyColors.greenColor),
            ),
          ],
        ),
      ),
    );
  }
}
