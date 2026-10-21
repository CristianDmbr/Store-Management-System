import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function OrderList(){

    const navigate = useNavigate("");

    const [role, setRole] = useState("");
    const [all_orders, setAllOrders] = useState([]);

    useEffect(() =>{
        fetch("http://localhost:8000/api/order_list",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setRole(data.role);
                setAllOrders(data.orders)
            })
    },[]);

    const orders_by_restaurants_status = all_orders.reduce((groups, order) => {
        const restaurant = order.restaurant_name;
        const status = order.order_status_display;

        if (!groups[restaurant]){
            groups[restaurant] = {}
        }

        if (!groups[restaurant][status]){
            groups[restaurant][status] = []
        }

        groups[restaurant][status].push(order);

        return groups;
    },{});

    return (
        <div>
            <h1>Order List</h1>

            <div>
                {Object.entries(orders_by_restaurants_status).map(([restaurant,orders_by_status]) => (
                    <div key = {restaurant}>
                        <h2>{restaurant}</h2>

                        {!orders_by_status && (
                            <h2>No Order</h2>
                        )}

                        {Object.entries(orders_by_status).map(([status,orders]) => (
                            <div key={status}>
                                <h3>{status}</h3>
                                {orders.map((order) => (
                                    <p key={order.pk}>Table Number : {order.table_number}</p>
                                ))}
                            </div>
                        ))}
                    </div>
                ))}
            </div>

            <div>
                {role === "supervisor" && (
                    <button onClick={(event) => {navigate("/supervisor_dashboard")}}>Back</button>
                )}
                {role === "staff" && (
                    <button onClick={(event) => {navigate("/staff_dashboard")}}>Back</button>
                )}
            </div>
        </div>
    )
}

export default OrderList;