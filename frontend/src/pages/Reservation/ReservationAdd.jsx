// The Reservation model has "created_at" field which does not need to be pushed here since its set to a default value
// in the models.py page.
// We still mention it inside of the serializer to be able to display it for reservation info page.
// Test
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

function ReservationAdd(){

    const navigate = useNavigate();
    const [csrf_token, setCSRFToken] = useState();
    const [all_restaurants, setRestaurants] = useState([]);

    const [name_of_reservation, setNameOfReservation] = useState("");
    const [restaurant_pk, setRestaurantPK] = useState("");
    const [is_active, setIsActive] = useState(true);
    const [kids, setKids] = useState();
    const [teens, setTeens] = useState();
    const [aduls, setAdults] = useState();
    const [reservation_date_time, setReservationDateTime] = useState("");
    const [phone_number, setPhoneNumber] = useState("");

    useEffect(() => {
        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
           })
            .then(request => request.json())
            .then(data => {
                setCSRFToken(data.csrfToken)
            })
        
        fetch("http://localhost:8000/api/my_restaurants",{
            credentials : "include"
        })
            .then(request => request.json()) 
            .then(data => {
                setRestaurants(data.restaurants)
            })
    },[]);

    function handleSubmit(event){
        event.preventDefault();

        const reservationData = {
            name_of_reservation : name_of_reservation,
            restaurant : restaurant_pk,
            is_active : is_active,
            kids : kids,
            teens : teens,
            aduls : aduls,
            reservation_date_time : reservation_date_time,
            phone_number : phone_number.trim() === "" ? null : phone_number
        }

        fetch("http://localhost:8000/api/reservation_list",{
            credentials : "include",
            method : "post",
            headers : {
                "X-CSRFToken" : csrf_token,
                "Content-Type": "application/json",
            },
            body : JSON.stringify(reservationData)
        })
            .then(() => {navigate("/reservation_list")})
    }

    return (
        <div>
            <h1>Add Reservation</h1>

            <form onSubmit={handleSubmit}>

                <div>
                    <label>Active : </label>
                    <input 
                        type= "checkbox"
                        checked={is_active}
                        onChange = {(event) => setIsActive(event.target.checked)}
                        />
                </div>

                <div>
                    <label>Reservation Name : </label>
                    <input 
                        type="text"
                        value={name_of_reservation}
                        onChange = {(event) => {setNameOfReservation(event.target.value)}}
                        required 
                    />
                </div>

                <div>
                    <label>Restaurant : </label>
                    <select value = {restaurant_pk} onChange = {(event) => {setRestaurantPK(event.target.value)}} required>
                        <option value="" disabled>Select a Restaurant</option>
                        {all_restaurants.map((restaurant) => (
                            <option value= {restaurant.pk} key = {restaurant.pk}>{restaurant.restaurant_name}</option>
                        ))}
                    </select>
                </div>

                <div>
                    <label>Number of :</label>
                    <div>
                        <label><small>Kids : </small></label>
                        <input
                            type="number"
                            min="0"
                            step="1"
                            value={kids}
                            onChange={(event) => {
                                const value = event.target.value;
                                if (value === "" || /^\d+$/.test(value)) { setKids(value);}
                                }}
                            />

                        <label><small> Teens : </small></label>
                        <input 
                            type="number" 
                            value={teens}
                            onChange = {(event) => {
                                const value = event.target.value;
                                if (value === "" || /^\d+$/.test(value)) { setTeens(value);
                                }}}
                            />

                        <label><small>Adults : </small></label>
                        <input 
                            type="number"
                            value={aduls}
                            onChange = {(event) => {
                                const value = event.target.value;
                                if (value === "" || /^\d+$/.test(value)) { setAdults(value); }
                                }} 
                            />

                    </div>
                </div>

                <div>
                    <label>Booking date and time : </label>
                    <input 
                        type="datetime-local" 
                        value={reservation_date_time}
                        onChange = {(event) => {setReservationDateTime(event.target.value)}}
                        required
                    />
                </div>

                <div>
                    <label>Phone Number <small>(optional)</small></label>
                    <input 
                    type="tel" 
                    value={phone_number}
                    onChange = {(event) => {setPhoneNumber(event.target.value)}}
                    />
                </div>

                <button type="submit">Submit</button>

            </form>

            <div>
                <button onClick={(event) => {navigate("/reservation_list")}}>Back</button>
            </div>

        </div>
    )
}

export default ReservationAdd;