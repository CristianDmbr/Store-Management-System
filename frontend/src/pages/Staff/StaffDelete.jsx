import {  useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"; 

function StaffDelete() {

    const navigate = useNavigate();

    return (
        <div>
            <h1>Delete Staff</h1>


            <div>
                <button onClick={() => navigate("/staff_list")}>No</button>
            </div>

        </div>
    )
}

export default StaffDelete;