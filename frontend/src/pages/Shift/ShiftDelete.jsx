import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect } from "react";

function DeleteShift() {

    const navigate = useNavigate();
    const { shift_pk } = useParams();
    
    const [csrfToken, setCSRFToken] = useState("");

    useEffect((event) => {
        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
        })
            .then(request => request.json())
            .then( data => {
                setCSRFToken(data.csrfToken)
            })
    },[])


    function HandleSubmit(event){
        fetch(`http://localhost:8000/api/shift_detail/${shift_pk}`,{
            method : "DELETE",
            credentials : "include",
            headers : {
                "X-CSRFToken" : csrfToken
            }
        })
            .then(navigate("/shifts_list"))

    }


    return(
        <div>
            <h1>Remove Shift</h1>

            <form onSubmit={HandleSubmit}>
                <button type="submit"><strong>Yes</strong></button>
            </form>

            <div>
                <button onClick={(event) => {navigate("/shifts_list")}}>No</button>
            </div>
            
        </div>
    )
}

export default DeleteShift;