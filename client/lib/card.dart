import 'package:flutter/material.dart';

enum Suit { hearts, diamonds, clubs, spades }

enum Rank { seven, eight, nine, ten, jack, queen, king, ace }

class Card {
  final Suit suit;
  final Rank rank;

  Card({required this.suit, required this.rank});

  @override
  String toString() {
    return '${rankToString(rank)} of ${suitToString(suit)}';
  }
}

Map<String, dynamic> toJson(Card card) {
  return {
    'suit': suitToString(card.suit),
    'rank': rankToString(card.rank),
  };
}

Suit suitFromString(String suit) {
  return Suit.values.firstWhere((s) => s.toString().split('.').last == suit);
}

Rank rankFromString(String rank) {
  return Rank.values.firstWhere((r) => r.toString().split('.').last == rank);
}

String rankToString(Rank rank) {
  switch (rank) {
    case Rank.seven:
      return 'seven';
    case Rank.eight:
      return 'eight';
    case Rank.nine:
      return 'nine';
    case Rank.ten:
      return 'ten';
    case Rank.jack:
      return 'jack';
    case Rank.queen:
      return 'queen';
    case Rank.king:
      return 'king';
    case Rank.ace:
      return 'ace';
    default:
      return rank.toString().split('.').last;
  }
}

String suitToString(Suit suit) {
  return suit.toString().split('.').last;
}

class CardWidget extends StatelessWidget {
  final Card card;

  const CardWidget({super.key, required this.card});

  @override
  Widget build(BuildContext context) {
    String imagePath = getCardImagePath(card);
    double screenWidth = MediaQuery.of(context).size.width;
    double cardWidth;
    double cardHeight;
    if (screenWidth < 750) {
      cardWidth = screenWidth / 8.75;
      cardHeight = cardWidth * 1.65;
    } else {
      cardWidth = screenWidth / 16;
      cardHeight = cardWidth * 1.5;
    }
    return SizedBox(
      width: cardWidth,
      height: cardHeight,
      child: Image.asset(
        imagePath,
        fit: BoxFit.cover,
      ),
    );
  }
}

String getCardImagePath(Card card) {
  return 'assets/${rankToString(card.rank)}_${suitToString(card.suit)}.png';
}
