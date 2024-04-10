import 'dart:async';
import 'package:coeur_artificiel/player.dart';
import 'package:coeur_artificiel/trick.dart';
import 'package:flutter/material.dart';
import 'package:coeur_artificiel/heart_game.dart';
import 'package:coeur_artificiel/card.dart' as MyCard;
import 'package:coeur_artificiel/settingspage.dart';

class GamePage extends StatefulWidget {
  final int numberOfRoundsEnteredByUser;

  const GamePage({Key? key, required this.numberOfRoundsEnteredByUser})
      : super(key: key);

  @override
  _GamePageState createState() => _GamePageState();
}

class _GamePageState extends State<GamePage> {
  bool _isPlaying = false;
  late HeartsGame game;
  int numberOfRounds = 0;
  List<int> generalScores = [0, 0, 0, 0];
  bool timerExpired = false;
  int number_of_rounds_entered_by_user = 0;
  //_GamePageState() : game = HeartsGame([0, 1, 2, 3], currentPlayer: 0, showTrickWinnerDialog);
  @override
  void initState() {
    super.initState();
    // Accédez au membre 'widget' dans initState
    number_of_rounds_entered_by_user = widget.numberOfRoundsEnteredByUser;
    game = HeartsGame(
      [0, 1, 2, 3],
      currentPlayer: 0,
      onTrickFinished: showTrickWinnerDialog, // Utilisez le callback ici.
    );
  }

