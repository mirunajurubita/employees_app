import '../networkservice/network_service.dart';
import 'package:firebase_messaging/firebase_messaging.dart';

class Repository {
  final NetworkService networkService;

  ///Instance of network class
  Repository({required this.networkService});

  ///SignIn Function
  Future signIn(username, password) async {
    
    final signInData = await networkService.signIn(username, password);

    
    
    if (signInData[0] == true) {
      try {
        return [true, signInData[1]['result']];
      } catch (e) {
        return [false, []];
      }
    }
    return [false, signInData[1]];
  }

  ///GetDashboardItems function
  Future<List> getDashboardItem() async {
    final signUpData = await networkService.getDashboardItems();

    if (signUpData[0] == true) {
      try {
        return [true, signUpData[1]];
      } catch (e) {
        return [false, []];
      }
    }
    return [false, signUpData[1]];
  }

  ///startTask function
  Future startTask(id) async {
    final signInData = await networkService.startTask(id);
    if (signInData[0] == true) {
      try {
        return [true, signInData[1]['result']];
      } catch (e) {
        return [false, []];
      }
    }
    return [false, signInData[1]];
  }

  ///startPause function
  Future startPause(id) async {
    final signInData = await networkService.startPause(id);
    if (signInData[0] == true) {
      try {
        return [true, signInData[1]['result']];
      } catch (e) {
        return [false, []];
      }
    }
    return [false, signInData[1]];
  }
  ///stopPause function
  Future stopPause(id) async {
    final signInData = await networkService.stopPause(id);
    if (signInData[0] == true) {
      try {
        return [true, signInData[1]['result']];
      } catch (e) {
        return [false, []];
      }
    }
    return [false, signInData[1]];
  }




  ///MarkedAsCompleted function
  Future markAsCompleted(id) async {
    final signInData = await networkService.markAsCompleted(id);
    if (signInData[0] == true) {
      try {
        return [true, signInData[1]['result']];
      } catch (e) {
        return [false, []];
      }
    }
    return [false, signInData[1]];
  }
}
