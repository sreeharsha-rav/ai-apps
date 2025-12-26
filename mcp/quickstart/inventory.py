from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Inventory Management")

food_items = {
    "F001": {"name": "Apple", "quantity": 100, "price": 0.99},
    "F002": {"name": "Banana", "quantity": 150, "price": 0.59},
    "F003": {"name": "Orange", "quantity": 80, "price": 1.29},
    "F004": {"name": "Bread", "quantity": 45, "price": 2.99},
    "F005": {"name": "Milk", "quantity": 60, "price": 3.49},
    "F006": {"name": "Eggs (dozen)", "quantity": 35, "price": 4.99},
    "F007": {"name": "Cheese", "quantity": 25, "price": 5.99},
    "F008": {"name": "Chicken Breast", "quantity": 40, "price": 8.99},
}

@mcp.resource("food://items")
def get_food_items() -> list[dict]:
    """
    Returns the list of food items in the inventory.
    
    Returns:
        list[dict]: A list of dictionaries representing food items.
    """
    return food_items

@mcp.resource("food://item/{item_id}")
def get_food_item(item_id: str) -> dict | None:
    """
    Returns a specific food item by its ID.
    
    Args:
        item_id (str): The ID of the food item.
        
    Returns:
        dict | None: A dictionary representing the food item, or None if not found.
    """
    if item_id in food_items:
        return food_items[item_id]
    return None

@mcp.resource("food://item/{item_id}/price")
def get_food_item_price(item_id: str) -> float | None:
    """
    Returns the price of a specific food item by its ID.
    
    Args:
        item_id (str): The ID of the food item.
        
    Returns:
        float | None: The price of the food item, or None if not found.
    """
    if item_id in food_items:
        return food_items[item_id]["price"]
    return None

@mcp.resource(
    uri="food://item/{item_id}/quantity",
    name="Get Food Item Quantity",
    title="Get Food Item Quantity Resource",
    description="Returns the quantity of a specific food item by its ID.",
    mime_type="application/json",
)
def get_food_item_quantity(item_id: str) -> int | None:
    """
    Returns the quantity of a specific food item by its ID.
    
    Args:
        item_id (str): The ID of the food item.
        
    Returns:
        int | None: The quantity of the food item, or None if not found.
    """
    if item_id in food_items:
        return food_items[item_id]["quantity"]
    return None

if __name__ == "__main__":
    mcp.run()
