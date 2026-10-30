import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

function MenuItemListForStaff(){

    const navigate = useNavigate();

    const [all_menu_items, setAllMenuItems] = useState([]);
    const [restaurant_pk, setRestaurantPk] = useState();

    useEffect(() => {
        fetch("http://localhost:8000/api/menu_items_list",{
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setAllMenuItems(data);
            })

        fetch("http://localhost:8000/api/get_staff_restaurant", {
            credentials : "include"
        })
            .then(request => request.json())
            .then(data => {
                setRestaurantPk(data.restaurant_pk);
            })
    },[]);

    const menuItemByCategory = all_menu_items.reduce((groups,menu_item)=>{
        const category_display = menu_item.display_category;

        if (!groups[category_display]){
            groups[category_display] = []
        };

        groups[category_display].push(menu_item);

        return groups;

    },{});

    return (
        <div>
            <h1>Menu List</h1>

            <div>
                {Object.entries(menuItemByCategory).sort(
                    (a,b) => {
                        const menuItemPriority = {
                            "Main" : 1,
                            "Starter" : 2,
                            "Snack" : 3,
                            "Desert" : 4,
                            "Drink" : 5
                        };
                    return menuItemPriority[a[0]] - menuItemPriority[b[0]];
                    }
                ).map(([category, menu_items]) => (
                    <div key={category}>
                        <h2>{category}</h2>
                        {menu_items.map((menu_item) => (
                            <div key={menu_item.pk} style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "10px" }}>
                                <p key={menu_item.pk}>{menu_item.name} £{menu_item.price} <small>({menu_item.calories}kcal)</small></p>
                                <button onClick={(event) => {navigate(`/menu_item_info/${menu_item.pk}/${restaurant_pk}`)}}><small>info</small></button>
                            </div>
                        ))}
                    </div>
                ))}
            </div>

            <div>
                <button onClick={(event) => {navigate("/staff_dashboard")}}>Dashboard</button>
            </div>

        </div>
    )
}

export default MenuItemListForStaff;