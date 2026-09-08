import { useState, useEffect } from "react";

function LoginPage() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [csrfToken, setCsrfToken] = useState("");

    useEffect(() => {
        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
        }).then(response => response.json())
          .then(data => {
            setCsrfToken(data.csrfToken)
          })
    }, [])

    function handleSubmit(event) {
        event.preventDefault();

        fetch("http://localhost:8000/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            credentials : "include",

            body: JSON.stringify({
                username: username,
                password: password,
    
            }),
        })
            .then(response => response.json())
            .then(data => {
                console.log(data)
            });
    }

    return (
        <div>
            <h1>Login</h1>

            <form onSubmit={handleSubmit}>
                
                <div>
                    <label>Username</label>
                    <input 
                        type = "text"
                        value = {username}
                        onChange = {(event) => setUsername(event.target.value)}/>
                </div>

                <div>
                    <label>Password</label>
                    <input
                        type = "text"
                        value = {password}
                        onChange = {(event) => setPassword(event.target.value)}
                    />
                </div>

                <button type="submit">
                    Login
                </button>

            </form>

        </div>
    );

}

export default LoginPage