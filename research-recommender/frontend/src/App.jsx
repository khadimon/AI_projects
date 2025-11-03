import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import React from "react";
import SearchBar from './components/SearchBar';

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <SearchBar />
    </div>
  );
}

export default App
