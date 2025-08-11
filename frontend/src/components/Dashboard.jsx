import React, { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';

const Dashboard = ({ user, onLogout, onSelectTicTacToe }) => {
  const [openSections, setOpenSections] = useState({
    objetivos: false,
    propostas: false,
    disciplinas: false,
    jogos: false
  });

  const toggleSection = (section) => {
    setOpenSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };
  
  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('username');
    onLogout();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 to-blue-800">
      {/* Header */}
      <header className="bg-blue-600 text-white px-6 py-4 flex justify-between items-center">
        <div className="flex items-center">
          <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center mr-3">
            <span className="text-blue-600 font-bold text-lg">👤</span>
          </div>
          <span className="font-semibold text-lg">{user.username || 'daniel'} | Conta Geral Ensino</span>
        </div>
        <button
          onClick={handleLogout}
          className="bg-blue-500 hover:bg-blue-700 px-4 py-2 rounded-lg transition-colors font-semibold"
        >
          Sair
        </button>
      </header>

      <div className="container mx-auto px-6 py-8">
        <div className="grid lg:grid-cols-4 gap-8">
          {/* Left Sidebar - Menu */}
          <div className="lg:col-span-1">
            <div className="bg-gray-900 rounded-2xl shadow-xl p-6 space-y-4">
              {/* Objetivos */}
              <div 
                className="flex items-center gap-3 text-white hover:bg-gray-800 p-3 rounded-lg cursor-pointer transition-colors"
                onClick={() => toggleSection('objetivos')}
              >
                <div className="w-8 h-8 bg-red-500 rounded-lg flex items-center justify-center">
                  <span className="text-white">🎯</span>
                </div>
                <span className="font-semibold">Objetivos</span>
              </div>
              
              {/* Propostas */}
              <div 
                className="flex items-center gap-3 text-white hover:bg-gray-800 p-3 rounded-lg cursor-pointer transition-colors"
                onClick={() => toggleSection('propostas')}
              >
                <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
                  <span className="text-white">🌱</span>
                </div>
                <span className="font-semibold">Propostas</span>
              </div>
              
              {/* Disciplinas */}
              <div 
                className="flex items-center gap-3 text-white hover:bg-gray-800 p-3 rounded-lg cursor-pointer transition-colors"
                onClick={() => toggleSection('disciplinas')}
              >
                <div className="w-8 h-8 bg-yellow-500 rounded-lg flex items-center justify-center">
                  <span className="text-white">📚</span>
                </div>
                <span className="font-semibold">Disciplinas</span>
              </div>
              
              {/* Jogos */}
              <div 
                className="flex items-center gap-3 text-white hover:bg-gray-800 p-3 rounded-lg cursor-pointer transition-colors"
                onClick={() => toggleSection('jogos')}
              >
                <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
                  <span className="text-white">🎮</span>
                </div>
                <span className="font-semibold">Jogos</span>
              </div>
            </div>
          </div>

          {/* Main Content - Games Grid */}
          <div className="lg:col-span-3">
            <div className="grid md:grid-cols-2 gap-6">
              {/* Jogo da Velha Educacional */}
              <div className="bg-blue-500 rounded-3xl shadow-xl p-8 text-white relative overflow-hidden">
                <div className="relative z-10">
                  {/* Tic Tac Toe Board Icon */}
                  <div className="bg-white rounded-2xl p-6 mb-6 w-fit">
                    <div className="grid grid-cols-3 gap-1 w-16 h-16">
                      <div className="bg-blue-500 rounded flex items-center justify-center text-white font-bold text-sm">X</div>
                      <div className="bg-orange-500 rounded flex items-center justify-center text-white font-bold text-sm">O</div>
                      <div className="bg-orange-500 rounded flex items-center justify-center text-white font-bold text-sm">O</div>
                      <div className="bg-blue-500 rounded flex items-center justify-center text-white font-bold text-sm">X</div>
                      <div className="bg-blue-500 rounded flex items-center justify-center text-white font-bold text-sm">X</div>
                      <div className="bg-orange-500 rounded flex items-center justify-center text-white font-bold text-sm">O</div>
                      <div className="bg-orange-500 rounded flex items-center justify-center text-white font-bold text-sm">O</div>
                      <div className="bg-blue-500 rounded flex items-center justify-center text-white font-bold text-sm">X</div>
                      <div className="bg-gray-300 rounded"></div>
                    </div>
                  </div>
                  
                  <h3 className="text-2xl font-bold mb-4">Jogo da Velha<br />Educacional</h3>
                  <p className="text-blue-100 mb-6 text-sm leading-relaxed">
                    O clássico jogo de estratégia agora com um toque educacional!
                  </p>
                  
                  <button
                    onClick={onSelectTicTacToe}
                    className="bg-yellow-500 hover:bg-yellow-600 text-blue-900 font-bold py-3 px-6 rounded-2xl transition-colors transform hover:scale-105"
                  >
                    Jogar Agora
                  </button>
                </div>
                
                {/* Decorative Elements */}
                <div className="absolute top-4 right-4 text-6xl opacity-20">⭐</div>
                <div className="absolute bottom-4 right-4 text-4xl opacity-20">✨</div>
              </div>

              {/* Campo Minado do Saber */}
              <div className="bg-orange-500 rounded-3xl shadow-xl p-8 text-white relative overflow-hidden">
                <div className="relative z-10">
                  {/* Minesweeper Grid Icon */}
                  <div className="bg-white rounded-2xl p-6 mb-6 w-fit">
                    <div className="grid grid-cols-3 gap-1 w-16 h-16">
                      <div className="bg-cyan-400 rounded flex items-center justify-center text-gray-800 font-bold text-xs">1</div>
                      <div className="bg-gray-300 rounded"></div>
                      <div className="bg-cyan-400 rounded flex items-center justify-center text-gray-800 font-bold text-xs">1</div>
                      <div className="bg-cyan-400 rounded flex items-center justify-center text-gray-800 font-bold text-xs">1</div>
                      <div className="bg-yellow-400 rounded flex items-center justify-center text-gray-800 font-bold text-xs">⭐</div>
                      <div className="bg-cyan-400 rounded flex items-center justify-center text-gray-800 font-bold text-xs">1</div>
                      <div className="bg-cyan-400 rounded flex items-center justify-center text-gray-800 font-bold text-xs">1</div>
                      <div className="bg-cyan-400 rounded flex items-center justify-center text-gray-800 font-bold text-xs">1</div>
                      <div className="bg-cyan-400 rounded flex items-center justify-center text-gray-800 font-bold text-xs">1</div>
                    </div>
                  </div>
                  
                  <h3 className="text-2xl font-bold mb-4">Campo Minado<br />do Saber</h3>
                  <p className="text-orange-100 mb-6 text-sm leading-relaxed">
                    Abra as células e responda as perguntas, mas cuidado com as minas!
                  </p>
                  
                  <button className="bg-yellow-500 hover:bg-yellow-600 text-orange-900 font-bold py-3 px-6 rounded-2xl transition-colors transform hover:scale-105">
                    Jogar Agora
                  </button>
                </div>
                
                {/* Decorative Elements */}
                <div className="absolute top-4 right-4 text-6xl opacity-20">💎</div>
                <div className="absolute bottom-4 right-4 text-4xl opacity-20">💥</div>
              </div>

              {/* Quiz Rápido Relâmpago */}
              <div className="bg-purple-600 rounded-3xl shadow-xl p-8 text-white relative overflow-hidden">
                <div className="relative z-10">
                  {/* Quiz Icon */}
                  <div className="bg-blue-600 rounded-2xl p-6 mb-6 w-fit">
                    <div className="flex items-center justify-center w-16 h-16">
                      <div className="relative">
                        <div className="bg-yellow-400 rounded-full w-8 h-8 flex items-center justify-center">
                          <span className="text-blue-800 font-bold text-lg">?</span>
                        </div>
                        <div className="absolute -top-1 -right-1">
                          <div className="bg-yellow-300 rounded w-4 h-6 transform rotate-12"></div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <h3 className="text-2xl font-bold mb-4">Quiz Rápido<br />Relâmpago</h3>
                  <p className="text-purple-100 mb-6 text-sm leading-relaxed">
                    Responda as perguntas rápidas antes do tempo acabar!
                  </p>
                  
                  <button className="bg-yellow-500 hover:bg-yellow-600 text-purple-900 font-bold py-3 px-6 rounded-2xl transition-colors transform hover:scale-105">
                    Jogar Agora
                  </button>
                </div>
                
                {/* Decorative Elements */}
                <div className="absolute top-4 right-4 text-6xl opacity-20">⚡</div>
                <div className="absolute bottom-4 right-4 text-4xl opacity-20">🔥</div>
              </div>

              {/* Força Interativa */}
              <div className="bg-green-500 rounded-3xl shadow-xl p-8 text-white relative overflow-hidden">
                <div className="relative z-10">
                  {/* Interactive Screen Icon */}
                  <div className="bg-white rounded-2xl p-6 mb-6 w-fit">
                    <div className="bg-green-600 rounded-lg p-2 relative w-16 h-16">
                      <div className="bg-blue-400 rounded h-8 mb-1"></div>
                      <div className="bg-gray-300 rounded h-2 mb-1"></div>
                      <div className="bg-gray-300 rounded h-2"></div>
                      <div className="absolute bottom-1 right-1 bg-blue-400 rounded-full w-4 h-4 flex items-center justify-center">
                        <span className="text-white text-xs font-bold">👤</span>
                      </div>
                    </div>
                  </div>
                  
                  <h3 className="text-2xl font-bold mb-4">Força Interativa</h3>
                  <p className="text-green-100 mb-6 text-sm leading-relaxed">
                    Descubra as palavras corretas antes que seja tardedema is!
                  </p>
                  
                  <button className="bg-yellow-500 hover:bg-yellow-600 text-green-900 font-bold py-3 px-6 rounded-2xl transition-colors transform hover:scale-105">
                    Jogar Agora
                  </button>
                </div>
                
                {/* Decorative Elements */}
                <div className="absolute top-4 right-4 text-6xl opacity-20">🔤</div>
                <div className="absolute bottom-4 right-4 text-4xl opacity-20">💪</div>
              </div>
            </div>
          </div>
        </div>

        {/* Expandable Sections Content */}
        {openSections.objetivos && (
          <div className="mt-8 bg-white rounded-2xl shadow-lg p-6">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Objetivos</h3>
            <p className="text-gray-700 leading-relaxed">
              Transformar o aprendizado em uma experiência interativa e envolvente,
              unindo diversão e conhecimento através de jogos educacionais.
            </p>
          </div>
        )}

        {openSections.propostas && (
          <div className="mt-8 bg-white rounded-2xl shadow-lg p-6">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Propostas</h3>
            <ul className="space-y-3 text-gray-700">
              <li className="flex items-start">
                <span className="text-blue-600 mr-2">•</span>
                Metodologia lúdica e interativa
              </li>
              <li className="flex items-start">
                <span className="text-blue-600 mr-2">•</span>
                Aprendizado baseado em jogos educacionais
              </li>
              <li className="flex items-start">
                <span className="text-blue-600 mr-2">•</span>
                Avaliação contínua através de atividades práticas
              </li>
              <li className="flex items-start">
                <span className="text-blue-600 mr-2">•</span>
                Desenvolvimento de habilidades críticas
              </li>
            </ul>
          </div>
        )}

        {openSections.disciplinas && (
          <div className="mt-8 bg-white rounded-2xl shadow-lg p-6">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Disciplinas</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg text-center">
                <div className="text-blue-600 text-2xl mb-2">📚</div>
                <div className="font-semibold text-gray-700">Português</div>
              </div>
              <div className="bg-green-50 p-4 rounded-lg text-center">
                <div className="text-green-600 text-2xl mb-2">🔢</div>
                <div className="font-semibold text-gray-700">Matemática</div>
              </div>
              <div className="bg-yellow-50 p-4 rounded-lg text-center">
                <div className="text-yellow-600 text-2xl mb-2">🏛️</div>
                <div className="font-semibold text-gray-700">História</div>
              </div>
              <div className="bg-red-50 p-4 rounded-lg text-center">
                <div className="text-red-600 text-2xl mb-2">🧪</div>
                <div className="font-semibold text-gray-700">Química</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;