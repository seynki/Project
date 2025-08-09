import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Users, Globe, Play, Wifi } from 'lucide-react';

const GameModeSelector = ({ onSelectMode }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-4 flex items-center justify-center">
      <div className="w-full max-w-4xl">
        <div className="text-center mb-8">
          <h1 className="text-5xl font-extrabold tracking-tight text-slate-800 mb-2">
            Jogo da Velha
          </h1>
          <p className="text-lg text-slate-600">
            Escolha o modo de jogo
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Local Game Mode */}
          <Card className="shadow-xl hover:shadow-2xl transition-all duration-200 cursor-pointer border border-slate-200/70 backdrop-blur-sm bg-white/90">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl text-purple-800 flex items-center justify-center gap-2 mb-2">
                <Users className="w-8 h-8" />
                Jogo Local
              </CardTitle>
              <p className="text-gray-600">Jogadores no mesmo dispositivo</p>
            </CardHeader>
            
            <CardContent className="space-y-4">
              <div className="text-center py-6">
                <div className="text-6xl mb-4">👥</div>
                <h3 className="text-xl font-semibold text-gray-700 mb-2">
                  2 Jogadores Locais
                </h3>
                <p className="text-gray-500 mb-4">
                  Joguem juntos usando o mesmo computador ou celular
                </p>
              </div>

              <div className="bg-purple-50 p-4 rounded-lg">
                <h4 className="font-semibold text-purple-800 mb-2">Vantagens:</h4>
                <ul className="text-sm text-purple-600 space-y-1">
                  <li>• Jogo instantâneo, sem espera</li>
                  <li>• Não precisa de internet</li>
                  <li>• Ideal para jogar pessoalmente</li>
                </ul>
              </div>

              <Button
                onClick={() => onSelectMode('local')}
                className="w-full text-lg py-3 bg-purple-600 hover:bg-purple-700"
              >
                <Play className="w-5 h-5 mr-2" />
                Jogar Localmente
              </Button>
            </CardContent>
          </Card>

          {/* Online Game Mode */}
          <Card className="shadow-xl hover:shadow-2xl transition-all duration-200 cursor-pointer border border-slate-200/70 backdrop-blur-sm bg-white/90">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl text-blue-800 flex items-center justify-center gap-2 mb-2">
                <Globe className="w-8 h-8" />
                Jogo Online
              </CardTitle>
              <p className="text-gray-600">Jogadores em dispositivos diferentes</p>
            </CardHeader>
            
            <CardContent className="space-y-4">
              <div className="text-center py-6">
                <div className="text-6xl mb-4">🌐</div>
                <h3 className="text-xl font-semibold text-gray-700 mb-2">
                  2 Jogadores Online
                </h3>
                <p className="text-gray-500 mb-4">
                  Joguem à distância em tempo real
                </p>
              </div>

              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-semibold text-blue-800 mb-2">Vantagens:</h4>
                <ul className="text-sm text-blue-600 space-y-1">
                  <li>• Jogue com amigos à distância</li>
                  <li>• Compartilhe código da sala</li>
                  <li>• Jogo simultâneo em tempo real</li>
                </ul>
              </div>

              <Button
                onClick={() => onSelectMode('online')}
                className="w-full text-lg py-3 bg-blue-600 hover:bg-blue-700"
              >
                <Wifi className="w-5 h-5 mr-2" />
                Jogar Online
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Help Text */}
        <div className="text-center mt-8 p-4 bg-white/50 rounded-lg">
          <p className="text-sm text-gray-600">
            <strong>História do Brasil:</strong> Responda perguntas sobre o período de 1500 até a Primeira República
          </p>
        </div>
      </div>
    </div>
  );
};

export default GameModeSelector;