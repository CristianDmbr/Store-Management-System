import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";

function MenuItemsPerRestaurant(){

    const navigate = useNavigate();
    const { restaurant_pk } = useParams();

    const [all_menu_items, setAllMenuItems] = useState([]);
    const [restaurant, setRestaurant] = useState();

    useEffect(() => {
        fetch(`http://localhost:8000/api/menu_items_per_restaurants/${restaurant_pk}`,{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setAllMenuItems(data.all_menu_items);
                setRestaurant(data.restaurant);
            })

    },[restaurant_pk])

    const groupedMenuItems = all_menu_items.reduce((groups, menu_item) => {
        if (!groups[menu_item.category]){
            groups[menu_item.category] = []
        };

        groups[menu_item.category].push(menu_item);

        return groups;
    },{})

    if (!restaurant){
        return(
            <h1>Loading</h1>
        )
    }

    return (
        <div>

            <h1>{restaurant.restaurant_name}'s Menu</h1>

            {Object.keys(groupedMenuItems).map(category => (
                <div key = {category}>
                    <h2>{category.toUpperCase()}</h2>
                    {groupedMenuItems[category]
                        .sort((menuItem1,menuItem2) => menuItem1.price - menuItem2.price)
                        .map(menu_item => (
                        <p key={menu_item.pk}>{menu_item.name} : {menu_item.price}</p>
                    ))}
                </div>
            ))}
        
            <div>
                <button onClick={(event) => {navigate("/restaurant_list")}}>Back</button>
            </div>
        </div>
    )

}
export default MenuItemsPerRestaurant;