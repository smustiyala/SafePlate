from app.database import Base, engine, SessionLocal
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.menu_item import MenuItem
from app.models.ingredient import Ingredient
from app.models.dietary_preference import DietaryPreference

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

preferences = [
    "Vegan",
    "Vegetarian",
    "Dairy-Free",
    "Egg-Free",
    "Nut-Free",
]

for name in preferences:
    db.add(DietaryPreference(name=name))

ingredients = {
    "Black Beans": Ingredient(name="Black Beans"),
    "Rice": Ingredient(name="Rice"),
    "Potatoes": Ingredient(name="Potatoes"),
    "Lettuce": Ingredient(name="Lettuce"),
    "Tomato": Ingredient(name="Tomato"),
    "Marinara Sauce": Ingredient(name="Marinara Sauce"),
    "Pasta": Ingredient(name="Pasta"),
    "Bread": Ingredient(name="Bread"),
    "Cheese": Ingredient(
        name="Cheese",
        is_vegan=False,
        is_vegetarian=True,
        contains_dairy=True,
    ),
    "Mozzarella": Ingredient(
        name="Mozzarella",
        is_vegan=False,
        is_vegetarian=True,
        contains_dairy=True,
    ),
    "Parmesan": Ingredient(
        name="Parmesan",
        is_vegan=False,
        is_vegetarian=True,
        contains_dairy=True,
    ),
    "Alfredo Sauce": Ingredient(
        name="Alfredo Sauce",
        is_vegan=False,
        is_vegetarian=True,
        contains_dairy=True,
        contains_egg=True,
    ),
    "Beef": Ingredient(
        name="Beef",
        is_vegan=False,
        is_vegetarian=False,
    ),
    "Chicken": Ingredient(
        name="Chicken",
        is_vegan=False,
        is_vegetarian=False,
    ),
    "Pepperoni": Ingredient(
        name="Pepperoni",
        is_vegan=False,
        is_vegetarian=False,
    ),
    "Sour Cream": Ingredient(
    name="Sour Cream",
    is_vegan=False,
    is_vegetarian=True,
    contains_dairy=True,
),
}

for ingredient in ingredients.values():
    db.add(ingredient)

restaurants = {
    "Taco Bell": Restaurant(name="Taco Bell", website="https://www.tacobell.com"),
    "Papa Johns": Restaurant(name="Papa Johns", website="https://www.papajohns.com"),
    "Olive Garden": Restaurant(name="Olive Garden", website="https://www.olivegarden.com"),
}

for restaurant in restaurants.values():
    db.add(restaurant)

db.commit()

menu_data = {
    "Taco Bell": {
        "Bean Burrito": ["Black Beans", "Rice", "Cheese"],
        "Black Bean Crunchwrap Supreme": ["Black Beans", "Lettuce", "Tomato", "Cheese", "Sour Cream"] if "Sour Cream" in ingredients else ["Black Beans", "Lettuce", "Tomato", "Cheese"],
        "Cheese Quesadilla": ["Cheese"],
        "Spicy Potato Soft Taco": ["Potatoes", "Lettuce", "Cheese"],
        "Nacho Fries": ["Potatoes", "Cheese"],
    },
    "Papa Johns": {
        "Cheese Pizza": ["Bread", "Mozzarella"],
        "Garden Fresh Pizza": ["Bread", "Tomato", "Mozzarella"],
        "Breadsticks": ["Bread"],
        "Veggie Papa Bowl": ["Tomato", "Cheese"],
        "Cheesesticks": ["Bread", "Cheese"],
    },
    "Olive Garden": {
        "Spaghetti with Marinara": ["Pasta", "Marinara Sauce"],
        "Fettuccine Alfredo": ["Pasta", "Alfredo Sauce", "Parmesan"],
        "Five Cheese Ziti al Forno": ["Pasta", "Cheese", "Mozzarella", "Parmesan"],
        "Minestrone Soup": ["Tomato", "Pasta"],
        "House Salad": ["Lettuce", "Tomato", "Parmesan"],
    },
}

for restaurant_name, items in menu_data.items():
    restaurant = db.query(Restaurant).filter(Restaurant.name == restaurant_name).first()

    for item_name, ingredient_names in items.items():
        menu_item = MenuItem(
            name=item_name,
            restaurant_id=restaurant.id,
        )

        for ingredient_name in ingredient_names:
            menu_item.ingredients.append(ingredients[ingredient_name])

        db.add(menu_item)

db.commit()
db.close()

print("SafePlate database seeded successfully.")