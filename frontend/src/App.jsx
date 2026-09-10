import { BrowserRouter, Routes, Route } from "react-router-dom"

import Restaurants from "./pages/Restaurants"
import LoginPage from "./pages/LoginPage";
import OwnerDashboard from "./pages/OwnerDashboard";
import SupervisorDashboard from "./pages/SupervisorDashboard";
import StaffDashboard from "./pages/StaffDashboard";
import RegisterPage from "./pages/RegisterPage";


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

        <Route
          path = "/owner_dashboard"
          element = {<OwnerDashboard/>}
        />

        <Route
          path = "/supervisor_dashboard"
          element = { <SupervisorDashboard/>}
        />

        <Route
          path = "/staff_dashboard"
          element = {<StaffDashboard/>}  
        />

        <Route
          path = "/register"
          element = {<RegisterPage/>}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;