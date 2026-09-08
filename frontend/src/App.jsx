import { BrowserRouter, Routes, Route } from "react-router-dom"

import Restaurants from "./pages/Restaurants"
import LoginPage from "./pages/LoginPage";


function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route
          path = "/restaurants"
          element = {<Restaurants /> }
        />

        <Route
          path = "/login"
          element = { <LoginPage />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;