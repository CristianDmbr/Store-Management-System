import { useState, useEffect } from "react";

function RestaurantList() {
    const [restaurants, setRestaurants] = useState([])

    useEffect(() => {
        fetch("http://127.0.0.1:8000/api/my_restaurants/")
            .then(response => response.json())
            .then(data => {
                setRestaurants(data);
            });
    }, []);

    return (
        <div>
            <h1>My Restaurants :</h1>

            {restaurants.map(restaurant => (
                <div key = {restaurant.pk}>
                    <h2>{restaurant.restaurant_name}</h2>
                    <p>{restaurant.location}</p>
                    <p>{restaurant.restaurant_cuisine}</p>
                </div>
            ))}

        </div>
    );
};
export default RestaurantList