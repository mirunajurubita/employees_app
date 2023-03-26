import 'package:flutter/material.dart';

class MyIconButton extends StatelessWidget {
  const MyIconButton(
      {Key? key,
      required this.onPressed,
      required this.icon,
      this.padding,
      this.removePadding})
      : super(key: key);
  final VoidCallback onPressed;
  final Widget icon;
  final EdgeInsetsGeometry? padding;
  final bool? removePadding;
  @override
  Widget build(BuildContext context) {
    return IconButton(
      splashRadius: 16,
      constraints: removePadding ?? false ? BoxConstraints() : null,
      padding: padding ?? const EdgeInsets.all(8),
      onPressed: onPressed,
      icon: icon,
    );
  }
}
