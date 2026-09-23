import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

function MenuItemAdd() {

    const navigate = useNavigate();
    const { restaurant_pk } = useParams();
    const [csrfToken, setCSRFToken] = useState();

    const [displayRestaurant, setRestaurantDisplay] = useState();

    const [name, setName] = useState("");
    const [restaurant, setRestaurant] = useState();
    const [price, setPrice] = useState(0);
    // Automatically adds the date
    const [date_added, setDateAdded] = useState(
        new Date().toISOString().split("T")[0]);
    const [description, setDescription] = useState("");
    const [category, setCategory] = useState("");
    const [availability, setAvailability] = useState(true);
    const [calories, setCalories] = useState(0);
    const [ingredience, setIngredience] = useState("");

    useEffect(() => {
        fetch(`http://localhost:8000/api/detail_restaurant/${restaurant_pk}`,{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setRestaurantDisplay(data)
                setRestaurant(data.pk)
            })
            .catch((error) => {
                console.log("Restaurant fetch failed ", error)
            })

        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setCSRFToken(data.csrfToken)
            })
    },[restaurant_pk])

    function handleSubmit(event) {
        event.preventDefault();

        fetch("http://localhost:8000/api/menu_items_list",{
            credentials : "include",
            method : "POST",
            headers : {
                "Content-Type" : "application/json",
                "X-CSRFToken" : csrfToken,
            },
            body : JSON.stringify({
                "name" : name,
                "restaurant" : restaurant_pk,
                "price" : price,
                "date_added" : date_added,
                "description" : description,
                "category" : category,
                "availability" : availability,
                "calories" : calories,
                "ingredience" : ingredience
            })
        })
            .then(() => navigate(`/menu_items_per_restaurant/${restaurant_pk}`))

    }

    if (!displayRestaurant) {
        return (
            <div>
                <h1>Loading</h1>

                <div>
                <button onClick={(event) => navigate(`/menu_items_per_restaurant/${restaurant_pk}`)}>Back</button>
                </div>
        
            </div>
        )
    }

    return (
        <div>
            <h1>Add Menu Item to {displayRestaurant.restaurant_name} </h1>

            <form onSubmit={handleSubmit}>

                <div>
                    <label>Name : </label>
                    <input 
                        type="text"
                        value = {name}
                        onChange = {(event) => {setName(event.target.value)}}
                    />
                </div>

                <div>
                    <label>Price : </label>
                    <span>£ </span>
                    <input
                        type="number"
                        min="0"
                        step="0.01"
                        value={price}
                        onChange={(event) => {
                            const value = event.target.value;

                            if (/^\d*\.?\d{0,2}$/.test(value)) {
                                setPrice(value);
                            }
                        }}
                    />
                </div>

                <div>
                    <label>Description :</label>
                    <input 
                        type="text" 
                        value={description}
                        onChange = {(event) => {setDescription(event.target.value)}}
                    />
                </div>

                <div>
                    <label>Category : </label>
                    <select value={category} onChange={(event) => {setCategory(event.target.value)}}>
                        <option value="" disabled>Choose a category</option>
                        <option value="starter"> Starter </option>
                        <option value="main">Main</option>
                        <option value="dessert">Dessert</option>
                        <option value="drink">Drink</option>
                        <option value="snack">Snack</option>
                    </select>
                </div>

                <div>
                    <label>Availability : </label>
                    <input 
                        type="checkbox" 
                        value = {availability}
                        onChange = {(event) => setAvailability(event.target.value)}
                    />
                </div>

                <div>
                    <label>Calories </label>
                    <span><small>(kcal)</small> : </span>

                    <input
                        type="number"
                        min="0"
                        step="0.01"
                        value={calories}
                        onChange={(event) => {
                            const value = event.target.value;

                            if (/^\d*\.?\d{0,2}$/.test(value)) {
                                setCalories(value);
                            }
                        }}
                    />
                </div>

                <div>
                    <label>Ingredience</label>
                    <input 
                        type="text"
                        value = {ingredience} 
                        onChange = {(event) => setIngredience(event.target.value)}
                    />
                </div>

                <button type="submit">Add</button>

            </form>

            <div>
                <button onClick={(event) => navigate(`/menu_items_per_restaurant/${restaurant_pk}`)}>Back</button>
            </div>
             
        </div>
    )
}

export default MenuItemAdd;