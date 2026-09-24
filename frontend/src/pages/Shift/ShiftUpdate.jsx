import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect } from "react";

function UpdateShift(){

    const navigate = useNavigate();
    const { shift_pk } = useParams();
    const [csrfToken, setCSRFToken] = useState();

    const [employee, setEmployee] = useState("");
    const [start_time, setStartTime] = useState("");
    const [end_time, setEndTime] = useState("");
    const [status, setStatus] = useState("");

    useEffect(() =>{
        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setCSRFToken(data.csrfToken)
            })
        
        fetch(`http://localhost:8000/api/shift_detail/${shift_pk}`,{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setEmployee(data.serialized_data.employee)
                // Slice allows to display the already existing date time
                // Without it the input box is empty
                setStartTime(data.serialized_data.start_time.slice(0, 16))
                setEndTime(data.serialized_data.end_time.slice(0, 16))
                setStatus(data.serialized_data.status)
            })
    },[shift_pk])

    function HandleUpdate(event) {
        event.preventDefault();

        fetch(`http://localhost:8000/api/shift_detail/${shift_pk}`,{
            credentials : "include",
            method : "PUT",
            headers : {
                "Content-Type": "application/json",
                "X-CSRFToken" : csrfToken
            },
            body : JSON.stringify({
                "employee" : employee,
                "start_time" : start_time,
                "end_time" : end_time,
                "status" : status
            })
        })
            .then(() => {navigate("/shifts_list")})
    }

    return(
        <div>
            <h1>Update Shift</h1>

            <form onSubmit={HandleUpdate} >

                <div>
                    <label>Start Time :</label>
                    <input 
                        type="datetime-local" 
                        value={start_time}
                        onChange = {(event) => {setStartTime(event.target.value)}}
                    />
                </div>

                <div>
                    <label>End Time :</label>
                    <input 
                        type="datetime-local"
                        value={end_time}
                        onChange = {(event) => {setEndTime(event.target.value)}} 
                    />
                </div>
            
                <div>
                    <label>Status :</label>
                    <select value = {status} onChange = {(event) => {setStatus(event.target.value)}}>
                        <option value="" disabled>Chose a Status</option>
                        <option value="planned"> Planned </option>
                        <option value="active"> Active </option>
                        <option value="completed"> Completed </option>
                    </select>

                </div>

                <button type="submit">Update</button>

            </form>

            <div>
                <button onClick={() => {navigate("/shifts_list")}}>Back</button>
            </div>

        </div>
    )
}

export default UpdateShift;