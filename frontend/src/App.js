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
  const [gameMode, setGameMode] = useState('menu'); // 'menu', 'local', 'online'
  const [players, setPlayers] = useState(null);
  const [gameKey, setGameKey] = useState(0);
  const [onlineGameData, setOnlineGameData] = useState(null);

  const handleSelectMode = (mode) => {
    setGameMode(mode);
    setPlayers(null);
    setOnlineGameData(null);
  };

  const handleStartLocalGame = (playerNames) => {
    setPlayers(playerNames);
  };

  const handleStartOnlineGame = (gameData) => {
    setOnlineGameData(gameData);
  };

  const handleBackToSetup = () => {
    if (gameMode === 'local') {
      setPlayers(null);
      setGameKey(prev => prev + 1);
    } else if (gameMode === 'online') {
      setOnlineGameData(null);
    }
  };

  const handleBackToMenu = () => {
    setGameMode('menu');
    setPlayers(null);
    setOnlineGameData(null);
    setGameKey(prev => prev + 1);
  };

  const handleGameEnd = (winnerName, symbol) => {
    console.log(`Jogo terminou! Vencedor: ${winnerName} (${symbol})`);
  };

  const renderContent = () => {
    // Game Mode Selection
    if (gameMode === 'menu') {
      return <GameModeSelector onSelectMode={handleSelectMode} />;
    }

    // Local Mode
    if (gameMode === 'local') {
      if (!players) {
        return <PlayerSetup onStartGame={handleStartLocalGame} onBackToMenu={handleBackToMenu} />;
      }
      return (
        <TicTacToeGame
          key={gameKey}
          players={players}
          onBackToSetup={handleBackToSetup}
          onGameEnd={handleGameEnd}
        />
      );
    }

    // Online Mode
    if (gameMode === 'online') {
      if (!onlineGameData) {
        return <OnlineGameSetup onStartGame={handleStartOnlineGame} onBackToMenu={handleBackToMenu} />;
      }
      return (
        <OnlineTicTacToeGame
          gameData={onlineGameData}
          onBackToSetup={handleBackToSetup}
        />
      );
    }

    return <GameModeSelector onSelectMode={handleSelectMode} />;
  };

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={renderContent()} />
        </Routes>
      </BrowserRouter>
      <Toaster />
    </div>
  );
}

export default App;