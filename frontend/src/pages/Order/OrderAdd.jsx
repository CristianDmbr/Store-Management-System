import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

function OrderAdd(){

    const navigate = useNavigate();
    const [csrfToken, setCSRFToken] = useState();

    const {restaurant_pk} = useParams();
    const [restaurantObject, setRestaurantObject] = useState(null);
    const [numberOfTablesForRestaurant, setNumberOfTablesForRestaurant] = useState();
    const [role, setRole] = useState();

    const [all_reservations, setAllReservations] = useState([]);
    const [all_staff_at_restaurant, setAllStaffAtRestaurant] = useState([]);

    const [reservation, setReservation] = useState("");
    const [staff, setStaff] = useState("");
    const [table_number, setTableNumber] = useState("");
    const [note, setNote] = useState("");

    useEffect(() => {
        fetch(`http://localhost:8000/api/detail_restaurant/${restaurant_pk}`,{
            credentials :"include"
        })
            .then(request => request.json())
            .then(data => {
                setRestaurantObject(data);
                setNumberOfTablesForRestaurant(data.number_of_tables);
            })
        
        fetch("http://localhost:8000/api/user_name", {
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setRole(data.role)
            })
        
        fetch("http://localhost:8000/api/reservation_list",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => { 
                setAllReservations(data)
            })
        
        fetch("http://localhost:8000/api/all_staff",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setAllStaffAtRestaurant(data)
            })
        
        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setCSRFToken(data.csrfToken)
            })
        
    },[restaurant_pk]);

    function handleSubmit(event) {
        event.preventDefault();

        const body = {
            "reservation" : reservation,
            "restaurant" : restaurant_pk,
            "staff" : staff,
            "table_number" : table_number,
            "status" : "not_been_served",
            "note" : note
        }

        fetch("http://localhost:8000/api/order_list",{
            "credentials" : "include",
            "method" : "post",
            headers : {
                "X-CSRFToken" : csrfToken,
                "Content-Type": "application/json",
            },
            body : JSON.stringify(body)
        })
            .then(() => navigate("/order_list"))
        
    };

    if (!restaurantObject) {
        return(
            <div>
                <h1>Loading</h1>
            </div>
        )
    }

    return (
        <div>
            <h1>Start Order at {restaurantObject.restaurant_name}</h1>

            <form onSubmit={handleSubmit}>
                <div>
                    <label>Reservation :</label>
                    <select value={reservation} onChange = {(event) => {setReservation(event.target.value)}}>
                        <option key={""} value="" disabled>Choose Reservation</option>
                        {all_reservations.map((reservation) => (
                            <option key={reservation.pk} value = {reservation.pk}>{reservation.name_of_reservation}</option>
                        ))}
                    </select>
                </div>

                <div>
                    {role === "Supervisor" && (
                        <div>
                            <label>Staff : </label>
                            <select value={staff} onChange = {(event) => {setStaff(event.target.value)}}>
                                <option key = {""} value="" disabled>Assign Staff</option>
                                {all_staff_at_restaurant.map((employee) => (
                                    <option key={employee.pk} value = {employee.pk}>{employee.name}</option>
                                ))}
                            </select>
                        </div>
                    )}
                </div>

                <div>
                    <label>TAble Number : </label>
                    <select value={table_number} onChange = {(event) => {setTableNumber(event.target.value)}}>
                        <option value="" disabled>Choose a table</option>
                        {/* Array.from generates table numbers from 1 to the restaurant's capacity.
                        (value, index) => index + 1 uses the index (starting at 0) to generate numbers starting at 1.
                        .map() loops through the completed array and converts each number into a dropdown option.
                        key identifies each option; value sets the selected option's value. */}
                        {Array.from( {length : numberOfTablesForRestaurant}, (value, index) => index + 1).map((table) => (
                            <option  key = {table} value={table}>{table}</option>
                        ))}
                    </select>
                </div>

                <div>
                    <label>Notes <small>(optional)</small> : </label>
                    <div>
                    <textarea 
                        type="textarea" 
                        value={note}
                        onChange = {(event) => {setNote(event.target.value)}}
                        rows = {8}
                        cols = {50}
                        placeholder = "Write any notes here ..."
                    />
                    </div>
                </div>

                <button type = "submit">Submit</button>
            </form>

            <div>
                <button onClick={(event) => {navigate("/order_list")}}>Back</button>
            </div>
        </div>
    )
}

export default OrderAdd;