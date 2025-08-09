import React from 'react';

const SubjectSelector = ({ onSelectSubject, onBack }) => {
  const subjects = [
    {
      id: 'portugues',
      name: 'Português',
      emoji: '📚',
      color: 'blue',
      available: false,
      description: 'Gramática, literatura e interpretação'
    },
    {
      id: 'matematica', 
      name: 'Matemática',
      emoji: '🔢',
      color: 'green',
      available: false,
      description: 'Números, operações e raciocínio'
    },
    {
      id: 'historia',
      name: 'História',
      emoji: '🏛️',
      color: 'yellow',
      available: true,
      description: 'Fatos históricos do Brasil'
    },
    {
      id: 'quimica',
      name: 'Química',
      emoji: '🧪',
      color: 'purple',
      available: true,
      description: 'Elementos, reações e compostos'
    },
    {
      id: 'geografia',
      name: 'Geografia',
      emoji: '🌍',
      color: 'red', 
      available: false,
      description: 'Território, população e recursos'
    }
  ];

  const getColorClasses = (color, available) => {
    if (!available) {
      return 'bg-gray-100 border-gray-300 text-gray-500 cursor-not-allowed';
    }
    
    const colors = {
      blue: 'bg-blue-50 border-blue-300 text-blue-700 hover:bg-blue-100',
      green: 'bg-green-50 border-green-300 text-green-700 hover:bg-green-100',
      yellow: 'bg-yellow-50 border-yellow-300 text-yellow-700 hover:bg-yellow-100',
      red: 'bg-red-50 border-red-300 text-red-700 hover:bg-red-100'
    };
    return colors[color] + ' cursor-pointer transform hover:scale-105';
  };

  const handleSubjectClick = (subject) => {
    if (subject.available) {
      onSelectSubject(subject.id);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 to-gray-200 p-6">
      <div className="container mx-auto max-w-4xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Escolha uma Matéria</h1>
          <p className="text-gray-600 text-lg">Selecione a disciplina para jogar o Jogo da Velha Educativo</p>
        </div>

        {/* Back Button */}
        <div className="mb-6">
          <button
            onClick={onBack}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg flex items-center gap-2 transition-colors"
          >
            ← Voltar ao Dashboard
          </button>
        </div>

        {/* Subjects Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {subjects.map((subject) => (
            <div
              key={subject.id}
              onClick={() => handleSubjectClick(subject)}
              className={`border-2 rounded-2xl p-6 text-center transition-all duration-200 ${getColorClasses(subject.color, subject.available)}`}
            >
              <div className="text-6xl mb-4">{subject.emoji}</div>
              <h3 className="text-xl font-bold mb-2">{subject.name}</h3>
              <p className="text-sm mb-4">{subject.description}</p>
              
              {subject.available ? (
                <div className="bg-green-500 text-white px-3 py-1 rounded-full text-xs font-semibold">
                  Disponível
                </div>
              ) : (
                <div className="bg-gray-400 text-white px-3 py-1 rounded-full text-xs font-semibold">
                  Em breve
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Info Card */}
        <div className="mt-8 bg-white rounded-2xl shadow-lg p-6">
          <div className="flex items-center gap-4">
            <div className="bg-blue-600 rounded-full p-3">
              <div className="text-white text-2xl">ℹ️</div>
            </div>
            <div>
              <h3 className="text-lg font-bold text-gray-800 mb-1">Como funciona?</h3>
              <p className="text-gray-600">
                Escolha uma matéria disponível, responda às perguntas corretamente para marcar suas jogadas 
                no tabuleiro e tente fazer três em linha para vencer!
              </p>
            </div>
          </div>
        </div>

        {/* Available Subject Highlight */}
        <div className="mt-6 bg-yellow-100 border-l-4 border-yellow-500 p-4 rounded-r-lg">
          <div className="flex items-center gap-2">
            <span className="text-yellow-600 text-xl">⭐</span>
            <div>
              <p className="text-yellow-800 font-semibold">Matéria em Destaque</p>
              <p className="text-yellow-700 text-sm">
                <strong>História</strong> está disponível com 20 perguntas sobre História do Brasil. 
                Teste seus conhecimentos!
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SubjectSelector;