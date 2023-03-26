
import 'package:employee_management/utils/getx_dependencies.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';
import "package:firebase_messaging/firebase_messaging.dart";
import 'package:firebase_core/firebase_core.dart';

import '././fcm.dart';
import '../../../../utils/overlay_progress_bar/overlay_progress_bar.dart';
import '../../../../utils/theme/color_const.dart';
import '../../../auth/signin/view/widget/auth_app_bar.dart';


class Home extends StatefulWidget {
  const Home({Key? key}) : super(key: key);
  
  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  ///Variable declare and initialize
  final _scrollController = ScrollController();
  bool isLoading = false;
  var outputFormat = DateFormat('dd/MM/yyyy HH:mm');
  RxString markedSelectedIndex = '-1'.obs;
  ProgressBar? _sendingMsgProgressBar;
  





  //ca idee am pus aici ASYNC 
  @override
  void  initState() {
    super.initState();
    initFcm();


  
    ///call this function to get the list of dashboard items
    kHomeController.getDashboardItem(context);
    _sendingMsgProgressBar = ProgressBar();
  }

  ///Logout function
  logout(context) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();

    if (prefs.getString("accessToken") != null) {
      prefs.clear();
      Navigator.of(context)
          .pushNamedAndRemoveUntil('/signIn', (Route<dynamic> route) => false);
    }
  }


    
  Future<bool> showPopup(context) async {
    
    return await showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: Text(
              "Are you sure you want to logout?",
              style: TextStyle(color: MyColors.backgroundGre1, fontSize: 16),
            ),
            content: Container(
              width: MediaQuery.of(context).size.width,
              height: 100,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 20),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      GestureDetector(
                        onTap: () {
                          logout(context);
                          // Navigator.of(context).pop();
                        },
                        child: Container(
                          height: 45,
                          width: 100,
                          alignment: Alignment.center,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(10),
                            color: MyColors.greenColor,
                          ),
                          child: const Text(
                            "Yes",
                            style: TextStyle(color: Colors.white),
                          ),
                        ),
                      ),
                      SizedBox(width: 15),
                      GestureDetector(
                        onTap: () {
                          Navigator.of(context).pop();
                        },
                        child: Container(
                          height: 45,
                          width: 100,
                          alignment: Alignment.center,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(10),
                            color: MyColors.greenColor,
                          ),
                          child: const Text("No",
                              style: TextStyle(color: Colors.white)),
                        ),
                      )
                    ],
                  )
                ],
              ),
            ),
          );
        });
  }

  void showSendingProgressBar() {
    _sendingMsgProgressBar!.show(context);
  }

  void hideSendingProgressBar() {
    _sendingMsgProgressBar!.hide();
  }

  @override
  void dispose() {
    _sendingMsgProgressBar!.hide();
    super.dispose();
  }
  final GlobalKey<RefreshIndicatorState> _refreshIndicatorKey =
      GlobalKey<RefreshIndicatorState>();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child:RefreshIndicator(
            key: _refreshIndicatorKey,
            
            color: Colors.white,
            backgroundColor: Colors.blue,
            strokeWidth: 4.0,
            onRefresh: () async {
          // Replace this delay with the code to be executed during refresh
          // and return a Future when code finishs execution.
          return kHomeController.getDashboardItem(context);
        },
            triggerMode: RefreshIndicatorTriggerMode.onEdge,

    
        child: SizedBox(
          height: MediaQuery.of(context).size.height,
          width: MediaQuery.of(context).size.width,

          child: Column(
            children: [
              AuthAppBar(
                label: "Employee Management",
                titleTextStyle:
                    TextStyle(color: MyColors.greenColor, fontSize: 20),
                showBackButton: false,
                showLogoutButton: true,
                onTapLogout: () {
                  showPopup(context);
                },
              ),
              Expanded(
                child: SizedBox(
                  width: MediaQuery.of(context).size.width,
                  child: SingleChildScrollView(
                    physics: const ScrollPhysics(),
                    child: Column(
                      mainAxisSize: MainAxisSize.max,
                      children: [
                        SizedBox(
                          height: 20.h,
                        ),

                        ///Update the state
                        Obx(() {
                          return kHomeController.isLoading.value
                              ? CircularProgressIndicator(
                                  color: MyColors.greenColor,
                                )
                              : kHomeController.getDashboardResponse.isEmpty
                                  ? const Center(
                                      child: Text("Nothing Found"),
                                    )
                                  : ListView.builder(
                                      controller: _scrollController,
                                      shrinkWrap: true,
                                      itemCount: kHomeController
                                          .getDashboardResponse.length,
                                      itemBuilder: (context, index) {
                                        ///Getting values from array
                                        print(kHomeController
                                          .getDashboardResponse.length);
                                        final headline = kHomeController
                                                .getDashboardResponse[index]
                                            ['headline'];
                                        final status = kHomeController
                                                .getDashboardResponse[index]
                                            ['is_active'];
                                        final body = kHomeController
                                                .getDashboardResponse[index]
                                            ['body'];
                                        final assigned_at = kHomeController
                                                .getDashboardResponse[index]
                                            ['assigned_at'];
                                        final deadline = kHomeController
                                                .getDashboardResponse[index]
                                            ['deadline'];
                                        final id = kHomeController
                                            .getDashboardResponse[index]['id'];
                                        
                                        return Padding(
                                          padding: const EdgeInsets.fromLTRB(
                                              20, 5, 20, 10),
                                          child: Column(
                                            children: [
                                              Card(
                                                color: MyColors.greenColor,
                                                margin: EdgeInsets.zero,
                                                elevation: 0,
                                                shape: RoundedRectangleBorder(
                                                    borderRadius:
                                                        BorderRadius.circular(
                                                            20)),
                                                child: Container(
                                                    width:
                                                        MediaQuery.of(context)
                                                            .size
                                                            .width,
                                                    margin:
                                                        const EdgeInsets.only(
                                                            bottom: 20),
                                                    child: Column(
                                                      children: [
                                                        SizedBox(
                                                            width:
                                                                MediaQuery.of(
                                                                        context)
                                                                    .size
                                                                    .width,
                                                            child: Container(
                                                              padding:
                                                                  const EdgeInsets
                                                                          .fromLTRB(
                                                                      20,
                                                                      20,
                                                                      0,
                                                                      5),
                                                              child: Text(
                                                                headline,
                                                                textAlign:
                                                                    TextAlign
                                                                        .start,
                                                                overflow:
                                                                    TextOverflow
                                                                        .ellipsis,
                                                                style: GoogleFonts.poppins(
                                                                    color: MyColors
                                                                        .whiteColor,
                                                                    fontSize:
                                                                        19,
                                                                    fontWeight:
                                                                        FontWeight
                                                                            .normal),
                                                              ),
                                                            )),
                                                        
                                                        SizedBox(
                                                            width:
                                                                MediaQuery.of(
                                                                        context)
                                                                    .size
                                                                    .width,
                                                            child: Container(
                                                              padding:
                                                                  const EdgeInsets
                                                                          .fromLTRB(
                                                                      20,
                                                                      0,
                                                                      0,
                                                                      10),
                                                              child: Text(
                                                                body,
                                                                textAlign:
                                                                    TextAlign
                                                                        .start,
                                                                overflow:
                                                                    TextOverflow
                                                                        .ellipsis,
                                                                style: GoogleFonts.poppins(
                                                                    color: MyColors
                                                                        .whiteColor,
                                                                    fontSize:
                                                                        17,
                                                                    fontWeight:
                                                                        FontWeight
                                                                            .normal),
                                                              ),
                                                            )),
                                                      
                                                        if (status == 1)
                                                        Container(
                                                            width:
                                                                MediaQuery.of(
                                                                        context)
                                                                    .size
                                                                    .width,
                                                            child: Column(
                                                              children: [
                                                                SizedBox(
                                                            width:
                                                                MediaQuery.of(
                                                                        context)
                                                                    .size
                                                                    .width,
                                                            child: Container(
                                                              padding:
                                                                  const EdgeInsets
                                                                          .fromLTRB(
                                                                      20,
                                                                      0,
                                                                      0,
                                                                      2),
                                                              child: Text(
                                                                'This task is active',
                                                                textAlign:
                                                                    TextAlign
                                                                        .start,
                                                                overflow:
                                                                    TextOverflow
                                                                        .ellipsis,
                                                                style: GoogleFonts.poppins(
                                                                    color: MyColors
                                                                        .whiteColor,
                                                                    fontSize:
                                                                        12,
                                                                    fontWeight:
                                                                        FontWeight
                                                                            .normal),
                                                              ),
                                                            )
                                                            ),
                                                                
                                                                Container(
                                                                      margin: const EdgeInsets
                                                                              .only(
                                                                          left:
                                                                              20),
                                                                      child:Row(
                                                                        children: [
                                                                          Container(
                                                                      margin: const EdgeInsets
                                                                              .only(
                                                                          left:
                                                                              0),
                                                                      child:
                                                                          ElevatedButton(
                                                                        onPressed:
                                                                            () {
                                                                          kHomeController.startPause(
                                                                              context,
                                                                              id);
                                                                          setState(
                                                                              () {
                                                                            kHomeController.sendingMsgProgressBar!.show(context);
                                                                          });
                                                                        },
                                                                        child:
                                                                            Text(
                                                                          "Start pause ",
                                                                          style:
                                                                              TextStyle(color: MyColors.greenColor),
                                                                        ),
                                                                      ),
                                                                    ),
                                                                    Container (margin: const EdgeInsets
                                                                              .only(
                                                                          left:
                                                                              11),
                                                                      child: ElevatedButton(
                                                                        onPressed:
                                                                            () {
                                                                          kHomeController.stopPause(
                                                                              context,
                                                                              id);
                                                                          setState(
                                                                              () {
                                                                            kHomeController.sendingMsgProgressBar!.show(context);
                                                                          });
                                                                        },
                                                                        child:
                                                                            Text(
                                                                          "Stop pause",
                                                                          style:
                                                                              TextStyle(color: MyColors.greenColor),
                                                                        ),
                                                                      ),     
                                                                      )
                                                                    ],
                                                                      )
                                                                          
                                                                    ),
                                                              ],
                                                            )
                                                             ),
                                                            
                                                          
                                                        
                                                        Container(
                                                          margin:
                                                              const EdgeInsets
                                                                      .only(
                                                                  left: 20,
                                                                  bottom: 10),
                                                          child: Row(
                                                            children: [
                                                              Container(
                                                                child: Text(
                                                                  ///Formatting the date
                                                                  outputFormat.format(
                                                                      DateTime.parse(
                                                                          assigned_at)),
                                                                  style: GoogleFonts.poppins(
                                                                      color: MyColors
                                                                          .whiteColor,
                                                                      fontSize:
                                                                          13,
                                                                      fontWeight:
                                                                          FontWeight
                                                                              .w600),
                                                                ),
                                                              ),
                                                              Container(
                                                                margin: const EdgeInsets
                                                                        .symmetric(
                                                                    horizontal:
                                                                        5),
                                                                child:
                                                                    const Text(
                                                                        '-'),
                                                              ),
                                                              Container(
                                                                child: Text(
                                                                  ///Formatting the date
                                                                  outputFormat.format(
                                                                      DateTime.parse(
                                                                          deadline)),
                                                                  // 'abc',
                                                                  style: GoogleFonts.poppins(
                                                                      color: MyColors
                                                                          .whiteColor,
                                                                      fontSize:
                                                                          13,
                                                                      fontWeight:
                                                                          FontWeight
                                                                              .w600),
                                                                ),
                                                              ),
                                                            ],
                                                          ),
                                                        ),
                                                        
                                                        Container(
                                                            width:
                                                                MediaQuery.of(
                                                                        context)
                                                                    .size
                                                                    .width,
                                                            child: Column(
                                                              children: [
                                                                Row(
                                                                  children: [
                                                                    if (status == 0)
                                                                    Container(
                                                                      margin: const EdgeInsets
                                                                              .only(
                                                                          left:
                                                                              20),
                                                                      
                                                                      child:
                                                                      
                                                                          ElevatedButton(
                                                                            
                                                                        onPressed:
                                                                            () {
                                                                          kHomeController.startTask(
                                                                              context,
                                                                              id);
                                                                          setState(
                                                                              () {
                                                                            kHomeController.sendingMsgProgressBar!.show(context);
                                                                          });
                                                                        },
                                                                        child:
                                                                            Text(
                                                                          "Start task ",
                                                                          style:
                                                                              TextStyle(color: MyColors.greenColor),
                                                                        ),
                                                                      ),
                                                                    ),
                                                                    Container(
                                                                      margin: const EdgeInsets
                                                                              .only(
                                                                          left:
                                                                              20),
                                                                      child:
                                                                          ElevatedButton(
                                                                        onPressed:
                                                                            () {
                                                                          kHomeController.markAsCompleted(
                                                                              context,
                                                                              id);
                                                                          setState(
                                                                              () {
                                                                            kHomeController.sendingMsgProgressBar!.show(context);
                                                                          });
                                                                        },
                                                                        child:
                                                                            Text(
                                                                          "Close task",
                                                                          style:
                                                                              TextStyle(color: MyColors.greenColor),
                                                                        ),
                                                                      ),
                                                                    ),
                                                                  ],
                                                                ),
                                                                
                                                              ],
                                                            )
                                                            ),
                                                      ],
                                                    )),
                                              ),
                                            ],
                                          ),
                                        );
                                      },
                                    );
                        })
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
        
      ),
      
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          // Show refresh indicator programmatically on button tap.
          _refreshIndicatorKey.currentState?.show();
        },
        icon: const Icon(Icons.refresh),
        label: const Text('Refresh Button'),
        backgroundColor: Color.fromARGB(255, 88, 125, 178),
      )
    );
  }
}

