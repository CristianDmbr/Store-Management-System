import { BrowserRouter, Routes, Route } from "react-router-dom"


import LoginPage from "./pages/LoginPage";
import OwnerDashboard from "./pages/OwnerDashboard";
import SupervisorDashboard from "./pages/SupervisorDashboard";
import StaffDashboard from "./pages/StaffDashboard";
import RegisterPage from "./pages/Restaurant/RegisterPage";

import RestaurantsList from "./pages/Restaurant/Restaurants";
import RestaurantInfo from "./pages/Restaurant/RestaurantInfo";
import DeleteRestaurant from "./pages/Restaurant/RestaurantDelete";
import AddRestaurant from "./pages/Restaurant/RestaurantAdd";



function App() {
  return (
    <BrowserRouter>
      <Routes>

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

        <Route
          path = "/restaurant_list"
          element = {<RestaurantsList /> }
        />

        <Route
          path = "/restaurant_info/:restaurant_pk"  
          element = {<RestaurantInfo/>}
        />

        <Route
          path = "/delete_restaurant/:restaurant_pk"
          element = {<DeleteRestaurant/>}
        />

        <Route
          path = "/add_restaurant"
          element = {<AddRestaurant/>}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;