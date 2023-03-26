import 'package:employee_management/utils/theme/color_const.dart';
import 'package:get/get.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter/material.dart';
import '../../../core/repo/repository.dart';
import '../../../utils/overlay_progress_bar/overlay_progress_bar.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';


class HomeController extends GetxController {
  Repository repository;
  
  HomeController({required this.repository});

  ///Rx variables
  RxBool isLoading = false.obs;
  RxBool isLoadingForMarked = false.obs;
  RxList getDashboardResponse = [].obs;
  ProgressBar? sendingMsgProgressBar = ProgressBar();

  ///Dispose method to dispose the overlay progress bar
  @override
  void dispose() {
    super.dispose();
    sendingMsgProgressBar!.hide();
  }

  ///Hide overlay progress bar
  void hideSendingProgressBar() {
    sendingMsgProgressBar!.hide();
  }


  ///Logout function
  logout(context) async {
    //await FirebaseMessaging.instance.deleteToken();
    SharedPreferences prefs = await SharedPreferences.getInstance();

    if (prefs.getString("accessToken") != null) {
      ///Clear the SharedPreferences (delete the token which is saved in it)
      prefs.clear();

      ///Go to the Login Screen and remove all previous routes
      Navigator.of(context)
          .pushNamedAndRemoveUntil('/signIn', (Route<dynamic> route) => false);
    }
  }

  ///Get Dashboard Items function
  ///
  
  getDashboardItem(context) {

    isLoading.value = true;
    repository.getDashboardItem().then((res) {
      if (res[0] == true) {
        isLoading.value = false;
        //print('valoarea res[1] e');
        //print(res[1]);
        getDashboardResponse.value =  res[1]['results'];
        //print('valoarea getdashboardreponse e');
        //print(getDashboardResponse.value);
      } else if (res[1]['detail'] == 'Invalid token.' ||
          res[1]['detail'] == 'Authentication credentials were not provided') {
        Get.snackbar('Error', 'Your session is out, Please login again',
            snackPosition: SnackPosition.TOP);
        logout(context);
      } else {
        isLoading.value = false;
        Get.snackbar('Error', res[1]['parameter error'],
            snackPosition: SnackPosition.TOP);
      }
    });
  }
  
  ///startTask function
  startTask(BuildContext context, id) {
    isLoadingForMarked.value = true;
    repository.startTask(id).then((res) {
      if (res[0] == true) {
        isLoadingForMarked.value = false;
        Get.snackbar('Success', res[1],
            snackPosition: SnackPosition.BOTTOM,
            backgroundColor: MyColors.greenColor);
        hideSendingProgressBar();
        getDashboardItem(context);
      } else {
        isLoadingForMarked.value = false;
        Get.snackbar('Error', res[1]['parameter error'],
            snackPosition: SnackPosition.BOTTOM, backgroundColor: Colors.red);
      }
    });
  }


  ///startPause function
  startPause(BuildContext context, id) {
    isLoadingForMarked.value = true;
    repository.startPause(id).then((res) {
      if (res[0] == true) {
        isLoadingForMarked.value = false;
        Get.snackbar('Success', res[1],
            snackPosition: SnackPosition.BOTTOM,
            backgroundColor: MyColors.greenColor);
        hideSendingProgressBar();
        getDashboardItem(context);
      } else {
        isLoadingForMarked.value = false;
        Get.snackbar('Error', res[1]['parameter error'],
            snackPosition: SnackPosition.BOTTOM, backgroundColor: Colors.red);
      }
    });
  }


  ///endPause function
  stopPause(BuildContext context, id) {
    isLoadingForMarked.value = true;
    repository.stopPause(id).then((res) {
      if (res[0] == true) {
        isLoadingForMarked.value = false;
        Get.snackbar('Success', res[1],
            snackPosition: SnackPosition.BOTTOM,
            backgroundColor: MyColors.greenColor);
        hideSendingProgressBar();
        getDashboardItem(context);
      } else {
        isLoadingForMarked.value = false;
        Get.snackbar('Error', res[1]['parameter error'],
            snackPosition: SnackPosition.BOTTOM, backgroundColor: Colors.red);
      }
    });
  }


  
  ///Mark as completed function
  markAsCompleted(BuildContext context, id) {
    isLoadingForMarked.value = true;
    repository.markAsCompleted(id).then((res) {
      if (res[0] == true) {
        isLoadingForMarked.value = false;
        Get.snackbar('Success', res[1],
            snackPosition: SnackPosition.BOTTOM,
            backgroundColor: MyColors.greenColor);
        hideSendingProgressBar();
        getDashboardItem(context);
      } else {
        isLoadingForMarked.value = false;
        Get.snackbar('Error', res[1]['parameter error'],
            snackPosition: SnackPosition.BOTTOM, backgroundColor: Colors.red);
      }
    });
  }
  
  

}

