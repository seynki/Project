import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Users, Trophy, Play, ArrowLeft } from 'lucide-react';

const PlayerSetup = ({ onStartGame, onBackToModeSelect }) => {
  const [player1Name, setPlayer1Name] = useState('');
  const [player2Name, setPlayer2Name] = useState('');

  const handleStartGame = () => {
    if (player1Name.trim() && player2Name.trim()) {
      onStartGame({
        player1: player1Name.trim(),
        player2: player2Name.trim()
      });
    }
  };

  const isValid = player1Name.trim() && player2Name.trim();

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-yellow-50 p-4 flex items-center justify-center">
      <Card className="w-full max-w-md shadow-lg">
        <CardHeader className="text-center">
          {onBackToModeSelect && (
            <Button
              onClick={onBackToModeSelect}
              variant="outline"
              className="mb-4 self-start"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Voltar aos Modos
            </Button>
          )}
          
          <CardTitle className="text-3xl text-green-800 flex items-center justify-center gap-2 mb-2">
            <Users className="w-8 h-8" />
            Jogo Local
          </CardTitle>
          <p className="text-gray-600">Configure os jogadores para começar</p>
        </CardHeader>
        
        <CardContent className="space-y-6">
          {/* Player 1 Input */}
          <div className="space-y-2">
            <Label htmlFor="player1" className="text-lg font-semibold text-purple-800">
              <span className="inline-flex items-center gap-2">
                <span className="w-8 h-8 bg-purple-100 text-purple-800 rounded-full flex items-center justify-center font-bold">
                  X
                </span>
                Jogador 1
              </span>
            </Label>
            <Input
              id="player1"
              type="text"
              placeholder="Digite o nome do Jogador 1"
              value={player1Name}
              onChange={(e) => setPlayer1Name(e.target.value)}
              className="text-lg p-3"
              maxLength={20}
            />
          </div>

          {/* Player 2 Input */}
          <div className="space-y-2">
            <Label htmlFor="player2" className="text-lg font-semibold text-orange-800">
              <span className="inline-flex items-center gap-2">
                <span className="w-8 h-8 bg-orange-100 text-orange-800 rounded-full flex items-center justify-center font-bold">
                  O
                </span>
                Jogador 2
              </span>
            </Label>
            <Input
              id="player2"
              type="text"
              placeholder="Digite o nome do Jogador 2"
              value={player2Name}
              onChange={(e) => setPlayer2Name(e.target.value)}
              className="text-lg p-3"
              maxLength={20}
            />
          </div>

          {/* Start Game Button */}
          <Button
            onClick={handleStartGame}
            disabled={!isValid}
            className="w-full text-lg py-3 bg-green-600 hover:bg-green-700 disabled:opacity-50"
          >
            <Play className="w-5 h-5 mr-2" />
            Começar Jogo Local
          </Button>

          {/* Info */}
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <Trophy className="w-8 h-8 mx-auto text-yellow-600 mb-2" />
            <p className="text-sm text-blue-800">
              <strong>Jogo no mesmo dispositivo</strong>
            </p>
            <p className="text-xs text-blue-600 mt-1">
              Jogadores alternam no mesmo computador/celular
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default PlayerSetup;