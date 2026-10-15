import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

function ReservationAdd(){

    const navigate = useNavigate();
    const [csrf_token, setCSRFToken] = useState();
    const [all_restaurants, setRestaurants] = useState([]);

    useEffect(() => {
        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
           })
            .then(request => request.json())
            .then(data => {
                setCSRFToken(data.csrfToken)
            })
        
        fetch("http://localhost:8000/api/my_restaurants",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setRestaurants(data.restaurants)
            })
        
    },[]);

    return (
        <div>
            <h1>Add Reservation</h1>

            <div>
                <button onClick={(event) => {navigate("/reservation_list")}}>Back</button>
            </div>

        </div>
    )
}

export default ReservationAdd;