  void showTrickWinnerDialog(int winningPlayerIndex) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Pli terminé'),
          content:
              Text('Le joueur numéro $winningPlayerIndex a remporté le pli.'),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop(); // Ferme le dialogue
                // Vous pouvez ici gérer le passage au pli suivant si nécessaire
              },
              child: const Text('Compris'),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    for (var player in game.players) {
      print('${player.number} hand: ${player.hand}');
    }
    double screenwidth = MediaQuery.of(context).size.width;
    double taille;
    if (screenwidth < 750) {
      taille = 40.0;
    } else {
      taille = 80.0;
    }
    return Scaffold(
      appBar: AppBar(
        title: const Text('Hearts Game'),
        backgroundColor: Colors.red[700],
        centerTitle: true,
      ),
      body: Container(
        decoration: const BoxDecoration(
          image: DecorationImage(
            image: AssetImage('assets/5120953.jpg'),
            fit: BoxFit.cover,
          ),
        ),
        child: Stack(
          children: [
            //timerDisplay(game, context),
            _buildPlayerHand1(game.players[1], context),
            _buildPlayerHand2(game.players[2], context),
            _buildPlayerHand3(game.players[3], context),
            Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  // Joueur 1
                  _buildPlayerHand0(game.players[0]),
                ],
              ),
            ),
            _buildCurrentTrick(game.currentTrick),
            TrickButton(playerNumber: 0, game: game),
            TrickButton(playerNumber: 1, game: game),
            TrickButton(playerNumber: 2, game: game),
            TrickButton(playerNumber: 3, game: game),
            PlayerInfoWidget(playerIndex: 0, scores: generalScores),
            PlayerAvatar(
              playerName: 'You',
              imagePath: 'assets/humain.png',
              playerIndex: 0,
              size: taille,
            ),
            PlayerAvatar(
              playerName: 'IA 1',
              imagePath: 'assets/robotAvatar.png',
              playerIndex: 1,
              size: taille,
            ),
            PlayerAvatar(
              playerName: 'IA 2',
              imagePath: 'assets/robotAvatar.png',
              playerIndex: 2,
              size: taille,
            ),
            PlayerAvatar(
              playerName: 'IA 3',
              imagePath: 'assets/robotAvatar.png',
              playerIndex: 3,
              size: taille,
            ),
          ],
        ),
      ),
    );
  }

  Widget timerDisplay(HeartsGame game, BuildContext context) {
    if (game.currentPlayer == 0) {
      return Positioned(
          top: ((MediaQuery.of(context).size.height - 50) / 4) * 2.9,
          left: (MediaQuery.of(context).size.width / 4) * 2.5,
          child: TimerWidget(
              initialSeconds: 10,
              onTimeout: () async {
                timerExpired = true;
                Player currentPlayer = game.players[game.currentPlayer];
                MyCard.Card cardToPlay = await game.cardToPlay(currentPlayer);
                game.play_card(currentPlayer, cardToPlay);
                timerExpired = false;
                _playRound();
              },
              game: game));
    }
    if (game.currentPlayer == 1) {
      return Positioned(
          top: ((MediaQuery.of(context).size.height - 100) / 2) * 0.75,
          left: (MediaQuery.of(context).size.width / 4) * 2.8,
          child: TimerWidget(initialSeconds: 10, onTimeout: () {}, game: game));
    }
    if (game.currentPlayer == 2) {
      return Positioned(
          top: ((MediaQuery.of(context).size.height - 100) / 4) * 0.5,
          left: (MediaQuery.of(context).size.width / 4) * 1.25,
          child: TimerWidget(initialSeconds: 10, onTimeout: () {}, game: game));
    }
    return Positioned(
        top: ((MediaQuery.of(context).size.height - 100) / 4) * 1.55,
        left: (MediaQuery.of(context).size.width / 4) * 0.8,
        child: TimerWidget(initialSeconds: 10, onTimeout: () {}, game: game));
  }

  Widget _buildPlayerHand0(Player player) {
    double screenwidth = MediaQuery.of(context).size.width;
    double largeur_bordure;
    if (screenwidth < 750) {
      largeur_bordure = 2;
    } else {
      largeur_bordure = 4;
    }
    if (game.currentPlayer == 0) {
      return SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Center(
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              for (int index = 0; index < player.hand.length; index++)
                GestureDetector(
                  onTap: () async {
                    if (timerExpired || _isPlaying) {
                      return;
                    }
                    final MyCard.Card touchedCard = player.hand[index];
                    if (player.moveAllowed(touchedCard, game.currentTrick)) {
                      game.play_card(player, touchedCard);
                    }
                    setState(() {}); // Met à jour l'interface utilisateur
                    await Future.delayed(const Duration(seconds: 3));
                    if (!_isPlaying) {
                      _isPlaying = true;
                      await _playRound();
                      _isPlaying = false;
                    }
                  },
                  child: Container(
                    decoration: BoxDecoration(
                      border: Border.all(
                        color: player.moveAllowed(
                                player.hand[index], game.currentTrick)
                            ? const Color.fromARGB(255, 59, 235, 65)
                            : Colors.red,
                        width: largeur_bordure,
                      ),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: MyCard.CardWidget(card: player.hand[index]),
                  ),
                ),
            ],
          ),
        ),
      );
    } else {
      return SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Center(
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              for (int index = 0; index < player.hand.length; index++)
                MyCard.CardWidget(card: player.hand[index]),
            ],
          ),
        ),
      );
    }
  }

  Future<void> _showEndGameDialog() async {
    return showDialog<void>(
      context: context,
      barrierDismissible:
          false, // L'utilisateur doit appuyer sur le bouton pour fermer le dialog
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Fin de la partie'),
          content: SingleChildScrollView(
            child: ListBody(
              children: <Widget>[
                Text('Les scores finaux sont :'),
                for (int i = 0; i < game.players.length; i++)
                  Text('Joueur ${i}: ${generalScores[i]} points'),
              ],
            ),
          ),
          actions: <Widget>[
            TextButton(
              child: const Text('Retour au Menu'),
              onPressed: () {
                Navigator.of(context).pop(); // Ferme le dialog
                Navigator.of(context).pushReplacement(
                  MaterialPageRoute(builder: (context) => const SettingsPage()),
                );
              },
            ),
          ],
        );
      },
    );
  }

  Future<void> _playRound() async {
    if (game.end_of_game()) {
      game.score();
      print(game.scores);
      for (int i = 0; i < 4; i++) {
        generalScores[i] += game.scores[i];
      }
      print(generalScores);
      numberOfRounds++;
      if (numberOfRounds == number_of_rounds_entered_by_user) {
        await _showEndGameDialog();
      } else {
        game = HeartsGame([0, 1, 2, 3],
            currentPlayer: 0, onTrickFinished: showTrickWinnerDialog);
      }
    }
    Player currentPlayer = game.players[game.currentPlayer];
    if (game.currentPlayer == 0) {
      setState(() {});
    } else {
      MyCard.Card cardToPlay = await game.cardToPlay(currentPlayer);
      game.play_card(currentPlayer, cardToPlay);
      setState(() {});
      await Future.delayed(const Duration(seconds: 3));
      await _playRound();
    }
  }

  Widget _buildPlayerHand1(Player player, BuildContext context) {
    int handlength = player.hand.length;
    if (handlength == 0) {
      return Container(
        width: 100.0,
        height: 100.0,
        color: Colors.transparent,
      );
    }
    double screenwidth = MediaQuery.of(context).size.width;
    double targetImageWidth;
    double targetImageHeigth;
    double right_position;
    if (screenwidth < 750) {
      right_position = 0;
      targetImageWidth = 60;
      targetImageHeigth = 60;
    } else {
      right_position = 0;
      targetImageWidth = 130;
      targetImageHeigth = 130;
    }
    return Positioned(
      top: 0,
      right: right_position,
      bottom: 0,
      child: Image.asset(
        "assets/listecartedos_${handlength}_1.png",
        width: targetImageWidth,
        height: targetImageHeigth,
      ),
    );
  }

  Widget _buildPlayerHand2(Player player, BuildContext context) {
    int handlength = player.hand.length;
    if (handlength == 0) {
      return Container(
        width: 100.0,
        height: 100.0,
        color: Colors.transparent,
      );
    }

    double screenwidth = MediaQuery.of(context).size.width;
    double targetImageWidth;
    double targetImageHeigth;
    double top_position;
    if (screenwidth < 750) {
      top_position = -30;
      targetImageWidth = 130;
      targetImageHeigth = 130;
    } else {
      top_position = -100;
      targetImageWidth = 350;
      targetImageHeigth = 350;
    }

    return Positioned(
      top: top_position,
      right: 0,
      left: 0,
      child: Align(
        alignment: Alignment.center,
        child: Image.asset(
          'assets/listecartedos_${handlength}_2.png',
          width: targetImageWidth,
          height: targetImageHeigth,
        ),
      ),
    );
  }

  Widget _buildPlayerHand3(Player player, BuildContext context) {
    int handlength = player.hand.length;
    if (handlength == 0) {
      return Container(
        width: 100.0,
        height: 100.0,
        color: Colors.transparent,
      );
    }
    double screenwidth = MediaQuery.of(context).size.width;
    double targetImageWidth;
    double targetImageHeigth;
    double left_position;
    if (screenwidth < 750) {
      left_position = -10;
      targetImageWidth = 70;
      targetImageHeigth = 70;
    } else {
      left_position = -10;
      targetImageWidth = 160;
      targetImageHeigth = 160;
    }
    return Positioned(
      top: 0,
      left: left_position,
      bottom: 0,
      child: Image.asset(
        "assets/listecartedos_${handlength}_3.png",
        width: targetImageWidth,
        height: targetImageHeigth,
      ),
    );
  }

  Widget _buildCurrentTrick(Trick trick) {
    double screenwidth = MediaQuery.of(context).size.width;
    if (screenwidth < 750) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            for (var card in trick.trick) MyCard.CardWidget(card: card),
          ],
        ),
      );
    } else {
      return Center(
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            for (var card in trick.trick) MyCard.CardWidget(card: card),
          ],
        ),
      );
    }
  }
}

