import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

function OrderItemAdd(){

    const navigate = useNavigate();
    const  { order_pk, restaurant_pk } = useParams();
 
    return (
        <div>
            <h1>Add Order Item</h1>
        </div>
    )
}

export default OrderItemAdd;