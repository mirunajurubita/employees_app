import 'package:employee_management/module/home/view/screen/home.dart';
import 'package:get/get.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../../../core/repo/repository.dart';
import 'package:flutter/material.dart';


class LoginController extends GetxController {
  final Repository repository;

  LoginController({required this.repository});

  ///Declare and initialize the bool Rx variable
  RxBool isLoading = false.obs;
  

  ///Save AccessToken here to SharedPreferences which will be used in splash screen
  saveTokenToSharedPreferences(context, accessToken) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    
    prefs.setString("accessToken", accessToken.toString());

    ///Go to Home Screen and remove all previous routes
    Navigator.of(context).pushAndRemoveUntil(
        MaterialPageRoute(builder: (context) => const Home()),
        (Route<dynamic> route) => false);
  }

  singIn(BuildContext context, username, password) {
    
    isLoading.value = true;
    repository.signIn(username, password).then((res) {
      if (res[0] == true) {
        isLoading.value = false;
        saveTokenToSharedPreferences(context, res[1]['token']);
      } else {
        isLoading.value = false;
        Get.snackbar('Error', res[1]['parameter error'],
            snackPosition: SnackPosition.BOTTOM, backgroundColor: Colors.red);
      }
    });
  }
}
