import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function StaffList(){

    const navigate = useNavigate();

    const [all_staff, setAllStaff] = useState([]);

    useEffect(() => {
        fetch("http://localhost:8000/api/all_staff",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setAllStaff(data)
            })
    })
    

    return (
        <div>
            <h1>Staff List</h1>

            <div>
                {all_staff.map((staff) => (
                    <div key = {staff.pk}>
                        <h2>{staff.name} {staff.surname}</h2>
                        <p>{staff.restaurant_name}</p>
                        <p>{staff.date_of_birth}</p>
                        <p>{staff.work_right}</p>
                    </div>
                ))}
            </div>

            <div>
                <button onClick={() => navigate("/owner_dashboard")}>Back</button>
            </div>

        </div>
    )
}

export default StaffList;