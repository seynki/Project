import React, { useState } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import TicTacToeGame from "./components/TicTacToeGame";
import PlayerSetup from "./components/PlayerSetup";
import { Toaster } from "./components/ui/toaster";

function App() {
  const [players, setPlayers] = useState(null);
  const [gameKey, setGameKey] = useState(0); // Para forçar re-render do jogo

  const handleStartGame = (playerNames) => {
    setPlayers(playerNames);
  };

  const handleBackToSetup = () => {
    setPlayers(null);
    setGameKey(prev => prev + 1); // Força reset completo do jogo
  };

  const handleGameEnd = (winnerName, symbol) => {
    // Aqui poderia salvar no backend
    console.log(`Jogo terminou! Vencedor: ${winnerName} (${symbol})`);
  };

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route
            path="/"
            element={
              !players ? (
                <PlayerSetup onStartGame={handleStartGame} />
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

export default App;