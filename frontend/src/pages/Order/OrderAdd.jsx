import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

function OrderAdd(){

    const navigate = useNavigate();
    const {restaurant_pk} = useParams();
    const [restaurantObject, setRestaurantObject] = useState(null);
    const [numberOfTablesForRestaurant, setNumberOfTablesForRestaurant] = useState();
    const [role, setRole] = useState();

    const [all_reservations, setAllReservations] = useState([]);
    const [all_staff_at_restaurant, setAllStaffAtRestaurant] = useState([]);

    const [reservation, setReservation] = useState("");
    const [restaurant, setRestaurant] = useState(restaurant_pk);
    const [staff, setStaff] = useState("");
    const [table_number, setTableNumber] = useState("");

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

    },[restaurant_pk]);

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
                <label>Table Number : </label>
            </div>

            <div>
                <button onClick={(event) => {navigate("/order_list")}}>Back</button>
            </div>
        </div>
    )
}

export default OrderAdd;