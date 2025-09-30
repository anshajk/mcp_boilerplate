from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(
    title="E-Commerce API",
    description="A RESTful API for an e-commerce platform",
    version="1.0.0",
)


# Enums
class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    BOOKS = "books"
    HOME = "home"
    SPORTS = "sports"
    BEAUTY = "beauty"


# Pydantic models for request/response
class Product(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category: ProductCategory
    stock_quantity: int = Field(..., ge=0)
    image_url: Optional[str] = None
    discount_percentage: Optional[float] = Field(default=0, ge=0, le=100)


class Customer(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    is_premium: bool = False


class OrderItem(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    price_at_purchase: float


class Order(BaseModel):
    customer_id: int
    items: List[OrderItem]
    total_amount: Optional[float] = None
    status: OrderStatus = OrderStatus.PENDING
    shipping_address: str
    payment_method: str


class CartItem(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


# In-memory storage for demo
products_db = {
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

customers_db = {
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

orders_db = {}
shopping_carts = {}  # customer_id -> list of cart items


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to the E-Commerce API",
        "version": "1.0.0",
        "endpoints": {
            "products": "/products - Browse and manage products",
            "customers": "/customers - Customer management",
            "orders": "/orders - Order management",
            "cart": "/cart - Shopping cart operations",
            "docs": "/docs - Interactive API documentation",
        },
    }


# ============ PRODUCT ENDPOINTS ============


@app.get("/products/")
async def list_products(
    category: Optional[ProductCategory] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock_only: bool = False,
    skip: int = 0,
    limit: int = Query(default=20, le=100),
):
    """List all products with optional filters"""
    products = list(products_db.values())

    # Apply filters
    if category:
        products = [p for p in products if p["category"] == category]
    if min_price is not None:
        products = [p for p in products if p["price"] >= min_price]
    if max_price is not None:
        products = [p for p in products if p["price"] <= max_price]
    if in_stock_only:
        products = [p for p in products if p["stock_quantity"] > 0]

    # Calculate discounted prices
    for product in products:
        if product["discount_percentage"] > 0:
            product["discounted_price"] = round(
                product["price"] * (1 - product["discount_percentage"] / 100), 2
            )

    return {"total": len(products), "products": products[skip : skip + limit]}


@app.get("/products/{product_id}")
async def get_product(product_id: int):
    """Get a specific product by ID"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")

    product = products_db[product_id].copy()
    if product["discount_percentage"] > 0:
        product["discounted_price"] = round(
            product["price"] * (1 - product["discount_percentage"] / 100), 2
        )

    return product


@app.post("/products/", status_code=status.HTTP_201_CREATED)
async def create_product(product: Product):
    """Create a new product (Admin only)"""
    product_id = max(products_db.keys()) + 1 if products_db else 1
    product_data = product.model_dump()
    product_data["id"] = product_id

    products_db[product_id] = product_data
    return {"message": "Product created successfully", "product": product_data}


@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    """Update a product (Admin only)"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")

    product_data = product.model_dump()
    product_data["id"] = product_id
    products_db[product_id] = product_data

    return {"message": "Product updated successfully", "product": product_data}


@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    """Delete a product (Admin only)"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")

    deleted_product = products_db.pop(product_id)
    return {"message": "Product deleted successfully", "product": deleted_product}


@app.get("/products/category/{category}")
async def get_products_by_category(category: ProductCategory):
    """Get all products in a specific category"""
    products = [p for p in products_db.values() if p["category"] == category]
    return {"category": category, "count": len(products), "products": products}


# ============ CUSTOMER ENDPOINTS ============


@app.get("/customers/", response_model=List[Customer])
async def list_customers(premium_only: bool = False):
    """List all customers"""
    customers = list(customers_db.values())
    if premium_only:
        customers = [c for c in customers if c["is_premium"]]
    return customers


@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int):
    """Get a specific customer by ID"""
    if customer_id not in customers_db:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customers_db[customer_id]


@app.post("/customers/", status_code=status.HTTP_201_CREATED)
async def create_customer(customer: Customer):
    """Register a new customer"""
    if customer.id in customers_db:
        raise HTTPException(status_code=400, detail="Customer ID already exists")

    customers_db[customer.id] = customer.model_dump()
    return {"message": "Customer created successfully", "customer": customer}


# ============ SHOPPING CART ENDPOINTS ============


@app.get("/cart/{customer_id}")
async def get_cart(customer_id: int):
    """Get customer's shopping cart"""
    if customer_id not in customers_db:
        raise HTTPException(status_code=404, detail="Customer not found")

    cart_items = shopping_carts.get(customer_id, [])
    cart_details = []
    total = 0

    for item in cart_items:
        if item["product_id"] in products_db:
            product = products_db[item["product_id"]]
            price = product["price"]

            # Apply discount if available
            if product["discount_percentage"] > 0:
                price = price * (1 - product["discount_percentage"] / 100)

            item_total = price * item["quantity"]
            total += item_total

            cart_details.append(
                {
                    "product_id": item["product_id"],
                    "product_name": product["name"],
                    "quantity": item["quantity"],
                    "unit_price": round(price, 2),
                    "item_total": round(item_total, 2),
                }
            )

    return {
        "customer_id": customer_id,
        "items": cart_details,
        "total_items": sum(item["quantity"] for item in cart_items),
        "total_amount": round(total, 2),
    }


@app.post("/cart/{customer_id}/add")
async def add_to_cart(customer_id: int, cart_item: CartItem):
    """Add a product to customer's cart"""
    if customer_id not in customers_db:
        raise HTTPException(status_code=404, detail="Customer not found")

    if cart_item.product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")

    product = products_db[cart_item.product_id]
    if product["stock_quantity"] < cart_item.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient stock. Only {product['stock_quantity']} available",
        )

    if customer_id not in shopping_carts:
        shopping_carts[customer_id] = []

    # Check if product already in cart
    cart = shopping_carts[customer_id]
    existing_item = next(
        (item for item in cart if item["product_id"] == cart_item.product_id), None
    )

    if existing_item:
        existing_item["quantity"] += cart_item.quantity
    else:
        cart.append(cart_item.model_dump())

    return {"message": "Product added to cart", "cart": shopping_carts[customer_id]}


@app.delete("/cart/{customer_id}/remove/{product_id}")
async def remove_from_cart(customer_id: int, product_id: int):
    """Remove a product from customer's cart"""
    if customer_id not in shopping_carts:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart = shopping_carts[customer_id]
    shopping_carts[customer_id] = [
        item for item in cart if item["product_id"] != product_id
    ]

    return {"message": "Product removed from cart"}


@app.delete("/cart/{customer_id}/clear")
async def clear_cart(customer_id: int):
    """Clear customer's cart"""
    if customer_id in shopping_carts:
        shopping_carts[customer_id] = []
    return {"message": "Cart cleared"}


# ============ ORDER ENDPOINTS ============


@app.post("/orders/", status_code=status.HTTP_201_CREATED)
async def create_order(order: Order):
    """Create a new order"""
    if order.customer_id not in customers_db:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Validate products and stock
    total_amount = 0
    for item in order.items:
        if item.product_id not in products_db:
            raise HTTPException(
                status_code=404, detail=f"Product {item.product_id} not found"
            )

        product = products_db[item.product_id]
        if product["stock_quantity"] < item.quantity:
            raise HTTPException(
                status_code=400, detail=f"Insufficient stock for {product['name']}"
            )

        # Calculate total
        price = item.price_at_purchase
        if product["discount_percentage"] > 0:
            price = price * (1 - product["discount_percentage"] / 100)
        total_amount += price * item.quantity

    # Create order
    order_id = max(orders_db.keys()) + 1 if orders_db else 1
    order_data = order.model_dump()
    order_data["id"] = order_id
    order_data["total_amount"] = round(total_amount, 2)
    order_data["created_at"] = datetime.now().isoformat()

    # Update stock
    for item in order.items:
        products_db[item.product_id]["stock_quantity"] -= item.quantity

    orders_db[order_id] = order_data

    # Clear customer's cart if exists
    if order.customer_id in shopping_carts:
        shopping_carts[order.customer_id] = []

    return {"message": "Order created successfully", "order": order_data}


@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    """Get order details"""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]


@app.get("/orders/customer/{customer_id}")
async def get_customer_orders(customer_id: int):
    """Get all orders for a customer"""
    customer_orders = [
        order for order in orders_db.values() if order["customer_id"] == customer_id
    ]
    return {"customer_id": customer_id, "orders": customer_orders}


@app.patch("/orders/{order_id}/status")
async def update_order_status(order_id: int, status: OrderStatus):
    """Update order status"""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")

    orders_db[order_id]["status"] = status
    orders_db[order_id]["updated_at"] = datetime.now().isoformat()

    return {"message": "Order status updated", "order": orders_db[order_id]}


# ============ STATISTICS & ANALYTICS ============


@app.get("/analytics/dashboard")
async def get_analytics():
    """Get e-commerce dashboard analytics"""
    total_revenue = sum(order["total_amount"] for order in orders_db.values())

    # Calculate average order value
    avg_order_value = total_revenue / len(orders_db) if orders_db else 0

    # Get order status breakdown
    status_breakdown = {}
    for order in orders_db.values():
        status = order["status"]
        status_breakdown[status] = status_breakdown.get(status, 0) + 1

    # Low stock products
    low_stock_products = [
        p
        for p in products_db.values()
        if p["stock_quantity"] < 10 and p["stock_quantity"] > 0
    ]

    return {
        "total_products": len(products_db),
        "total_customers": len(customers_db),
        "total_orders": len(orders_db),
        "total_revenue": round(total_revenue, 2),
        "average_order_value": round(avg_order_value, 2),
        "order_status_breakdown": status_breakdown,
        "low_stock_alert": len(low_stock_products),
        "low_stock_products": low_stock_products,
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": {
            "products": len(products_db),
            "customers": len(customers_db),
            "orders": len(orders_db),
            "active_carts": len(shopping_carts),
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
