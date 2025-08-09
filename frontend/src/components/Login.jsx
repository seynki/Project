import React, { useState } from 'react';

const Login = ({ onLoginSuccess }) => {
  const [isLogin, setIsLogin] = useState(true); // true for login, false for register
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Function to validate if input contains only person names (letters, spaces, accents)
  const isValidPersonName = (name) => {
    // Allow letters (including accented), spaces, apostrophes, and hyphens
    const nameRegex = /^[a-zA-ZÀ-ÿ\s'-]+$/;
    return nameRegex.test(name) && name.trim().length >= 2;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    // Validate name format for both login and register
    if (!isValidPersonName(username)) {
      setError('Por favor, digite apenas nomes de pessoas (letras e espaços)');
      setIsLoading(false);
      return;
    }

    if (!isLogin) {
      // Registration validation
      if (password !== confirmPassword) {
        setError('As senhas não coincidem');
        setIsLoading(false);
        return;
      }
      if (password.length < 6) {
        setError('A senha deve ter pelo menos 6 caracteres');
        setIsLoading(false);
        return;
      }
    }

    try {
      const endpoint = isLogin ? '/api/auth/login' : '/api/auth/register';
      const body = isLogin 
        ? { username, password }
        : { username, password, confirm_password: confirmPassword };

      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
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
        setError(errorData.detail || `Erro ao ${isLogin ? 'fazer login' : 'registrar'}`);
      }
    } catch (err) {
      setError('Erro de conexão com o servidor');
    } finally {
      setIsLoading(false);
    }
  };

  const toggleMode = () => {
    setIsLogin(!isLogin);
    setError('');
    setUsername('');
    setPassword('');
    setConfirmPassword('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center p-4">
      <div className="bg-blue-400 bg-opacity-80 p-8 rounded-2xl shadow-2xl w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Geral Ensino</h1>
          <p className="text-yellow-300 text-lg font-semibold">APRENDA SE DIVERTINDO</p>
        </div>

        <div className="flex mb-6">
          <button
            type="button"
            onClick={() => setIsLogin(true)}
            className={`flex-1 py-2 px-4 rounded-l-full font-semibold transition-colors ${
              isLogin 
                ? 'bg-yellow-500 text-white' 
                : 'bg-white bg-opacity-50 text-blue-800 hover:bg-opacity-70'
            }`}
          >
            Entrar
          </button>
          <button
            type="button"
            onClick={() => setIsLogin(false)}
            className={`flex-1 py-2 px-4 rounded-r-full font-semibold transition-colors ${
              !isLogin 
                ? 'bg-yellow-500 text-white' 
                : 'bg-white bg-opacity-50 text-blue-800 hover:bg-opacity-70'
            }`}
          >
            Cadastrar
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <input
              type="text"
              placeholder="João Silva, Maria Santos"
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

          {!isLogin && (
            <div>
              <input
                type="password"
                placeholder="Confirmar Senha"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full px-4 py-3 rounded-full bg-white bg-opacity-90 border-0 focus:outline-none focus:ring-2 focus:ring-yellow-400 text-gray-700 placeholder-gray-500"
                required
              />
            </div>
          )}

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
            {isLoading 
              ? (isLogin ? 'Entrando...' : 'Cadastrando...') 
              : (isLogin ? 'Entrar' : 'Cadastrar')
            }
          </button>
        </form>

        {isLogin && (
          <div className="mt-6 text-center text-sm text-blue-100">
            <p>Usuário de teste: <strong>admin</strong></p>
            <p>Senha: <strong>123456</strong></p>
          </div>
        )}

        <div className="mt-4 text-center">
          <button
            type="button"
            onClick={toggleMode}
            className="text-yellow-300 hover:text-yellow-200 text-sm underline transition-colors"
          >
            {isLogin ? 'Não tem conta? Cadastre-se' : 'Já tem conta? Faça login'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login;