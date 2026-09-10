import { useEffect } from 'react';
import { useState } from 'react';
import { useNavigate, useParams } from "react-router-dom";

function DeleteRestaurant(){

    const { restaurant_pk } = useParams();

    const navigate = useNavigate();
    const [csrfToken, setCSRFToken] = useState();

    function handleSubmit(event) {
        event.preventDefault()

        fetch(`http://localhost:8000/api/detail_restaurant/${restaurant_pk}`,{
            method : "DELETE",
            credentials : "include",
            headers : {
                "X-CSRFToken" : csrfToken
            }
        }).then(() => console.log("Deleted"))
          .then(() => navigate("/restaurant_list"))
    }

    useEffect(() => {
        fetch("http://localhost:8000/api/csrf", {
            credentials : "include"
        }).then(request => request.json())
          .then(data => {
            setCSRFToken(data.csrfToken)
          })
    },[restaurant_pk]);

    return (
        <div>
            <h1>Delete Restaurant ?</h1>

                <div>
                    <form onSubmit={handleSubmit}>
                        <button type='submit'>Delete</button>
                    </form>
                </div>
                <div>
                    <button onClick={(event) => navigate('/restaurant_list')}>No</button>
                </div>
        </div>
    )
}

export default DeleteRestaurant;