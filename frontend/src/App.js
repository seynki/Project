import React, { useState } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import TicTacToeGame from "./components/TicTacToeGame";
import PlayerSetup from "./components/PlayerSetup";
import GameModeSelector from "./components/GameModeSelector";
import OnlineGameSetup from "./components/OnlineGameSetup";
import OnlineTicTacToeGame from "./components/OnlineTicTacToeGame";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import SubjectSelector from "./components/SubjectSelector";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import { Toaster } from "./components/ui/toaster";

function AppContent() {
  const { user, isAuthenticated, isLoading, login, logout } = useAuth();
  const [currentView, setCurrentView] = useState('dashboard'); // 'dashboard', 'subjects', 'game'
  const [gameMode, setGameMode] = useState('select'); // 'select', 'local', 'online'
  const [players, setPlayers] = useState(null);
  const [gameKey, setGameKey] = useState(0);
  const [onlineRoom, setOnlineRoom] = useState(null);
  const [selectedSubject, setSelectedSubject] = useState(null);

  // Authentication loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center">
        <div className="text-white text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p className="text-lg">Carregando...</p>
        </div>
      </div>
    );
  }

  // Show login if not authenticated
  if (!isAuthenticated) {
    return <Login onLoginSuccess={login} />;
  }

  // Authenticated user views
  const handleSelectTicTacToe = () => {
    setCurrentView('subjects');
  };

  const handleSelectSubject = (subjectId) => {
    if (subjectId === 'historia' || subjectId === 'quimica') {
      setSelectedSubject(subjectId);
      setCurrentView('game');
      setGameMode('select');
    }
  };

  const handleBackToDashboard = () => {
    setCurrentView('dashboard');
    setGameMode('select');
    setPlayers(null);
    setOnlineRoom(null);
    setSelectedSubject(null);
    setGameKey(prev => prev + 1);
  };

  const handleBackToSubjects = () => {
    setCurrentView('subjects');
    setGameMode('select');
    setPlayers(null);
    setOnlineRoom(null);
    setGameKey(prev => prev + 1);
  };

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
      setGameKey(prev => prev + 1);
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

  // Dashboard view
  if (currentView === 'dashboard') {
    return <Dashboard user={user} onLogout={logout} onSelectTicTacToe={handleSelectTicTacToe} />;
  }

  // Subject selection view
  if (currentView === 'subjects') {
    return <SubjectSelector onSelectSubject={handleSelectSubject} onBack={handleBackToDashboard} />;
  }

  // Game views (História or Química)
  if (currentView === 'game' && (selectedSubject === 'historia' || selectedSubject === 'quimica')) {
    const subjectTitles = {
      'historia': 'História do Brasil',
      'quimica': 'Química'
    };
    
    const subjectColors = {
      'historia': 'from-yellow-50 to-orange-50',
      'quimica': 'from-purple-50 to-pink-50'
    };
    // Game Mode Selection for selected subject
    if (gameMode === 'select') {
      return (
        <div className="App">
          <div className={`min-h-screen bg-gradient-to-br ${subjectColors[selectedSubject]}`}>
            <div className="container mx-auto px-6 py-8">
              <div className="mb-6">
                <button
                  onClick={handleBackToSubjects}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg flex items-center gap-2 transition-colors"
                >
                  ← Voltar às Matérias
                </button>
              </div>
              
              <div className="text-center mb-8">
                <h1 className="text-4xl font-bold text-gray-800 mb-2">{subjectTitles[selectedSubject]}</h1>
                <p className="text-gray-600 text-lg">Escolha o modo de jogo</p>
              </div>
              
              <GameModeSelector onSelectMode={handleSelectMode} />
            </div>
          </div>
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
                    <div className={`min-h-screen bg-gradient-to-br ${subjectColors[selectedSubject]}`}>
                      <div className="container mx-auto px-6 py-8">
                        <div className="mb-6">
                          <button
                            onClick={handleBackToModeSelect}
                            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg flex items-center gap-2 transition-colors"
                          >
                            ← Voltar aos Modos
                          </button>
                        </div>
                        <PlayerSetup 
                          onStartGame={handleStartLocalGame}
                          onBackToModeSelect={handleBackToModeSelect}
                        />
                      </div>
                    </div>
                  ) : (
                    <TicTacToeGame
                      key={gameKey}
                      players={players}
                      onBackToSetup={handleBackToSetup}
                      onGameEnd={handleGameEnd}
                      subject={selectedSubject}
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
          <div className="min-h-screen bg-gradient-to-br from-yellow-50 to-orange-50">
            {!onlineRoom ? (
              <div className="container mx-auto px-6 py-8">
                <div className="mb-6">
                  <button
                    onClick={handleBackToModeSelect}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg flex items-center gap-2 transition-colors"
                  >
                    ← Voltar aos Modos
                  </button>
                </div>
                <OnlineGameSetup
                  onBackToModeSelect={handleBackToModeSelect}
                  onRoomCreated={handleRoomCreated}
                  onRoomJoined={handleRoomJoined}
                />
              </div>
            ) : (
              <OnlineTicTacToeGame
                roomData={onlineRoom}
                onBackToSetup={handleBackToSetup}
                onDisconnect={handleOnlineDisconnect}
              />
            )}
          </div>
          <Toaster />
        </div>
      );
    }
  }

  // Fallback error state
  return (
    <div className="App">
      <div className="min-h-screen bg-gradient-to-br from-red-50 to-orange-50 p-4 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-red-800 mb-4">Erro</h1>
          <p className="text-red-600 mb-4">Estado da aplicação inválido</p>
          <button 
            onClick={handleBackToDashboard}
            className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Voltar ao Dashboard
          </button>
        </div>
      </div>
      <Toaster />
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;