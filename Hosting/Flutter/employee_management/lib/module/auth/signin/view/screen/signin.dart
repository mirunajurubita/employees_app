import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';

import '../../../../../utils/getx_dependencies.dart';
import '../../../../../utils/stringConst/ui_string_const.dart';
import '../../../../../utils/theme/color_const.dart';
import '../../../../../utils/widget/common_action_button.dart';
import '../../../../../utils/widget/common_text_field.dart';
import '../../../../../utils/widget/sign_up_field_title.dart';



class SignIn extends StatefulWidget {
  const SignIn({Key? key}) : super(key: key);

  @override
  State<SignIn> createState() => _SignInState();
}

  

class _SignInState extends State<SignIn> {
  String username = '';
  String password = '';
  bool obscure = true;


  SnackbarController? validateEmail(String? value, String? password) {
    String pattern =
        r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]"
        r"{0,253}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]"
        r"{0,253}[a-zA-Z0-9])?)*$";

    ///This validation will use in the case of email (currently we are using username)
    // if (value == null || value.isEmpty || !regex.hasMatch(value)) {
    if (value == null || value.isEmpty) {
      ///Snack bar alert if username is missed
      return Get.snackbar('Error', 'Please enter the valid username address',
          backgroundColor: Colors.red);
    } else if (password == null || password.isEmpty) {
      ///Snack bar alert if password is missed
      return Get.snackbar('Error', 'Please enter the valid password',
          backgroundColor: Colors.red);
    }
    
    ///Call login function, which is in Login controller with 3 params
    return kLoginController.singIn(context, value, password);
  }
  
  @override
  Widget build(BuildContext context) {
    
    return Scaffold(

      body: Stack(
        children: [
          SafeArea(
            child: Form(
              autovalidateMode: AutovalidateMode.always,
              child: Column(
                children: [
                  Expanded(
                    child: SingleChildScrollView(
                      child: Container(
                        color: MyColors.whiteColor,

                        ///Defining full height and width of the screen
                        height: MediaQuery.of(context).size.height,
                        width: MediaQuery.of(context).size.width,
                        child: Column(
                          children: [
                            SizedBox(height: 164.h),
                            // const Text("Employee Management"),
                            SizedBox(height: 21.h),

                            ///Custom SignUpFieldsTitle widget (lib->utils->widget)
                            SignUpFieldsTitle(
                              text: UiStringConst
                                  .loginScreenUiString.LOGIN_SUGGESTION,
                            ),
                            SizedBox(height: 120.h),

                            ///Custom CommonTextField widget (lib->utils->widget)
                            CommonTextField(
                              hintText: UiStringConst
                                  .loginScreenUiString.USERNAME_HINT,
                              textInputAction: TextInputAction.next,
                              onChanged: (newValue) {
                                username = newValue;
                              },
                              contentPadding:
                                  const EdgeInsets.fromLTRB(50, 10, 0, 16),
                              suffix: const Text(""),
                            ),
                            SizedBox(height: 21.h),

                            ///Custom CommonTextField widget (lib->utils->widget)
                            CommonTextField(
                              hintText: UiStringConst
                                  .loginScreenUiString.PASSWORD_HINT,
                              textInputAction: TextInputAction.done,
                              obscureText: obscure,
                              onChanged: (newValue) {
                                password = newValue;
                              },
                              contentPadding:
                                  const EdgeInsets.fromLTRB(50, 10, 0, 16),
                              suffix: obscure
                                  ? GestureDetector(
                                      onTap: () {
                                        setState(() {
                                          obscure = false;
                                        });
                                      },
                                      child: const Icon(
                                          Icons.remove_red_eye_outlined,
                                          color: Colors.grey,
                                          size: 26),
                                    )
                                  : GestureDetector(
                                      onTap: () {
                                        setState(() {
                                          obscure = true;
                                        });
                                      },
                                      child: Image.asset(
                                        "assets/icons/hide.png",
                                        color: Colors.grey,
                                      ),
                                    ),
                            ),
                            SizedBox(height: 10.h),
                            Row(
                              children: [
                                SizedBox(width: 53.w),
                                const Spacer(),
                                SizedBox(width: 53.w),
                              ],
                            ),
                            SizedBox(height: 120.h),

                            /// Using Obx to update state
                            Obx(() {
                              return kLoginController.isLoading.value
                                  ? CircularProgressIndicator(
                                      color: MyColors.greenColor,
                                    )
                                  : CommonActionButton(
                                      text: 'Login',
                                      showBorder: true,
                                      onTap: () {
                                        kLoginController.singIn(
                                            context, username, password);
                                      },
                                    );
                            }),
                            SizedBox(
                              height: 50.h,
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
