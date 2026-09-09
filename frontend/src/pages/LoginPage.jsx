import { useState, useEffect } from "react";

function LoginPage() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    // It will be used to pass the token security requests.
    const [csrfToken, setCsrfToken] = useState("");

    // Extract the token of the current session.
    useEffect(() => {
        fetch("http://localhost:8000/api/csrf",{
            credentials : "include"
        }).then(response => response.json())
          .then(data => {
            // Update the useCase of the token
            setCsrfToken(data.csrfToken)
          })
    }, [])

    // event is information about what happened.
    function handleSubmit(event) {
        // Normally once submitted, the Browser reloads/submits by itself, but we want React to have control.
        // We want React -> Handle the Submission -> send fetch() -> wait for Django -> decide what to do
        // Just tells the browser to not perform the form's default submission, "JavaScript will handle it."
        event.preventDefault();

        fetch("http://localhost:8000/api/login", 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            credentials : "include",

            // States what gets sent to Django.
            // .stringify converts the sent data into JSON so the API view can use it with <request.data> and we can do
            // username = request.data.get("username")
            body: JSON.stringify({
                username: username,
                password: password,
    
            }),
        })
            // 
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
                        value = {username} // The Use case variable created earlier
                        // Means every time there is a change to this input box, run this code and the value is from event.target.value
                        onChange = {(event) => setUsername(event.target.value) }/> //  

                </div>

                <div>
                    <label>Password</label>
                    <input
                        type = "password"
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