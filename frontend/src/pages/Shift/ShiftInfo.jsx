import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom"; 

function InfoShift(){

    const navigate = useNavigate();

    const { shift_pk } = useParams();
    
    // From Shift Serializer
    const [employee_name_display, setEmployeeName] = useState("");
    const [employee_surname_display, setEmployeeSurname] = useState("");
    const [start_time_display, setStartTimeDisplay] = useState("");
    const [end_time_display, setEndTimeDisplay] = useState("");
    const [status_display, setStatusDisplay] = useState("");
    const [restaurant_name, setRestaurantName] = useState("");
    // From Shift Model
    const [duration_hours, setDurationHours] = useState("");
    const [earnings, setEarnings] = useState("");

    useEffect((event) => {
        fetch(`http://localhost:8000/api/shift_detail/${shift_pk}`, {
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setEmployeeName(data.serialized_data.employee_name_display)
                setEmployeeSurname(data.serialized_data.employee_surname_display)
                setStartTimeDisplay(data.serialized_data.start_time_display)
                setEndTimeDisplay(data.serialized_data.end_time_display)
                setStatusDisplay(data.serialized_data.status_display)
                setRestaurantName(data.serialized_data.display_restaurant)
                setDurationHours(data.duration_hours)
                setEarnings(data.earnings)
            })
    })


    return (
        <div>
            <h1>Shift Info</h1>

            <div>

                <div>
                    <label> Employee : </label>
                    <p>{employee_name_display} {employee_surname_display}</p>
                </div>

                <div>
                    <label>Duration :</label>
                    <p>{duration_hours} Hrs</p>
                </div>

                <div>
                    <label>Start Time : </label>
                    <p>{start_time_display}</p>
                </div>

                <div>
                    <label>End Time : </label>
                    <p>{end_time_display}</p>
                </div>

                <div>
                    <label>Status :</label>
                    <p>{status_display}</p>
                </div>

                <div>
                    <label>Restaurant Name</label>
                    <p>{restaurant_name}</p>
                </div>

                <div>
                    <label>Earning :</label>
                    <p>£{earnings}</p>
                </div>


            </div>

            <div>
                <button onClick={(event) => {navigate("/shifts_list")}}>Back</button>
            </div>

        </div>
    )
}

export default InfoShift;