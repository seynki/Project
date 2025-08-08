import React, { useState } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import TicTacToeGame from "./components/TicTacToeGame";
import PlayerSetup from "./components/PlayerSetup";
import GameModeSelector from "./components/GameModeSelector";
import OnlineGameSetup from "./components/OnlineGameSetup";
import OnlineTicTacToeGame from "./components/OnlineTicTacToeGame";
import { Toaster } from "./components/ui/toaster";

function App() {
  const [gameMode, setGameMode] = useState('select'); // 'select', 'local', 'online'
  const [players, setPlayers] = useState(null);
  const [gameKey, setGameKey] = useState(0); // Para forçar re-render do jogo
  const [onlineRoom, setOnlineRoom] = useState(null);

  const handleSelectMode = (mode) => {
    setGameMode(mode);
    setPlayers(null);
    setOnlineRoom(null);
  };

  const handleStartLocalGame = (playerNames) => {
    setPlayers(playerNames);
  };

  const handleBackToSetup = () => {
    if (gameMode === 'local') {
      setPlayers(null);
      setGameKey(prev => prev + 1); // Força reset completo do jogo
    } else if (gameMode === 'online') {
      setOnlineRoom(null);
    }
  };

  const handleBackToModeSelect = () => {
    setGameMode('select');
    setPlayers(null);
    setOnlineRoom(null);
    setGameKey(prev => prev + 1);
  };

  const handleGameEnd = (winnerName, symbol) => {
    // Aqui poderia salvar no backend
    console.log(`Jogo terminou! Vencedor: ${winnerName} (${symbol})`);
  };

  const handleRoomCreated = (roomData) => {
    setOnlineRoom(roomData);
  };

  const handleRoomJoined = (roomData) => {
    setOnlineRoom(roomData);
  };

  const handleOnlineDisconnect = () => {
    setOnlineRoom(null);
  };

  // Game Mode Selection
  if (gameMode === 'select') {
    return (
      <div className="App">
        <GameModeSelector onSelectMode={handleSelectMode} />
        <Toaster />
      </div>
    );
  }

  // Local Game Mode
  if (gameMode === 'local') {
    return (
      <div className="App">
        <BrowserRouter>
          <Routes>
            <Route
              path="/"
              element={
                !players ? (
                  <PlayerSetup 
                    onStartGame={handleStartLocalGame}
                    onBackToModeSelect={handleBackToModeSelect}
                  />
                ) : (
                  <TicTacToeGame
                    key={gameKey}
                    players={players}
                    onBackToSetup={handleBackToSetup}
                    onGameEnd={handleGameEnd}
                  />
                )
              }
            />
          </Routes>
        </BrowserRouter>
        <Toaster />
      </div>
    );
  }

  // Online Game Mode
  if (gameMode === 'online') {
    return (
      <div className="App">
        {!onlineRoom ? (
          <OnlineGameSetup
            onBackToModeSelect={handleBackToModeSelect}
            onRoomCreated={handleRoomCreated}
            onRoomJoined={handleRoomJoined}
          />
        ) : (
          <OnlineTicTacToeGame
            roomData={onlineRoom}
            onBackToSetup={handleBackToSetup}
            onDisconnect={handleOnlineDisconnect}
          />
        )}
        <Toaster />
      </div>
    );
  }

  return (
    <div className="App">
      <div className="min-h-screen bg-gradient-to-br from-red-50 to-orange-50 p-4 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-red-800 mb-4">Erro</h1>
          <p className="text-red-600 mb-4">Estado de jogo inválido</p>
          <button 
            onClick={handleBackToModeSelect}
            className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Voltar ao Início
          </button>
        </div>
      </div>
      <Toaster />
    </div>
  );
}

export default App;