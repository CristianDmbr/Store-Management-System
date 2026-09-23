import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
  
function ShiftList(){

    const navigate = useNavigate();

    const [all_shifts, setAllShifts] = useState([]);
    const [role, setRole] = useState("");

    useEffect(() => {
        fetch("http://localhost:8000/api/shift_list",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setAllShifts(data.all_shifts)
                setRole(data.role)
            })
    },[])

    const groupedShifts = all_shifts.reduce((group, shift) => {
        if (!group[shift.employee]){
            group[shift.employee] = [];
        }

        group[shift.employee].push(shift);

        return group
    },{})

    return (
        <div>
            <h1>Shift List</h1>

            {Object.keys(groupedShifts).map((employeePK) =>{
                const shifts = groupedShifts[employeePK];
                const employee = shifts[0];
                return(
                    <div key = {employeePK}>
                        <h2>{employee.employee_name_display} {employee.employee_surname_display}</h2>
                        {shifts.map((shift) => (
                            <p key = {shift.pk}>
                                {shift.start_time_display} : {shift.end_time_display} <small>{shift.status_display}</small>
                            </p>
            ))}
                    </div>
                )
            })}

            <div>
                <button onClick = {(event) => {navigate("/owner_dashboard")}}>Back</button>
            </div>

        </div>
    )
}

export default ShiftList;