import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

function OrderInfo(){

    const navigate = useNavigate();
    const {order_pk} = useParams();
    const [orderObject, setOrderObject] = useState(null);
    const [allOrderItems, setAllOrderItems] = useState([]);

    useEffect(() => {
        fetch(`http://localhost:8000/api/detail_order/${order_pk}`,{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setOrderObject(data)
            })
        
        fetch(`http://localhost:8000/api/order_items_per_order/${order_pk}`,{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setAllOrderItems(data)
                console.log(allOrderItems)
            })
    },[order_pk]);

    if (!orderObject){
        return(<div><h1>Loading</h1></div>)
    }
    
    return (
        <div>
            {(!orderObject.reservation) && (
                <div><h1>Order Info</h1></div>
            )}
            {(orderObject.reservation) && (
                <div><h1>{orderObject.reservation_display_name}'s order info : </h1></div>
            )}

            <hr/>

            <div style={{
                display : "flex",
                alignItems : "center",
                gap : "5px"
            }}>
                <label>Restaurant</label>
                <h3>{orderObject.restaurant_name}</h3>
                <h3>|</h3>
                <label>Served by : </label>
                <h3>{orderObject.staff_display_name}</h3>
                <h3>|</h3>
                <label>Date time of order :</label>
                <h3>
                    {new Date(orderObject.date_time_of_order).toLocaleString("en-GB")}
                </h3>
                <label>Status : </label>
                <h3>{orderObject.order_status_display}</h3>
                <label>Table Number :</label>
                <h3>{orderObject.table_number}</h3>
            </div>

            {(orderObject.note) && (
                <div>
                    <h2><strong>Note :</strong></h2>
                    <h3>{orderObject.note}</h3>
                </div>
            )}

            <hr/>
                

            <div>
                <button onClick={(event) => {navigate("/order_list")}}>Back</button>
            </div>
        </div>
    )
}

export default OrderInfo;