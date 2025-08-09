import React from 'react';

const Dashboard = ({ user, onLogout, onSelectTicTacToe }) => {
  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('username');
    onLogout();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 to-gray-200">
      {/* Header */}
      <header className="bg-blue-600 text-white px-6 py-4 flex justify-between items-center">
        <div className="flex items-center">
          <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center mr-3">
            <span className="text-blue-600 font-bold text-lg">👤</span>
          </div>
          <span className="font-semibold">{user.id || '124'} | Conta Geral Ensino</span>
        </div>
        <button
          onClick={handleLogout}
          className="bg-blue-500 hover:bg-blue-700 px-4 py-2 rounded-lg transition-colors"
        >
          Sair
        </button>
      </header>

      <div className="container mx-auto px-6 py-8">
        <div className="grid md:grid-cols-2 gap-8">
          {/* Left Column - Objetivos, Propostas, Disciplinas */}
          <div className="space-y-6">
            {/* Objetivos */}
            <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
              <div className="bg-blue-600 text-white px-6 py-4">
                <h2 className="text-xl font-bold">Objetivos</h2>
              </div>
              <div className="p-6">
                <p className="text-gray-700 leading-relaxed">
                  Transformar o aprendizado em uma experiência interativa e envolvente,
                  unindo diversão e conhecimento.
                </p>
              </div>
            </div>

            {/* Propostas */}
            <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
              <div className="bg-blue-600 text-white px-6 py-4">
                <h2 className="text-xl font-bold">Propostas</h2>
              </div>
              <div className="p-6">
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
            </div>

            {/* Disciplinas */}
            <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
              <div className="bg-blue-600 text-white px-6 py-4">
                <h2 className="text-xl font-bold">Disciplinas</h2>
              </div>
              <div className="p-6">
                <div className="grid grid-cols-2 gap-4">
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
                    <div className="text-red-600 text-2xl mb-2">🌍</div>
                    <div className="font-semibold text-gray-700">Geografia</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column - Jogo da Velha */}
          <div className="flex items-start">
            <div className="bg-blue-600 rounded-2xl shadow-xl p-8 text-white w-full">
              <div className="text-center mb-6">
                <div className="text-6xl mb-4">
                  <span className="text-red-500 font-bold">X</span>
                  <span className="text-orange-500 font-bold">O</span>
                </div>
                <h2 className="text-3xl font-bold mb-2">Jogo da Velha</h2>
                <p className="text-blue-200 leading-relaxed">
                  O clássico jogo de estratégia agora com um toque
                  educacional! Escolha uma matéria e, para marcar um
                  espaço, responda corretamente à pergunta exibida. Três
                  acertos em linha e você vence!
                </p>
              </div>

              <button
                onClick={onSelectTicTacToe}
                className="w-full bg-yellow-500 hover:bg-yellow-600 text-blue-900 font-bold py-4 px-6 rounded-xl text-lg transition-colors transform hover:scale-105"
              >
                Jogar Agora
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;