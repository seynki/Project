import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import TicTacToeGame from "./components/TicTacToeGame";
import { Toaster } from "./components/ui/toaster";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<TicTacToeGame />} />
        </Routes>
      </BrowserRouter>
      <Toaster />
    </div>
  );
}

export default App;