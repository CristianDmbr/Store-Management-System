import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

function ShiftListStaff(){

    const navigate = useNavigate();

    const [all_shifts, setAllShifts] = useState([]);
    const [role, setRole] = useState();

    useEffect(() => {
        fetch("http://localhost:8000/api/shift_list",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setAllShifts(data.all_shifts);
                setRole(data.role);
            })
    },[]);

    const allShiftsSortedByStatus = all_shifts.reduce((groups,shift) => {
        const category = shift.status_display;

        if (!groups[category]){
            groups[category] = [];
        } 

        groups[category].push(shift);
        
        return groups;

    },{});

    return (
        <div>
            <h1>Shift List</h1>

            <div>
                {Object.entries(allShiftsSortedByStatus).sort(
                    (a,b) => {
                        const shiftPriority = {
                            "Planned" : 1,
                            "Active" : 2,
                            "Completed" : 3,
                        };
                    
                        return shiftPriority[a[0]] - shiftPriority[b[0]];
                    }
                ).map(([status, shifts]) => (
                    <div key={status} >
                        <br />
                        <h2>{status}</h2>
                        {shifts.map((shift) => (
                            <div key={shift.pk} style={{ display: "flex", alignItems: "center", gap: "10px", "justifyContent": "center",}}>
                                <p key={shift.pk}>{new Date(shift.start_time).toLocaleString("en-UK")} - {new Date(shift.end_time).toLocaleString("en-UK")} <small>({shift.duration_hours}hrs)</small></p>
                                <button key = {"button"} onClick={(event) => {navigate(`/shift_info/${shift.pk}`)}}><small>info</small></button>
                            </div>
                        ))}
                    </div>
                ))
                
                }
            </div>

            <br />
            <div>
                <button onClick={(event) => {navigate("/staff_dashboard")}}>Dashboard</button>
            </div>

        </div>
    )
}

export default ShiftListStaff;