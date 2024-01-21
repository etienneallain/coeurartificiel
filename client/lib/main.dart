import 'package:coeur_artificiel/gamepage.dart';
import 'package:coeur_artificiel/settingspage.dart';
import 'package:coeur_artificiel/card.dart' as MyCard;

import 'package:flutter/material.dart';

class CardGameHomePage extends StatefulWidget {
  @override
  _CardGameHomePageState createState() => _CardGameHomePageState();
}

class _CardGameHomePageState extends State<CardGameHomePage> {
  bool showRules = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        fit: StackFit.expand,
        children: <Widget>[
          Image.asset(
            'assets/5120953.jpg',
            fit: BoxFit.cover,
          ),
          if (showRules)
            Stack(
              fit: StackFit.expand,
              children: <Widget>[
                GestureDetector(
                  onTap: () {
                    setState(() {
                      showRules = false;
                    });
                  },
                  child: Image.asset(
                    'assets/5120953.jpg',
                    fit: BoxFit.cover,
                  ),
                ),
                Center(
                  child: Container(
                    width: 0.7 * MediaQuery.of(context).size.width,
                    height: 0.7 * MediaQuery.of(context).size.height,
                    decoration: BoxDecoration(
                      color: Colors.red,
                      borderRadius: BorderRadius.circular(20.0),
                    ),
                    child: Stack(
                      children: <Widget>[
                        Positioned(
                          top: 5,
                          right: 5,
                          child: GestureDetector(
                            onTap: () {
                              setState(() {
                                showRules = false;
                              });
                            },
                            child: Icon(Icons.close),
                          ),
                        ),
                        Column(
                          children: <Widget>[
                            Align(
                              alignment: Alignment.topCenter,
                              child: Text(
                                'Règles du Jeu',
                                style: TextStyle(
                                  fontSize: 20,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                            Expanded(
                              child: SingleChildScrollView(
                                child: Padding(
                                  padding: const EdgeInsets.all(8.0),
                                  child: Text(
                                    'Objectif :\nL\'objectif du jeu est d\'éviter de prendre des cartes de cœur, car elles valent des points négatifs. Le but est d\'avoir le moins de points à la fin de la partie.\n\nMise en place :\nNous disposons d\'un jeu de 32 cartes. Chaque joueur dispose de 8 cartes.\n\nDéroulement du jeu :\nAu premier tour, le meneur (celui qui débute la partie) joue une carte d\'une certaine couleur (carreau, pique, trèfle, coeur). Les autres joueurs doivent suivre la couleur jouée s\'ils le peuvent. Si un joueur ne peut pas suivre la couleur, il peut jouer n\'importe quelle carte. Le joueur qui a joué la carte la plus forte de la couleur demandée par le meneur récupère le pli et commence le pli suivant. À partir du deuxième tour, le joueur qui a récupéré le dernier pli commence le nouveau tour en jouant n\'importe quelle carte.\n\nScores :\nLes cœurs valent -5 points chacun. Mais si on dispose à la fin de la partie tous les coeurs on gagne +40 points au lieu de -40 points.\n\nStratégie :\nIl y a deux stratégies possibles :\nSoit on évite de gagner des plis contenant des cœurs.\nSoit on essaye de remporter tous les plis qui contiennent des cœurs et donc obtenir tous les coeurs du jeu.',
                                    style: TextStyle(fontSize: 16),
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          if (!showRules)
            Positioned(
              top: 20,
              right: 20,
              child: GestureDetector(
                onTap: () {
                  setState(() {
                    showRules = true;
                  });
                },
                child: Image.asset(
                  'assets/regle_flutter.png',
                  width: 50,
                  height: 50,
                ),
              ),
            ),
          if (!showRules)
            Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Image.asset(
                    'assets/image_center-removebg-preview.png',
                    width: 450,
                    height: 450,
                  ),
                  SizedBox(height: 10),
                  GestureDetector(
                    onTap: () {
                      Navigator.pushNamed(context, '/settings');
                    },
                    child: Image.asset(
                      'assets/tap_to_start.png',
                      width: 200,
                      height: 200,
                    ),
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }
}

/*
void simulateHeartsGame() {
  var game = HeartsGame([0, 1, 2, 3], currentPlayer: 0);

  while (!game.end_of_game()) {
    print('\nTurn: ${game.turn + 1}');
    print('Current Player: ${game.currentPlayer}');
    
    // Affiche la main du joueur actuel
    print('Player ${game.currentPlayer} Hand: ${game.players[game.currentPlayer].hand}');

    // Simulation du joueur jouant une carte aléatoire
    MyCard.Card cardPlayed = await game.cardToPlay(game.players[game.currentPlayer]);
    print('Player ${game.currentPlayer} plays: $cardPlayed');

    // Joue la carte simulée
    game.play_card(game.players[game.currentPlayer], cardPlayed);

    // Affiche l'état du pli actuel
    print('Current Trick: ${game.currentTrick.trick}');

    // Affiche le gagnant du pli si tous les joueurs ont joué
  /*  if (game.turn % 4 == 3) {
      int winnerIndex = game.check_winner_trick(game.currentTrick);
      print('Trick Winner: Player $winnerIndex');
    }*/
  }

  // Affiche les plis gagnés par chaque joueur à la fin de la partie
  for (var player in game.players) {
    print('Player ${player.number} Tricks: ${player.listOfTrick}');
    print('Score obtained by the player ${player.number} : ${game.scores[player.number]}');
  }
}
*/
void main() {
  //simulateHeartsGame();
  runApp(MaterialApp(
    debugShowCheckedModeBanner: false,
    home: CardGameHomePage(),
    routes: {
      '/settings': (context) => SettingsPage(),
      '/game': (context) => GamePage(),
    },
  ));
}
