import { useState, useEffect } from 'react';
import { useNavigate, useParams } from "react-router-dom";

function RestaurantInfo(){

    const navigate = useNavigate();

    // Extract the restaurant pk.
    const { restaurant_pk } = useParams();

    // Set them to null because if say string is "" or stats are {} empty, jsx will try to immediatelly process the dot properties and nothing will appear
    const [restaurant, setRestaurant] = useState(null);
    const [restaurant_stats, setStats] = useState(null);
    // Stats categories
    const [financials, setFinancials] = useState(null);
    const [orders, setOrders] = useState(null);
    const [menu, setMenu] = useState(null);
    const [staff, setStaff] = useState(null);
    const [labour_hours,setLabourHours] = useState(null);
    const [labour_cost, setLabourCost] = useState(null);
    const [food_stats, setFoodStats] = useState(null);
    const [food_revenue, setFoodRevenue] = useState(null);
    const [reservations, setReservations] = useState(null);

    useEffect(() => {
        fetch(`http://localhost:8000/api/detail_restaurant/${restaurant_pk}`,{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setRestaurant(data);
            });
        fetch(`http://localhost:8000/api/restaurant_stats/${restaurant_pk}`,{
            credentials : 'include'
        })
            .then(request => request.json())
            .then(data => {
                setStats(data);
                setFinancials(data.financials);
                setOrders(data.orders);
                setMenu(data.menu);
                setStaff(data.staff);
                setLabourHours(data.labour_hours);
                setLabourCost(data.labour_cost);
                setFoodStats(data.food_stats);
                setFoodRevenue(data.food_revenue);
                setReservations(data.reservations);
            });
        

        },[restaurant_pk])

    if (!restaurant || !restaurant_stats) {
        return (
            <p>Loading...</p>
        )
    }

    return (
        <div>
            <h1>{restaurant.restaurant_name}'s Info</h1>
                <div>
                    <h2>Basic Information : </h2>
                        <p>Location : {restaurant.location_display}</p>
                        <p>Cuisine : {restaurant.restaurant_cuisine_display}</p>
                        <p>Capacity : {restaurant.capacity}</p>
                        <p>Tables : {restaurant.number_of_tables}</p>
                        <p>Date Openend : {restaurant.date_opened}</p>
                        <p>Supervisor : {restaurant.supervisor}</p>
                </div>

                <div>
                    <h2> Financial Stats : </h2>
                        <p>Total Earned : £{financials.total_earned_general}</p>
                        <p>Earned Today : £{financials.total_earned_today} </p>
                        <p>Earned Last Week : £{financials.total_earned_last_week}</p>
                        <p>Earned Last Month : £{financials.total_earned_last_month}</p>
                        <p>Earned Last Year : £{financials.total_earned_last_year}</p>
                        <p><strong>Average Transaction : £{financials.average_transaction_value}</strong></p>
                </div>

                <div>
                    <h2>Orders :</h2>
                        <p>Total orders : {orders.total_orders_general}</p>
                        <p>Today : {orders.orders_today}</p>
                        <p>Last Week : {orders.orders_last_week}</p>
                        <p>Last Month: {orders.orders_last_month}</p>
                        <p>Last Year : {orders.orders_last_year}</p>
                </div>

                <div>
                    <h2>Menu :</h2>
                        <p>Number of menu items : {menu.menu_size}</p>
                </div>

                <dir>
                    <h2>Staff :</h2>
                        <p>Total staff count : {staff.general_staff_count}</p>
                        <p>Chiefs count : {staff.chief_staff_count}</p>
                        <p>Waiters count : {staff.waiter_staff_count}</p>
                        <p>Cleaners count : {staff.cleaner_staff_count}</p>
                        <p><strong>Average Age : {staff.average_age}</strong></p>
                </dir>

                <div>
                    <h2>Labour Hours :</h2>
                        <p>Total Labour hours : {labour_hours.total_labour_hours}hrs</p>
                        <p>Last Week : {labour_hours.last_week_labour_hours}hrs</p>
                        <p>Last Month : {labour_hours.last_month_labour_hours}hrs</p>
                        <p>Last Year : {labour_hours.last_year_labour_hours}</p>
                </div>

                <div>
                    <h2>Labour Cost :</h2>
                        <p>Total Labour Cost : £{labour_cost.total_labour_cost}</p>
                        <p>Last week : £{labour_cost.last_week_labour_cost}</p>
                        <p>Last month : £{labour_cost.last_month_labour_cost}</p>
                        <p>Last Year : £{labour_cost.last_year_labour_cost}</p>
                </div>

                <div>
                    <h2>Food Stats :</h2>
                        <p>Number of Starters ordered : {food_stats.number_of_starters_ordered}</p>
                        <p>Number of Starters : {food_stats.number_of_starters}</p>
                        <p>Number of Mains ordered : {food_stats.number_of_mains_ordered}</p>
                        <p>Number of Main : {food_stats.number_of_mains}</p>
                        <p>Number of Deserts ordered : {food_stats.number_of_deserts_ordered}</p>
                        <p>Number of Deserts : {food_stats.number_of_deserts}</p>
                        <p>Number of Drinks ordered : {food_stats.number_of_drinks_ordered}</p>
                        <p>Number of Drinks : {food_stats.number_of_drinks}</p>
                        <p>Number of Snacks ordered : {food_stats.number_of_snacks_ordered}</p>
                        <p>Number of Snacks : {food_stats.number_of_snacks}</p>
                        
                        <p>Most popular Category : <strong>{food_stats.most_popular_category}</strong></p>

                        <h3>Category Percent</h3>
                            <p>Starters : %{food_stats.starters_percent}</p>
                            <p>Mains : %{food_stats.mains_percent}</p>
                            <p>Desserts : %{food_stats.desserts_percent}</p>
                            <p>Drinks : %{food_stats.drinks_percent}</p>
                            <p>Snacks : %{food_stats.snacks_percent}</p>
                </div>

                <div>
                    <h2>Food Revenue :</h2>
                        <p>Most Profitable Category : {food_revenue.most_profitable_category}</p>
                        <p>Least Profitable Category : {food_revenue.least_profitable_category}</p>
                        <p>Starters : £{food_revenue.starter_revenue}</p>
                        <p>Mains : £{food_revenue.main_revenue}</p>
                        <p>Dessert : £{food_revenue.dessert_revenue}</p>
                        <p>Drinks : £{food_revenue.drink_revenue}</p>
                        <p>Snacks : £{food_revenue.snack_revenue}</p>
                </div>

                <div>
                    <h2>Reservations : </h2>
                        <p>Active Reservations : {reservations.active_reservations}</p>
                        <p>Inactive Reservations : {reservations.inactive_reservations}</p>
                        <p>Total Reservations : {reservations.total_reservations}</p>
                        <p>Today : {reservations.reservations_today}</p>
                        <p>This Week : {reservations.reservations_this_week}</p>
                        <p>This Month : {reservations.reservations_this_month}</p>
                        <p>This Year : {reservations.reservations_this_year}</p>
                </div>

            <div>
                <button onClick={(event) => navigate("/restaurant_list")}>Back</button>
            </div>

        </div>
    )
}

export default RestaurantInfo;