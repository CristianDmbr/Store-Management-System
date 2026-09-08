import { BrowserRouter, Routes, Route } from "react-router-dom"

import Restaurants from "./Restaurants"


function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route
          path = "/restaurants"
          element = {<Restaurants /> }
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;