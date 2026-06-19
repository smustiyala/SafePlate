import { useEffect, useState } from "react";
import { api } from "./api";
import "./App.css";

function App() {
  const [restaurants, setRestaurants] = useState([]);
  const [selectedRestaurant, setSelectedRestaurant] = useState("");
  const [userId, setUserId] = useState("");
  const [results, setResults] = useState(null);

  const [registerForm, setRegisterForm] = useState({
    username: "",
    email: "",
    password: "",
    preferences: [],
  });

  const [loginForm, setLoginForm] = useState({
    email: "",
    password: "",
  });

  const [message, setMessage] = useState("");

  const preferenceOptions = [
    { id: 1, name: "Vegan" },
    { id: 2, name: "Vegetarian" },
    { id: 3, name: "Dairy-Free" },
    { id: 4, name: "Egg-Free" },
    { id: 5, name: "Nut-Free" },
  ];

  useEffect(() => {
    api
      .get("/restaurants/")
      .then((response) => setRestaurants(response.data))
      .catch(() => setMessage("Could not load restaurants."));
  }, []);

  const togglePreference = (preferenceId) => {
    if (registerForm.preferences.includes(preferenceId)) {
      setRegisterForm({
        ...registerForm,
        preferences: registerForm.preferences.filter(
          (id) => id !== preferenceId
        ),
      });
    } else {
      setRegisterForm({
        ...registerForm,
        preferences: [...registerForm.preferences, preferenceId],
      });
    }
  };

  const handleRegister = async (event) => {
    event.preventDefault();

    try {
      const response = await api.post("/users/register", {
        username: registerForm.username,
        email: registerForm.email,
        password: registerForm.password,
      });

      const newUserId = response.data.id;
      setUserId(newUserId);

      for (const preferenceId of registerForm.preferences) {
        await api.post(
          `/dietary-preferences/users/${newUserId}/preferences/${preferenceId}`
        );
      }

      setMessage(
        `Registered as ${response.data.username}. Preferences saved. You are ready to check compatibility.`
      );

      setResults(null);
    } catch {
      setMessage("Registration failed. Try a different email or username.");
    }
  };

  const handleLogin = async (event) => {
    event.preventDefault();

    try {
      await api.post("/users/login", loginForm);

      const usersResponse = await api.get("/users/");
      const matchedUser = usersResponse.data.find(
        (user) => user.email === loginForm.email
      );

      if (matchedUser) {
        setUserId(matchedUser.id);
        setMessage("Login successful. You are ready to check compatibility.");
        setResults(null);
      } else {
        setMessage("Login successful, but user profile could not be loaded.");
      }
    } catch {
      setMessage("Login failed.");
    }
  };

  const checkCompatibility = async () => {
    if (!userId) {
      setMessage("Register or login before checking compatibility.");
      return;
    }

    if (!selectedRestaurant) {
      setMessage("Choose a restaurant first.");
      return;
    }

    try {
      const response = await api.get(
        `/compatibility/restaurants/${selectedRestaurant}/compatible-menu-items/${userId}`
      );
      setResults(response.data);
      setMessage("");
    } catch {
      setMessage("Could not load compatibility results.");
    }
  };

  return (
    <div className="page">
      <header className="hero">
        <h1>SafePlate</h1>
        <p>Find restaurant menu items that match your dietary needs.</p>
      </header>

      <section className="grid">
        <div className="card">
          <h2>Register</h2>
          <form onSubmit={handleRegister}>
            <input
              placeholder="Username"
              value={registerForm.username}
              onChange={(e) =>
                setRegisterForm({
                  ...registerForm,
                  username: e.target.value,
                })
              }
            />

            <input
              placeholder="Email"
              value={registerForm.email}
              onChange={(e) =>
                setRegisterForm({
                  ...registerForm,
                  email: e.target.value,
                })
              }
            />

            <input
              placeholder="Password"
              type="password"
              value={registerForm.password}
              onChange={(e) =>
                setRegisterForm({
                  ...registerForm,
                  password: e.target.value,
                })
              }
            />

            <div className="preferences">
              <p>Select Dietary Preferences:</p>

              {preferenceOptions.map((preference) => (
                <label key={preference.id} className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={registerForm.preferences.includes(preference.id)}
                    onChange={() => togglePreference(preference.id)}
                  />
                  {preference.name}
                </label>
              ))}
            </div>

            <button type="submit">Register</button>
          </form>
        </div>

        <div className="card">
          <h2>Login</h2>
          <form onSubmit={handleLogin}>
            <input
              placeholder="Email"
              value={loginForm.email}
              onChange={(e) =>
                setLoginForm({
                  ...loginForm,
                  email: e.target.value,
                })
              }
            />

            <input
              placeholder="Password"
              type="password"
              value={loginForm.password}
              onChange={(e) =>
                setLoginForm({
                  ...loginForm,
                  password: e.target.value,
                })
              }
            />

            <button type="submit">Login</button>
          </form>
        </div>
      </section>

      {message && <p className="message">{message}</p>}

      <section className="card">
        <h2>Check Restaurant Compatibility</h2>

        <p>
          Current User:{" "}
          <strong>{userId ? `User #${userId}` : "Register or login first"}</strong>
        </p>

        <select
          value={selectedRestaurant}
          onChange={(e) => setSelectedRestaurant(e.target.value)}
        >
          <option value="">Choose a restaurant</option>
          {restaurants.map((restaurant) => (
            <option key={restaurant.id} value={restaurant.id}>
              {restaurant.name}
            </option>
          ))}
        </select>

        <button onClick={checkCompatibility}>Check Compatibility</button>
      </section>

      {results && (
        <section className="card">
          <h2>{results.restaurant} Results</h2>

          {results.results.map((item, index) => (
            <div key={index} className={`result ${item.status}`}>
              <h3>{item.menu_item}</h3>
              <p>
                Status: <strong>{item.status}</strong>
              </p>

              {item.issues.length > 0 && (
                <>
                  <p>Issues:</p>
                  <ul>
                    {item.issues.map((issue, i) => (
                      <li key={i}>{issue}</li>
                    ))}
                  </ul>
                </>
              )}

              {item.recommendations.length > 0 && (
                <>
                  <p>Recommendations:</p>
                  <ul>
                    {item.recommendations.map((rec, i) => (
                      <li key={i}>{rec}</li>
                    ))}
                  </ul>
                </>
              )}
            </div>
          ))}
        </section>
      )}
    </div>
  );
}

export default App;