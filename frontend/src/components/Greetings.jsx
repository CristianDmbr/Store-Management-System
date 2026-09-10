import { useState, useEffect } from "react";

function UserGreetings() {
    const [name, setName] = useState("")
    const [greeting, setGreeting] = useState("")

    useEffect(() => {
        fetch("http://localhost:8000/api/user_name",{
            credentials : "include"
        })
            .then(response => response.json())
            .then(data => {
                setName(data.username)
            })

        fetch("http://localhost:8000/api/time_greetings",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setGreeting(data.greeting)})
            },[]);
        
        
    return (
        <div>
            <h1> {greeting} {name} !</h1>
        </div>
    ); 
}

export default UserGreetings;