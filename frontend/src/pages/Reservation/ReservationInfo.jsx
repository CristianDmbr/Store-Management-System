import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

function ReservationInfo(){

    const navigate = useNavigate("");
    const { reservation_pk } = useParams();

    const [reservation, setReservation] = useState(null);

    useEffect(() => {
        fetch(`http://localhost:8000/api/detail_reservation/${reservation_pk}`,{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setReservation(data)
            })
    },[reservation_pk]);

    if (!reservation) {
        return (
            <div>
                <h1>Loading</h1>
            </div>
        )
    }
    
    return(
        <div>
            <h1>Reservation Information</h1>
            <p>
                <label>Reservation Name</label> : {reservation.name_of_reservation}
            </p>
            <p>
                <label>Restaurant</label> : {reservation.restaurant_name_display}
            </p>

            <p>
                <label>Is Active ?</label> : {reservation.is_active === true ? "Yes" : "No"}
            </p>

            <p>
                <label>Number of Kids</label> : {reservation.kids}
            </p>

            <p>
                <label>Number of Teens</label> : {reservation.teens}
            </p>

            <p>
                <label>Number of Aduls</label> : {reservation.adults}
            </p>

            <p>
                <label>Reservation Date Time Display</label> : {reservation.reservation_date_time_display}
            </p>

            <p>
                <label>Created At</label> : {reservation.created_at_display}
            </p>

            <p>
                <label>Phone Number</label> : {reservation.phone_number ? reservation.phone_number : "None"}
            </p>

            <div>
                <button onClick={(event) => {navigate("/reservation_list")}}>Back</button>
            </div>

        </div>
    )

}

export default ReservationInfo;