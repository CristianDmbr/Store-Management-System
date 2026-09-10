import UserGreetings from "../components/Greetings";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { useEffect } from "react";
 
function OwnerDashboard() {

    const navigate = useNavigate("");

    const [csrfToken, setToken] = useState("")

    useEffect(() => {
        fetch("http://localhost:8000/api/csrf", {
            credentials : "include"
        }).then(request => request.json())
          .then(data => {
            setToken(data.csrfToken)
          })
    },[])

    function logout() {
        fetch("http://localhost:8000/api/logout",{
            credentials : "include",
            method : "POST",
            headers : {
                "X-CSRFToken" : csrfToken 
            }
        })
            .then(response => response.data)
            .then(data => {
                console.log(data);
                console.log("Logged out")
                navigate("/login");
            });
    }

    return (
        <div>
            <UserGreetings />
            <h1>Owner's Dashboard</h1>

            <div>
                <button onClick={(event) => navigate("/restaurant_list")}>Manage Restaurants</button>
            </div>

            <div>
                <button onClick={logout}> Logout </button>
            </div>
        </div>
    );
};

export default OwnerDashboard