import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Trophy, RotateCcw, ArrowLeft, Wifi, WifiOff, Copy } from 'lucide-react';
import { toast } from '../hooks/use-toast';
import OnlineGlobalRanking from './OnlineGlobalRanking';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const WS_URL = BACKEND_URL.replace('http', 'ws');

const OnlineTicTacToeGame = ({ gameData, onBackToSetup }) => {
  const [room, setRoom] = useState(gameData.room);
  const [isConnected, setIsConnected] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [selectedCell, setSelectedCell] = useState(null);
  const [lastAnswerInfo, setLastAnswerInfo] = useState(null);
  const [ranking, setRanking] = useState([]);
  const wsRef = useRef(null);

  const playerName = gameData.playerName;
  const isPlayerX = room.player1?.name === playerName;
  const playerSymbol = isPlayerX ? 'X' : 'O';
  const isMyTurn = room.current_player === playerSymbol;

  // WebSocket connection
  useEffect(() => {
    const connectWebSocket = () => {
      try {
        wsRef.current = new WebSocket(`${WS_URL}/ws/${room.code}`);
        
        wsRef.current.onopen = () => {
          console.log('WebSocket connected');
          setIsConnected(true);
        };

        wsRef.current.onmessage = (event) => {
          const data = JSON.parse(event.data);
          handleWebSocketMessage(data);
        };

        wsRef.current.onclose = () => {
          console.log('WebSocket disconnected');
          setIsConnected(false);
          
          // Attempt to reconnect after 3 seconds
          setTimeout(connectWebSocket, 3000);
        };

        wsRef.current.onerror = (error) => {
          console.error('WebSocket error:', error);
        };

      } catch (error) {
        console.error('Failed to connect WebSocket:', error);
        setTimeout(connectWebSocket, 3000);
      }
    };

    connectWebSocket();

    // Cleanup on component unmount
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [room.code]);

  // Load initial ranking
  useEffect(() => {
    loadRanking();
  }, []);

  const loadRanking = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/players/ranking`);
      const data = await response.json();
      setRanking(data.ranking || []);
    } catch (error) {
      console.error('Error loading ranking:', error);
    }
  };

  const handleWebSocketMessage = (data) => {
    console.log('WebSocket message:', data);

    switch (data.type) {
      case 'room_update':
        setRoom(data.room);
        break;

      case 'question_generated':
        setCurrentQuestion(data.question);
        setSelectedCell(data.selected_cell);
        break;

      case 'answer_result':
        setLastAnswerInfo({
          isCorrect: data.result.correct,
          player: playerName,
          message: data.result.correct ? `Resposta correta! ✅` : `Resposta incorreta! ❌`,
          correctAnswer: data.result.correct_answer
        });
        
        setRoom(data.room);
        setCurrentQuestion(null);
        setSelectedCell(null);
        
        // Reload ranking if game finished
        if (data.result.winner) {
          setTimeout(loadRanking, 1000);
        }
        break;

      case 'game_reset':
        setRoom(data.room);
        setCurrentQuestion(null);
        setSelectedCell(null);
        setLastAnswerInfo(null);
        break;
    }
  };

  const handleCellClick = async (index) => {
    if (!isMyTurn || currentQuestion || room.game_status !== 'playing') {
      if (!isMyTurn) {
        toast({
          title: "Não é sua vez!",
          description: "Aguarde a vez do seu oponente",
          duration: 2000,
        });
      }
      return;
    }

    // Check if cell is clickable
    if (room.board[index] !== null && room.board_colors[index] !== 'red') {
      return;
    }

    try {
      const response = await fetch(`${BACKEND_URL}/api/game/click-cell`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          room_code: room.code,
          player_name: playerName,
          cell_index: index
        })
      });

      if (!response.ok) {
        const error = await response.json();
        toast({
          title: "Erro",
          description: error.detail || "Não foi possível clicar na célula",
          duration: 3000,
        });
      }
    } catch (error) {
      console.error('Error clicking cell:', error);
      toast({
        title: "Erro de conexão",
        description: "Verifique sua internet",
        duration: 3000,
      });
    }
  };

  const handleAnswer = async (selectedAnswer) => {
    if (!currentQuestion) return;

    try {
      const response = await fetch(`${BACKEND_URL}/api/game/submit-answer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          room_code: room.code,
          player_name: playerName,
          answer: selectedAnswer,
          cell_index: selectedCell
        })
      });

      if (!response.ok) {
        const error = await response.json();
        toast({
          title: "Erro",
          description: error.detail || "Não foi possível enviar resposta",
          duration: 3000,
        });
      }
    } catch (error) {
      console.error('Error submitting answer:', error);
      toast({
        title: "Erro de conexão",
        description: "Verifique sua internet",
        duration: 3000,
      });
    }
  };

  const resetGame = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/game/reset/${room.code}`, {
        method: 'POST'
      });

      if (!response.ok) {
        throw new Error('Failed to reset game');
      }
    } catch (error) {
      console.error('Error resetting game:', error);
      toast({
        title: "Erro",
        description: "Não foi possível reiniciar o jogo",
        duration: 3000,
      });
    }
  };

  const copyRoomCode = () => {
    navigator.clipboard.writeText(room.code);
    toast({
      title: "Código copiado! 📋",
      description: "Compartilhe com mais pessoas",
      duration: 2000,
    });
  };

  const renderCell = (index) => {
    const cellValue = room.board[index];
    const cellColor = room.board_colors[index];
    const isSelected = selectedCell === index;
    const canClick = isMyTurn && room.game_status === 'playing' && !currentQuestion && 
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
    
    if (cellColor === 'red' && canClick) {
      cellStyle += ' animate-pulse border-orange-400';
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
    return room.current_player === 'X' ? room.player1?.name : room.player2?.name;
  };

  const ConnectionStatus = () => (
    <div className="flex items-center gap-2">
      {isConnected ? (
        <>
          <Wifi className="w-4 h-4 text-green-600" />
          <span className="text-sm text-green-600">Online</span>
        </>
      ) : (
        <>
          <WifiOff className="w-4 h-4 text-red-600" />
          <span className="text-sm text-red-600">Reconectando...</span>
        </>
      )}
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-6">
          <div className="flex items-center justify-between mb-4">
            <Button
              onClick={onBackToSetup}
              variant="outline"
              className="flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" />
              Sair da Sala
            </Button>
            
            <div className="flex items-center gap-4">
              <ConnectionStatus />
              <div className="flex items-center gap-2">
                <Badge className="bg-blue-100 text-blue-800">
                  {room.code}
                </Badge>
                <Button onClick={copyRoomCode} size="sm" variant="outline">
                  <Copy className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </div>
          
          <h1 className="text-4xl font-bold text-blue-800 mb-2">
            Jogo da Velha Histórico - Online
          </h1>
          <p className="text-gray-600 mb-2">
            História do Brasil • 1500 - Primeira República
          </p>
          
          {room.game_status === 'playing' && (
            <div className="text-2xl font-bold text-blue-800">
              Vez de: <span className={isMyTurn ? "text-green-600" : "text-orange-600"}>
                {getCurrentPlayerName()} 
                {isMyTurn ? " (Você!)" : ""}
              </span>
            </div>
          )}
          
          {/* Players Display */}
          <div className="flex justify-center gap-8 mt-4">
            <div className="text-center">
              <span className="font-bold text-lg text-purple-800">
                {room.player1?.name || 'Aguardando...'} (X)
              </span>
              {isPlayerX && (
                <Badge className="ml-2 bg-green-100 text-green-700 text-xs">
                  Você
                </Badge>
              )}
            </div>
            <div className="text-center">
              <span className="font-bold text-lg text-orange-800">
                {room.player2?.name || 'Aguardando...'} (O)
              </span>
              {!isPlayerX && room.player2 && (
                <Badge className="ml-2 bg-green-100 text-green-700 text-xs">
                  Você
                </Badge>
              )}
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
                  Tabuleiro Online
                </CardTitle>
                <div className="flex justify-center gap-4 mt-2">
                  <div className="text-center">
                    <Badge variant="outline" className="bg-purple-100 text-purple-800 mb-1">
                      {room.player1?.name} (X)
                    </Badge>
                    <div className="text-sm">
                      <Badge variant="outline" className="bg-green-100 text-green-800 mr-1">
                        ✓ {room.score?.playerX?.correct || 0}
                      </Badge>
                      <Badge variant="outline" className="bg-red-100 text-red-800">
                        ✗ {room.score?.playerX?.incorrect || 0}
                      </Badge>
                    </div>
                  </div>
                  <div className="text-center">
                    <Badge variant="outline" className="bg-orange-100 text-orange-800 mb-1">
                      {room.player2?.name} (O)
                    </Badge>
                    <div className="text-sm">
                      <Badge variant="outline" className="bg-green-100 text-green-800 mr-1">
                        ✓ {room.score?.playerO?.correct || 0}
                      </Badge>
                      <Badge variant="outline" className="bg-red-100 text-red-800">
                        ✗ {room.score?.playerO?.incorrect || 0}
                      </Badge>
                    </div>
                  </div>
                </div>
              </CardHeader>
              
              <CardContent>
                <div className="grid grid-cols-3 gap-3 mb-6">
                  {Array.from({ length: 9 }).map((_, index) => renderCell(index))}
                </div>
                
                {room.game_status === 'finished' && room.winner && (
                  <div className="text-center p-4 bg-green-100 rounded-lg mb-4">
                    <Trophy className="w-12 h-12 mx-auto text-yellow-600 mb-2" />
                    <h3 className="text-xl font-bold text-green-800">
                      {room.winner} Venceu!
                    </h3>
                    <p className="text-green-600">
                      Conseguiu 3 marcas verdes em linha! +1 ponto no ranking!
                    </p>
                  </div>
                )}

                {room.game_status === 'finished' && !room.winner && (
                  <div className="text-center p-4 bg-yellow-100 rounded-lg mb-4">
                    <h3 className="text-xl font-bold text-yellow-800">
                      Empate!
                    </h3>
                    <p className="text-yellow-600">
                      Ninguém conseguiu 3 marcas verdes em linha.
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
                    {!lastAnswerInfo.isCorrect && lastAnswerInfo.correctAnswer && (
                      <p className="text-red-600 text-sm mt-2">
                        <strong>Resposta correta:</strong> {lastAnswerInfo.correctAnswer}
                      </p>
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
                      {isMyTurn ? "Sua vez! Clique em uma célula" : "Aguarde sua vez..."}
                    </h3>
                    <p className="text-gray-500">
                      {isMyTurn ? "para responder uma pergunta sobre a História do Brasil" : 
                                  `${getCurrentPlayerName()} está jogando`}
                    </p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="text-center p-2 bg-purple-100 rounded-lg">
                      <span className="text-lg font-bold text-purple-800">
                        {playerName} responde:
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

          {/* Online Ranking */}
          <div>
            <OnlineGlobalRanking currentPlayers={[room.player1?.name, room.player2?.name].filter(Boolean)} ranking={ranking} />
          </div>
        </div>

        {/* Game Rules */}
        <Card className="mt-8 shadow-lg">
          <CardHeader>
            <CardTitle className="text-xl text-center text-blue-800">
              Como Jogar Online
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-4 gap-4 text-sm">
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
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <Wifi className="w-8 h-8 mx-auto text-blue-600 mb-2" />
                <h4 className="font-semibold text-blue-800">Online</h4>
                <p className="text-blue-600">Jogue em tempo real à distância!</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default OnlineTicTacToeGame;