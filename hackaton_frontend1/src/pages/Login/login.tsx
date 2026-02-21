import React, { useState, useMemo } from 'react';
import './login.scss';
import { hasSQLInjection } from '../../utils/sqlInjection';
import { useNavigate } from 'react-router-dom';

interface LoginFormState {
  login: string;
  password: string;
  rememberMe: boolean;
}

interface LoginErrors {
  login?: string;
  password?: string;
}

const Login: React.FC = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState<LoginFormState>({
    login: '',
    password: '',
    rememberMe: false,
  });

  const [errors, setErrors] = useState<LoginErrors>({});
  const [isLoading, setIsLoading] = useState(false);

  // Валидация логина (проверка на пустоту и SQL-инъекции)
  const validateLogin = (login: string): string | undefined => {
    if (!login) return 'Логин или email обязателен';
    if (hasSQLInjection(login)) return 'Обнаружены подозрительные символы';
    return undefined;
  };

  // Валидация пароля (только на заполненность)
  const validatePassword = (password: string): string | undefined => {
    if (!password) return 'Пароль обязателен';
    return undefined;
  };

  // Проверка, можно ли разблокировать кнопку
  const isFormValid = useMemo(() => {
    const allFilled = formData.login.trim() !== '' && formData.password.trim() !== '';
    const noErrors = !errors.login && !errors.password;
    return allFilled && noErrors;
  }, [formData, errors]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));

    // Валидация при изменении
    if (name === 'login') {
      const error = validateLogin(value);
      setErrors(prev => ({ ...prev, login: error }));
    } else if (name === 'password') {
      const error = validatePassword(value);
      setErrors(prev => ({ ...prev, password: error }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Финальная проверка
    const loginError = validateLogin(formData.login);
    const passwordError = validatePassword(formData.password);

    if (loginError || passwordError) {
      setErrors({ login: loginError, password: passwordError });
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          login: formData.login,
          password: formData.password,
          remember_me: formData.rememberMe,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Ошибка авторизации');
      }

      // Сохраняем токен в localStorage
      if (data.access_token) {
        localStorage.setItem('access_token', data.access_token);
      }

      // Перенаправляем на главную страницу (или другую)
      navigate('/');
    } catch (error: any) {
      console.error('Ошибка:', error);
      alert(error.message || 'Не удалось войти');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <form className="form" onSubmit={handleSubmit}>
        <h2 className="title">Авторизация</h2>

        <div className="field">
          <label htmlFor="login" className="label">
            Логин или email
          </label>
          <input
            type="text"
            id="login"
            name="login"
            className={`input ${errors.login ? 'inputError' : ''}`}
            value={formData.login}
            onChange={handleChange}
            disabled={isLoading}
            required
          />
          {errors.login && <div className="errorMessage">{errors.login}</div>}
        </div>

        <div className="field">
          <label htmlFor="password" className="label">
            Пароль
          </label>
          <input
            type="password"
            id="password"
            name="password"
            className={`input ${errors.password ? 'inputError' : ''}`}
            value={formData.password}
            onChange={handleChange}
            disabled={isLoading}
            required
          />
          {errors.password && <div className="errorMessage">{errors.password}</div>}
        </div>

        <div className="forgotPassword">
          <a href="/forgot-password">Забыли пароль?</a>
        </div>

        <div className="checkboxContainer">
          <input
            type="checkbox"
            id="rememberMe"
            name="rememberMe"
            className="checkbox"
            checked={formData.rememberMe}
            onChange={handleChange}
            disabled={isLoading}
          />
          <label htmlFor="rememberMe">Запомнить меня</label>
        </div>

        <button
          type="submit"
          className="button"
          disabled={!isFormValid || isLoading}
        >
          {isLoading ? 'Вход...' : 'Войти'}
        </button>
      </form>
    </div>
  );
};

export default Login;