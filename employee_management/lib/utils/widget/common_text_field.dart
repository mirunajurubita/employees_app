import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

import '../theme/color_const.dart';

class CommonTextField extends StatelessWidget {
  const CommonTextField(
      {Key? key,
      required this.hintText,
      this.prefix,
      this.suffix,
      required this.textInputAction,
      this.keyboardType,
      this.obscureText,
      this.initialValue,
      required this.onChanged,
      this.margin,
      this.textAlign,
      this.validator,
      this.inputFormatters,
      this.contentPadding})
      : super(key: key);
  final String hintText;
  final Widget? prefix;
  final Widget? suffix;
  final String? initialValue;
  final void Function(String) onChanged;
  final TextInputAction? textInputAction;
  final TextInputType? keyboardType;
  final bool? obscureText;
  final EdgeInsetsGeometry? margin;
  final TextAlign? textAlign;
  final String? Function(String?)? validator;
  final List<TextInputFormatter>? inputFormatters;
  final EdgeInsets? contentPadding;

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: margin ?? EdgeInsets.symmetric(horizontal: 40.w),
      decoration: BoxDecoration(
          color: MyColors.whiteColor,
          borderRadius: BorderRadius.circular(100),
          border: Border.all(color: Colors.grey)),
      child: SizedBox(
        height: 50,
        child: TextFormField(
          initialValue: initialValue,
          onChanged: onChanged,
          textAlign: textAlign ?? TextAlign.center,
          cursorColor: Colors.grey,
          textInputAction: textInputAction,
          keyboardType: keyboardType,
          obscureText: obscureText ?? false,
          validator: validator,
          inputFormatters: inputFormatters,
          style: TextStyle(color: Colors.grey),
          decoration: InputDecoration(
            prefixIcon: prefix,
            suffixIcon: suffix,
            contentPadding:
                contentPadding ?? const EdgeInsets.fromLTRB(16, 16, 16, 16),
            hintText: hintText,
            hintStyle: TextStyle(color: Colors.grey),
            isDense: true,
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(100),
              borderSide: const BorderSide(color: Colors.grey),
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(100),
              borderSide: const BorderSide(color: Colors.grey),
            ),
          ),
        ),
      ),
    );
  }
}
