import { useState } from 'react'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import './App.css'

import RestaurantList from "./RestaurantList"

// Where UI gets constructed

function App() {
  return (
    <RestaurantList />
  );
}

export default App;