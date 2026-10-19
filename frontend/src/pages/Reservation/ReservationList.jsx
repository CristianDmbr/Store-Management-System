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
            .then(data => {
                setReservations(data)
            })
    },[]);

    return(
        <div>
            <h1>Reservation List</h1>

            <div>
                {all_reservations.map((reservation) => (
                    <div key={reservation.pk}>
                        <h2> {reservation.name_of_reservation} ({reservation.restaurant_name_display}) : {reservation.reservation_date_time_display}</h2>
                            <button onClick={(event) => {navigate(`/reservation_info/${reservation.pk}`)}}><small>info</small></button>
                            <button onClick={(event) => {navigate(`/reservation_delete/${reservation.pk}`)}}><strong>Delete</strong></button>
                    </div>
                ))}
            </div>

            <div>
                <button onClick={(event) => {navigate("/reservation_add")}}>Book Reservation</button>
            </div>
              
            <div>
                <button onClick={(event) => {navigate("/supervisor_dashboard")}}>Dash Board</button>
            </div>

        </div>
    )
}

export default ReservationList;