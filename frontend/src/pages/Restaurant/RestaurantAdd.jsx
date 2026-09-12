import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function AddRestaurant(){

    const navigate = useNavigate("");

    const [csrfToken, setCSRFToken] = useState("");
    const [supervisors, setSupervisors] = useState([]);

    const [restaurant_name, setRestaurantName] = useState("");
    const [date_opened, setDateOpened] = useState("");
    const [location, setLocation] = useState("");
    const [restaurant_cuisine, setRestaurantCuisine] = useState("");
    const [capacity, setCapacity] = useState("");
    const [number_of_tables, setNumberOfTables] = useState("");
    const [supervisor, setSupervisor] = useState("");

    function handleSubmit(event) {
        event.preventDefault();

        fetch("http://localhost:8000/api/my_restaurants/",{
            credentials : "include",
            method : "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body : JSON.stringify({
                "supervisor" : supervisor,
                "restaurant_name" : restaurant_name,
                "date_opened" : date_opened,
                "location" : location,
                "restaurant_cuisine" : restaurant_cuisine,
                "capacity" : capacity,
                "number_of_tables" : number_of_tables,
            })  
        }).then( () => navigate("/restaurant_list"))
    }

    useEffect(() => {
        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setCSRFToken(data.csrfToken)
            });    
        
        fetch("http://localhost:8000/api/get_supervisors", {
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setSupervisors(data);
            });
    },[])  



    return (
        <div>
            <h1>Add Restaurant</h1>

            <form onSubmit = {handleSubmit}>

                <div>
                    <label>Restaurant Name</label>
                    <input
                        type = "text"
                        value = {restaurant_name}
                        onChange = {(event) => setRestaurantName(event.target.value)}
                        />
                </div>

                <div>
                    <label>Date Opened</label>
                    <input 
                        type="date"
                        value = {date_opened}
                        onChange = {(event) => {setDateOpened(event.target.value)}} 
                        />
                </div>

                <div>
                    <label>Select Supervisor</label>
                    <select value={supervisor} onChange = {(event) => setSupervisor(event.target.value)}>
                            <option value="" disabled>Select a Supervisor</option>
                            {supervisors.map((user) => (
                                <option key = {user.id} value = {user.id}>
                                    {user.username}
                                </option>
                            ))}
                    </select>
                </div>

                <div>
                    <label>Restaurant Cuisine</label>
                    <select value = {restaurant_cuisine} onChange = {(event) => setRestaurantCuisine(event.target.value)}>
                        <option value="" disabled>Select Cuisine</option>
                        <option value="fast_food">Fast Food</option>
                        <option value="italian">Italian</option>
                        <option value="indian">Indian</option>
                        <option value="british">British</option>
                        <option value="spanish">Spanish</option>
                        <option value="chinese">Chinese</option>
                        <option value="japanese">Japanese</option>
                        <option value="korean">Korean</option>
                    </select>
                </div>

                <div>
                    <label>Location</label>
                    <select value = {location} onChange = {(event) => setLocation(event.target.value)}>
                        <option value="" disabled>Select Option</option>
                        <option value="east_london">East London</option>
                        <option value="south_london">South London</option>
                        <option value="north_london">North London</option>
                        <option value="west_london">West London</option>
                    </select>
                </div>

                <div>
                    <label>Capacity</label>
                    <input 
                        type="number"
                        value= {capacity}
                        onChange = {(event) => setCapacity(event.target.value)}
                        />
                </div>

                <div>
                    <label>Number of Tables</label>
                    <input 
                        type="number"
                        value = {number_of_tables}
                        onChange = {(event) => setNumberOfTables(event.target.value)} 
                        />
                </div>
            
                <button type="submit">Add</button>

            </form>

            <div>
                <button onClick={(event) => {navigate("/restaurant_list")}}>Back</button>
            </div>

        </div>
    )
}

export default AddRestaurant;