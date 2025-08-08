import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Users, Wifi, Monitor, Trophy } from 'lucide-react';

const GameModeSelector = ({ onSelectMode }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-yellow-50 p-4 flex items-center justify-center">
      <Card className="w-full max-w-2xl shadow-lg">
        <CardHeader className="text-center">
          <CardTitle className="text-4xl text-green-800 flex items-center justify-center gap-2 mb-2">
            <Trophy className="w-10 h-10" />
            Jogo da Velha Histórico
          </CardTitle>
          <p className="text-gray-600 text-lg">
            Escolha como deseja jogar
          </p>
        </CardHeader>
        
        <CardContent className="space-y-6">
          <div className="grid md:grid-cols-2 gap-6">
            {/* Local Mode */}
            <Card className="cursor-pointer hover:shadow-lg transition-all duration-200 border-2 hover:border-green-400">
              <CardContent className="p-6 text-center" onClick={() => onSelectMode('local')}>
                <Monitor className="w-16 h-16 mx-auto text-green-600 mb-4" />
                <h3 className="text-xl font-bold text-green-800 mb-2">
                  Local
                </h3>
                <p className="text-gray-600 mb-4">
                  Jogue no mesmo computador com um amigo
                </p>
                <div className="space-y-2 text-sm text-gray-500">
                  <p>✓ Sem necessidade de internet</p>
                  <p>✓ Jogo instantâneo</p>
                  <p>✓ Perfeito para sala de aula</p>
                </div>
                <Button className="w-full mt-4 bg-green-600 hover:bg-green-700">
                  <Users className="w-4 h-4 mr-2" />
                  Jogar Local
                </Button>
              </CardContent>
            </Card>

            {/* Online Mode */}
            <Card className="cursor-pointer hover:shadow-lg transition-all duration-200 border-2 hover:border-blue-400">
              <CardContent className="p-6 text-center" onClick={() => onSelectMode('online')}>
                <Wifi className="w-16 h-16 mx-auto text-blue-600 mb-4" />
                <h3 className="text-xl font-bold text-blue-800 mb-2">
                  Online
                </h3>
                <p className="text-gray-600 mb-4">
                  Jogue com amigos pela internet
                </p>
                <div className="space-y-2 text-sm text-gray-500">
                  <p>✓ Salas com códigos únicos</p>
                  <p>✓ Ranking global real</p>
                  <p>✓ Jogue à distância</p>
                </div>
                <Button className="w-full mt-4 bg-blue-600 hover:bg-blue-700">
                  <Wifi className="w-4 h-4 mr-2" />
                  Jogar Online
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Info Section */}
          <div className="text-center p-4 bg-yellow-50 rounded-lg border border-yellow-200">
            <Trophy className="w-8 h-8 mx-auto text-yellow-600 mb-2" />
            <p className="text-sm text-yellow-800">
              <strong>Como funciona:</strong> Responda perguntas de História do Brasil para marcar células no tabuleiro. 
              Resposta correta = marca verde. Resposta incorreta = marca vermelha (pode ser conquistada!). 
              Vence quem fizer 3 marcas verdes em linha.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default GameModeSelector;