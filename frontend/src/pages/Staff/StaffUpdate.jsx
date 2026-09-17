import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

function StaffUpdate(){

    const navigate = useNavigate();
    const { staff_pk } = useParams();
    const [role, setRole] = useState("");
    const [allSupervisors, setAllSupervisors] = useState([]);
    const [allRestaurants, setAllRestaurants] = useState([]);
    const [csrfToken, setCSRFToken] = useState();

    const [staff, setStaff] = useState(null);
    
    const [user, setUser] = useState();
    const [name, setName] = useState();
    const [display_name, setDisplayName] = useState();
    const [surname, setSurname] = useState();
    const [manager, setManager] = useState();
    const [restaurant, setRestaurant] = useState();
    const [date_of_birth, setDateOfBirth] = useState();
    const [date_time_employed, setDateTimeEmployed] = useState();
    const [work_right, setWorkRight] = useState();
    const [position, setPosition] = useState();
    const [pay_per_hour, setPayPerHour] = useState();


    useEffect(() => {
        fetch(`http://localhost:8000/api/detail_staff/${staff_pk}`,{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setRole(data.role)

                setUser(data.staff.user)
                setName(data.staff.name)
                setDisplayName(data.staff.name)
                setSurname(data.staff.surname)
                setManager(data.staff.manager)
                setRestaurant(data.staff.restaurant)
                setDateOfBirth(data.staff.date_of_birth)
                setDateTimeEmployed(data.staff.date_time_employed)
                setWorkRight(data.staff.work_right)
                setPosition(data.staff.position)
                setPayPerHour(data.staff.pay_per_hour)

                setStaff(data.staff)
            })
        
        fetch("http://localhost:8000/api/my_restaurants", {
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setAllRestaurants(data.restaurants)
            })

        fetch("http://localhost:8000/api/get_supervisors",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setAllSupervisors(data)
            })
        
        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setCSRFToken(data.csrfToken)
            })
    },[staff_pk])

    function handleSubmit(event) {
        event.preventDefault();

        fetch(`http://localhost:8000/api/detail_staff/${staff_pk}`,{
            method : "PUT",
            credentials : "include",
            headers : {
                "X-CSRFToken" : csrfToken,
                "Content-Type": "application/json"
            },
            body : JSON.stringify({
                "user" : user,
                "name" : name,
                "surname" : surname,
                "manager" : manager,
                "restaurant" : restaurant,
                "date_of_birth" : date_of_birth,
                "date_time_employed" : date_time_employed,
                "work_right" : work_right,
                "position" : position,
                "pay_per_hour" : pay_per_hour
            })
        })
            .then(response => {
                if (response.ok) {
                    navigate("/staff_list");
                } else {
                    console.log("Updated Failed", response.status)
                }
            })
    }


    if (!staff) {
        return <h1>Loading</h1>
    }

    return (
        <div>
            <h1>Update {display_name}'s profile</h1>

            <form onSubmit={handleSubmit}>

                <div>
                    <label>Name</label>
                    <input 
                        type="text" 
                        value={name}
                        onChange = {(event) => setName(event.target.value)}
                    />
                </div>

                <div>
                    <label>Surname</label>
                    <input 
                        type="text"
                        value={surname}
                        onChange = {(event) => setSurname(event.target.value)}
                    />
                </div>
                
                <div>
                    { role == "Owner" && (
                        <div>
                            <label>Manager</label>
                            <select value={manager} onChange = {(event) => setManager(event.target.value)}>
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
                        {allRestaurants.map((rest) => (
                            <option key ={rest.pk} value ={rest.pk} >{rest.restaurant_name}</option>
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
                    <label>Work Right</label>
                    <select value= {work_right} onChange = {(event) => setWorkRight(event.target.value)}>
                        <option value={"temp_visa"}>Temporary Visa</option>
                        <option value={"student_visa"}>Student Visa</option>
                        <option value={"uk_passport"}>UK Passport</option>
                        <option value={"eu_passport"}> European Passport</option>
                    </select>
                </div>

                <div>
                    <label>Position</label>
                    <select value={position} onChange = {(event) => setPosition(event.target.value)}>
                        <option value={"chief"}>Chief</option>
                        <option value={"waiter"}>Waiter</option>
                        <option value={"cleaner"}>Cleaner</option>
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
                    <button type="submit">Update</button>
                </div>

            </form>

            <div>
                <button onClick={(event) => navigate("/staff_list")}>Back</button>
            </div>

        </div>
    )
}

export default StaffUpdate;