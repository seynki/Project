import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Trophy, Medal, Award, TrendingUp, Loader2 } from 'lucide-react';

const GlobalRanking = ({ currentPlayers = null }) => {
  const [rankings, setRankings] = useState([]);
  const [loading, setLoading] = useState(true);

  const backendUrl = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    fetchRankings();
  }, []);

  const fetchRankings = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${backendUrl}/api/rankings`);
      if (response.ok) {
        const data = await response.json();
        setRankings(data.rankings);
      } else {
        console.error('Failed to fetch rankings');
      }
    } catch (error) {
      console.error('Error fetching rankings:', error);
    } finally {
      setLoading(false);
    }
  };
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
    return currentPlayers && (
      playerName === currentPlayers.player1 || 
      playerName === currentPlayers.player2
    );
  };

  return (
    <Card className="shadow-lg">
      <CardHeader className="text-center">
        <CardTitle className="text-2xl text-green-800 flex items-center justify-center gap-2">
          <TrendingUp className="w-6 h-6" />
          Ranking Global
        </CardTitle>
        <p className="text-gray-600">Top jogadores de todos os tempos</p>
      </CardHeader>
      
      <CardContent>
        {loading ? (
          <div className="flex justify-center items-center py-8">
            <Loader2 className="w-8 h-8 animate-spin text-green-600" />
            <span className="ml-2 text-gray-600">Carregando ranking...</span>
          </div>
        ) : (
          <>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {rankings.map((player, index) => {
                const position = index + 1;
                const isCurrent = isCurrentPlayer(player.name);
                
                return (
                  <div
                    key={player.id}
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
                              Jogando
                            </Badge>
                          )}
                        </div>
                        <div className="text-sm text-gray-500">
                          {player.games} jogos • {player.wins} vitórias
                        </div>
                      </div>
                    </div>
                    
                    <div className="text-right">
                      <Badge className={`${getBadgeColor(position)} font-bold`}>
                        {player.points} pts
                      </Badge>
                      {player.winRate && (
                        <div className="text-xs text-gray-500 mt-1">
                          {player.winRate}% vitórias
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
            
            <div className="mt-4 p-3 bg-blue-50 rounded-lg text-center">
              <p className="text-sm text-blue-800">
                <strong>{rankings.length}</strong> jogadores registrados
              </p>
              <p className="text-xs text-blue-600 mt-1">
                Pontuação atualizada em tempo real
              </p>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
};

export default GlobalRanking;