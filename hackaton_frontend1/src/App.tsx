import React from 'react';
import logo from './logo.svg';
import './App.css';
import Login from './pages/Login/login';
import Registration from './pages/Register/Registration';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/register" element={<Registration />} />
        <Route path="/login" element={<Login />} />
        {/* другие маршруты */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
