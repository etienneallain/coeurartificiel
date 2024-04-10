import 'package:coeur_artificiel/card.dart';

class Trick{
  List<Card> trick=[];
  //int currentplayer=0;

  Trick(){
    trick=[];
  }

  bool get isEmpty => trick.isEmpty;
  //int get currentPlayer => currentplayer;

  void addCard(Card card) {
    trick.add(card);
  }

  @override
  String toString() {
    return 'Trick: ${trick.map((card) => card.toString()).toList()}';
  }

}
