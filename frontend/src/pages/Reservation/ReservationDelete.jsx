import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
 
function ReservationDelete(){

    const navigate = useNavigate("");
    const { reservation_pk } = useParams();
    const [ csrf_token, setCSRFToken ] = useState("");

    const [reservation, setReservation] = useState(null);

    useEffect(() => {
        fetch(`http://localhost:8000/api/detail_reservation/${reservation_pk}`,{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setReservation(data)
            })
        
        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setCSRFToken(data.csrfToken)
            })
    },[reservation_pk]);

    function handleSubmit(event) {
        event.preventDefault();

        fetch(`http://localhost:8000/api/detail_reservation/${reservation_pk}`,{
            credentials : "include",
            method : "delete",
            headers : {
                "X-CSRFToken" : csrf_token
            }
        })
            .then(() => navigate("/reservation_list"))
    }; 

    if (!reservation) {
        return (
            <div>
                <h1>Loading</h1>
                <div>
                    <button onClick={(event) => {navigate("/reservation_list")}}>Back</button>
                </div>
            </div>
        )
    }

    return (
        <div>
            <h1>Delete {reservation.name_of_reservation}'s reservation for {reservation.restaurant_name_display} ?</h1>

            <form onSubmit={handleSubmit}>
                <button type="submit"><strong>Yes</strong></button>
            </form>

            <div>
                <button onClick={(event) => {navigate("/reservation_list")}}>No</button>
            </div>

        </div>
    )
}

export default ReservationDelete;