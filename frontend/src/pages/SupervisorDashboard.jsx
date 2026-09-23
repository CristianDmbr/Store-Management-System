import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import UserGreetings from "../components/Greetings";


function SupervisorDashboard() { 

    const navigate = useNavigate();
    const [csrfToken, setCSRFToken] = useState();

    useEffect((event) => {
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

        fetch("http://localhost:8000/api/logout", {
            method : "post",
            headers : {
                "X-CSRFToken" : csrfToken
            }
        })
            .then(() => {
                navigate("/login")
            })
    }

    return (
        <div>
            <h1>Supervisor's Dashboard page</h1>
            <UserGreetings/>

            <button onClick={(event) => {navigate("/staff_list")}}>Manage Staff</button>

            <div>
                <button onClick={handleSubmit}>Logout</button>
            </div>

        </div>
    );
};

export default SupervisorDashboard