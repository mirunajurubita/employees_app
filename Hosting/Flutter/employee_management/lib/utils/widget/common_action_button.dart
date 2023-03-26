import 'package:flutter/material.dart';

import '../theme/color_const.dart';

class CommonActionButton extends StatelessWidget {
  const CommonActionButton(
      {Key? key,
      this.showBorder,
      this.showBackgroundColor,
      required this.text,
      required this.onTap,
      this.labelStyle})
      : super(key: key);
  final bool? showBorder;
  final bool? showBackgroundColor;
  final String text;
  final TextStyle? labelStyle;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      child: Container(
        decoration: BoxDecoration(
            color: showBackgroundColor ?? true
                ? MyColors.whiteColor
                : Colors.transparent,
            border: showBorder ?? false ? Border.all(color: Colors.grey) : null,
            borderRadius: BorderRadius.circular(100)),
        padding: const EdgeInsets.fromLTRB(70, 12, 70, 12),
        child: Text(
          text,
          style: labelStyle ??
              TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: MyColors.greenColor),
        ),
      ),
    );
  }
}
