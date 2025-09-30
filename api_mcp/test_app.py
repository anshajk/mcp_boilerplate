import pytest
from app import app, customers_db, orders_db, products_db, shopping_carts
from fastapi.testclient import TestClient

# Create test client
client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_databases():
    """Reset all databases before each test"""
    # Reset products
    products_db.clear()
    products_db.update(
        {
            1: {
                "id": 1,
                "name": "Wireless Headphones",
                "description": "Premium noise-cancelling wireless headphones",
                "price": 299.99,
                "category": "electronics",
                "stock_quantity": 50,
                "image_url": "https://example.com/headphones.jpg",
                "discount_percentage": 10,
            },
            2: {
                "id": 2,
                "name": "Running Shoes",
                "description": "Lightweight running shoes for athletes",
                "price": 129.99,
                "category": "sports",
                "stock_quantity": 100,
                "image_url": "https://example.com/shoes.jpg",
                "discount_percentage": 15,
            },
            3: {
                "id": 3,
                "name": "Smart Watch",
                "description": "Fitness tracking smart watch with heart rate monitor",
                "price": 249.99,
                "category": "electronics",
                "stock_quantity": 30,
                "image_url": "https://example.com/watch.jpg",
                "discount_percentage": 0,
            },
        }
    )

    # Reset customers
    customers_db.clear()
    customers_db.update(
        {
            1: {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+1-555-0123",
                "address": "123 Main St, New York, NY 10001",
                "is_premium": True,
            },
            2: {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane@example.com",
                "phone": "+1-555-0456",
                "address": "456 Oak Ave, Los Angeles, CA 90001",
                "is_premium": False,
            },
        }
    )

    # Reset orders and carts
    orders_db.clear()
    shopping_carts.clear()

    yield


# ============ ROOT ENDPOINT TESTS ============


