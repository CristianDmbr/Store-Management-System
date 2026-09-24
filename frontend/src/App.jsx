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
import UpdateRestaurant from "./pages/Restaurant/RestaurantUpdate";

import StaffList from "./pages/Staff/StaffList";
import StaffInfo from "./pages/Staff/StaffInfo";
import StaffDelete from "./pages/Staff/StaffDelete";
import StaffAdd from "./pages/Staff/StaffAdd";
import StaffUpdate from "./pages/Staff/StaffUpdate";

import MenuItemsPerRestaurant from "./pages/MenuItem/MenuItemsPerRestaurant";
import MenuItemInfo from "./pages/MenuItem/MenuItemInfo";
import DeleteMenuItem from "./pages/MenuItem/MenuItemDelete";
import MenuItemAdd from "./pages/MenuItem/MenuItemAdd";
import UpdateMenuItem from "./pages/MenuItem/MenuItemUpdate";

import ShiftList from "./pages/Shift/ShiftList";
import AddShift from "./pages/Shift/ShiftAdd";
import InfoShift from "./pages/Shift/ShiftInfo";



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

        <Route
          path = "/update_restaurant/:restaurant_pk"
          element = {<UpdateRestaurant/>}
        />



        <Route
          path="/staff_list"
          element = {<StaffList/>}
        />

        <Route
          path = "/staff_info/:staff_pk"
          element = {<StaffInfo/>}
        />

        <Route
          path = "/staff_delete/:staff_pk"
          element = {<StaffDelete/>}
        />

        <Route
          path = "/staff_add"
          element = {<StaffAdd/>}
        />

        <Route
          path = "/staff_update/:staff_pk"
          element = {<StaffUpdate/>}
        />


        <Route
          path = "/menu_items_per_restaurant/:restaurant_pk"
          element = {<MenuItemsPerRestaurant/>}
        />
        <Route
          path = "/menu_item_info/:menu_item_pk/:restaurant_pk"
          element = {<MenuItemInfo/>}
        />

        <Route
          path = "/menu_item_delete/:menu_item_pk/:restaurant_pk"
          element = {<DeleteMenuItem/>}
        />

        <Route
          path = "/menu_item_add/:restaurant_pk"
          element = {<MenuItemAdd/>}
        />

        <Route
          path = "/menu_item_update/:menu_item_pk/:restaurant_pk"
          element = {<UpdateMenuItem/>}
        />



        <Route
          path = "/shifts_list"
          element = {<ShiftList/>}
        />

        <Route
          path = "/shift_add"
          element = {<AddShift/>}
        />

        <Route
          path = "/shift_info/:shift_pk"
          element = {<InfoShift/>}
        />


      </Routes>
    </BrowserRouter>
  );
}

export default App;