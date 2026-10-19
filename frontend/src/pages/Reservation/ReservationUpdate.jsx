import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect } from "react";
 
function ReservationUpate(){

    const navigate = useNavigate("");
    const { reservation_pk } = useParams();

    const [csrfToken, setCSRFToken] = useState();
    const [reservation, setReservation] = useState("");
    const [all_restaurants, setAllRestaurants] = useState([]);

    const [reservation_name, setReservationName] = useState("");
    const [restaurant_pk, setRestaurantPK] = useState("");
    const [restaurant_name_display, setRestaurantNameDisplay] = useState("");
    const [is_active, setIsActive] = useState("");
    const [kids, setKids] = useState("");
    const [teens, setTeens] = useState("");
    const [adults, setAdults] = useState("");
    const [reservation_date_time, setReservationDateTime] = useState("");
    const [phone_number, setPhoneNumber] = useState("");

    useEffect((event) => {
        fetch(`http://localhost:8000/api/detail_reservation/${reservation_pk}`,{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setReservation(data)
                setReservationName(data.name_of_reservation)
                setRestaurantPK(data.restaurant)
                setRestaurantNameDisplay(data.restaurant_name_display)
                setIsActive(data.is_active)
                setKids(data.kids)
                setTeens(data.teens)
                setAdults(data.adults)
                setReservationDateTime(data.reservation_date_time.slice(0,16))
                setPhoneNumber(data.phone_number === null ? "" : data.phone_number)
            })
        
        fetch("http://localhost:8000/api/my_restaurants/",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setAllRestaurants(data.restaurants)
            })
        
        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setCSRFToken(data.csrfToken)
            })
    },[]);

    function handleUpdate(event){
        event.preventDefault();

        const submitted_data = {
            name_of_reservation : reservation_name,
            restaurant : restaurant_pk,
            is_active : is_active,
            kids : kids,
            teens : teens,
            adults : adults,
            reservation_date_time : reservation_date_time,
            phone_number : phone_number.trim() == "" ? null : phone_number           
        }

        fetch(`http://localhost:8000/api/detail_reservation/${reservation_pk}`,{
            credentials : "include",
            method : "put",
            headers : {
                "X-CSRFToken" : csrfToken,
                "Content-Type": "application/json",
            },
            body : JSON.stringify(submitted_data)
        })
            .then(() => {navigate("/reservation_list")})
    };

    if (!reservation){
        return(
            <div><h1>Loading</h1></div>
        )
    }

    return (
        <div>
            <h1>Update {reservation.name_of_reservation}'s reservation</h1>

            <form onSubmit={handleUpdate}>

                <div>
                    <label>Change Name </label>
                    <input 
                        type="text" 
                        value={reservation_name}
                        onChange = {(event) => {setReservationName(event.target.value)}}    
                    />
                </div>

                <div>
                    <label>Restaurant :</label>
                    <select value={restaurant_pk} onChange = {(event) => {setRestaurantPK(event.target.value)}}>
                        {all_restaurants.map((restaurant) => (
                            <option value={restaurant.pk} key = {restaurant.pk}>{restaurant.restaurant_name}</option>
                        ))}
                    </select>
                </div>

                <div>
                    <label>Active ? </label>
                    <input 
                        type="checkbox" 
                        checked = {is_active}
                        onChange = {(event) => {setIsActive(event.target.checked)}}
                    />
                </div>

                <div>
                    <label>Number of : </label>
                    <div>
                        <label>Kids : </label>
                        <input
                            type="number"
                            min="0"
                            step="1"
                            value={kids}
                            onChange={(event) => {
                                const value = event.target.value;
                                if (value === "" || /^\d+$/.test(value)) {
                                    setKids(value);
                                }
                            }}
                        />

                        <label> Teens : </label>
                        <input
                            type="number"
                            min="0"
                            step="1"
                            value={teens}
                            onChange={(event) => {
                                const value = event.target.value;
                                if (value === "" || /^\d+$/.test(value)) {
                                    setTeens(value);
                                }
                            }}
                        />

                        <label> Adults : </label>
                        <input
                            type="number"
                            min="0"
                            step="1"
                            value={adults}
                            onChange={(event) => {
                                const value = event.target.value;
                                if (value === "" || /^\d+$/.test(value)) {
                                    setAdults(value);
                                }
                            }}
                        />
                    </div>
                </div>

                <div>
                    <label>Change Reservation Date Time : </label>
                    <input 
                        type="datetime-local" 
                        value={reservation_date_time}
                        onChange = {(event) => {setReservationDateTime(event.target.value)}}
                    />
                </div>
                
                <div>
                    <label>Phone Number : </label>
                    <input 
                        type="tel"
                        value={phone_number}
                        onChange = {(event) => {setPhoneNumber(event.target.value)}}
                    />
                </div>

                <button type="submit">Update</button>

            </form>
            
            <div>
                <button onClick={(event) => (navigate("/reservation_list"))}>Back</button>
            </div>

        </div>
    )
}

export default ReservationUpate;