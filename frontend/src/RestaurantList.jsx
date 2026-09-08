import { useState, useEffect } from "react";

function RestaurantList() {
    const [restaurants, setRestaurants] = useState([])

    useEffect(() => {
        fetch("http://localhost:8000/api/my_restaurants/", {
            credentials: "include"
        })
            .then(response => {
                console.log("Status" + response.status);
                return response.json();
            })
            .then(data => {
                console.log("Data:" + data)
                setRestaurants(data);
            });
    }, []);

    return (
        <div>
            <h1>My Restaurants :</h1>

            {restaurants.map(restaurant => (
                <div key = {restaurant.pk}>
                    <h2>{restaurant.restaurant_name}</h2>
                    <p>{restaurant.location_display}</p>
                    <p>{restaurant.restaurant_cuisine_display}</p>
                </div>
            ))}

        </div>
    );
};

export default RestaurantList