// ignore_for_file: must_be_immutable

import 'package:employee_management/utils/theme/color_const.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

import '../../../../../utils/widget/my_icon_button.dart';

class AuthAppBar extends StatelessWidget {
  AuthAppBar(
      {Key? key,
      required this.label,
      this.showBackButton,
      this.showLogoutButton,
      this.titleTextStyle,
      this.onTap,
      this.onTapLogout})
      : super(key: key);
  final String label;
  bool? showBackButton = true;
  bool? showLogoutButton = true;
  final TextStyle? titleTextStyle;
  VoidCallback? onTap;
  VoidCallback? onTapLogout;

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
          border:
              Border(bottom: BorderSide(color: MyColors.greenColor, width: 1))),
      child: Padding(
        padding: EdgeInsets.all(5.h),
        child: Row(
          children: [
            Expanded(
              flex: 2,
              child: Align(
                alignment: Alignment.centerRight,
                child: showBackButton ?? true
                    ? MyIconButton(
                        onPressed: onTap ??
                            () {
                              Navigator.pop(context);
                            },
                        icon: const Icon(
                          Icons.arrow_back_ios,
                          color: Colors.white,
                          size: 16,
                        ),
                      )
                    : const SizedBox(),
              ),
            ),
            Expanded(
              flex: 8,
              child: Center(
                child: Text(
                  label,
                  style: titleTextStyle ??
                      TextStyle(
                          fontSize: 34.sp,
                          fontWeight: FontWeight.bold,
                          color: Colors.white),
                ),
              ),
            ),
            Expanded(
              flex: 2,
              child: Align(
                alignment: Alignment.centerRight,
                child: showLogoutButton ?? true
                    ? MyIconButton(
                        onPressed: onTapLogout!,
                        icon: Icon(
                          Icons.logout,
                          color: MyColors.greenColor,
                          size: 24,
                        ),
                      )
                    : const SizedBox(),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
