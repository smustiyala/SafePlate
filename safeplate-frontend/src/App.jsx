import { useEffect, useState } from "react";
import { api } from "./api";

function App() {
  const [restaurants, setRestaurants] = useState([]);

  useEffect(() => {
    api.get("/restaurants/")
      .then((response) => {
        setRestaurants(response.data);
      })
      .catch((error) => {
        console.error("Error fetching restaurants:", error);
      });
  }, []);

  return (
    <div>
      <h1>SafePlate</h1>
      <p>Dietary Compatibility Platform</p>

      <h2>Restaurants</h2>

      {restaurants.length === 0 ? (
        <p>No restaurants found.</p>
      ) : (
        <ul>
          {restaurants.map((restaurant) => (
            <li key={restaurant.id}>
              {restaurant.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;