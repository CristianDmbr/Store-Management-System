import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

function ReservationList(){

    const navigate = useNavigate();
    const [all_reservations, setReservations] = useState([]);

    useEffect(() => {
        fetch("http://localhost:8000/api/reservation_list",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => setReservations(data))
            console.log(all_reservations)
    },[])

    return(
        <div>
            <h1>Reservation List</h1>
            
            <div>
                <button onClick={(event) => {navigate("/supervisor_dashboard")}}>Dash Board</button>
            </div>

        </div>
    )
}

export default ReservationList;