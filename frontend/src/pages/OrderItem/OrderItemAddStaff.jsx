import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

function OrderAddItemForStaff(){

    const navigate = useNavigate();
    const [csrfToken, setCSRFToken] = useState();
    const { order_pk, restaurant_pk } = useParams();

    const [all_menu_items, setAllMenuItems] = useState([]);
    const [menu_item_pk, setMenuItemPK] = useState("");
    const [quantity, setQuantity] = useState("");
    
    useEffect(() => {
        fetch(`http://localhost:8000/api/menu_items_per_restaurants/${restaurant_pk}`,{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setAllMenuItems(data.all_menu_items)
            })
        
        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setCSRFToken(data.csrfToken)
            })
    },[restaurant_pk]);

    function handleOrderItemAddStaff(){
        event.preventDefault();

        const body = {
            "order" : order_pk,
            "menu_item" : menu_item_pk,
            "quantity" : quantity,
        }

        fetch("http://localhost:8000/api/order_item",{
            credentials : "include",
            method : "POST",
            headers : {
                "X-CSRFToken" : csrfToken,
                "Content-Type": "application/json",
            },
            body : JSON.stringify(body)
        })
            .then(() => {navigate(`/order_info/${order_pk}`)})
    };
    
    return (
        <div>
            <h1>Add Menu Item as Staff</h1>

            <div>
                <form onSubmit={handleOrderItemAddStaff}>

                    <div>
                        <label>Menu Item :</label>
                        <select value={menu_item_pk} onChange = {(event) => {setMenuItemPK(event.target.value)}}>
                            <option key = "" value="" disabled>Select an item</option>
                            {all_menu_items.map((menu_item) => (
                                <option key = {menu_item.pk} value= {menu_item.pk}>{menu_item.name}</option>
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
            </div>

            <div>
                <button onClick={(event) => {navigate(`/order_info/${order_pk}`)}}>Back</button>
            </div>

        </div>
    )
}

export default OrderAddItemForStaff;