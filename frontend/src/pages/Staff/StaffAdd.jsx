import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import AddRestaurant from "../Restaurant/RestaurantAdd";

function StaffAdd(){

    const navigate = useNavigate();
    const [csrfToken, setCSRFToken] = useState();
    const [role, setRole] = useState();

    const [allSupervisors, setAllSupervisors] = useState([]);
    const [allRestaurants, setAllRestaurants] = useState([]);

    // User Creation Serializer
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    // Staff Creatiom Serializer
    const [name, setName] = useState("");
    const [surname, setSurname] = useState("");
    const [manager, setManager] = useState("");
    const [restaurant, setRestaurant] = useState("");
    const [date_of_birth, setDateOfBirth] = useState("");
    const [date_time_employed, setDateTimeEmployed] = useState("");
    const [work_right, setWorkRight] = useState("");
    const [position, setPosition] = useState("");
    const [pay_per_hour, setPayPerHour] = useState("");

    useEffect(() => {
        fetch("http://localhost:8000/api/get_supervisors",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setAllSupervisors(data)
            })
        
        fetch("http://localhost:8000/api/my_restaurants/",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setAllRestaurants(data.restaurants)
                setRole(data.role)

            })
        
        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setCSRFToken(data.csrfToken)
            })
        
    },[])

    function handleSubmit(event) {
        event.preventDefault();

        fetch("http://localhost:8000/api/all_staff", {
            method : "POST",
            credentials : "include",
            headers : {
                "X-CSRFToken" : csrfToken,
                "Content-Type": "application/json",
            },
            body : JSON.stringify({
                "username" : username,
                "password" : password,
                "name" : name,
                "surname" : surname,
                "manager" : manager,
                "restaurant" : restaurant,
                "date_of_birth" : date_of_birth,
                "work_right" : work_right,
                "position" : position,
                "pay_per_hour" : pay_per_hour
            })
        })  
            .then(() => navigate("/staff_list"))
    }

    if (!csrfToken){
        return <h1>Loading</h1>
    }

    return (
        <div>
            <h1>Add Staff</h1>
            
            
            <div>
                <form onSubmit={handleSubmit}>    
                        <div>
                            <label>Username</label>
                            <input 
                                type="text"
                                value = {username}
                                onChange = {(event) => setUsername(event.target.value)}
                                />
                        </div>

                        <div>
                            <label>Password</label>
                            <input 
                                type="text" 
                                value = {password}
                                onChange = {(event) => setPassword(event.target.value)}
                                />
                        </div>

                        <div>
                            <label>Name</label>
                            <input 
                                type="text" 
                                value = {name}
                                onChange = {(event) => setName(event.target.value)}
                            />
                        </div>

                        <div>
                            <label>Surname</label>
                            <input 
                                type="text" 
                                value = {surname}
                                onChange = {(event) => setSurname(event.target.value)}
                            />
                        </div>

                        <div>
                            {role === "Owner" && (
                                <div>
                                    <label>Manager</label>
                                    <select value = {manager} onChange = {(event) => setManager(event.target.value)}>
                                        <option value="" disabled>Select Manager</option>
                                        {allSupervisors.map((supervisor) => (
                                            <option key = {supervisor.id} value={supervisor.id}>{supervisor.username}</option>
                                        ))}
                                    </select>
                                </div>
                            )}
                        </div>

                        <div>
                            <label>Restaurant</label>
                            <select value={restaurant} onChange = {(event) => setRestaurant(event.target.value)}>
                                <option value="" disabled > Choose Restaurant </option>
                                {allRestaurants.map((restaurant) => (
                                    <option key={restaurant.pk} value = {restaurant.pk} >{restaurant.restaurant_name}</option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label>Date of Birth</label>
                            <input 
                                type="date" 
                                value = {date_of_birth}
                                onChange = {(event) => setDateOfBirth(event.target.value)}
                            />
                        </div>

                        <div>
                            <label>Date & Time of employment</label>
                            <input 
                                type="datetime-local"
                                value = {date_time_employed}
                                onChange = {(event) => setDateTimeEmployed(event.target.value)} 
                            />
                        </div>

                        <div>
                            <label>Work right</label>
                            <select value={work_right} onChange = {(event) => setWorkRight(event.target.value)}>
                                <option value="" disabled>Chose Right to Work</option>
                                <option value="temp_visa"> Temporary Visa</option>
                                <option value="student_visa">Student Visa</option>
                                <option value="eu_passport">EU Passport</option>
                                <option value="uk_passport">UK Passport</option>
                            </select>
                        </div>

                        <div>
                            <label>Position</label>
                            <select value = {position} onChange = {(event) => setPosition(event.target.value)}>
                                <option value="" disabled>Chose Position</option>
                                <option value="chief">Chief</option>
                                <option value="waiter">Waiter</option>
                                <option value="cleaner">Cleaner</option>
                            </select>
                        </div>

                        <div>
                            <label>Pay per hour</label>
                            <input 
                                type="number"
                                step="0.01"
                                value={pay_per_hour}
                                onChange={(event) => {
                                    const value = event.target.value;

                                    if (/^\d*\.?\d{0,2}$/.test(value)) {
                                        setPayPerHour(value);
                                    }
                                }}
                            />
                        </div>

                        <div>
                            <button type="submit">Add</button>
                        </div>

                </form>
            </div>
        


            <div>
                <button onClick={() => navigate("/staff_list")}>Back</button>
            </div>

        </div>
    )
}

export default StaffAdd;