import { useState, useEffect } from "react";
import { resolvePath, useNavigate } from "react-router-dom";

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

    const restaurant_orders_by_status = all_orders.reduce((groups,order) => {
        const restaurant_pk = order.restaurant;
        const restaurant_name = order.restaurant_name;
        const status = order.order_status_display;

        if (!groups[restaurant_pk]) {
            groups[restaurant_pk] = {
                "restaurant_name" : restaurant_name,
                "orders_by_status" : {}
            }
        };

        if (!groups[restaurant_pk].orders_by_status[status]){
            groups[restaurant_pk].orders_by_status[status] = []
        };
        

        groups[restaurant_pk].orders_by_status[status].push(order);

        return groups;

    },{});

    return (
        <div>
            <h1>Order List</h1>

            <div >
                {Object.entries(restaurant_orders_by_status).map(([restaurant, restaurant_data]) => (
                    <div key={restaurant}>
                        <h2>{restaurant_data.restaurant_name}</h2>

                        {!restaurant_data.orders_by_status && (
                            <h3>No Orders</h3>
                        )}
                        
                        
                        {Object.entries(restaurant_data.orders_by_status).sort(
                            (a,b) => {
                                const statusOrder = {
                                    "Not served" : 1,
                                    "Waiting" : 2,
                                    "Complete" : 3                                
                            };
                            return statusOrder[a[0]] - statusOrder[b[0]];
                        }).map(([status,orders]) => (
                            
                            <div key={status}>
                                <h3>{status}</h3>
                                {orders.map((order) => ( 
                                    <div key={order.pk} style={{
                                        display : "flex",
                                        alignItems: "center",
                                        justifyContent: "center",
                                    }}>
                                        <p key={order.pk}> Table Number : {order.table_number} ({order.reservation === null ? "Walk-In" : order.reservation_display_name}) ({new Date(order.date_time_of_order).toLocaleString("en-GB")})</p> 
                                        {role === "supervisor" && (
                                            <button onClick = {(event) => {navigate(`/order_delete/${order.pk}`)}}><strong>Delete</strong></button> 
                                        )}
                                        <button onClick={(event) => {navigate(`/order_info/${order.pk}`)}}>View</button>
                                    </div>
                                ))}
                            </div>
                        ))}
                        <div>
                            {role === "Supervisor" && (<button onClick={(event) => {navigate(`/order_add/${restaurant}`)}}>Start Order</button>)}
                        </div>
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