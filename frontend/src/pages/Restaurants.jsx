import { useState, useEffect } from "react";
import { useNavigate} from "react-router-dom"

function RestaurantsList() {

    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [restaurants,setRestaurants] = useState([])

    useEffect(() => {
        fetch("http://localhost:8000/api/user_name",{
            credentials : "include"
        }).then(request => request.json())
          .then(data => {
            setUsername(data.username)
          });

        fetch("http://localhost:8000/api/my_restaurants",{
            credentials : "include"
        }).then(request => request.json())
          .then(data => {
            setRestaurants(data)
          });
    },[]);

    return (
        <div>
            <h1> {username}'s Restaurant List</h1>

            <div>
                {restaurants.map((restaurant) => (
                    <div key = {restaurant.pk}>
                        <h2>{restaurant.restaurant_name}</h2>
                        <p>Location : {restaurant.location_display}</p>
                        <p>Cuisine : {restaurant.restaurant_cuisine_display}</p>
                        <p>Capacity : {restaurant.capacity}</p>
                        <p>Tables : {restaurant.number_of_tables}</p>

                        <button onClick={(event) => navigate(`/restaurant_info/${restaurant.pk}`)}>View details</button>
                        <button onClick={(event) => navigate(`/delete_restaurant/${restaurant.pk}`)}>Delete</button>

                    </div>
                ))} 
            </div>

            <div>
                <button onClick={(event) => navigate("/owner_dashboard")} >Dashboard</button>
            </div>

        </div>
    )

}

export default RestaurantsList;