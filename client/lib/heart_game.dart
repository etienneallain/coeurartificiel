import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:coeur_artificiel/card.dart';
import 'package:coeur_artificiel/player.dart';
import 'package:coeur_artificiel/trick.dart';

typedef TrickFinishedCallback = void Function(int winningPlayerIndex);

class HeartsGame {
  final TrickFinishedCallback onTrickFinished;

  List<Player> players = [];
  List<Card> deck = [];
  Map<int, Trick> trickMap = {};
  int turn = 0;
  Trick currentTrick = Trick();
  int currentPlayer;
  List<int> scores = [0, 0, 0, 0];
  List<int> flag = [1, 1, 1, 1];

  HeartsGame(List<int> playerNumbers,
      {required this.currentPlayer, required this.onTrickFinished}) {
    trickMap = {};
    for (var playerNumber in playerNumbers) {
      players.add(Player(number: playerNumber));
    }

    for (var suit in Suit.values) {
      for (var rank in Rank.values) {
        deck.add(Card(suit: suit, rank: rank));
      }
    }
    deck.shuffle();
    for (var player in players) {
      player.hand = deck.sublist(0, 8);
      deck.removeRange(0, 8);
    }
  }

  void update_flag() {
    for (Trick pli in players[currentPlayer].listOfTrick.values) {
      for (Card carte in pli.trick) {
        if (carte.suit == Suit.hearts) {
          for (int i = 0; i < 4; i++) {
            if (i != currentPlayer) {
              flag[i] = -1;
            }
          }
        }
      }
    }
  }

  int check_winner_trick(Trick trick) {
    if (trick.trick.isEmpty) {
      // Aucune carte jouée dans le pli
      return -1;
    }
    Suit leadSuit = trick.trick[0].suit;
    Card winningCard = trick.trick[0];
    int winningPlayerIndex = 0;
    if (currentPlayer == 3) {
      winningPlayerIndex = 0;
    }
    if (currentPlayer == 2) {
      winningPlayerIndex = 3;
    }
    if (currentPlayer == 1) {
      winningPlayerIndex = 2;
    }
    if (currentPlayer == 0) {
      winningPlayerIndex = 1;
    }
    for (int i = 1; i < trick.trick.length; i++) {
      if (currentPlayer == 3) {
        Card currentCard = trick.trick[i];
        if (currentCard.suit == leadSuit &&
            currentCard.rank.index > winningCard.rank.index) {
          winningCard = currentCard;
          winningPlayerIndex = i;
        }
      }
      if (currentPlayer == 2) {
        Card currentCard = trick.trick[i];
        if (currentCard.suit == leadSuit &&
            currentCard.rank.index > winningCard.rank.index) {
          winningCard = currentCard;
          winningPlayerIndex = i - 1;
        }
      }
      if (currentPlayer == 1) {
        Card currentCard = trick.trick[i];
        if (currentCard.suit == leadSuit &&
            currentCard.rank.index > winningCard.rank.index) {
          winningCard = currentCard;
          winningPlayerIndex = (i + 2) % 4;
        }
      }
      if (currentPlayer == 0) {
        Card currentCard = trick.trick[i];
        if (currentCard.suit == leadSuit &&
            currentCard.rank.index > winningCard.rank.index) {
          winningCard = currentCard;
          winningPlayerIndex = (i + 1) % 4;
        }
      }
    }
    return winningPlayerIndex;
  }

  bool end_of_game() {
    if (players[0].hand.isEmpty &&
        players[1].hand.isEmpty &&
        players[2].hand.isEmpty &&
        players[3].hand.isEmpty) {
      return true;
    } else {
      return false;
    }
  }

  Future<void> play_card(Player player, Card card) async {
    if (players[currentPlayer].playCard(card, currentTrick) == true) {
      //players[currentPlayer].playCard(card, currentTrick);
      currentTrick.addCard(card);
    } else {
      return;
    }

    if (turn % 4 == 3) {
      // Tous les joueurs ont joué, évaluer le pli
      currentPlayer = check_winner_trick(currentTrick);

      onTrickFinished(
          currentPlayer); // Appel du callback avec l'index du gagnant
      print('Trick Winner: Player $currentPlayer');
      players[currentPlayer].listOfTrick[trickMap.length] = currentTrick;
      trickMap[trickMap.length] = currentTrick;
      update_flag();
      print(flag);
      await Future.delayed(const Duration(seconds: 1));
      currentTrick = Trick();
      turn = 0;
    } else {
      // Tour suivant
      currentPlayer = (currentPlayer + 1) % 4;
      turn++;
    }
  }

  Future<Card> cardToPlay(Player player) async {
    List<Card> listOfPossibleCards = player.getPossibleCards(currentTrick);
    List<Card> playable_cards;
    if (player.number == 1) {
      playable_cards = players[0].hand + players[2].hand + players[3].hand;
    }
    if (player.number == 2) {
      playable_cards = players[0].hand + players[1].hand + players[3].hand;
    } else {
      playable_cards = players[0].hand + players[1].hand + players[2].hand;
    }
    final response = await http.post(
      Uri.parse('http://127.0.0.1:5000/play_move'),
      body: json.encode({
        'taille': listOfPossibleCards.length,
        'trick_number': trickMap.length,
        'cards_in_hand': player.hand.map((card) => toJson(card)).toList(),
        'card_played_in_trick':
            currentTrick.trick.map((card) => toJson(card)).toList(),
        'playable_cards': playable_cards.map((card) => toJson(card)).toList(),
        'order_of_play': currentTrick.trick.length,
        'trump_color':
            currentTrick.trick.firstOrNull?.suit.toString().split('.').last,
        'flag': flag[player.number],
      }),
      headers: {'Content-Type': 'application/json'},
    );
    if (response.statusCode == 200) {
      /*final int nombreAleatoire =
          int.parse(json.decode(response.body)['nombre_aleatoire']);
      // Utilisez le nombre aléatoire pour choisir la carte appropriée
      return listOfPossibleCards[nombreAleatoire];*/
      final Map<String, dynamic> decodedBody = json.decode(response.body);
      final suitString =
          decodedBody['suit'] as String; // Obtient 'clubs' comme chaîne
      final rankString =
          decodedBody['rank'] as String; // Obtient 'ten' comme chaîne

      // Convertir les chaînes en énumérations
      final Suit suit = suitFromString(suitString);
      final Rank rank = rankFromString(rankString);
      final Card cardToPlay = Card(suit: suit, rank: rank);
      int indice_carte_a_jouer = 0;
      for (int i = 0; i < player.hand.length; i++) {
        if (player.hand[i].suit == cardToPlay.suit &&
            player.hand[i].rank == cardToPlay.rank) {
          indice_carte_a_jouer = i;
        }
      }
      //print(cardToPlay);
      return player.hand[indice_carte_a_jouer];
    } else {
      throw Exception('Erreur lors de la requête au serveur');
    }
  }

  void score() {
    for (int i = 0; i < 4; i++) {
      int nbHearts = 0;
      int res = 0;
      for (Trick trick in players[i].listOfTrick.values) {
        for (Card card in trick.trick) {
          if (suitToString(card.suit) == "hearts") {
            nbHearts++;
          }
        }
      }
      res -= nbHearts * 5;
      if (nbHearts == 8) {
        res += 80;
      }
      scores[i] = res;
    }
  }
}
