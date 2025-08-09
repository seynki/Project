import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Badge } from './ui/badge';
import { Plus, LogIn, Copy, ArrowLeft, Loader2, Users, AlertCircle } from 'lucide-react';
import { toast } from '../hooks/use-toast';
import axios from 'axios';

const OnlineGameSetup = ({ onBackToModeSelect, onRoomCreated, onRoomJoined }) => {
  const [mode, setMode] = useState('select'); // 'select', 'create', 'join'
  const [loading, setLoading] = useState(false);
  const [roomCode, setRoomCode] = useState('');
  const [createdRoom, setCreatedRoom] = useState(null);

  // Get player name from localStorage (login)
  const playerName = localStorage.getItem('username') || 'Usuário';

  const backendUrl = process.env.REACT_APP_BACKEND_URL;

  const handleCreateRoom = async () => {
    if (!playerName.trim()) {
      toast({
        title: "Erro de autenticação",
        description: "Você precisa estar logado para criar uma sala",
        variant: "destructive"
      });
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${backendUrl}/api/rooms/create`, {
        player_name: playerName.trim()
      });

      const { room_code, player_id } = response.data;
      
      setCreatedRoom({
        room_code,
        player_id,
        player_name: playerName.trim()
      });

      toast({
        title: "Sala criada!",
        description: `Código da sala: ${room_code}. Compartilhe com seu amigo!`,
        duration: 5000
      });

      // Call parent callback
      onRoomCreated({
        room_code,
        player_id,
        player_name: playerName.trim(),
        is_creator: true
      });

    } catch (error) {
      console.error('Error creating room:', error);
      toast({
        title: "Erro ao criar sala",
        description: error.response?.data?.detail || "Tente novamente em alguns segundos",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const handleJoinRoom = async () => {
    if (!playerName.trim()) {
      toast({
        title: "Nome necessário",
        description: "Digite seu nome para entrar na sala",
        variant: "destructive"
      });
      return;
    }

    if (!roomCode.trim()) {
      toast({
        title: "Código necessário",
        description: "Digite o código da sala para entrar",
        variant: "destructive"
      });
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${backendUrl}/api/rooms/join`, {
        room_code: roomCode.trim().toUpperCase(),
        player_name: playerName.trim()
      });

      const { room_code: joinedRoomCode, player_id } = response.data;

      toast({
        title: "Entrou na sala!",
        description: `Conectado à sala ${joinedRoomCode}. Aguardando o jogo começar...`,
        duration: 3000
      });

      // Call parent callback
      onRoomJoined({
        room_code: joinedRoomCode,
        player_id,
        player_name: playerName.trim(),
        is_creator: false
      });

    } catch (error) {
      console.error('Error joining room:', error);
      const errorMessage = error.response?.data?.detail || "Erro desconhecido";
      toast({
        title: "Erro ao entrar na sala",
        description: errorMessage,
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const copyRoomCode = async () => {
    if (createdRoom) {
      try {
        await navigator.clipboard.writeText(createdRoom.room_code);
        toast({
          title: "Código copiado!",
          description: "Código da sala copiado para a área de transferência",
          duration: 2000
        });
      } catch (error) {
        toast({
          title: "Código da sala",
          description: `Compartilhe este código: ${createdRoom.room_code}`,
          duration: 4000
        });
      }
    }
  };

  if (mode === 'select') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-4 flex items-center justify-center">
        <div className="w-full max-w-4xl">
          <div className="text-center mb-8">
            <Button
              onClick={onBackToModeSelect}
              variant="outline"
              className="mb-4"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Voltar aos Modos
            </Button>
            
            <h1 className="text-4xl font-bold text-blue-800 mb-2">
              Jogo Online
            </h1>
            <p className="text-lg text-gray-600">
              Crie uma sala ou entre em uma existente
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            {/* Create Room */}
            <Card className="shadow-lg hover:shadow-xl transition-shadow cursor-pointer">
              <CardHeader className="text-center">
                <CardTitle className="text-2xl text-green-800 flex items-center justify-center gap-2 mb-2">
                  <Plus className="w-8 h-8" />
                  Criar Sala
                </CardTitle>
                <p className="text-gray-600">Crie uma nova sala de jogo</p>
              </CardHeader>
              
              <CardContent className="space-y-4">
                <div className="text-center py-4">
                  <div className="text-5xl mb-4">🏗️</div>
                  <p className="text-gray-500 mb-4">
                    Você será o jogador X e receberá um código para compartilhar
                  </p>
                </div>

                <div className="bg-green-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-green-800 mb-2">Como funciona:</h4>
                  <ul className="text-sm text-green-600 space-y-1">
                    <li>1. Digite seu nome</li>
                    <li>2. Clique em "Criar Sala"</li>
                    <li>3. Compartilhe o código com seu amigo</li>
                    <li>4. Aguarde ele entrar para começar</li>
                  </ul>
                </div>

                <Button
                  onClick={() => setMode('create')}
                  className="w-full text-lg py-3 bg-green-600 hover:bg-green-700"
                >
                  <Plus className="w-5 h-5 mr-2" />
                  Criar Nova Sala
                </Button>
              </CardContent>
            </Card>

            {/* Join Room */}
            <Card className="shadow-lg hover:shadow-xl transition-shadow cursor-pointer">
              <CardHeader className="text-center">
                <CardTitle className="text-2xl text-orange-800 flex items-center justify-center gap-2 mb-2">
                  <LogIn className="w-8 h-8" />
                  Entrar na Sala
                </CardTitle>
                <p className="text-gray-600">Use um código para entrar</p>
              </CardHeader>
              
              <CardContent className="space-y-4">
                <div className="text-center py-4">
                  <div className="text-5xl mb-4">🚪</div>
                  <p className="text-gray-500 mb-4">
                    Você será o jogador O e precisa de um código de sala
                  </p>
                </div>

                <div className="bg-orange-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-orange-800 mb-2">Como funciona:</h4>
                  <ul className="text-sm text-orange-600 space-y-1">
                    <li>1. Digite seu nome</li>
                    <li>2. Digite o código da sala</li>
                    <li>3. Clique em "Entrar na Sala"</li>
                    <li>4. O jogo começará automaticamente</li>
                  </ul>
                </div>

                <Button
                  onClick={() => setMode('join')}
                  className="w-full text-lg py-3 bg-orange-600 hover:bg-orange-700"
                >
                  <LogIn className="w-5 h-5 mr-2" />
                  Entrar em Sala
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    );
  }

  if (mode === 'create') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-50 p-4 flex items-center justify-center">
        <Card className="w-full max-w-md shadow-lg">
          <CardHeader className="text-center">
            <Button
              onClick={() => setMode('select')}
              variant="outline"
              className="mb-4 self-start"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Voltar
            </Button>
            
            <CardTitle className="text-3xl text-green-800 flex items-center justify-center gap-2 mb-2">
              <Plus className="w-8 h-8" />
              Criar Sala
            </CardTitle>
            <p className="text-gray-600">Configure sua nova sala de jogo</p>
          </CardHeader>
          
          <CardContent className="space-y-6">
            {!createdRoom ? (
              <>
                <div className="space-y-2">
                  <Label htmlFor="playerName" className="text-lg font-semibold text-green-800">
                    Seu Nome
                  </Label>
                  <Input
                    id="playerName"
                    type="text"
                    value={playerName}
                    className="text-lg p-3 bg-gray-100"
                    disabled={true}
                    readOnly
                  />
                </div>

                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <Users className="w-8 h-8 mx-auto text-green-600 mb-2" />
                  <p className="text-sm text-green-800">
                    <strong>Você será o Jogador X</strong>
                  </p>
                  <p className="text-xs text-green-600 mt-1">
                    O primeiro jogador sempre começa
                  </p>
                </div>

                <Button
                  onClick={handleCreateRoom}
                  disabled={loading}
                  className="w-full text-lg py-3 bg-green-600 hover:bg-green-700 disabled:opacity-50"
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      Criando Sala...
                    </>
                  ) : (
                    <>
                      <Plus className="w-5 h-5 mr-2" />
                      Criar Sala
                    </>
                  )}
                </Button>
              </>
            ) : (
              <>
                <div className="text-center p-6 bg-green-100 rounded-lg">
                  <div className="text-4xl mb-4">🎉</div>
                  <h3 className="text-xl font-bold text-green-800 mb-2">
                    Sala Criada!
                  </h3>
                  <p className="text-green-600 mb-4">
                    Compartilhe este código com seu amigo:
                  </p>
                  
                  <div className="flex items-center justify-center gap-2 mb-4">
                    <Badge className="text-2xl py-2 px-4 bg-green-600 text-white">
                      {createdRoom.room_code}
                    </Badge>
                    <Button
                      onClick={copyRoomCode}
                      variant="outline"
                      size="sm"
                    >
                      <Copy className="w-4 h-4" />
                    </Button>
                  </div>
                  
                  <p className="text-sm text-green-600">
                    Aguardando o segundo jogador entrar...
                  </p>
                </div>

                <div className="text-center p-4 bg-yellow-50 rounded-lg border border-yellow-200">
                  <AlertCircle className="w-6 h-6 mx-auto text-yellow-600 mb-2" />
                  <p className="text-sm text-yellow-800">
                    <strong>Mantenha esta página aberta!</strong><br />
                    O jogo começará automaticamente quando seu amigo entrar.
                  </p>
                </div>
              </>
            )}
          </CardContent>
        </Card>
      </div>
    );
  }

  if (mode === 'join') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 to-amber-50 p-4 flex items-center justify-center">
        <Card className="w-full max-w-md shadow-lg">
          <CardHeader className="text-center">
            <Button
              onClick={() => setMode('select')}
              variant="outline"
              className="mb-4 self-start"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Voltar
            </Button>
            
            <CardTitle className="text-3xl text-orange-800 flex items-center justify-center gap-2 mb-2">
              <LogIn className="w-8 h-8" />
              Entrar na Sala
            </CardTitle>
            <p className="text-gray-600">Entre em uma sala existente</p>
          </CardHeader>
          
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="playerName" className="text-lg font-semibold text-orange-800">
                Seu Nome
              </Label>
              <Input
                id="playerName"
                type="text"
                value={playerName}
                className="text-lg p-3 bg-gray-100"
                disabled={true}
                readOnly
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="roomCode" className="text-lg font-semibold text-orange-800">
                Código da Sala
              </Label>
              <Input
                id="roomCode"
                type="text"
                placeholder="Digite o código (ex: ABC123)"
                value={roomCode}
                onChange={(e) => setRoomCode(e.target.value.toUpperCase())}
                className="text-lg p-3 font-mono"
                maxLength={6}
                disabled={loading}
              />
            </div>

            <div className="text-center p-4 bg-orange-50 rounded-lg">
              <Users className="w-8 h-8 mx-auto text-orange-600 mb-2" />
              <p className="text-sm text-orange-800">
                <strong>Você será o Jogador O</strong>
              </p>
              <p className="text-xs text-orange-600 mt-1">
                Aguardará sua vez após o jogador X
              </p>
            </div>

            <Button
              onClick={handleJoinRoom}
              disabled={!roomCode.trim() || loading}
              className="w-full text-lg py-3 bg-orange-600 hover:bg-orange-700 disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                  Entrando...
                </>
              ) : (
                <>
                  <LogIn className="w-5 h-5 mr-2" />
                  Entrar na Sala
                </>
              )}
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }
};

export default OnlineGameSetup;