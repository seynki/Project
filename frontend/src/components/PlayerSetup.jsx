import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Users, Trophy, Play, ArrowLeft } from 'lucide-react';

const PlayerSetup = ({ onStartGame, onBackToModeSelect }) => {
  const handleStartGame = () => {
    onStartGame({
      player1: 'X',
      player2: 'O'
    });
  };

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
          <p className="text-gray-600">Jogue no mesmo dispositivo</p>
        </CardHeader>
        
        <CardContent className="space-y-6">
          {/* Players Info */}
          <div className="space-y-4">
            <div className="flex items-center justify-center gap-4 p-4 bg-purple-50 rounded-lg">
              <span className="w-12 h-12 bg-purple-100 text-purple-800 rounded-full flex items-center justify-center font-bold text-xl">
                X
              </span>
              <span className="text-lg font-semibold text-purple-800">Jogador X</span>
            </div>
            
            <div className="text-center text-gray-500 font-semibold">VS</div>
            
            <div className="flex items-center justify-center gap-4 p-4 bg-orange-50 rounded-lg">
              <span className="w-12 h-12 bg-orange-100 text-orange-800 rounded-full flex items-center justify-center font-bold text-xl">
                O
              </span>
              <span className="text-lg font-semibold text-orange-800">Jogador O</span>
            </div>
          </div>

          {/* Start Game Button */}
          <Button
            onClick={handleStartGame}
            className="w-full text-lg py-3 bg-green-600 hover:bg-green-700"
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