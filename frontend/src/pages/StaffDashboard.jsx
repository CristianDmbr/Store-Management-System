import { useState } from "react";
import { useEffect, useCase } from "react";
import { useNavigate } from "react-router-dom";

function StaffDashboard(){

    const navigate = useNavigate();
    const [ csrfToken, setCSRFToken] = useState();

    useEffect(() => {
        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setCSRFToken(data.csrfToken)
            })
    },[]);

    function handleSubmit(event){
        event.preventDefault();

        fetch("api/logout",{
            credentials : "include",
            method : "POST",
            headers : {
                "X-CSRF" : csrfToken
            }
        })
            .then(navigate("/login"))
    }

    return (
        <div>
            <h1>Staff Dashboard</h1>

            <div>
                <button onClick={handleSubmit}>Logout</button>
            </div>
        </div>
    );
};

export default StaffDashboard