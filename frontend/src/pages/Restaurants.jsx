import RestaurantList from "../components/RestaurantList";
import UserGreetings from "../components/Greetings";

function Restaurants(){
    return (
        <div>
            <UserGreetings />
            <h2>Restaurant Page</h2>
            <RestaurantList />
        </div>
    )
}

export default Restaurants