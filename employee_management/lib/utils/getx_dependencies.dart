import 'package:employee_management/module/home/controller/HomeController.dart';
import 'package:get/get.dart';

import '../core/networkservice/network_service.dart';
import '../core/repo/repository.dart';
import '../module/auth/signin/controller/LoginController.dart';

///Dependency injections

final kLoginController = Get.put(
    LoginController(repository: Repository(networkService: NetworkService())));

final kHomeController = Get.put(
    HomeController(repository: Repository(networkService: NetworkService())));
