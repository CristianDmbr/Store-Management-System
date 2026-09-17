import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function StaffList(){

    const navigate = useNavigate();

    const [all_staff, setAllStaff] = useState([]);

    useEffect(() => {
        fetch("http://localhost:8000/api/all_staff", {
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setAllStaff(data)
            })
    },[])

    return (
        <div>
            <h1>Staff List</h1>

            {all_staff.map((staff) => {
                return(
                    <div key={staff.pk}>
                        <h2>{staff.name} {staff.surname}</h2>
                        <p>{staff.restaurant_name} ( {staff.position_display} )</p>   
                        <button onClick={(event) => navigate(`/staff_info/${staff.pk}`)}>Info</button>
                        <button onClick={(event) => navigate(`/staff_delete/${staff.pk}`)}>Delete</button>
                        <button onClick={(event) => navigate(`/staff_update/${staff.pk}`)}>Update</button>
                    </div>
                )
            })}

            <div>
                <button onClick={() => {navigate("/staff_add")}}>Add Staff</button>
            </div>

            <div>
                <button onClick={(event) => navigate("/owner_dashboard")}>Back</button>
            </div>

        </div>
    )
     

}

export default StaffList;