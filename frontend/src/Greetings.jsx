import { useState, useEffect } from "react";

function UserGreetings() {
    const [name, setName] = useState("")

    useEffect(() => {
        fetch("http://localhost:8000/api/user_name",{
            credentials : "include"
        })
            .then(response => response.json())
            .then(data => {
                setName(data.username)
            })})
        console.log(name)
    return (
        <div>
            <h1>Greetings {name} !</h1>
        </div>
    ) 
}

export default UserGreetings