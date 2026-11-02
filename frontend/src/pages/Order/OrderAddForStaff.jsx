import { useState, useEffect } from "react";
import {  useNavigate } from "react-router-dom";

function OrderAddForStaff(){

    const navigate = useNavigate();
    const [csrfToken, setCSRFToken] = useState("");

    const [restaurant_pk, setRestaurantPK] = useState("");
    const [restaurant_display_name, setRestaurantDisplayName] = useState("");
    const [staff_pk, setStaffPK] = useState("");
    const [staff_object, setStaffObject] = useState(null);
    const [all_reservations, setAllReservations] = useState([]);
    const [reservation_pk, setReservationPk] = useState("");
    const [number_of_tables, setNumberOfTables] = useState("");
    const [table_number, setTableNumber] = useState("");
    const [note, setNote] = useState("");


    useEffect(()=>{
        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setCSRFToken(data.csrfToken);
            })

        fetch("http://localhost:8000/api/get_staff_restaurant/",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setRestaurantPK(data.restaurant_pk);
                setRestaurantDisplayName(data.restaurant_display_name);
            })
        
        fetch("http://localhost:8000/api/get_staff_logged_in",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setStaffPK(data.staff_object.pk);
                setStaffObject(data.staff_object);
            })
        
        fetch("http://localhost:8000/api/reservation_list",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setAllReservations(data);
            })
        
    },[]);

    useEffect(() => {
        if (!restaurant_pk) return;

        fetch(`http://localhost:8000/api/detail_restaurant/${restaurant_pk}`,{
            "credentials" : "include"
        })
            .then(request => request.json())
            .then(data => {
                setNumberOfTables(data.number_of_tables);
            })

    },[restaurant_pk]);

    function handleStartOrderForStaff(event){
        event.preventDefault();

        const body = {
            "restaurant" : restaurant_pk,
            "staff" : staff_pk,
            "reservation" : reservation_pk,
            "status" : "not_been_served",
            "note" : note,
            "table_number" : table_number
        }

        fetch("http://localhost:8000/api/order_list",{
            credentials : "include",
            method : "POST",
            headers : {
                "X-CSRFToken" : csrfToken,
                "Content-Type": "application/json",
            },
            body : JSON.stringify(body)
        })
            .then(() => {navigate("/order_list")})
    };
    
    return(
        <div>
            
            <h1>Start Order at {restaurant_display_name}</h1>

            <div>
                <form onSubmit={handleStartOrderForStaff}>

                    <div>
                        <label>Reservation :</label>
                        <select value={reservation_pk} onChange={(event) => {setReservationPk(event.target.value)}}>
                            <option value="" disabled>Choose a reservation</option>
                            {all_reservations.map((reservation) => (
                                <option key={reservation.pk} value = {reservation.pk}>{reservation.name_of_reservation}</option>
                            ))}
                        </select>
                    </div>

                    <div>
                        <label>Table Number :</label>
                        <select
                            value={table_number}
                            onChange={(event) => {setTableNumber(event.target.value)}}
                        >
                           <option value="" disabled>Choose a table</option>
                            {Array.from({ length: number_of_tables }, (_, index) => (
                                <option key={index + 1} value={index + 1}>
                                    Table {index + 1}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div style={{ display: "flex", flexDirection: "column", alignItems: "center"}}>
                        <label>Any Notes : </label>
                        <textarea 
                            value={note}
                            onChange={(event) => setNote(event.target.value)}
                            placeholder="Add any special requests or notes..."                           
                            rows={4}
                            cols={40}
                        />
                    </div>

                    <button type="Submit">Submit</button>
                    
                </form>
            </div>

            <div>
                <button onClick={(event) => {navigate("/order_list")}}>Back</button>
            </div>

        </div>
    )    
}

export default OrderAddForStaff;