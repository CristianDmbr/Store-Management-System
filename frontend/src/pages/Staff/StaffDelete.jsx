import {  useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom"; 

function StaffDelete() {

    const navigate = useNavigate();
    const { staff_pk } = useParams()

    const [csrfToken, setCSRFToken] = useState(null);
    const [staff, setStaff] = useState(null);

    useEffect(() => {
        fetch(`http://localhost:8000/api/detail_staff/${staff_pk}`,{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setStaff(data)
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
            credentials : "include",
            method : "DELETE",
            headers : {
                "X-CSRFToken" : csrfToken
            }
        })  
            .then(response => {
                if (!response.ok) {
                    throw new Error("Failed to Delete Staff")
                }
            })
            .then(() => navigate("/staff_list"))
    }

    if (!staff) {
        return <h1>Loading</h1>
    }

    return (
        <div>
            <h1>Remove {staff.name}? </h1>

            <form onSubmit={handleSubmit}>
                <button type="submit"><strong>YES</strong></button>
            </form>

            <div>
                <button onClick={() => navigate("/staff_list")}>No</button>
            </div>

        </div>
    )
}

export default StaffDelete;