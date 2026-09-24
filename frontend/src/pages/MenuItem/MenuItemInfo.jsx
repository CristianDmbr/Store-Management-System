import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect } from "react";

function MenuItemInfo() {

    const navigate = useNavigate();
    const { menu_item_pk, restaurant_pk } = useParams();

    const [menu_item, setMenuItem] = useState();
    const [role, setRole] = useState();

    const [restaurant, setRestaurant] = useState();
    const [price, setPrice] = useState();
    const [date_added, setDateAdded] = useState();
    const [description, setDescription] = useState();
    const [display_category, setDisplayCategory] = useState();
    const [availability, setAvailability] = useState();
    const [calories, setCalories] = useState();
    const [ingredience, setIngredience] = useState();

    useEffect(() => {
        fetch(`http://localhost:8000/api/menu_item_detail/${menu_item_pk}`, {
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                setMenuItem(data);
                setRestaurant(data.display_restaurant_name);
                setPrice(data.price);
                setDateAdded(data.date_added);
                setDescription(data.description);
                setDisplayCategory(data.display_category);
                setAvailability(data.availability);
                setCalories(data.calories);
                setIngredience(data.ingredience);
            });

        fetch("http://localhost:8000/api/user_name",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => (
                setRole(data.role)
            ))

    }, [menu_item_pk]);

    if (!menu_item) {
        return (
            <div>
                <h1>Loading...</h1>
            </div>
        );
    }

    return (
        <div>

            <h1>{menu_item.name}</h1>

            <div>
                <h2>Basic Information</h2>

                <p>
                    <strong>Restaurant:</strong> {restaurant}
                </p>

                <p>
                    <strong>Category:</strong> {display_category}
                </p>

                <p>
                    <strong>Price:</strong> £{price}
                </p>

                <p>
                    <strong>Availability:</strong> {availability ? "Available" : "Unavailable"}
                </p>

                <p>
                    <strong>Date Added:</strong> {date_added}
                </p>
            </div>

            <div>
                <h2>Nutrition</h2>

                <p>
                    <strong>Calories:</strong> {calories}
                </p>
            </div>

            <div>
                <h2>Description</h2>

                <p>
                    {description || "No description"}
                </p>
            </div>

            <div>
                <h2>Ingredients</h2>

                <p>
                    {ingredience || "No ingredients listed"}
                </p>
            </div>

            <button onClick={(event) => navigate(`/menu_items_per_restaurant/${restaurant_pk}`) }> Back to Menu </button>
            {role == "Owner" && (
                <button onClick={(event) => navigate(`/menu_item_update/${menu_item_pk}/${restaurant_pk}`)}><strong>Update</strong></button>
            )}

        </div>
    );
}

export default MenuItemInfo;