def test_root_endpoint():
    """Test the root endpoint returns welcome message"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "E-Commerce API" in data["message"]
    assert "endpoints" in data


# ============ PRODUCT ENDPOINT TESTS ============


def test_list_products():
    """Test listing all products"""
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "products" in data
    assert data["total"] == 3
    assert len(data["products"]) == 3


def test_list_products_with_category_filter():
    """Test filtering products by category"""
    response = client.get("/products/?category=electronics")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2  # Headphones and Smart Watch
    for product in data["products"]:
        assert product["category"] == "electronics"


def test_list_products_with_price_filter():
    """Test filtering products by price range"""
    response = client.get("/products/?min_price=200&max_price=300")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2  # Headphones and Smart Watch
    for product in data["products"]:
        assert 200 <= product["price"] <= 300


def test_list_products_in_stock_only():
    """Test filtering for in-stock products only"""
    # First, set one product out of stock
    products_db[1]["stock_quantity"] = 0

    response = client.get("/products/?in_stock_only=true")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    for product in data["products"]:
        assert product["stock_quantity"] > 0


def test_list_products_pagination():
    """Test product pagination"""
    response = client.get("/products/?skip=1&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["products"]) == 2


def test_get_product_by_id():
    """Test getting a specific product"""
    response = client.get("/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Wireless Headphones"
    assert "discounted_price" in data  # Has discount


def test_get_product_not_found():
    """Test getting a non-existent product"""
    response = client.get("/products/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_create_product():
    """Test creating a new product"""
    new_product = {
        "name": "Yoga Mat",
        "description": "Non-slip yoga mat",
        "price": 39.99,
        "category": "sports",
        "stock_quantity": 200,
        "image_url": "https://example.com/yoga-mat.jpg",
        "discount_percentage": 5,
    }

    response = client.post("/products/", json=new_product)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Product created successfully"
    assert data["product"]["name"] == "Yoga Mat"
    assert "id" in data["product"]


def test_create_product_invalid_data():
    """Test creating a product with invalid data"""
    invalid_product = {
        "name": "Test Product",
        "price": -10,  # Invalid: negative price
        "category": "electronics",
        "stock_quantity": 10,
    }

    response = client.post("/products/", json=invalid_product)
    assert response.status_code == 422  # Validation error


def test_update_product():
    """Test updating an existing product"""
    updated_product = {
        "name": "Updated Headphones",
        "description": "Updated description",
        "price": 349.99,
        "category": "electronics",
        "stock_quantity": 60,
        "discount_percentage": 15,
    }

    response = client.put("/products/1", json=updated_product)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Product updated successfully"
    assert data["product"]["name"] == "Updated Headphones"
    assert data["product"]["price"] == 349.99


def test_update_product_not_found():
    """Test updating a non-existent product"""
    product_data = {
        "name": "Test",
        "price": 100,
        "category": "electronics",
        "stock_quantity": 10,
    }

    response = client.put("/products/999", json=product_data)
    assert response.status_code == 404


def test_delete_product():
    """Test deleting a product"""
    response = client.delete("/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Product deleted successfully"

    # Verify product is deleted
    response = client.get("/products/1")
    assert response.status_code == 404


def test_delete_product_not_found():
    """Test deleting a non-existent product"""
    response = client.delete("/products/999")
    assert response.status_code == 404


def test_get_products_by_category():
    """Test getting products by category"""
    response = client.get("/products/category/electronics")
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "electronics"
    assert data["count"] == 2
    assert len(data["products"]) == 2


# ============ CUSTOMER ENDPOINT TESTS ============


def test_list_customers():
    """Test listing all customers"""
    response = client.get("/customers/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_list_premium_customers_only():
    """Test filtering for premium customers"""
    response = client.get("/customers/?premium_only=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["is_premium"] is True


def test_get_customer_by_id():
    """Test getting a specific customer"""
    response = client.get("/customers/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"


def test_get_customer_not_found():
    """Test getting a non-existent customer"""
    response = client.get("/customers/999")
    assert response.status_code == 404


def test_create_customer():
    """Test creating a new customer"""
    new_customer = {
        "id": 3,
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "phone": "+1-555-0789",
        "address": "789 Pine St, Chicago, IL 60601",
        "is_premium": False,
    }

    response = client.post("/customers/", json=new_customer)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Customer created successfully"
    assert data["customer"]["name"] == "Alice Johnson"


def test_create_customer_duplicate_id():
    """Test creating a customer with duplicate ID"""
    duplicate_customer = {
        "id": 1,  # Already exists
        "name": "Duplicate",
        "email": "duplicate@example.com",
    }

    response = client.post("/customers/", json=duplicate_customer)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()


def test_create_customer_invalid_email():
    """Test creating a customer with invalid email"""
    invalid_customer = {
        "id": 5,
        "name": "Test User",
        "email": "invalid-email",  # Invalid email format
    }

    response = client.post("/customers/", json=invalid_customer)
    assert response.status_code == 422  # Validation error


# ============ SHOPPING CART ENDPOINT TESTS ============


def test_get_empty_cart():
    """Test getting an empty cart"""
    response = client.get("/cart/1")
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == 1
    assert data["items"] == []
    assert data["total_items"] == 0
    assert data["total_amount"] == 0


def test_add_to_cart():
    """Test adding a product to cart"""
    cart_item = {"product_id": 1, "quantity": 2}

    response = client.post("/cart/1/add", json=cart_item)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Product added to cart"
    assert len(data["cart"]) == 1


def test_add_to_cart_multiple_items():
    """Test adding multiple different products to cart"""
    # Add first item
    client.post("/cart/1/add", json={"product_id": 1, "quantity": 2})
    # Add second item
    client.post("/cart/1/add", json={"product_id": 2, "quantity": 1})

    # Get cart
    response = client.get("/cart/1")
    assert response.status_code == 200
    data = response.json()
    assert data["total_items"] == 3  # 2 + 1
    assert len(data["items"]) == 2


def test_add_to_cart_same_product_twice():
    """Test adding the same product twice (should increment quantity)"""
    # Add item first time
    client.post("/cart/1/add", json={"product_id": 1, "quantity": 2})
    # Add same item again
    client.post("/cart/1/add", json={"product_id": 1, "quantity": 3})

    # Get cart
    response = client.get("/cart/1")
    data = response.json()
    assert len(data["items"]) == 1  # Still one item
    assert data["items"][0]["quantity"] == 5  # 2 + 3


def test_add_to_cart_insufficient_stock():
    """Test adding more items than available in stock"""
    cart_item = {"product_id": 1, "quantity": 1000}  # More than available (50)

    response = client.post("/cart/1/add", json=cart_item)
    assert response.status_code == 400
    assert "insufficient stock" in response.json()["detail"].lower()


def test_add_to_cart_invalid_customer():
    """Test adding to cart for non-existent customer"""
    cart_item = {"product_id": 1, "quantity": 1}

    response = client.post("/cart/999/add", json=cart_item)
    assert response.status_code == 404
    assert "customer not found" in response.json()["detail"].lower()


def test_add_to_cart_invalid_product():
    """Test adding non-existent product to cart"""
    cart_item = {"product_id": 999, "quantity": 1}

    response = client.post("/cart/1/add", json=cart_item)
    assert response.status_code == 404
    assert "product not found" in response.json()["detail"].lower()


def test_get_cart_with_items():
    """Test getting cart with items and verify calculations"""
    # Add items to cart
    client.post("/cart/1/add", json={"product_id": 1, "quantity": 2})

    response = client.get("/cart/1")
    assert response.status_code == 200
    data = response.json()

    assert data["customer_id"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["product_name"] == "Wireless Headphones"
    assert data["items"][0]["quantity"] == 2

    # Verify discount is applied (10% off 299.99)
    expected_price = 299.99 * 0.9  # 269.991
    assert abs(data["items"][0]["unit_price"] - expected_price) < 0.01


def test_remove_from_cart():
    """Test removing a product from cart"""
    # Add item first
    client.post("/cart/1/add", json={"product_id": 1, "quantity": 2})

    # Remove item
    response = client.delete("/cart/1/remove/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Product removed from cart"

    # Verify cart is empty
    cart_response = client.get("/cart/1")
    assert len(cart_response.json()["items"]) == 0


def test_remove_from_empty_cart():
    """Test removing from non-existent cart"""
    response = client.delete("/cart/999/remove/1")
    assert response.status_code == 404


def test_clear_cart():
    """Test clearing entire cart"""
    # Add multiple items
    client.post("/cart/1/add", json={"product_id": 1, "quantity": 2})
    client.post("/cart/1/add", json={"product_id": 2, "quantity": 1})

    # Clear cart
    response = client.delete("/cart/1/clear")
    assert response.status_code == 200
    assert response.json()["message"] == "Cart cleared"

    # Verify cart is empty
    cart_response = client.get("/cart/1")
    assert len(cart_response.json()["items"]) == 0


# ============ ORDER ENDPOINT TESTS ============


def test_create_order():
    """Test creating a new order"""
    order = {
        "customer_id": 1,
        "items": [
            {"product_id": 1, "quantity": 2, "price_at_purchase": 299.99},
            {"product_id": 2, "quantity": 1, "price_at_purchase": 129.99},
        ],
        "shipping_address": "123 Main St, New York, NY 10001",
        "payment_method": "credit_card",
        "status": "pending",
    }

    response = client.post("/orders/", json=order)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Order created successfully"
    assert "id" in data["order"]
    assert "total_amount" in data["order"]
    assert "created_at" in data["order"]


def test_create_order_updates_stock():
    """Test that creating an order reduces product stock"""
    initial_stock = products_db[1]["stock_quantity"]

    order = {
        "customer_id": 1,
        "items": [{"product_id": 1, "quantity": 5, "price_at_purchase": 299.99}],
        "shipping_address": "123 Main St",
        "payment_method": "credit_card",
    }

    response = client.post("/orders/", json=order)
    assert response.status_code == 201

    # Verify stock was reduced
    assert products_db[1]["stock_quantity"] == initial_stock - 5


def test_create_order_clears_cart():
    """Test that creating an order clears the customer's cart"""
    # Add items to cart
    client.post("/cart/1/add", json={"product_id": 1, "quantity": 2})

    # Create order
    order = {
        "customer_id": 1,
        "items": [{"product_id": 1, "quantity": 2, "price_at_purchase": 299.99}],
        "shipping_address": "123 Main St",
        "payment_method": "credit_card",
    }

    client.post("/orders/", json=order)

    # Verify cart is cleared
    cart_response = client.get("/cart/1")
    assert len(cart_response.json()["items"]) == 0


