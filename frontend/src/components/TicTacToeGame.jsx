import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Trophy, RotateCcw, CheckCircle, XCircle, Users, Crown, ArrowLeft } from 'lucide-react';
import { toast } from '../hooks/use-toast';
import { mockQuestions } from '../data/mock';
import GlobalRanking from './GlobalRanking';

const TicTacToeGame = ({ players, onBackToSetup, onGameEnd }) => {
  const [board, setBoard] = useState(Array(9).fill(null));
  const [boardColors, setBoardColors] = useState(Array(9).fill(null)); // 'green' or 'red'
  const [currentPlayer, setCurrentPlayer] = useState('X');
  const [gameStatus, setGameStatus] = useState('playing'); // playing, won, draw
  const [winner, setWinner] = useState(null);
  const [score, setScore] = useState({ 
    playerX: { correct: 0, incorrect: 0 }, 
    playerO: { correct: 0, incorrect: 0 } 
  });
  const [globalScore, setGlobalScore] = useState({
    'Jogador X': 0,
    'Jogador O': 0
  });
  const [totalGames, setTotalGames] = useState(0);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [selectedCell, setSelectedCell] = useState(null);
  const [showAnswer, setShowAnswer] = useState(false);
  const [usedQuestions, setUsedQuestions] = useState([]);
  const [lastAnswerInfo, setLastAnswerInfo] = useState(null);

  const winningLines = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], // rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8], // columns
    [0, 4, 8], [2, 4, 6] // diagonals
  ];

  const checkWinner = (newBoard, newBoardColors) => {
    for (let line of winningLines) {
      const [a, b, c] = line;
      // Precisa ter as 3 posições preenchidas pelo mesmo jogador E todas verdes (acertos)
      if (newBoard[a] && 
          newBoard[a] === newBoard[b] && 
          newBoard[a] === newBoard[c] &&
          newBoardColors[a] === 'green' &&
          newBoardColors[b] === 'green' &&
          newBoardColors[c] === 'green') {
        return newBoard[a]; // Return 'X' or 'O'
      }
    }
    return null;
  };

  const getRandomQuestion = () => {
    const availableQuestions = mockQuestions.filter(q => !usedQuestions.includes(q.id));
    if (availableQuestions.length === 0) {
      return mockQuestions[Math.floor(Math.random() * mockQuestions.length)];
    }
    return availableQuestions[Math.floor(Math.random() * availableQuestions.length)];
  };

  const handleCellClick = (index) => {
    if (gameStatus !== 'playing' || currentQuestion) {
      return;
    }

    // Permite clicar se estiver vazio OU se for uma marca vermelha (erro)
    if (board[index] !== null && boardColors[index] !== 'red') {
      return;
    }

    const question = getRandomQuestion();
    setCurrentQuestion(question);
    setSelectedCell(index);
    setShowAnswer(false);
  };

  const handleAnswer = (selectedAnswer) => {
    if (!currentQuestion) return;

    const isCorrect = selectedAnswer === currentQuestion.correctAnswer;
    const newBoard = [...board];
    const newBoardColors = [...boardColors];
    const previousOwner = board[selectedCell]; // Quem tinha essa célula antes (se havia)
    
    // Marca a célula com a letra do jogador atual
    newBoard[selectedCell] = currentPlayer;
    
    if (isCorrect) {
      newBoardColors[selectedCell] = 'green';
      setScore(prev => ({
        ...prev,
        [currentPlayer === 'X' ? 'playerX' : 'playerO']: {
          ...prev[currentPlayer === 'X' ? 'playerX' : 'playerO'],
          correct: prev[currentPlayer === 'X' ? 'playerX' : 'playerO'].correct + 1
        }
      }));
      
      const currentPlayerName = currentPlayer === 'X' ? 'Jogador X' : 'Jogador O';
      const message = previousOwner ? 
        `${currentPlayerName} conquistou a célula! ✅` : 
        `${currentPlayerName} acertou! ✅`;
      
      setLastAnswerInfo({
        isCorrect: true,
        player: currentPlayerName,
        message: message,
        conquered: !!previousOwner
      });
      
      toast({
        title: message,
        description: previousOwner ? 
          "Você tomou uma célula do adversário com sua resposta correta!" :
          "Resposta correta! Sua marca foi colocada no tabuleiro.",
        duration: 2000,
      });
    } else {
      newBoardColors[selectedCell] = 'red';
      setScore(prev => ({
        ...prev,
        [currentPlayer === 'X' ? 'playerX' : 'playerO']: {
          ...prev[currentPlayer === 'X' ? 'playerX' : 'playerO'],
          incorrect: prev[currentPlayer === 'X' ? 'playerX' : 'playerO'].incorrect + 1
        }
      }));
      
      const currentPlayerName = currentPlayer === 'X' ? players.player1 : players.player2;
      setLastAnswerInfo({
        isCorrect: false,
        player: currentPlayerName,
        message: `${currentPlayerName} errou! ❌`,
        correctAnswer: currentQuestion.correctAnswer
      });
      toast({
        title: `${currentPlayerName} Errou ❌`, 
        description: `A resposta correta era: ${currentQuestion.correctAnswer}. O adversário pode conquistar esta célula!`,
        duration: 4000,
      });
    }

    setBoard(newBoard);
    setBoardColors(newBoardColors);
    setUsedQuestions(prev => [...prev, currentQuestion.id]);

    // Check for winner - agora precisa das cores também
    const gameWinner = checkWinner(newBoard, newBoardColors);
    if (gameWinner) {
      const winnerName = gameWinner === 'X' ? players.player1 : players.player2;
      setWinner(winnerName);
      setGameStatus('won');
      
      // Adiciona 1 ponto ao vencedor
      setGlobalScore(prev => ({
        ...prev,
        [winnerName]: (prev[winnerName] || 0) + 1
      }));
      setTotalGames(prev => prev + 1);
      
      // Callback para notificar o jogo acabou
      if (onGameEnd) {
        onGameEnd(winnerName, gameWinner);
      }
      
      toast({
        title: `🎉 ${winnerName} Venceu!`,
        description: "Conseguiu 3 acertos em linha (todos verdes)! +1 ponto no ranking!",
        duration: 5000,
      });
    } else if (newBoard.every(cell => cell !== null) && newBoardColors.every(color => color === 'green')) {
      // Empate só se tudo estiver preenchido E verde
      setGameStatus('draw');
      setTotalGames(prev => prev + 1);
      toast({
        title: "Empate!",
        description: "Tabuleiro completo, mas ninguém conseguiu 3 acertos seguidos.",
        duration: 3000,
      });
    } else {
      // Alterna para o próximo jogador
      setCurrentPlayer(currentPlayer === 'X' ? 'O' : 'X');
    }

    setCurrentQuestion(null);
    setSelectedCell(null);
    setShowAnswer(false);
  };

  const resetGame = () => {
    setBoard(Array(9).fill(null));
    setBoardColors(Array(9).fill(null));
    setCurrentPlayer('X');
    setGameStatus('playing');
    setWinner(null);
    setScore({ 
      playerX: { correct: 0, incorrect: 0 }, 
      playerO: { correct: 0, incorrect: 0 } 
    });
    setCurrentQuestion(null);
    setSelectedCell(null);
    setShowAnswer(false);
    setUsedQuestions([]);
    setLastAnswerInfo(null);
    toast({
      title: "Novo Jogo Iniciado!",
      description: `${players.player1} (X) começa! Boa sorte com as perguntas sobre História do Brasil!`,
      duration: 2000,
    });
  };

  const renderCell = (index) => {
    const cellValue = board[index];
    const cellColor = boardColors[index];
    const isSelected = selectedCell === index;
    const canClick = gameStatus === 'playing' && !currentQuestion && 
                    (cellValue === null || cellColor === 'red');
    
    let cellStyle = 'aspect-square rounded-lg border-2 transition-all duration-200 text-4xl font-bold flex items-center justify-center ';
    
    if (cellValue === 'X') {
      cellStyle += cellColor === 'green' 
        ? 'bg-green-100 border-green-500 text-green-700' 
        : 'bg-red-100 border-red-500 text-red-700';
    } else if (cellValue === 'O') {
      cellStyle += cellColor === 'green' 
        ? 'bg-green-100 border-green-500 text-green-700' 
        : 'bg-red-100 border-red-500 text-red-700';
    } else {
      cellStyle += 'bg-white border-gray-300';
    }
    
    if (canClick) {
      cellStyle += ' hover:border-blue-400 hover:bg-blue-50 cursor-pointer';
    } else {
      cellStyle += ' cursor-not-allowed opacity-60';
    }
    
    if (isSelected) {
      cellStyle += ' ring-4 ring-yellow-400 border-yellow-500';
    }
    
    // Adiciona efeito pulsante para células vermelhas (conquistáveis)
    // Vermelho estático (sem animação) para erros
    if (cellColor === 'red') {
      cellStyle += ' border-red-400';
    }
    
    return (
      <button
        key={index}
        className={cellStyle}
        onClick={() => handleCellClick(index)}
        disabled={!canClick}
        title={cellColor === 'red' ? 'Célula conquistável! Clique para tentar tomar.' : ''}
      >
        {cellValue && (
          <span className="text-5xl font-bold">
            {cellValue}
          </span>
        )}
      </button>
    );
  };

  const getCurrentPlayerName = () => {
    return currentPlayer === 'X' ? players.player1 : players.player2;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-yellow-50 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header with Back Button */}
        <div className="text-center mb-6">
          <div className="flex items-center justify-between mb-4">
            <Button
              onClick={onBackToSetup}
              variant="outline"
              className="flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" />
              Trocar Jogadores
            </Button>
            
            <div className="flex items-center gap-4">
              <Badge className="bg-blue-100 text-blue-800">
                Partida #{totalGames + 1}
              </Badge>
            </div>
          </div>
          
          <h1 className="text-4xl font-bold text-green-800 mb-2">
            Jogo da Velha Histórico
          </h1>
          <p className="text-gray-600 mb-2">
            História do Brasil • 1500 - Primeira República
          </p>
          {gameStatus === 'playing' && (
            <div className="text-2xl font-bold text-blue-800">
              Vez de: <span className="text-purple-600">{getCurrentPlayerName()}</span>
            </div>
          )}
          
          {/* Players Score Display */}
          <div className="flex justify-center gap-8 mt-4">
            <div className="text-center">
              <div className="flex items-center gap-2 justify-center">
                <Crown className="w-5 h-5 text-purple-600" />
                <span className="font-bold text-lg text-purple-800">{players.player1}</span>
              </div>
              <Badge className="bg-purple-100 text-purple-800">
                {globalScore[players.player1] || 0} pontos
              </Badge>
            </div>
            <div className="text-center">
              <div className="flex items-center gap-2 justify-center">
                <Crown className="w-5 h-5 text-orange-600" />
                <span className="font-bold text-lg text-orange-800">{players.player2}</span>
              </div>
              <Badge className="bg-orange-100 text-orange-800">
                {globalScore[players.player2] || 0} pontos
              </Badge>
            </div>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Game Board */}
          <div className="lg:col-span-2">
            <Card className="shadow-lg">
              <CardHeader className="text-center">
                <CardTitle className="text-2xl text-blue-800 flex items-center justify-center gap-2">
                  <Trophy className="w-6 h-6" />
                  Tabuleiro
                </CardTitle>
                <div className="flex justify-center gap-4 mt-2">
                  <div className="text-center">
                    <Badge variant="outline" className="bg-purple-100 text-purple-800 mb-1">
                      {players.player1} (X)
                    </Badge>
                    <div className="text-sm">
                      <Badge variant="outline" className="bg-green-100 text-green-800 mr-1">
                        ✓ {score.playerX.correct}
                      </Badge>
                      <Badge variant="outline" className="bg-red-100 text-red-800">
                        ✗ {score.playerX.incorrect}
                      </Badge>
                    </div>
                  </div>
                  <div className="text-center">
                    <Badge variant="outline" className="bg-orange-100 text-orange-800 mb-1">
                      {players.player2} (O)
                    </Badge>
                    <div className="text-sm">
                      <Badge variant="outline" className="bg-green-100 text-green-800 mr-1">
                        ✓ {score.playerO.correct}
                      </Badge>
                      <Badge variant="outline" className="bg-red-100 text-red-800">
                        ✗ {score.playerO.incorrect}
                      </Badge>
                    </div>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-3 gap-3 mb-6">
                  {Array.from({ length: 9 }).map((_, index) => renderCell(index))}
                </div>
                
                {gameStatus === 'won' && (
                  <div className="text-center p-4 bg-green-100 rounded-lg mb-4">
                    <Trophy className="w-12 h-12 mx-auto text-yellow-600 mb-2" />
                    <h3 className="text-xl font-bold text-green-800">
                      {winner} Venceu!
                    </h3>
                    <p className="text-green-600">
                      Conseguiu 3 marcas verdes em linha! +1 ponto no ranking global!
                    </p>
                  </div>
                )}

                {gameStatus === 'draw' && (
                  <div className="text-center p-4 bg-yellow-100 rounded-lg mb-4">
                    <h3 className="text-xl font-bold text-yellow-800">
                      Empate!
                    </h3>
                    <p className="text-yellow-600">
                      Tabuleiro completo, mas ninguém conseguiu 3 em linha.
                    </p>
                  </div>
                )}

                {lastAnswerInfo && (
                  <div className={`text-center p-3 rounded-lg mb-4 ${
                    lastAnswerInfo.isCorrect ? 'bg-green-50 border-2 border-green-200' : 'bg-red-50 border-2 border-red-200'
                  }`}>
                    <p className={`font-semibold ${lastAnswerInfo.isCorrect ? 'text-green-800' : 'text-red-800'}`}>
                      {lastAnswerInfo.message}
                    </p>
                    {lastAnswerInfo.conquered && (
                      <p className="text-orange-600 text-sm mt-1 font-semibold">
                        🎯 Célula conquistada do adversário!
                      </p>
                    )}
                    {!lastAnswerInfo.isCorrect && (
                      <div className="mt-2">
                        <p className="text-red-600 text-sm">
                          <strong>Resposta correta:</strong> {lastAnswerInfo.correctAnswer}
                        </p>
                        <p className="text-orange-600 text-xs mt-1">
                          ⚠️ Esta célula pode ser conquistada pelo adversário!
                        </p>
                      </div>
                    )}
                  </div>
                )}

                <Button 
                  onClick={resetGame} 
                  className="w-full bg-blue-600 hover:bg-blue-700"
                >
                  <RotateCcw className="w-4 h-4 mr-2" />
                  Nova Partida
                </Button>
              </CardContent>
            </Card>

            {/* Question Panel */}
            <Card className="shadow-lg mt-6">
              <CardHeader className="text-center">
                <CardTitle className="text-2xl text-blue-800">
                  Pergunta Histórica
                </CardTitle>
              </CardHeader>
              <CardContent>
                {!currentQuestion ? (
                  <div className="text-center py-12">
                    <div className="text-6xl mb-4">🏛️</div>
                    <h3 className="text-xl font-semibold text-gray-700 mb-2">
                      {getCurrentPlayerName()}, clique em uma célula
                    </h3>
                    <p className="text-gray-500">
                      para responder uma pergunta sobre a História do Brasil
                    </p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="text-center p-2 bg-purple-100 rounded-lg">
                      <span className="text-lg font-bold text-purple-800">
                        {getCurrentPlayerName()} responde:
                      </span>
                    </div>
                    <div className="p-4 bg-blue-50 rounded-lg">
                      <h3 className="font-semibold text-blue-800 mb-3">
                        {currentQuestion.question}
                      </h3>
                      <div className="grid gap-2">
                        {currentQuestion.options.map((option, index) => (
                          <Button
                            key={index}
                            variant="outline"
                            className="justify-start text-left h-auto py-3 px-4 hover:bg-blue-100"
                            onClick={() => handleAnswer(option)}
                          >
                            <span className="font-medium mr-2">
                              {String.fromCharCode(65 + index)})
                            </span>
                            {option}
                          </Button>
                        ))}
                      </div>
                    </div>
                    
                    <div className="p-3 bg-gray-50 rounded-lg">
                      <p className="text-sm text-gray-600">
                        <strong>Período:</strong> {currentQuestion.period}
                      </p>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Global Ranking */}
          <div>
            <GlobalRanking currentPlayers={players} />
          </div>
        </div>

        {/* Game Rules */}
        <Card className="mt-8 shadow-lg">
          <CardHeader>
            <CardTitle className="text-xl text-center text-green-800">
              Como Jogar
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-4 text-sm">
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <span className="text-3xl mb-2 block text-green-600 font-bold">✓</span>
                <h4 className="font-semibold text-green-800">Resposta Correta</h4>
                <p className="text-green-600">Marca VERDE no tabuleiro</p>
              </div>
              <div className="text-center p-4 bg-red-50 rounded-lg">
                <span className="text-3xl mb-2 block text-red-600 font-bold">✗</span>
                <h4 className="font-semibold text-red-800">Resposta Incorreta</h4>
                <p className="text-red-600">Marca VERMELHA - adversário pode conquistar!</p>
              </div>
              <div className="text-center p-4 bg-yellow-50 rounded-lg">
                <Trophy className="w-8 h-8 mx-auto text-yellow-600 mb-2" />
                <h4 className="font-semibold text-yellow-800">Vitória</h4>
                <p className="text-yellow-600">3 marcas VERDES em linha = +1 ponto!</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default TicTacToeGame;