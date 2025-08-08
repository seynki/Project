import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Trophy, Medal, Award, TrendingUp, Crown } from 'lucide-react';

const OnlineGlobalRanking = ({ currentPlayers = [], ranking = [] }) => {
  const getRankIcon = (position) => {
    switch (position) {
      case 1:
        return <Trophy className="w-6 h-6 text-yellow-500" />;
      case 2:
        return <Medal className="w-6 h-6 text-gray-400" />;
      case 3:
        return <Award className="w-6 h-6 text-amber-600" />;
      default:
        return <span className="w-6 h-6 flex items-center justify-center text-gray-500 font-bold">{position}</span>;
    }
  };

  const getBadgeColor = (position) => {
    switch (position) {
      case 1:
        return "bg-yellow-100 text-yellow-800 border-yellow-300";
      case 2:
        return "bg-gray-100 text-gray-800 border-gray-300";
      case 3:
        return "bg-amber-100 text-amber-800 border-amber-300";
      default:
        return "bg-blue-100 text-blue-800 border-blue-300";
    }
  };

  const isCurrentPlayer = (playerName) => {
    return currentPlayers.includes(playerName);
  };

  if (ranking.length === 0) {
    return (
      <Card className="shadow-lg">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl text-green-800 flex items-center justify-center gap-2">
            <TrendingUp className="w-6 h-6" />
            Ranking Online
          </CardTitle>
          <p className="text-gray-600">Carregando estatísticas...</p>
        </CardHeader>
        
        <CardContent>
          <div className="text-center py-8">
            <div className="animate-spin w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full mx-auto mb-4"></div>
            <p className="text-gray-500">Buscando dados do ranking...</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="shadow-lg">
      <CardHeader className="text-center">
        <CardTitle className="text-2xl text-green-800 flex items-center justify-center gap-2">
          <TrendingUp className="w-6 h-6" />
          Ranking Global Online
        </CardTitle>
        <p className="text-gray-600">Top jogadores de todos os tempos</p>
      </CardHeader>
      
      <CardContent>
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {ranking.map((player, index) => {
            const position = index + 1;
            const isCurrent = isCurrentPlayer(player.name);
            
            return (
              <div
                key={player._id || player.id || index}
                className={`flex items-center justify-between p-3 rounded-lg border transition-all duration-200 ${
                  isCurrent 
                    ? 'bg-green-50 border-green-200 ring-2 ring-green-300' 
                    : 'bg-white border-gray-200 hover:bg-gray-50'
                }`}
              >
                <div className="flex items-center gap-3">
                  {getRankIcon(position)}
                  <div>
                    <div className="flex items-center gap-2">
                      <span className={`font-semibold ${isCurrent ? 'text-green-800' : 'text-gray-800'}`}>
                        {player.name}
                      </span>
                      {isCurrent && (
                        <Badge variant="outline" className="bg-green-100 text-green-700 text-xs">
                          <Crown className="w-3 h-3 mr-1" />
                          Jogando
                        </Badge>
                      )}
                    </div>
                    <div className="text-sm text-gray-500">
                      {player.games} jogos • {player.wins} vitórias • {player.losses || 0} derrotas
                    </div>
                  </div>
                </div>
                
                <div className="text-right">
                  <Badge className={`${getBadgeColor(position)} font-bold`}>
                    {player.points} pts
                  </Badge>
                  <div className="text-xs text-gray-500 mt-1">
                    {player.win_rate?.toFixed(1) || 0}% vitórias
                  </div>
                </div>
              </div>
            );
          })}
        </div>
        
        {ranking.length > 0 && (
          <div className="mt-4 p-3 bg-blue-50 rounded-lg text-center">
            <p className="text-sm text-blue-800">
              <strong>{ranking.length}</strong> jogadores registrados
            </p>
            <p className="text-xs text-blue-600 mt-1">
              Pontuação atualizada em tempo real • +1 ponto por vitória
            </p>
          </div>
        )}

        {ranking.length === 0 && (
          <div className="mt-4 p-3 bg-yellow-50 rounded-lg text-center">
            <Trophy className="w-8 h-8 mx-auto text-yellow-600 mb-2" />
            <p className="text-sm text-yellow-800">
              Seja o primeiro no ranking!
            </p>
            <p className="text-xs text-yellow-600 mt-1">
              Vença jogos para ganhar pontos
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default OnlineGlobalRanking;