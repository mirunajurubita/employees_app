import 'package:employee_management/utils/theme/color_const.dart';
import 'package:flutter/material.dart';

class ProgressBar {
  OverlayEntry? _progressOverlayEntry;

  ///Show overlay progress bar
  void show(BuildContext context) {
    _progressOverlayEntry = _createdProgressEntry(context);
    Overlay.of(context)!.insert(_progressOverlayEntry!);
  }

  ///Hide overlay progress bar
  void hide() {
    if (_progressOverlayEntry != null) {
      _progressOverlayEntry!.remove();
      _progressOverlayEntry = null;
    }
  }

  OverlayEntry _createdProgressEntry(BuildContext context) => OverlayEntry(
      builder: (BuildContext context) => Stack(
            children: <Widget>[
              Container(
                ///Overlay background
                color: Color(0xff97A8C2).withOpacity(0.5),
              ),
              Positioned(
                top: screenHeight(context) / 2,
                left: screenWidth(context) / 2,

                ///Circular progress color
                child: CircularProgressIndicator(color: MyColors.greenColor),
              )
            ],
          ));

  /// Set height of overlay screen
  double screenHeight(BuildContext context) =>
      MediaQuery.of(context).size.height;

  /// Set width of overlay screen
  double screenWidth(BuildContext context) => MediaQuery.of(context).size.width;
}
