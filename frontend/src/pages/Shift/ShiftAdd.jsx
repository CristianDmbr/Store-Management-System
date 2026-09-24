import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
 
function AddShift(){

    const navigate = useNavigate();
    const [csrfToken, setCSRFToken] = useState("");
    const [all_employees, setAllEmployees] = useState([]);

    const [ employee, setEmployee ] = useState("");
    const [ start_time, setStartTime] = useState("");
    const [ end_time, setEndTime] = useState("");
    const [ status, setStatus ] = useState("");


    useEffect(() => {
        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setCSRFToken(data.csrfToken)
            })
        
        fetch("http://localhost:8000/api/all_staff",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setAllEmployees(data)
            })
        
    },[])

    function HandleSubmit(event) {
        event.preventDefault();

        fetch("http://localhost:8000/api/shift_list",{
            method : "post",
            credentials : "include",
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
        .then(response => {

            if (!response.ok) {

                return response.json().then(data => {

                    console.log("Django error:", data);

                    throw new Error(`HTTP ${response.status}`);

                });

            }

            return response.json();

        })
            .then(() => navigate("/shifts_list"))
            .catch((error) => {
                console.log(error)
            })
    }

    return (
        <div>
            <h1>Add Shift :</h1>

            <form onSubmit={HandleSubmit}>

                <div>
                    <label>Staff : </label>
                    <select value={employee} onChange = {(event) => {setEmployee(event.target.value)}}>
                        <option value="" disabled>Choose a Staff Member</option>
                        {all_employees.map((employee) => (
                            <option key = {employee.pk} value = {employee.pk}>{employee.name} {employee.surname}</option>
                        ))}
                    </select>
                </div>

                <div>
                    <label>Start Time</label>
                    <input 
                        type="datetime-local" 
                        value = {start_time}
                        onChange = {(event) => {setStartTime(event.target.value)}}
                    />
                </div>

                <div>
                    <label>End Time</label>
                    <input 
                        type="datetime-local" 
                        value= {end_time}
                        onChange = {(event) => {setEndTime(event.target.value)}}
                    />
                </div>

                <div>
                    <label>Status</label>
                    <select value = {status} onChange = {(event) => {setStatus(event.target.value)}}>
                        <option value="" disabled>Chose a Status</option>
                        <option value = "planned">Planned</option>
                        <option value = "active" >Active</option>
                        <option value="completed">Completed</option>
                    </select>
                </div>

                <button type="submit">Add</button>

            </form>

            <div>
                <button onClick={(event) => {navigate("/shifts_list")}}>Back</button>
            </div>

        </div>
    )
}

export default AddShift;