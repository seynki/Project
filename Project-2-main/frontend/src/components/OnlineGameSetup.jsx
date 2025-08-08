import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Users, Trophy, Play, Plus, UserPlus, Wifi, WifiOff, Copy } from 'lucide-react';
import { toast } from '../hooks/use-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const OnlineGameSetup = ({ onStartGame, onBackToMenu }) => {
  const [playerName, setPlayerName] = useState('');
  const [roomCode, setRoomCode] = useState('');
  const [mode, setMode] = useState('menu'); // 'menu', 'create', 'join', 'waiting'
  const [currentRoom, setCurrentRoom] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  const createRoom = async () => {
    if (!playerName.trim()) {
      toast({
        title: "Nome obrigatório",
        description: "Digite seu nome para criar a sala",
        duration: 3000,
      });
      return;
    }

    try {
      const response = await fetch(`${BACKEND_URL}/api/game/create-room`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_name: playerName.trim() })
      });
      
      const data = await response.json();
      
      if (data.success) {
        setCurrentRoom(data.room);
        setMode('waiting');
        setIsConnected(true);
        
        toast({
          title: "Sala criada! 🎉",
          description: `Código: ${data.room_code}. Compartilhe com seu amigo!`,
          duration: 5000,
        });
      }
    } catch (error) {
      console.error('Error creating room:', error);
      toast({
        title: "Erro ao criar sala",
        description: "Tente novamente em alguns segundos",
        duration: 3000,
      });
    }
  };

  const joinRoom = async () => {
    if (!playerName.trim() || !roomCode.trim()) {
      toast({
        title: "Dados obrigatórios",
        description: "Digite seu nome e o código da sala",
        duration: 3000,
      });
      return;
    }

    try {
      const response = await fetch(`${BACKEND_URL}/api/game/join-room`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          room_code: roomCode.trim().toUpperCase(),
          player_name: playerName.trim()
        })
      });
      
      if (!response.ok) {
        throw new Error('Room not found or full');
      }
      
      const data = await response.json();
      
      if (data.success) {
        setCurrentRoom(data.room);
        setIsConnected(true);
        
        // Start game immediately when both players are present
        onStartGame({
          room: data.room,
          playerName: playerName.trim(),
          mode: 'online'
        });
        
        toast({
          title: "Conectado à sala! 🎮",
          description: "Jogo iniciado com sucesso!",
          duration: 3000,
        });
      }
    } catch (error) {
      console.error('Error joining room:', error);
      toast({
        title: "Erro ao entrar na sala",
        description: "Código inválido ou sala cheia",
        duration: 3000,
      });
    }
  };

  const copyRoomCode = () => {
    if (currentRoom) {
      navigator.clipboard.writeText(currentRoom.code);
      toast({
        title: "Código copiado! 📋",
        description: "Cole no WhatsApp e envie para seu amigo",
        duration: 2000,
      });
    }
  };

  const startGameWhenReady = () => {
    if (currentRoom && currentRoom.player1 && currentRoom.player2) {
      onStartGame({
        room: currentRoom,
        playerName: playerName.trim(),
        mode: 'online'
      });
    }
  };

  // Connection indicator
  const ConnectionStatus = () => (
    <div className="flex items-center gap-2 mb-4">
      {isConnected ? (
        <>
          <Wifi className="w-4 h-4 text-green-600" />
          <span className="text-sm text-green-600">Online</span>
        </>
      ) : (
        <>
          <WifiOff className="w-4 h-4 text-gray-400" />
          <span className="text-sm text-gray-400">Offline</span>
        </>
      )}
    </div>
  );

  const renderMenu = () => (
    <CardContent className="space-y-6">
      <ConnectionStatus />
      
      {/* Player Name Input */}
      <div className="space-y-2">
        <Label htmlFor="playerName" className="text-lg font-semibold text-blue-800">
          Seu Nome
        </Label>
        <Input
          id="playerName"
          type="text"
          placeholder="Digite seu nome"
          value={playerName}
          onChange={(e) => setPlayerName(e.target.value)}
          className="text-lg p-3"
          maxLength={20}
        />
      </div>

      {/* Action Buttons */}
      <div className="grid gap-4">
        <Button
          onClick={() => setMode('create')}
          className="w-full text-lg py-4 bg-green-600 hover:bg-green-700"
        >
          <Plus className="w-5 h-5 mr-2" />
          Criar Sala
        </Button>
        
        <Button
          onClick={() => setMode('join')}
          variant="outline"
          className="w-full text-lg py-4 border-2 border-blue-600 text-blue-600 hover:bg-blue-50"
        >
          <UserPlus className="w-5 h-5 mr-2" />
          Entrar na Sala
        </Button>
      </div>

      <Button
        onClick={onBackToMenu}
        variant="outline"
        className="w-full"
      >
        Voltar ao Menu
      </Button>
    </CardContent>
  );

  const renderCreate = () => (
    <CardContent className="space-y-6">
      <ConnectionStatus />
      
      <div className="text-center">
        <div className="text-6xl mb-4">🎮</div>
        <h3 className="text-xl font-semibold text-gray-700 mb-2">
          Criar Nova Sala
        </h3>
        <p className="text-gray-500">
          Você será o jogador X e aguardará alguém entrar
        </p>
      </div>

      <Button
        onClick={createRoom}
        disabled={!playerName.trim()}
        className="w-full text-lg py-3 bg-green-600 hover:bg-green-700"
      >
        <Play className="w-5 h-5 mr-2" />
        Criar Sala
      </Button>

      <Button
        onClick={() => setMode('menu')}
        variant="outline"
        className="w-full"
      >
        Voltar
      </Button>
    </CardContent>
  );

  const renderJoin = () => (
    <CardContent className="space-y-6">
      <ConnectionStatus />
      
      <div className="space-y-2">
        <Label htmlFor="roomCode" className="text-lg font-semibold text-orange-800">
          Código da Sala
        </Label>
        <Input
          id="roomCode"
          type="text"
          placeholder="Ex: ABC123"
          value={roomCode}
          onChange={(e) => setRoomCode(e.target.value.toUpperCase())}
          className="text-lg p-3 text-center font-mono"
          maxLength={6}
        />
      </div>

      <Button
        onClick={joinRoom}
        disabled={!playerName.trim() || !roomCode.trim()}
        className="w-full text-lg py-3 bg-orange-600 hover:bg-orange-700"
      >
        <UserPlus className="w-5 h-5 mr-2" />
        Entrar na Sala
      </Button>

      <Button
        onClick={() => setMode('menu')}
        variant="outline"
        className="w-full"
      >
        Voltar
      </Button>
    </CardContent>
  );

  const renderWaiting = () => (
    <CardContent className="space-y-6">
      <ConnectionStatus />
      
      <div className="text-center">
        <div className="text-6xl mb-4 animate-bounce">⏳</div>
        <h3 className="text-xl font-semibold text-gray-700 mb-2">
          Aguardando Jogador...
        </h3>
        <p className="text-gray-500 mb-4">
          Compartilhe o código abaixo com seu amigo
        </p>
        
        {currentRoom && (
          <div className="p-4 bg-blue-50 rounded-lg border-2 border-blue-200">
            <p className="text-sm text-blue-600 mb-2">Código da Sala:</p>
            <div className="flex items-center justify-center gap-2">
              <span className="text-3xl font-mono font-bold text-blue-800">
                {currentRoom.code}
              </span>
              <Button
                onClick={copyRoomCode}
                size="sm"
                variant="outline"
                className="ml-2"
              >
                <Copy className="w-4 h-4" />
              </Button>
            </div>
          </div>
        )}
        
        <div className="mt-4">
          <p className="text-sm text-gray-600">
            Você será o <strong className="text-purple-600">Jogador X</strong>
          </p>
        </div>
      </div>

      <Button
        onClick={() => setMode('menu')}
        variant="outline"
        className="w-full"
      >
        Cancelar
      </Button>
    </CardContent>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-4 flex items-center justify-center">
      <Card className="w-full max-w-md shadow-lg">
        <CardHeader className="text-center">
          <CardTitle className="text-3xl text-blue-800 flex items-center justify-center gap-2 mb-2">
            <Users className="w-8 h-8" />
            Multiplayer Online
          </CardTitle>
          <p className="text-gray-600">
            {mode === 'menu' && 'Jogue com amigos pela internet'}
            {mode === 'create' && 'Crie uma sala e convide um amigo'}
            {mode === 'join' && 'Entre na sala do seu amigo'}
            {mode === 'waiting' && 'Aguardando segundo jogador...'}
          </p>
        </CardHeader>
        
        {mode === 'menu' && renderMenu()}
        {mode === 'create' && renderCreate()}
        {mode === 'join' && renderJoin()}
        {mode === 'waiting' && renderWaiting()}
      </Card>
    </div>
  );
};

export default OnlineGameSetup;