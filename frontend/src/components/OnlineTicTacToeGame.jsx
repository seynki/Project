import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Trophy, RotateCcw, CheckCircle, XCircle, Users, Crown, ArrowLeft, Wifi, WifiOff } from 'lucide-react';
import { toast } from '../hooks/use-toast';

const OnlineTicTacToeGame = ({ roomData, onBackToSetup, onDisconnect, subject = 'historia' }) => {
  const [gameState, setGameState] = useState({
    board: Array(9).fill(null),
    boardColors: Array(9).fill(null),
    currentPlayer: 'X',
    gameStatus: 'waiting', // waiting, playing, won, draw
    winner: null,
    players: {},
    playerSymbols: {}
  });
  
  const [connectionStatus, setConnectionStatus] = useState('connecting'); // connecting, connected, disconnected
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [selectedCell, setSelectedCell] = useState(null);
  const [isMyTurn, setIsMyTurn] = useState(false);
  const [lastMoveInfo, setLastMoveInfo] = useState(null);
  const [waitingForPlayer, setWaitingForPlayer] = useState(true);

  const ws = useRef(null);
  const reconnectAttempts = useRef(0);
  const reconnectTimer = useRef(null);
  const lastPongAt = useRef(Date.now());

  const backendUrl = process.env.REACT_APP_BACKEND_URL;
  const wsUrl = backendUrl.replace('https://', 'wss://').replace('http://', 'ws://');

  const scheduleReconnect = () => {
    const attempt = reconnectAttempts.current;
    const baseDelay = Math.min(1000 * Math.pow(2, attempt), 30000); // cap at 30s
    const jitter = Math.floor(Math.random() * 1000); // 0-1s jitter
    const delay = baseDelay + jitter;
    if (reconnectTimer.current) clearTimeout(reconnectTimer.current);
    reconnectTimer.current = setTimeout(() => {
      reconnectAttempts.current = attempt + 1;
      console.log(`Tentativa de reconexão ${reconnectAttempts.current} (delay ${delay}ms)`);
      connectWebSocket();
    }, delay);
  };

  const connectWebSocket = () => {
    try {
      // Close existing connection
      if (ws.current) {
        try { ws.current.onclose = null; ws.current.close(); } catch (_) {}
      }

      setConnectionStatus('connecting');
      ws.current = new WebSocket(`${wsUrl}/api/ws/${roomData.player_id}`);
      
      ws.current.onopen = () => {
        console.log('WebSocket connected');
        setConnectionStatus('connected');
        reconnectAttempts.current = 0;
        lastPongAt.current = Date.now();
        
        // Join room after connection is established
        setTimeout(() => {
          if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({
              type: 'join_room',
              room_code: roomData.room_code
            }));
          }
        }, 100);

        toast({
          title: "Conectado!",
          description: "Conexão estabelecida com o servidor",
          duration: 2000
        });
      };

      ws.current.onmessage = (event) => {
        const message = JSON.parse(event.data);
        handleWebSocketMessage(message);
      };

      ws.current.onclose = (event) => {
        console.log('WebSocket disconnected:', event.code, event.reason);
        setConnectionStatus('disconnected');
        // Schedule unlimited reconnects (unless closed cleanly 1000)
        if (event.code !== 1000) {
          scheduleReconnect();
        }
      };

      ws.current.onerror = (error) => {
        console.error('WebSocket error:', error);
        setConnectionStatus('disconnected');
      };

    } catch (error) {
      console.error('Error connecting WebSocket:', error);
      setConnectionStatus('disconnected');
      scheduleReconnect();
    }
  };

  const handleWebSocketMessage = (message) => {
    // console.log('Received message:', message);
    switch (message.type) {
      case 'connected':
        lastPongAt.current = Date.now();
        break;
      case 'pong':
        // Heartbeat response, connection is alive
        lastPongAt.current = Date.now();
        break;
      case 'ping':
        // Server keepalive ping: reply with client ping to receive a pong back
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
          ws.current.send(JSON.stringify({ type: 'ping' }));
        }
        break;
      case 'room_state':
        const room = message.room;
        setGameState({
          board: room.board.board,
          boardColors: room.board.board_colors,
          currentPlayer: room.board.current_player,
          gameStatus: room.board.game_status,
          winner: room.board.winner,
          players: room.players,
          playerSymbols: room.player_symbols
        });
        
        // Check if it's my turn
        const mySymbol = room.player_symbols[roomData.player_id];
        setIsMyTurn(room.board.current_player === mySymbol && room.board.game_status === 'playing');
        
        // Check if we're waiting for another player
        setWaitingForPlayer(Object.keys(room.players).length < 2);
        break;

      case 'player_joined':
        toast({
          title: "Jogador entrou!",
          description: `${message.player_name} entrou na sala`,
          duration: 3000
        });
        // Se o servidor enviar o estado da sala junto ao evento, sincronize completamente
        if (message.room) {
          const room = message.room;
          setGameState({
            board: room.board.board,
            boardColors: room.board.board_colors,
            currentPlayer: room.board.current_player,
            gameStatus: room.board.game_status,
            winner: room.board.winner,
            players: room.players,
            playerSymbols: room.player_symbols
          });
          const mySymbol2 = room.player_symbols[roomData.player_id];
          setIsMyTurn(room.board.current_player === mySymbol2 && room.board.game_status === 'playing');
          setWaitingForPlayer(Object.keys(room.players).length < 2);
        } else {
          setWaitingForPlayer(message.player_count < 2);
        }
        break;

      case 'game_update':
        const updatedRoom = message.room;
        setGameState({
          board: updatedRoom.board.board,
          boardColors: updatedRoom.board.board_colors,
          currentPlayer: updatedRoom.board.current_player,
          gameStatus: updatedRoom.board.game_status,
          winner: updatedRoom.board.winner,
          players: updatedRoom.players,
          playerSymbols: updatedRoom.player_symbols
        });

        // Update turn status
        const mySymbolUpdated = updatedRoom.player_symbols[roomData.player_id];
        setIsMyTurn(updatedRoom.board.current_player === mySymbolUpdated && updatedRoom.board.game_status === 'playing');

        // Show move result
        const move = message.move;
        setLastMoveInfo({
          playerName: move.player_name,
          isCorrect: move.is_correct,
          answer: move.answer,
          correctAnswer: move.correct_answer,
          cellIndex: move.cell_index
        });

        // Clear current question
        setCurrentQuestion(null);
        setSelectedCell(null);

        // Show toast for move result
        if (move.player_id === roomData.player_id) {
          // My move
          toast({
            title: move.is_correct ? "Resposta correta! ✅" : "Resposta incorreta ❌",
            description: move.is_correct 
              ? "Sua marca foi colocada no tabuleiro"
              : `Resposta correta: ${move.correct_answer}`,
            duration: 3000
          });
        } else {
          // Opponent's move
          toast({
            title: `${move.player_name} ${move.is_correct ? 'acertou' : 'errou'}`,
            description: move.is_correct 
              ? "Adversário marcou no tabuleiro"
              : "Você pode conquistar esta célula!",
            duration: 3000
          });
        }

        // Check for game end
        if (updatedRoom.board.game_status === 'won') {
          const winnerSymbol = updatedRoom.board.winner;
          const winnerPlayerId = Object.keys(updatedRoom.player_symbols).find(
            pid => updatedRoom.player_symbols[pid] === winnerSymbol
          );
          const winnerName = updatedRoom.players[winnerPlayerId];
          
          setTimeout(() => {
            toast({
              title: winnerPlayerId === roomData.player_id ? "🎉 Você venceu!" : `${winnerName} venceu!`,
              description: "Conseguiu 3 acertos em linha!",
              duration: 5000
            });
          }, 1000);
        }
        break;

      case 'question':
        setCurrentQuestion(message.question);
        setSelectedCell(message.cell_index);
        break;

      case 'player_answering':
        if (message.player_name !== roomData.player_name) {
          toast({
            title: `${message.player_name} está respondendo...`,
            description: `Célula ${message.cell_index + 1} selecionada`,
            duration: 2000
          });
        }
        break;

      case 'player_disconnected':
        toast({
          title: "Jogador desconectou",
          description: `${message.player_name} saiu do jogo`,
          variant: "destructive",
          duration: 5000
        });
        break;

      case 'error':
        toast({
          title: "Erro",
          description: message.message,
          variant: "destructive",
          duration: 3000
        });
        break;
    }
  };

  useEffect(() => {
    connectWebSocket();
    
    // Heartbeat: send ping every 15s and watchdog for missing pongs
    const heartbeatInterval = setInterval(() => {
      if (ws.current && ws.current.readyState === WebSocket.OPEN) {
        try {
          ws.current.send(JSON.stringify({ type: 'ping' }));
        } catch (_) {}
      }
    }, 15000);

    const watchdogInterval = setInterval(() => {
      const now = Date.now();
      // If no pong for 45s, force reconnect
      if (connectionStatus === 'connected' && now - lastPongAt.current > 45000) {
        console.warn('Heartbeat timeout, reconnecting...');
        try { ws.current && ws.current.close(4001, 'heartbeat-timeout'); } catch (_) {}
      }
    }, 5000);
    
    const onOnline = () => {
      console.log('Network online - attempting reconnect');
      if (connectionStatus !== 'connected') connectWebSocket();
    };
    const onOffline = () => {
      console.log('Network offline');
      setConnectionStatus('disconnected');
    };
    window.addEventListener('online', onOnline);
    window.addEventListener('offline', onOffline);

    return () => {
      clearInterval(heartbeatInterval);
      clearInterval(watchdogInterval);
      window.removeEventListener('online', onOnline);
      window.removeEventListener('offline', onOffline);
      if (reconnectTimer.current) clearTimeout(reconnectTimer.current);
      if (ws.current) {
        try { ws.current.close(1000, 'Component unmounted'); } catch (_) {}
      }
    };
  // eslint-disable-next-line
  }, []);

  const handleCellClick = (index) => {
    if (!isMyTurn || currentQuestion || gameState.gameStatus !== 'playing' || connectionStatus !== 'connected') {
      return;
    }

    // Can click if empty or red (error that can be conquered)
    if (gameState.board[index] !== null && gameState.boardColors[index] !== 'red') {
      return;
    }

    // Check WebSocket connection before sending
    if (!ws.current || ws.current.readyState !== WebSocket.OPEN) {
      toast({
        title: "Sem conexão",
        description: "Aguarde a reconexão para jogar",
        variant: "destructive",
        duration: 2000
      });
      return;
    }

    // Request question for this cell
    ws.current.send(JSON.stringify({
      type: 'get_question',
      room_code: roomData.room_code,
      cell_index: index,
      subject: subject
    }));
  };

  const handleAnswer = (selectedAnswer) => {
    if (!currentQuestion || !ws.current || ws.current.readyState !== WebSocket.OPEN) {
      toast({
        title: "Sem conexão",
        description: "Aguarde a reconexão para responder",
        variant: "destructive",
        duration: 2000
      });
      return;
    }

    ws.current.send(JSON.stringify({
      type: 'make_move',
      room_code: roomData.room_code,
      cell_index: selectedCell,
      selected_answer: selectedAnswer,
      question: currentQuestion
    }));
  };

  const renderCell = (index) => {
    const cellValue = gameState.board[index];
    const cellColor = gameState.boardColors[index];
    const isSelected = selectedCell === index;
    const canClick = isMyTurn && !currentQuestion && gameState.gameStatus === 'playing' && 
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
    
    // Mantém vermelho estático para células erradas (sem animação)
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

  const getMySymbol = () => {
    return gameState.playerSymbols[roomData.player_id] || '';
  };

  const getOpponentName = () => {
    const opponentId = Object.keys(gameState.players).find(id => id !== roomData.player_id);
    return opponentId ? gameState.players[opponentId] : 'Aguardando...';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-cyan-50 p-4">
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
              Sair do Jogo
            </Button>
            
            <div className="flex items-center gap-4">
              <Badge className={`${connectionStatus === 'connected' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                {connectionStatus === 'connected' ? (
                  <>
                    <Wifi className="w-4 h-4 mr-1" />
                    Conectado
                  </>
                ) : (
                  <>
                    <WifiOff className="w-4 h-4 mr-1" />
                    Desconectado
                  </>
                )}
              </Badge>
              
              <Badge className="bg-blue-100 text-blue-800">
                Sala: {roomData.room_code}
              </Badge>
            </div>
          </div>
          
          <h1 className="text-4xl font-bold text-blue-800 mb-2">
            Jogo da Velha Online
          </h1>
          <p className="text-gray-600 mb-2">
            Química • Jogo em Tempo Real
          </p>

          {waitingForPlayer ? (
            <div className="text-xl font-bold text-orange-600">
              Aguardando segundo jogador entrar...
            </div>
          ) : gameState.gameStatus === 'playing' ? (
            <div className={`text-2xl font-bold ${isMyTurn ? 'text-green-600' : 'text-orange-600'}`}>
              {isMyTurn ? "Sua vez!" : `Vez de ${getOpponentName()}`}
            </div>
          ) : null}
          
          {/* Players Display */}
          <div className="flex justify-center gap-8 mt-4">
            <div className="text-center">
              <div className="flex items-center gap-2 justify-center">
                <Crown className="w-5 h-5 text-purple-600" />
                <span className="font-bold text-lg text-purple-800">
                  {roomData.player_name} (Você)
                </span>
              </div>
              <Badge className="bg-purple-100 text-purple-800">
                Jogador {getMySymbol()}
              </Badge>
            </div>
            <div className="text-center">
              <div className="flex items-center gap-2 justify-center">
                <Crown className="w-5 h-5 text-orange-600" />
                <span className="font-bold text-lg text-orange-800">
                  {getOpponentName()}
                </span>
              </div>
              <Badge className="bg-orange-100 text-orange-800">
                Jogador {getMySymbol() === 'X' ? 'O' : 'X'}
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
                  Tabuleiro Online
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-3 gap-3 mb-6">
                  {Array.from({ length: 9 }).map((_, index) => renderCell(index))}
                </div>
                
                {gameState.gameStatus === 'won' && (
                  <div className="text-center p-4 bg-green-100 rounded-lg mb-4">
                    <Trophy className="w-12 h-12 mx-auto text-yellow-600 mb-2" />
                    <h3 className="text-xl font-bold text-green-800">
                      {gameState.winner === getMySymbol() ? 'Você venceu!' : `${getOpponentName()} venceu!`}
                    </h3>
                    <p className="text-green-600">
                      Conseguiu 3 marcas verdes em linha!
                    </p>
                  </div>
                )}

                {gameState.gameStatus === 'draw' && (
                  <div className="text-center p-4 bg-yellow-100 rounded-lg mb-4">
                    <h3 className="text-xl font-bold text-yellow-800">
                      Empate!
                    </h3>
                    <p className="text-yellow-600">
                      Tabuleiro completo, mas ninguém conseguiu 3 em linha.
                    </p>
                  </div>
                )}

                {lastMoveInfo && (
                  <div className={`text-center p-3 rounded-lg mb-4 ${
                    lastMoveInfo.isCorrect ? 'bg-green-50 border-2 border-green-200' : 'bg-red-50 border-2 border-red-200'
                  }`}>
                    <p className={`font-semibold ${lastMoveInfo.isCorrect ? 'text-green-800' : 'text-red-800'}`}>
                      {lastMoveInfo.playerName} {lastMoveInfo.isCorrect ? 'acertou! ✅' : 'errou! ❌'}
                    </p>
                    {!lastMoveInfo.isCorrect && (
                      <p className="text-red-600 text-sm mt-1">
                        <strong>Resposta correta:</strong> {lastMoveInfo.correctAnswer}
                      </p>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Question Panel */}
            <Card className="shadow-lg mt-6">
              <CardHeader className="text-center">
                <CardTitle className="text-2xl text-blue-800">
                  {subject === 'historia' && 'Desafio de História'}
                  {subject === 'quimica' && 'Desafio de Química'}
                  {subject === 'matematica' && 'Desafio de Matemática'}
                </CardTitle>
              </CardHeader>
              <CardContent>
                {!currentQuestion ? (
                  <div className="text-center py-12">
                    <div className="text-6xl mb-4">
                      {subject === 'historia' && '🏛️'}
                      {subject === 'quimica' && '🧪'}
                      {subject === 'matematica' && '🔢'}
                    </div>
                    {waitingForPlayer ? (
                      <>
                        <h3 className="text-xl font-semibold text-gray-700 mb-2">
                          Aguardando segundo jogador...
                        </h3>
                        <p className="text-gray-500">
                          Compartilhe o código da sala: <strong>{roomData.room_code}</strong>
                        </p>
                      </>
                    ) : isMyTurn ? (
                      <>
                        <h3 className="text-xl font-semibold text-gray-700 mb-2">
                          Sua vez! Clique em uma célula
                        </h3>
                        <p className="text-gray-500">
                          para responder uma pergunta sobre {subject === 'historia' && 'a História do Brasil'}
                          {subject === 'quimica' && 'Química'}
                          {subject === 'matematica' && 'Matemática'}
                        </p>
                      </>
                    ) : (
                      <>
                        <h3 className="text-xl font-semibold text-gray-700 mb-2">
                          Aguardando {getOpponentName()}
                        </h3>
                        <p className="text-gray-500">
                          Vez do adversário fazer sua jogada
                        </p>
                      </>
                    )}
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="text-center p-2 bg-purple-100 rounded-lg">
                      <span className="text-lg font-bold text-purple-800">
                        Sua pergunta:
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

          {/* Game Info */}
          <div>
            <Card className="shadow-lg">
              <CardContent className="space-y-4">
                <div className="text-center p-3 bg-blue-50 rounded-lg">
                  <p className="text-2xl font-mono text-blue-600">{roomData.room_code}</p>
                </div>
                
                <div className="text-right">
                  <p className="text-xs text-gray-500 mt-1">
                    {Object.keys(gameState.players).length}/2 jogadores
                  </p>
                </div>
              </CardContent>
            </Card>
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
                <p className="text-yellow-600">3 marcas VERDES em linha!</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default OnlineTicTacToeGame;