class TimerWidget extends StatefulWidget {
  final int initialSeconds;
  final Function() onTimeout;
  final HeartsGame game;

  const TimerWidget({
    super.key,
    required this.initialSeconds,
    required this.onTimeout,
    required this.game,
  });

  @override
  _TimerWidgetState createState() => _TimerWidgetState();
}

class _TimerWidgetState extends State<TimerWidget> {
  late int secondsRemaining;
  late Timer _timer;
  late int currentPlayer;

  @override
  void initState() {
    super.initState();
    secondsRemaining = widget.initialSeconds;
    currentPlayer = widget.game.currentPlayer;
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (secondsRemaining > 0) {
        setState(() {
          secondsRemaining--;
        });
      } else {
        //_timer.cancel();
        widget.onTimeout();
      }
    });
  }

  @override
  void didUpdateWidget(covariant TimerWidget oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.game.currentPlayer != currentPlayer) {
      currentPlayer = widget.game.currentPlayer;
      secondsRemaining = widget.initialSeconds;
    }
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Container(
        width: 35,
        height: 35,
        decoration: const BoxDecoration(
          shape: BoxShape.circle,
          color: Colors.red,
        ),
        child: Center(
          child: Text(
            '$secondsRemaining',
            style: const TextStyle(
              fontSize: 24,
              color: Colors.white,
            ),
          ),
        ),
      ),
    );
  }
}

class TrickButton extends StatelessWidget {
  final int playerNumber;
  final HeartsGame game;

  const TrickButton(
      {super.key, required this.playerNumber, required this.game});

