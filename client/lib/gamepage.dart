import 'dart:async';
import 'package:coeur_artificiel/player.dart';
import 'package:coeur_artificiel/trick.dart';
import 'package:flutter/material.dart';
import 'package:coeur_artificiel/heart_game.dart';
import 'package:coeur_artificiel/card.dart' as MyCard;

class GamePage extends StatefulWidget {
  const GamePage({Key? key}) : super(key: key);

  @override
  _GamePageState createState() => _GamePageState();
}

class _GamePageState extends State<GamePage> {
  bool _isPlaying = false;
  HeartsGame game;
  int numberOfRounds = 0;
  List<int> generalScores = [0, 0, 0, 0];
  bool timerExpired = false;
  _GamePageState() : game = HeartsGame([0, 1, 2, 3], currentPlayer: 0);

  @override
  Widget build(BuildContext context) {
    for (var player in game.players) {
      print('${player.number} hand: ${player.hand}');
    }
    return Scaffold(
      appBar: AppBar(
        title: Text('Hearts Game'),
        backgroundColor: Colors.red[700],
        centerTitle: true,
      ),
      body: Container(
        decoration: BoxDecoration(
          image: DecorationImage(
            image: AssetImage('assets/5120953.jpg'),
            fit: BoxFit.cover,
          ),
        ),
        child: Stack(
          children: [
            timerDisplay(game, context),
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
              imagePath: 'humain.png',
              playerIndex: 0,
              size: 60.0,
              top: (MediaQuery.of(context).size.height / 4) * 2.5,
              left: (MediaQuery.of(context).size.width / 4) * 1.85,
            ),
            PlayerAvatar(
              playerName: 'Intelligence Artificielle 1',
              imagePath: 'robotAvatar.png',
              playerIndex: 0,
              size: 60.0,
              top: (MediaQuery.of(context).size.height / 4) * 1.55,
              left: (MediaQuery.of(context).size.width / 4) * 2.8,
            ),
            PlayerAvatar(
              playerName: 'Intelligence Artificielle 2',
              imagePath: 'robotAvatar.png',
              playerIndex: 0,
              size: 60.0,
              top: (MediaQuery.of(context).size.height / 4) * 1.1,
              left: (MediaQuery.of(context).size.width / 4) * 1.63,
            ),
            PlayerAvatar(
              playerName: 'Intelligence Artificielle 3',
              imagePath: 'robotAvatar.png',
              playerIndex: 0,
              size: 60.0,
              top: (MediaQuery.of(context).size.height / 4) * 1.55,
              left: (MediaQuery.of(context).size.width / 4) * 0.65,
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
          left: (MediaQuery.of(context).size.width / 4) * 1.1,
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
          top: ((MediaQuery.of(context).size.height - 100) / 2) * 1.25,
          left: (MediaQuery.of(context).size.width / 4) * 3.25,
          child: TimerWidget(initialSeconds: 10, onTimeout: () {}, game: game));
    }
    if (game.currentPlayer == 2) {
      return Positioned(
          top: ((MediaQuery.of(context).size.height - 100) / 4) * 1.1,
          left: (MediaQuery.of(context).size.width / 4) * 2.5,
          child: TimerWidget(initialSeconds: 10, onTimeout: () {}, game: game));
    }
    return Positioned(
        top: ((MediaQuery.of(context).size.height - 100) / 4) * 2.65,
        left: (MediaQuery.of(context).size.width / 4) * 0.7,
        child: TimerWidget(initialSeconds: 10, onTimeout: () {}, game: game));
  }

  Widget _buildPlayerHand0(Player player) {
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
                    await Future.delayed(Duration(seconds: 3));
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
                            ? Color.fromARGB(255, 59, 235, 65)
                            : Colors.red,
                        width: 4.5,
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

  Future<void> _playRound() async {
    if (game.end_of_game()) {
      for (int i = 0; i < 3; i++) {
        generalScores[i] += game.scores[i];
      }
      numberOfRounds++;
      if (numberOfRounds == 8) {
        return;
      } else {
        game = HeartsGame([0, 1, 2, 3], currentPlayer: 0);
      }
    }
    Player currentPlayer = game.players[game.currentPlayer];
    if (game.currentPlayer == 0) {
      setState(() {});
    } else {
      MyCard.Card cardToPlay = await game.cardToPlay(currentPlayer);
      game.play_card(currentPlayer, cardToPlay);
      setState(() {});
      await Future.delayed(Duration(seconds: 3));
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
    double aspectRatio;
    if (screenwidth < 500) {
      targetImageWidth = screenwidth * 0.8;
      aspectRatio = 2.5;
    } else {
      targetImageWidth = screenwidth * 0.48;
      aspectRatio = 4.5;
    }
    return Positioned(
      top: 0,
      right: 25,
      bottom: 0,
      child: Image.asset(
        "listecartedos_${handlength}_1.png",
        width: targetImageWidth / aspectRatio,
        height: targetImageWidth / aspectRatio,
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
    double aspectRatio;
    if (screenwidth < 500) {
      targetImageWidth = screenwidth * 0.8;
      aspectRatio = 2.5;
    } else {
      targetImageWidth = screenwidth * 1.1;
      aspectRatio = 4;
    }

    return Positioned(
      top: -90,
      left: screenwidth / 2 - targetImageWidth / (2 * aspectRatio),
      child: Image.asset(
        'listecartedos_${handlength}_2.png',
        width: targetImageWidth / aspectRatio, // Adjust the width as needed
        height: targetImageWidth / aspectRatio, // Adjust the height as needed
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
    double aspectRatio;
    if (screenwidth < 500) {
      targetImageWidth = screenwidth * 0.8;
      aspectRatio = 2.5;
    } else {
      targetImageWidth = screenwidth * 1;
      aspectRatio = 3.5;
    }

    return Positioned(
      top: MediaQuery.of(context).size.height / 2 -
          targetImageWidth / (2 * aspectRatio),
      left: -70,
      child: Image.asset(
        'listecartedos_${handlength}_3.png',
        width: targetImageWidth / aspectRatio,
        height: targetImageWidth / aspectRatio,
      ),
    );
  }

  Widget _buildCurrentTrick(Trick trick) {
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

class TimerWidget extends StatefulWidget {
  final int initialSeconds;
  final Function() onTimeout;
  final HeartsGame game;

  TimerWidget({
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
    _timer = Timer.periodic(Duration(seconds: 1), (timer) {
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
        width: 50,
        height: 50,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: Colors.red,
        ),
        child: Center(
          child: Text(
            '$secondsRemaining',
            style: TextStyle(
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

  TrickButton({required this.playerNumber, required this.game});

  @override
  Widget build(BuildContext context) {
    // Récupérez le pli gagné par le joueur
    Map<int, Trick> listOfTrick = game.players[playerNumber].listOfTrick;

    return Positioned(
      // Ajustez la position en fonction du joueur
      top: playerNumber == 0
          ? (MediaQuery.of(context).size.height / 4) * 2.85
          : playerNumber == 1
              ? (MediaQuery.of(context).size.height / 4) * 1.9
              : playerNumber == 2
                  ? (MediaQuery.of(context).size.height / 4) * 1
                  : (MediaQuery.of(context).size.height / 4) * 1.9,
      left: playerNumber == 0
          ? (MediaQuery.of(context).size.width / 4) * 1.9
          : playerNumber == 1
              ? (MediaQuery.of(context).size.width / 4) * 3.2
              : playerNumber == 2
                  ? (MediaQuery.of(context).size.width / 4) * 1.9
                  : (MediaQuery.of(context).size.width / 4) * 0.65,

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
                    : Text('Aucun pli gagné pour ce joueur'),
                actions: [
                  TextButton(
                    onPressed: () {
                      Navigator.of(context).pop();
                    },
                    child: Text('Fermer'),
                  ),
                ],
              );
            },
          );
        },
        child: Container(
          width: 90,
          height: 30,
          decoration: BoxDecoration(
            color: Colors.red,
            borderRadius: BorderRadius.circular(10),
          ),
          child: Center(
            child: Text(
              'List of Tricks',
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

  PlayerInfoWidget({
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
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: Colors.transparent,
          ),
          child: Center(
            child: Image.asset('scores.png'),
          ),
        ),
      ),
    );
  }

  Widget buildInfoWidget() {
    return AlertDialog(
      title: Text(
        'Scores',
        textAlign: TextAlign.center,
      ),
      content: Container(
        width: 300,
        height: 200,
        color: Colors.white,
        child: Column(
          children: [
            for (int i = 0; i < widget.scores.length; i++)
              Container(
                padding: EdgeInsets.all(8),
                margin: EdgeInsets.all(4),
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
            ElevatedButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: Text('Fermer'),
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

  PlayerAvatar({
    required this.playerName,
    required this.imagePath,
    required this.playerIndex,
    this.size = 50.0,
    this.top = 10.0,
    this.left = 10.0,
  });

  @override
  Widget build(BuildContext context) {
    return Positioned(
      top: top + (playerIndex * 60.0),
      left: left,
      child: Row(
        children: [
          Container(
            width: size,
            height: size,
            decoration: BoxDecoration(
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
          SizedBox(width: 10.0),
          Text(
            playerName,
            style: TextStyle(
              fontSize: 16.0,
              fontWeight: FontWeight.bold,
              fontStyle: FontStyle.italic,
              color: Colors.white,
            ),
          ),
        ],
      ),
    );
  }
}
