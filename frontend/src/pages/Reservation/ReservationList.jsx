import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import React from "react";

function ReservationList(){

    const navigate = useNavigate();
    const [all_reservations, setAllReservations] = useState([]);

    useEffect(() => {
        fetch("http://localhost:8000/api/reservation_list",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setAllReservations(data)
            })
    },[]);

    const groupedReservations = all_reservations.reduce((groups,reservation) => {
        if (!groups[reservation.restaurant_name_display]){
            groups[reservation.restaurant_name_display] = []
        }

        groups[reservation.restaurant_name_display].push(reservation);

        return groups;
    },{})

    return (
        <div>
            <h1>Reservation List</h1>

            {Object.keys(groupedReservations).map((restaurant) => {
                const reservations = groupedReservations[restaurant];
                const reservation_first = reservations[0]
                return(
                    <div key = {reservation_first.restaurant}>
                        <h2>{restaurant}</h2>
                        {reservations.map((reservation) => (
                            <React.Fragment key = {reservation.pk}>
                                <p>{reservation.name_of_reservation} : {reservation.restaurant_name_display} ({reservation.reservation_date_time_display})</p>
                                <>
                                    <button onClick={(event) => {navigate(`/reservation_info/${reservation.pk}`)}}>info</button>
                                    <button>delete</button>
                                    <button>update</button>
                                </>
                            </React.Fragment>
                        ))}
                    </div>
                )
            })}

            <div>
                <button>Book Reservation</button>
            </div>

            <div>
                <button onClick={(event) => {navigate("/supervisor_dashboard")}}>Dashboard</button>
            </div>

        </div>
    )
}

export default ReservationList;