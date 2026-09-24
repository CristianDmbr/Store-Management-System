import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import React from "react";
  
function ShiftList(){

    const navigate = useNavigate("");

    const [all_shifts, setAllShifts] = useState([]);
    const [role, setRole] = useState("");
    const [csrfToken, setCSRFToken] = useState("");

    useEffect(() => {
        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setCSRFToken(data.csrfToken)
            })

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

    function HandleRedirects(event) {
        if (role == "Owner"){
            navigate("/owner_dashboard")
        }
        else if (role == "Supervisor"){
            navigate("/supervisor_dashboard")
        }
    }

    // Not actually refreshing the page, we are modidying all shifts to remove the one we removed.
    // Because React does not allow to refresh and navigate on the same page we are already on.
    // Deleting from the Database does not immediatelly update the useState.
    function HandleDeleteshift(shift_pk){
        fetch(`http://localhost:8000/api/shift_detail/${shift_pk}`,{
            credentials : "include",
            method : "delete",
            headers : {
                "X-CSRFToken" : csrfToken
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error: ${response.status}`);
            }
            setAllShifts(
                // Filter all of the shift that doesn't have the shift pk. Arrow function.
                // Every time we click it, we remove the pk we deleted from the Database from the useState as well.
                all_shifts.filter(shift => shift.pk !== shift_pk)
            );
        })
        .catch(error => {
            console.log(error);
        });
    }

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
                            <React.Fragment key={shift.pk}>
                                <p> {shift.start_time_display} : {shift.end_time_display}{" "} <small>{shift.status_display}</small> </p>

                                {role === "Supervisor" && (
                                    <>
                                        <button onClick={() => navigate(`/shift_info/${shift.pk}`)}> View </button>

                                        <button onClick={() => HandleDeleteshift(shift.pk)}>Remove</button>
                                    </>
                                )}
                            </React.Fragment>
                        ))}
                    </div>
                )
            })}

            {role == "Supervisor" && (
                <div>
                    <button onClick={(event) => {navigate("/shift_add")}}>Schedule Shift</button>
                </div>
            )}

            <div>
                <button onClick = {HandleRedirects}>Back</button>
            </div>

        </div>
    )
}

export default ShiftList;