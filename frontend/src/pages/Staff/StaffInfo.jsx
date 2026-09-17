import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

function StaffInfo(){

    const navigate = useNavigate();

    const { staff_pk } = useParams();
    const [staff, setStaff] = useState("");

    useEffect(() => {
        fetch(`http://localhost:8000/api/detail_staff/${staff_pk}`, {
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setStaff(data.staff)
            });
    }, [staff_pk])

    if (!staff){
        return <h1>Loading</h1>
    }

    return (
        <div>
            <h1>Info Page</h1>

                <h2>{staff.name} {staff.surname}</h2>
                <p>Restaurant : {staff.restaurant_name}</p>
                <p>Date of Birth : {staff.date_of_birth}</p>
                <p>Date Employed : {new Date(staff.date_time_employed).toLocaleDateString("en-GB")}</p>
                <p>Work Right : {staff.display_work_right}</p>
                <p>Position : {staff.position_display}</p>
                <p>Pay per hour : {staff.pay_per_hour}</p>

            <div>
                <button onClick={() => navigate("/staff_list")}>Back</button>
            </div>

        </div>
    )
}

export default StaffInfo;