def test_create_order_invalid_customer():
    """Test creating order for non-existent customer"""
    order = {
        "customer_id": 999,
        "items": [{"product_id": 1, "quantity": 1, "price_at_purchase": 299.99}],
        "shipping_address": "123 Main St",
        "payment_method": "credit_card",
    }

    response = client.post("/orders/", json=order)
    assert response.status_code == 404


def test_create_order_invalid_product():
    """Test creating order with non-existent product"""
    order = {
        "customer_id": 1,
        "items": [{"product_id": 999, "quantity": 1, "price_at_purchase": 100}],
        "shipping_address": "123 Main St",
        "payment_method": "credit_card",
    }

    response = client.post("/orders/", json=order)
    assert response.status_code == 404


def test_create_order_insufficient_stock():
    """Test creating order with insufficient stock"""
    order = {
        "customer_id": 1,
        "items": [
            {
                "product_id": 1,
                "quantity": 1000,  # More than available
                "price_at_purchase": 299.99,
            }
        ],
        "shipping_address": "123 Main St",
        "payment_method": "credit_card",
    }

    response = client.post("/orders/", json=order)
    assert response.status_code == 400
    assert "insufficient stock" in response.json()["detail"].lower()


def test_get_order():
    """Test getting order details"""
    # Create an order first
    order = {
        "customer_id": 1,
        "items": [{"product_id": 1, "quantity": 1, "price_at_purchase": 299.99}],
        "shipping_address": "123 Main St",
        "payment_method": "credit_card",
    }

    create_response = client.post("/orders/", json=order)
    order_id = create_response.json()["order"]["id"]

    # Get the order
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["customer_id"] == 1


def test_get_order_not_found():
    """Test getting non-existent order"""
    response = client.get("/orders/999")
    assert response.status_code == 404


