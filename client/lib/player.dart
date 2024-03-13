// player.dart
import 'package:coeur_artificiel/card.dart';
import 'package:coeur_artificiel/trick.dart';

class Player {
  final int number;
  List<Card> hand = [];
  Map<int, Trick> listOfTrick = {};

  Player({required this.number});

  List<Card> getCardsInSuit(Suit suit) {
    return hand.where((card) => card.suit == suit).toList();
  }

  bool moveAllowed(Card playedCard, Trick currentTrick) {
    if (currentTrick.isEmpty) {
      return true;
    }

    Suit leadSuit = currentTrick.trick[0].suit;

    if (playedCard.suit == leadSuit) {
      return true;
    } else {
      List<Card> cardsInLeadSuit = getCardsInSuit(leadSuit);
      if (cardsInLeadSuit.isEmpty) {
        return true;
      } else {
        return false;
      }
    }
  }

  bool playCard(Card card, Trick currentTrick) {
    if (hand.contains(card) && moveAllowed(card, currentTrick)) {
      hand.remove(card);
      return true;
    } else {
      return false;
    }
  }

  List<Card> getPossibleCards(Trick currentTrick) {
    Suit? leadSuit = currentTrick.isEmpty ? null : currentTrick.trick[0].suit;

    if (leadSuit == null) {
      return List.from(hand);
    } else {
      List<Card> cardsInLeadSuit = getCardsInSuit(leadSuit);

      if (cardsInLeadSuit.isNotEmpty) {
        return List.from(cardsInLeadSuit);
      } else {
        return List.from(hand);
      }
    }
  }
}
