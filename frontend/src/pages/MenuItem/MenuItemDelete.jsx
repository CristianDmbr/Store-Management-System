import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect } from "react";

function DeleteMenuItem(){

    const navigate = useNavigate();
    const [csrfToken, setCSRFToken] = useState();
    const { menu_item_pk, restaurant_pk } = useParams();

    const [menuItem, setMenuItem] = useState();

    useEffect(() => {
        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setCSRFToken(data.csrfToken)
            })
        
        fetch(`http://localhost:8000/api/menu_item_detail/${menu_item_pk}`,{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setMenuItem(data)
            })
        
    }, [menu_item_pk]);

    if (!menuItem) {
        return (
            <div>
                <h1>Loading</h1>
                <div>
                    <button onClick={(event) => navigate(`/menu_items_per_restaurant/${restaurant_pk}`)}>Back</button>
                </div>
            </div>
        )
    }

    function handleSubmit(event) {
        event.preventDefault();
        
        fetch(`http://localhost:8000/api/menu_item_detail/${menu_item_pk}`,{
            method : "DELETE",
            credentials : "include",
            headers : {
                "X-CSRFToken" : csrfToken
            }
        })
            .then(response => {
                if (response.ok) {
                    navigate(`/menu_items_per_restaurant/${restaurant_pk}`);
                } else {
                    response.json().then(data => {
                        console.log("Detail Failed", data.status);
                        console.log("Error" , data)
                    });
                }
            })
            .catch(error => {
                console.log("Request failed", error)
            })
    }

    return(
        <div>
            <h1>Delete {menuItem.name} ?</h1>

            <form onSubmit = {handleSubmit}>
                <button type="submit">Yes</button>
            </form>

            <div>
                <button onClick={(event) => navigate(`/menu_items_per_restaurant/${restaurant_pk}`)}>Back</button>
            </div>

        </div>
    )
}

export default DeleteMenuItem;