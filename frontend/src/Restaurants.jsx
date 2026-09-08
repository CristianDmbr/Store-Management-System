import RestaurantList from "./RestaurantList";
import UserGreetings from "./Greetings";

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