import React, { useState } from 'react';

const Login = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        // Store token in localStorage
        localStorage.setItem('auth_token', data.access_token);
        localStorage.setItem('user_id', data.user_id);
        localStorage.setItem('username', data.username);
        
        onLoginSuccess(data);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Erro ao fazer login');
      }
    } catch (err) {
      setError('Erro de conexão com o servidor');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center p-4">
      <div className="bg-blue-400 bg-opacity-80 p-8 rounded-2xl shadow-2xl w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Geral Ensino</h1>
          <p className="text-yellow-300 text-lg font-semibold">APRENDA SE DIVERTINDO</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <input
              type="text"
              placeholder="Usuário"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-3 rounded-full bg-white bg-opacity-90 border-0 focus:outline-none focus:ring-2 focus:ring-yellow-400 text-gray-700 placeholder-gray-500"
              required
            />
          </div>

          <div>
            <input
              type="password"
              placeholder="Senha"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 rounded-full bg-white bg-opacity-90 border-0 focus:outline-none focus:ring-2 focus:ring-yellow-400 text-gray-700 placeholder-gray-500"
              required
            />
          </div>

          {error && (
            <div className="text-red-200 text-sm text-center bg-red-600 bg-opacity-50 p-2 rounded-lg">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-3 px-4 rounded-full transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Entrando...' : 'Entrar'}
          </button>
        </form>

        <div className="mt-6 text-center text-sm text-blue-100">
          <p>Usuário de teste: <strong>admin</strong></p>
          <p>Senha: <strong>123456</strong></p>
        </div>
      </div>
    </div>
  );
};

export default Login;