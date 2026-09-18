import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

function MenuItemsPerRestaurant(){

    const navigate = useNavigate();
    const {restaurant_pk} = useParams();

    const [menu_items, setMenuItems] = useState([]);
    const [restaurant, setRestaurant] = useState();

    useEffect(() => {

        fetch(`http://localhost:8000/api/menu_items_per_restaurants/${restaurant_pk}`, {
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setMenuItems(data.all_menu_items)
                setRestaurant(data.restaurant)
                console.log(data.all_menu_items)
                console.log(data.restaurant)
            })

    }, [restaurant_pk])

    const groupedMenuItems = menu_items.reduce((groups, menu_item) =>{
        
        if ( !groups[menu_item.category]) {
            groups[menu_item.category] = [];
        }

        groups[menu_item.category].push(menu_item);
    
        return groups

    }, {});

    return (
        <div>
            <h1>Menu Items per Restaurant</h1>

            {Object.keys(groupedMenuItems).map(category => (

                <div key={category}>
                    <h2>{category}</h2>
                    {groupedMenuItems[category].map(menu_item => (
                        <p key={menu_item.pk}>
                            {menu_item.name}
                        </p>
                    ))}
                </div>

                ))}
            <div>
                <button onClick={(event) => navigate("/restaurant_list")}>Back</button>
            </div>

        </div>
    )
}

export default MenuItemsPerRestaurant;