def test_get_customer_orders():
    """Test getting all orders for a customer"""
    # Create multiple orders
    order = {
        "customer_id": 1,
        "items": [{"product_id": 1, "quantity": 1, "price_at_purchase": 299.99}],
        "shipping_address": "123 Main St",
        "payment_method": "credit_card",
    }

    client.post("/orders/", json=order)
    client.post("/orders/", json=order)

    # Get customer orders
    response = client.get("/orders/customer/1")
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == 1
    assert len(data["orders"]) == 2


def test_update_order_status():
    """Test updating order status"""
    # Create an order first
    order = {
        "customer_id": 1,
        "items": [{"product_id": 1, "quantity": 1, "price_at_purchase": 299.99}],
        "shipping_address": "123 Main St",
        "payment_method": "credit_card",
    }

    create_response = client.post("/orders/", json=order)
    order_id = create_response.json()["order"]["id"]

    # Update status
    response = client.patch(f"/orders/{order_id}/status?status=shipped")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Order status updated"
    assert data["order"]["status"] == "shipped"
    assert "updated_at" in data["order"]


def test_update_order_status_not_found():
    """Test updating status of non-existent order"""
    response = client.patch("/orders/999/status?status=shipped")
    assert response.status_code == 404


# ============ ANALYTICS ENDPOINT TESTS ============


def test_analytics_dashboard():
    """Test analytics dashboard endpoint"""
    response = client.get("/analytics/dashboard")
    assert response.status_code == 200
    data = response.json()

    assert "total_products" in data
    assert "total_customers" in data
    assert "total_orders" in data
    assert "total_revenue" in data
    assert "average_order_value" in data
    assert "order_status_breakdown" in data
    assert "low_stock_alert" in data
    assert "low_stock_products" in data


def test_analytics_with_orders():
    """Test analytics with actual order data"""
    # Create an order
    order = {
        "customer_id": 1,
        "items": [{"product_id": 1, "quantity": 1, "price_at_purchase": 299.99}],
        "shipping_address": "123 Main St",
        "payment_method": "credit_card",
    }

    client.post("/orders/", json=order)

    # Get analytics
    response = client.get("/analytics/dashboard")
    data = response.json()

    assert data["total_orders"] == 1
    assert data["total_revenue"] > 0
    assert data["average_order_value"] > 0


def test_analytics_low_stock_products():
    """Test low stock alerts in analytics"""
    # Set a product to low stock
    products_db[1]["stock_quantity"] = 5

    response = client.get("/analytics/dashboard")
    data = response.json()

    assert data["low_stock_alert"] >= 1
    assert len(data["low_stock_products"]) >= 1


# ============ HEALTH CHECK TESTS ============


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "database" in data
    assert data["database"]["products"] == 3
    assert data["database"]["customers"] == 2


# ============ INTEGRATION TESTS ============


def test_complete_shopping_flow():
    """Test complete e-commerce flow from browsing to order"""
    # 1. Browse products
    products_response = client.get("/products/")
    assert products_response.status_code == 200

    # 2. Add items to cart
    client.post("/cart/1/add", json={"product_id": 1, "quantity": 2})
    client.post("/cart/1/add", json={"product_id": 2, "quantity": 1})

    # 3. View cart
    cart_response = client.get("/cart/1")
    assert cart_response.status_code == 200
    assert cart_response.json()["total_items"] == 3

    # 4. Create order
    order = {
        "customer_id": 1,
        "items": [
            {"product_id": 1, "quantity": 2, "price_at_purchase": 299.99},
            {"product_id": 2, "quantity": 1, "price_at_purchase": 129.99},
        ],
        "shipping_address": "123 Main St, New York, NY 10001",
        "payment_method": "credit_card",
    }

    order_response = client.post("/orders/", json=order)
    assert order_response.status_code == 201
    order_id = order_response.json()["order"]["id"]

    # 5. Verify cart is cleared
    cart_after = client.get("/cart/1")
    assert len(cart_after.json()["items"]) == 0

    # 6. Check order status
    order_detail = client.get(f"/orders/{order_id}")
    assert order_detail.json()["status"] == "pending"

    # 7. Update order status
    status_update = client.patch(f"/orders/{order_id}/status?status=shipped")
    assert status_update.json()["order"]["status"] == "shipped"


def test_discount_calculation_in_cart():
    """Test that discounts are correctly applied in cart"""
    # Product 1 has 10% discount
    client.post("/cart/1/add", json={"product_id": 1, "quantity": 1})

    cart_response = client.get("/cart/1")
    cart_data = cart_response.json()

    # Original price: 299.99, with 10% discount = 269.991
    expected_price = 299.99 * 0.9
    assert abs(cart_data["items"][0]["unit_price"] - expected_price) < 0.01


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
