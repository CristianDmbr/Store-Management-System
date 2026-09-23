import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";

function UpdateMenuItem() {

    const navigate = useNavigate();
    const { menu_item_pk, restaurant_pk } = useParams();
    const [csrfToken, setCSRFToken] = useState();

    const [name, setName] = useState("");
    const [displayName, setDisplayName] = useState("");
    // Do not update the restaurant, use the pk from useParams()
    const [price, setPrice] = useState("");
    // Date added should also not be updated
    const [date_added, setDateAdded] = useState("");
    const [description, setDescription] = useState("");
    const [category, setCategory] = useState("");
    const [availability, setAvailability] = useState(true);
    const [calories, setCalories] = useState("");
    const [ingredience, setIngredience] = useState("");

    useEffect(() => {
        fetch(`http://localhost:8000/api/menu_item_detail/${menu_item_pk}`,{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setName(data.name),
                setDisplayName(data.name);
                setPrice(data.price),
                setDateAdded(data.date_added),
                setDescription(data.description),
                setCategory(data.category),
                setAvailability(data.availability),
                setCalories(data.calories),
                setIngredience(data.ingredience)
            })

        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setCSRFToken(data.csrfToken)
            })
    },[menu_item_pk])

    function handleSubmit(event) {
        event.preventDefault();

        fetch(`http://localhost:8000/api/menu_item_detail/${menu_item_pk}`,{
            method : "PUT",
            credentials : "include",
            headers : {
                "X-CSRFToken" : csrfToken,
                "Content-Type" : "application/json"
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
            .then(() => navigate(`/menu_item_info/${menu_item_pk}/${restaurant_pk}`))
            .catch((error) => {
                console.log(error)
            })
    }


    return (
        <div>
            <h1>Update {displayName}</h1>

                <form onSubmit={handleSubmit}>

                    <div>
                        <label>Name</label>
                        <input 
                            type="text" 
                            value={name}
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
                        <label>Category </label>
                        <select value={category} onChange = {(event) => {setCategory(event.target.value)}}>
                            <option value="starter">Starter</option>
                            <option value="main">Main</option>
                            <option value="dessert">Dessert</option>
                            <option value="drink">Drink</option>
                            <option value="snack">Snack</option>
                        </select>
                    </div>

                    <div>
                        <label>Available </label>
                        <input 
                            type="checkbox" 
                            checked= {availability}
                            onChange = {(event) => {setAvailability(event.target.checked)}}
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
                        <label>Description</label>
                        <input 
                            type="text" 
                            value={description}
                            onChange= {(event) => {setDescription(event.target.value)}}
                        />
                    </div>

                    <div>
                        <label>Ingredience</label>
                        <input 
                            type="text" 
                            value={ingredience}
                            onChange = {(event) => {setIngredience(event.target.value)}}
                        />
                    </div>

                    <button type="submit">Update</button>

                </form>


            <div>
                <button onClick={(event) => {navigate(`/menu_items_per_restaurant/${restaurant_pk}`)}}>Back</button>
            </div>

        </div>
    )
}

export default UpdateMenuItem;