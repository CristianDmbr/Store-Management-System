import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react"; 

function RegisterPage() {

    const navigate = useNavigate()

    const [csrfToken, setCsrfToken] = useState("")
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")

    useEffect(() => {
        fetch("http://localhost:8000/api/csrf", {
            credentials : "include"
        }).then(request => request.json())
          .then(data => 
            setCsrfToken(data.csrfToken));
    },[]);

    function handleSumision(event){
            fetch("http://localhost:8000/api/create_user",
            {
                credentials : "include",
                method : "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body : JSON.stringify({
                    "username" : username,
                    "password" : password
                })
            }).then(request => request.json())
              .then(data => {
                console.log(data.username)
              })
    }

    return (
        <div>
            <h1>Register Page</h1>

                <div>
                    <form onSubmit={handleSumision}>

                        <div>
                            <label> Unsername </label>
                                <input 
                                    type="text"
                                    data = {username}
                                    onChange = {(event) => setUsername(data.target.value)}
                                    />
                        </div>
                            
                        <div>
                            <label> Password </label>
                                <input
                                    type="password"
                                    data = {password}
                                    onChange = {(event) => setPassword(data.target.value)}  />
                        </div>
                    </form>
                </div>

            <div>
                <button type="submit" onClick={() => navigate("/login")}>
                    Login
                </button>
            </div>

        </div>

    )
}

export default RegisterPage