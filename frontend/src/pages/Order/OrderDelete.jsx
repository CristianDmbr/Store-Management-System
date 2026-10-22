import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect } from "react";

function OrderDelete(){

    const navigate = useNavigate();
    const {order_pk} = useParams();

    const [csft_token, setCSRFToken] = useState();
    const [orderObject, setOrderObject] = useState(null);

    useEffect(()=>{

        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setCSRFToken(data.csrfToken)
            })
        
        fetch(`http://localhost:8000/api/detail_order/${order_pk}`,{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setOrderObject(data)
            })

    },[order_pk]);

    function handleDelete(event){
        event.preventDefault();

        fetch(`http://localhost:8000/api/detail_order/${order_pk}`,{
            credentials : "include",
            method : "delete",
            headers : {
                "X-CSRFToken" : csft_token
            }
        })
            .then(() => navigate("/order_list"))
    };

    if (!orderObject) {
        return (
            <div><h1>Loading</h1></div>
        )
    }

    return (
        <div>
            <h1>Delete Reservation ? </h1>

            <form onSubmit={handleDelete}>
                <button type="submit"><strong>DELETE</strong></button>
            </form>

            <div>
                <button onClick={(event) => {navigate("/order_list")}}>No</button>
            </div>

        </div>
    )
}

export default OrderDelete;