import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

function OrderItemAdd(){

    const navigate = useNavigate();
    const [csrfToken, setCSRFToken] = useState();
    const  { order_pk, restaurant_pk } = useParams();

    const [all_menu_items, setAllMenuItems] = useState([]);
    const [quantity, setQuantity] = useState(1);
    const [price_sold_at, setPriceSoldAt] = useState();
    const [menu_item, setMenuItem] = useState();

    useEffect(() => {
        fetch(`http://localhost:8000/api/menu_items_per_restaurants/${restaurant_pk}`,{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setAllMenuItems(data.all_menu_items);
            })
        
        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
        })    
            .then(request => request.json())
            .then(data => {
                setCSRFToken(data.csrfToken);
            })
    },[restaurant_pk]);

    function addOrderItem(event) {
        event.preventDefault();

        const body  = {
            "order" : order_pk,
            "menu_item" : menu_item,
            "quantity" : quantity,
        }

        fetch(`http://localhost:8000/api/order_item`,{
            credentials : "include",
            method : "post",
            headers : {
                "X-CSRFToken" : csrfToken,
                "Content-Type": "application/json",
            },
            body : JSON.stringify(body)
        })
        .then(async (response) => {

            const data = await response.json();
    
            console.log("Status:", response.status);
    
            console.log("Response from Django:", data);
    
            if (!response.ok) {
    
                throw new Error(JSON.stringify(data));
    
            }
    
            navigate(`/order_info/${order_pk}`);
    
        })
    
        .catch((error) => {
    
            console.error("Error adding order item:", error);
    
        });
    };

 
    return (
        <div>
            <h1>Add Order Item</h1>
            
            <form onSubmit={addOrderItem}>
                <div>
                    <label>Menu Item :</label>
                    <select value={menu_item} onChange = {(event) => {setMenuItem(event.target.value)}}>
                        <option key = {""} value="" disabled>Menu Item</option>
                        {all_menu_items.map((menu_item) => (
                            <option value = {menu_item.pk} key = {menu_item.pk}>{menu_item.name}</option>
                        ))}
                    </select>
                </div>
                <div>
                    <label htmlFor="quantity">Quantity: </label>
                    <input
                        id="quantity"
                        type="number"
                        min="1"
                        step="1"
                        value={quantity}
                        onChange={(event) => {
                            const value = event.target.value;
                            if (value === "" || /^\d+$/.test(value)) {
                                setQuantity(value);
                            }
                        }}
                        required
                    />
                    </div>


                <button type="submit">Add</button>
            </form>


            <div>
                <button onClick={(event) => {navigate(`/order_info/${order_pk}`)}}>Back</button>
            </div>
        </div>
    )
}

export default OrderItemAdd;