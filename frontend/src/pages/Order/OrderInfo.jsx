import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

function OrderInfo(){

    const navigate = useNavigate();
    const [csrfToken, setCSRFToken] = useState("");
    const [role, setRole] = useState("");

    const {order_pk} = useParams();
    const [orderObject, setOrderObject] = useState(null);
    const [allOrderItems, setAllOrderItems] = useState([]);
    const [restaurant_pk, setRestaurantPk] = useState();

    useEffect(() => {
        fetch(`http://localhost:8000/api/detail_order/${order_pk}`,{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setOrderObject(data);
                setRestaurantPk(data.restaurant);
            })
        
        fetch(`http://localhost:8000/api/order_items_per_order/${order_pk}`,{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setAllOrderItems(data);
            })
        
        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setCSRFToken(data.csrfToken)
            })
        
            fetch("http://localhost:8000/api/user_name",{
                credentials : "include"
            })
                .then(request => request.json())
                .then(data => {
                    setRole(data.role)
                })

    },[order_pk]);

    const orderItemSortedByCategory = allOrderItems.reduce((groups,order_item) => {
        const order_category = order_item.menu_item_category_display

        if (!groups[order_category]){
            groups[order_category] = []
        };

        groups[order_category].push(order_item);

        return groups;

    },{});

    // < async > because we do not want to freeze the whole React app while we wait for the response from this function

    // There are two functions to handle errors
    // 1. Fetch the error, displays it and then interrupts the flow.
    // 2. Creates a new error object which gets passed to the catch and but also interrupts the flow
    async function handleDeleteOrderItem(order_item_pk) {
        // < try > is part of JavaScript's error handling mechanism. It allows to execute code that might produce an error and handle that error if it occurs. 
        // < catch(error) > is the handle function incase there is an error inside of the try.
        try {
            // < await > means wait for this request to finish before we continue with what's under this fetch request.
            // This does mean that other functions outside of the handleDeleteOrderItem can still run tho.
            const response = await fetch(
                `http://localhost:8000/api/order_menu_item_decrease/${order_item_pk}`,
                {
                    method: "DELETE",
                    credentials: "include",
                    headers: {
                        "X-CSRFToken": csrfToken
                    }
                }
            );
            
            // Incase the response is not okay get the error message from the response body
            // Retries the error message and display it.
            // return exits the function.
            if (!response.ok) {
                const errorData = await response.json();
                console.error("Failed to update order item:", errorData);
                return;
            }
    
            // Fetch the latest order items from Django once we done delete an order item.
            // We use await again to prevent running of outher code under the fetch.
            // Just means wait for the updated list of order items before running the code underneath
            const updatedResponse = await fetch(
                `http://localhost:8000/api/order_items_per_order/${order_pk}`,
                {
                    credentials: "include"
                }
            );
    
            if (!updatedResponse.ok) {
                // Throw generates an error and interupts the normal execution of the code
                // This error get's passed to the catch (error)
                throw new Error("Failed to refresh order items.");
            }
    
            const updatedItems = await updatedResponse.json();
    
            // Update React state with the latest database records
            setAllOrderItems(updatedItems);
    
        } catch (error) {
            console.error("Error deleting order item:", error);
        }
    };

    async function handleStatusUpdateToComplete(order_pk) {
        try {
            const response = await fetch(`http://localhost:8000/api/order_update_to_complete/${order_pk}`,{
                credentials : "include",
                method : "PATCH",
                headers : {
                    "X-CSRFToken" : csrfToken,
                    "Content-Type": "application/json",
                },
            });

            if (!response.ok){
                const errorData = await response.json();
                console.error("Error when updating the Order status to Complete ", errorData);
                return;
            }

            navigate("/order_list");

        } catch (error) {
            console.error("Error updating order status to Complete", error);
        }
    };

    async function handleStatusUpdateToWaiting(order_pk){
        try {
            const response = await fetch(`http://localhost:8000/api/order_update_to_waiting/${order_pk}`,{
                credentials : "include",
                method : "PATCH",
                headers : {
                    "X-CSRFToken" : csrfToken,
                    "Content-Type": "application/json",
                },
            });

            if (!response.ok){
                const errorMessage = await response.json();
                console.error("Error when updating the Order status to Waiting ", errorMessage);
                return;
            }

            navigate("/order_list");

        } catch (error) {
            console.error("Error updating order status to Waiting ")
        }
    }
    
    if (!orderObject){
        return(<div><h1>Loading</h1></div>)
    };
    
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

            <h2>Order List</h2>

            <div>
                {Object.entries(orderItemSortedByCategory)
                .sort((a,b) => {
                    const menuItemPriority = {
                        "Main" : 1,
                        "Starter" : 2,
                        "Snack" : 3,
                        "Desert" : 4,
                        "Drink" : 5
                    };

                    return menuItemPriority[a[0]] - menuItemPriority[b[0]];
                })
                .map(([category, orders]) => (
                    <div key={category}>
                        <h3>{category}</h3>
                        {orders.map((order_item) => 
                            Array.from({length : order_item.quantity}, (_, index) => (
                                <div key={`${order_item.pk} - ${index}`}>
                                    <p key={`${order_item.pk} - ${index}`}>
                                    {order_item.menu_item_name_display} - £{order_item.price_sold_at}
                                    </p>
                                    <button onClick={() => handleDeleteOrderItem(order_item.pk)}>Delete</button>
                                </div>
                            ))
                        )}
                    </div>
                ))}
            </div>

            <br />
            
            
            {( role === "Owner" || role === "Supervisor") && (
                <button onClick={(event) => {navigate(`/order_menu_item_add/${order_pk}/${restaurant_pk}`)}}> Add menu Item </button>
            )}

            {role === "Staff" && (
                <button onClick={(event) => {navigate(`/order_add_for_staff/${order_pk}`)}}>Add Menu Item</button>
            )}

            <br />
            
            <div>
                {(orderObject.status === "not_been_served") && (
                    <button onClick={() => {handleStatusUpdateToWaiting(order_pk)}}>Update Order Status to Waiting</button>
                )}
                {(orderObject.status === "waiting") && (
                    <button onClick={() => {handleStatusUpdateToComplete(order_pk)}}>Complete Order</button>
                )}
            </div>

            <br />

            <div>
                <button onClick={(event) => {navigate("/order_list")}}>Back</button>
            </div>
        </div>
    )
}

export default OrderInfo;