  @override
  Widget build(BuildContext context) {
    Map<int, Trick> listOfTrick = game.players[playerNumber].listOfTrick;
    double screenwidth = MediaQuery.of(context).size.width;
    double button_width;
    double button_height;
    double top_player_0;
    double top_player_1;
    double top_player_2;
    double top_player_3;
    double left_player_0;
    double left_player_1;
    double left_player_2;
    double left_player_3;
    if (screenwidth < 750) {
      button_width = 45;
      button_height = 25;
      top_player_0 = (MediaQuery.of(context).size.height / 3.9) * 2.7;
      top_player_1 = (MediaQuery.of(context).size.height / 3.9) * 2.0;
      top_player_2 = (MediaQuery.of(context).size.height / 4.4) * 1.0;
      top_player_3 = (MediaQuery.of(context).size.height / 3.9) * 2.0;
      left_player_0 = (MediaQuery.of(context).size.width / 4.8) * 2.15;
      left_player_1 = (MediaQuery.of(context).size.width / 4.4) * 3.05;
      left_player_2 = (MediaQuery.of(context).size.width / 4.8) * 2.15;
      left_player_3 = (MediaQuery.of(context).size.width / 9) * 2.0;
    } else {
      button_width = 75;
      button_height = 40;
      top_player_0 = (MediaQuery.of(context).size.height / 3.9) * 2.6;
      top_player_1 = (MediaQuery.of(context).size.height / 3.9) * 1.8;
      top_player_2 = (MediaQuery.of(context).size.height / 4.4) * 1.1;
      top_player_3 = (MediaQuery.of(context).size.height / 3.9) * 1.8;
      left_player_0 = (MediaQuery.of(context).size.width / 4.8) * 1.9;
      left_player_1 = (MediaQuery.of(context).size.width / 4.4) * 3.4;
      left_player_2 = (MediaQuery.of(context).size.width / 4.8) * 2.6;
      left_player_3 = (MediaQuery.of(context).size.width / 9) * 1.7;
    }

    return Positioned(
      top: playerNumber == 0
          ? top_player_0
          : playerNumber == 1
              ? top_player_1
              : playerNumber == 2
                  ? top_player_2
                  : top_player_3,
      left: playerNumber == 0
          ? left_player_0
          : playerNumber == 1
              ? left_player_1
              : playerNumber == 2
                  ? left_player_2
                  : left_player_3,
      child: InkWell(
        onTap: () {
          showDialog(
            context: context,
            builder: (BuildContext context) {
              return AlertDialog(
                title: Text(
                  'Pli gagné par Joueur $playerNumber',
                  textAlign: TextAlign.center,
                ),
                backgroundColor: Colors.green[900],
                content: listOfTrick.isNotEmpty
                    ? Column(
                        children: [
                          for (var trick in listOfTrick.values)
                            Row(
                              children: [
                                for (var card in trick.trick)
                                  MyCard.CardWidget(card: card),
                              ],
                            ),
                        ],
                      )
                    : const Text('Aucun pli gagné pour ce joueur'),
                actions: [
                  TextButton(
                    onPressed: () {
                      Navigator.of(context).pop();
                    },
                    child: const Text('Fermer',
                        style: TextStyle(color: Colors.red)),
                  ),
                ],
              );
            },
          );
        },
        child: Container(
          width: button_width,
          height: button_height,
          decoration: BoxDecoration(
            color: Colors.red,
            borderRadius: BorderRadius.circular(30),
          ),
          child: const Center(
            child: Text(
              'Tricks',
              style: TextStyle(
                color: Colors.white,
                fontSize: 12,
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class PlayerInfoWidget extends StatefulWidget {
  final int playerIndex;
  final List<int> scores;

  const PlayerInfoWidget({
    super.key,
    required this.playerIndex,
    required this.scores,
  });

  @override
  _PlayerInfoWidgetState createState() => _PlayerInfoWidgetState();
}

class _PlayerInfoWidgetState extends State<PlayerInfoWidget> {
  bool isInfoVisible = false;

  @override
  Widget build(BuildContext context) {
    return Positioned(
      top: 10,
      right: 10,
      child: GestureDetector(
        onTap: () {
          showDialog(
            context: context,
            builder: (BuildContext context) {
              return buildInfoWidget();
            },
          );
        },
        child: Container(
          width: 80,
          height: 80,
          decoration: const BoxDecoration(
            shape: BoxShape.circle,
            color: Colors.transparent,
          ),
          child: Center(
            child: Image.asset('assets/scores.png'),
          ),
        ),
      ),
    );
  }

  Widget buildInfoWidget() {
    double screenwidth = MediaQuery.of(context).size.width;
    double widthscore;
    double heightscore;
    if (screenwidth < 750) {
      widthscore = 300;
      heightscore = 250;
    } else {
      widthscore = 300;
      heightscore = 250;
    }
    return AlertDialog(
      title: const Text(
        'Scores',
        textAlign: TextAlign.center,
      ),
      content: Container(
        width: widthscore,
        height: heightscore,
        color: Colors.white,
        child: Column(
          children: [
            Expanded(
              child: SingleChildScrollView(
                child: Column(
                  children: [
                    for (int i = 0; i < widget.scores.length; i++)
                      Container(
                        padding: const EdgeInsets.all(8),
                        margin: const EdgeInsets.all(4),
                        decoration: BoxDecoration(
                          color: Colors.red,
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text('Player $i'),
                            Text('Score: ${widget.scores[i]}'),
                          ],
                        ),
                      ),
                  ],
                ),
              ),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: const Text('Fermer'),
            ),
          ],
        ),
      ),
    );
  }
}

class PlayerAvatar extends StatelessWidget {
  final String playerName;
  final String imagePath;
  final int playerIndex;
  final double size;
  final double top;
  final double left;
  final double right;

  const PlayerAvatar({
    Key? key,
    required this.playerName,
    required this.imagePath,
    required this.playerIndex,
    this.size = 50.0,
    this.top = 10.0,
    this.left = 10.0,
    this.right = 10,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    double screenwidth = MediaQuery.of(context).size.width;
    double shift;
    if (screenwidth < 750) {
      if (playerIndex == 1) {
        shift = 80;
      } else {
        shift = 100;
      }
    } else {
      shift = 160;
    }
    if (playerIndex == 0) {
      return Positioned(
        bottom: shift,
        left: 0,
        right: 0,
        child: Column(
          children: [
            Text(
              playerName,
              style: const TextStyle(
                fontSize: 16.0,
                fontWeight: FontWeight.bold,
                fontStyle: FontStyle.italic,
                color: Colors.white,
              ),
            ),
            const SizedBox(height: 5.0),
            Container(
              width: size,
              height: size,
              decoration: const BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.transparent,
              ),
              child: ClipOval(
                child: Image.asset(
                  imagePath,
                  width: size,
                  height: size,
                  fit: BoxFit.cover,
                ),
              ),
            ),
          ],
        ),
      );
    }
    if (playerIndex == 1) {
      return Positioned(
        top: 0,
        bottom: 0,
        right: shift,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              playerName,
              style: const TextStyle(
                fontSize: 16.0,
                fontWeight: FontWeight.bold,
                fontStyle: FontStyle.italic,
                color: Colors.white,
              ),
            ),
            const SizedBox(height: 5.0),
            Container(
              width: size,
              height: size,
              decoration: const BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.transparent,
              ),
              child: ClipOval(
                child: Image.asset(
                  imagePath,
                  width: size,
                  height: size,
                  fit: BoxFit.cover,
                ),
              ),
            ),
          ],
        ),
      );
    }
    if (playerIndex == 2) {
      return Positioned(
        top: shift,
        left: 0,
        right: 0,
        child: Column(
          children: [
            Text(
              playerName,
              style: const TextStyle(
                fontSize: 16.0,
                fontWeight: FontWeight.bold,
                fontStyle: FontStyle.italic,
                color: Colors.white,
              ),
            ),
            const SizedBox(height: 5.0),
            Container(
              width: size,
              height: size,
              decoration: const BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.transparent,
              ),
              child: ClipOval(
                child: Image.asset(
                  imagePath,
                  width: size,
                  height: size,
                  fit: BoxFit.cover,
                ),
              ),
            ),
          ],
        ),
      );
    } else {
      return Positioned(
        bottom: 0,
        left: shift,
        top: 0,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              playerName,
              style: const TextStyle(
                fontSize: 16.0,
                fontWeight: FontWeight.bold,
                fontStyle: FontStyle.italic,
                color: Colors.white,
              ),
            ),
            const SizedBox(height: 5.0),
            Container(
              width: size,
              height: size,
              decoration: const BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.transparent,
              ),
              child: ClipOval(
                child: Image.asset(
                  imagePath,
                  width: size,
                  height: size,
                  fit: BoxFit.cover,
                ),
              ),
            ),
          ],
        ),
      );
    }
  }
}
