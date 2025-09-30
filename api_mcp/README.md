# E-Commerce API

[![E-Commerce API Tests](https://github.com/anshajk/mcp_boilerplate/actions/workflows/api-tests.yml/badge.svg)](https://github.com/anshajk/mcp_boilerplate/actions/workflows/api-tests.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive FastAPI-based e-commerce platform API with product management, shopping cart, order processing, and analytics.

## Features

This e-commerce API demonstrates:
- **Product Management** - CRUD operations for products with categories and discounts
- **Customer Management** - Customer registration and profile management
- **Shopping Cart** - Add/remove items, view cart totals
- **Order Processing** - Create orders, track status, view order history
- **Analytics Dashboard** - Revenue tracking, order statistics, inventory alerts
- **Stock Management** - Automatic inventory updates
- **Discount System** - Percentage-based product discounts
- Request/response validation with Pydantic models
- Auto-generated API documentation

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

Start the server with:
```bash
python app.py
```

Or use uvicorn directly:
```bash
uvicorn app:app --reload
```

The server will start at `http://localhost:8000`

## Running Tests

The project includes comprehensive pytest test suite covering all API endpoints.

### Install Test Dependencies

Test dependencies are included in `requirements.txt`. If you haven't installed them:

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest test_app.py -v
```

Or use the test runner script:

```bash
python run_tests.py
```

### Run Specific Tests

**Run tests for a specific endpoint:**
```bash
pytest test_app.py::test_list_products -v
```

**Run tests matching a pattern:**
```bash
pytest test_app.py -k "product" -v
```

**Run with coverage:**
```bash
pytest test_app.py --cov=app --cov-report=html
```

### Test Coverage

The test suite includes:
- ✅ **50 test cases** - All passing
- ✅ Product management (CRUD operations + filtering)
- ✅ Customer management
- ✅ Shopping cart functionality
- ✅ Order processing and status updates
- ✅ Analytics and dashboard
- ✅ Input validation and error handling
- ✅ Integration tests for complete workflows
- ✅ Edge cases and boundary conditions
- ✅ Business logic (discounts, stock management, totals)

**Test Results:**
```
50 passed in 0.22s ✅
100% endpoint coverage
```

For detailed test documentation, see [TEST_COVERAGE.md](TEST_COVERAGE.md)

## CI/CD Pipeline

### GitHub Actions

This project uses GitHub Actions for continuous integration and testing. The workflow automatically:

- ✅ Runs tests on Python 3.10, 3.11, and 3.12
- ✅ Performs code linting with flake8
- ✅ Checks code formatting with Black and isort
- ✅ Generates test coverage reports
- ✅ Runs security scans with Bandit
- ✅ Checks dependencies for vulnerabilities with Safety

**Workflow triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Manual workflow dispatch

**View workflow status:** [![E-Commerce API Tests](https://github.com/anshajk/mcp_boilerplate/actions/workflows/api-tests.yml/badge.svg)](https://github.com/anshajk/mcp_boilerplate/actions/workflows/api-tests.yml)

### Running Locally

To run the same checks locally before pushing:

```bash
# Install dev dependencies
pip install black isort flake8 bandit safety pytest-cov

# Format code
black .
isort .

# Lint
flake8 . --max-line-length=127

# Security scan
bandit -r .

# Run tests with coverage
pytest test_app.py --cov=app --cov-report=html
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Example API Usage

### Products

**List all products:**
```bash
curl "http://localhost:8000/products/"
```

**Filter products by category:**
```bash
curl "http://localhost:8000/products/?category=electronics&in_stock_only=true"
```

**Filter by price range:**
```bash
curl "http://localhost:8000/products/?min_price=100&max_price=300"
```

**Get a specific product:**
```bash
curl http://localhost:8000/products/1
```

**Create a new product:**
```bash
curl -X POST "http://localhost:8000/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop Pro",
    "description": "High-performance laptop for professionals",
    "price": 1499.99,
    "category": "electronics",
    "stock_quantity": 25,
    "image_url": "https://example.com/laptop.jpg",
    "discount_percentage": 10
  }'
```

**Get products by category:**
```bash
curl "http://localhost:8000/products/category/electronics"
```

### Customers

**Register a new customer:**
```bash
curl -X POST "http://localhost:8000/customers/" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 3,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "phone": "+1-555-0789",
    "address": "789 Pine St, Chicago, IL 60601",
    "is_premium": false
  }'
```

**List all customers:**
```bash
curl http://localhost:8000/customers/
```

**Get premium customers only:**
```bash
curl "http://localhost:8000/customers/?premium_only=true"
```

### Shopping Cart

**View cart:**
```bash
curl http://localhost:8000/cart/1
```

**Add item to cart:**
```bash
curl -X POST "http://localhost:8000/cart/1/add" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
```

**Remove item from cart:**
```bash
curl -X DELETE "http://localhost:8000/cart/1/remove/1"
```

**Clear cart:**
```bash
curl -X DELETE "http://localhost:8000/cart/1/clear"
```

### Orders

**Create an order:**
```bash
curl -X POST "http://localhost:8000/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "items": [
      {
        "product_id": 1,
        "quantity": 1,
        "price_at_purchase": 299.99
      },
      {
        "product_id": 2,
        "quantity": 2,
        "price_at_purchase": 129.99
      }
    ],
    "shipping_address": "123 Main St, New York, NY 10001",
    "payment_method": "credit_card",
    "status": "pending"
  }'
```

**Get order details:**
```bash
curl http://localhost:8000/orders/1
```

**Get customer's order history:**
```bash
curl http://localhost:8000/orders/customer/1
```

**Update order status:**
```bash
curl -X PATCH "http://localhost:8000/orders/1/status?status=shipped"
```

### Analytics

**View dashboard analytics:**
```bash
curl http://localhost:8000/analytics/dashboard
```

### Health Check

```bash
curl http://localhost:8000/health
```

## Data Models

### Product Categories
- `electronics`
- `clothing`
- `books`
- `home`
- `sports`
- `beauty`

### Order Status Flow
- `pending` → `processing` → `shipped` → `delivered`
- Can be `cancelled` at any time before delivery

## Project Structure

```
api_mcp/
├── app.py              # Main FastAPI application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Key E-Commerce Features

1. **Product Catalog**: Browse products with filtering by category, price range, and stock availability
2. **Discount System**: Automatic price calculation with percentage discounts
3. **Shopping Cart**: Session-based cart management for each customer
4. **Order Management**: Complete order lifecycle from creation to delivery
5. **Inventory Control**: Automatic stock updates and low-stock alerts
6. **Customer Segmentation**: Premium vs regular customer classification
7. **Analytics Dashboard**: Real-time business metrics and insights

## Business Logic Highlights

- **Stock Validation**: Prevents orders that exceed available inventory
- **Automatic Cart Clearing**: Cart is emptied after successful order
- **Price Calculation**: Discounts applied automatically at checkout
- **Order Tracking**: Status updates throughout the fulfillment process
- **Low Stock Alerts**: Dashboard warnings for products below threshold

## Next Steps

- Add authentication (JWT tokens, OAuth)
- Implement payment gateway integration (Stripe, PayPal)
- Add product reviews and ratings
- Implement wish lists and favorites
- Add email notifications for orders
- Database integration (PostgreSQL, MongoDB)
- Image upload for products
- Advanced search with Elasticsearch
- Recommendation engine
- Multi-currency support
- Deploy to production (Docker, Kubernetes, AWS/GCP)

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/products/` | List products with filters |
| GET | `/products/{id}` | Get product details |
| POST | `/products/` | Create product |
| PUT | `/products/{id}` | Update product |
| DELETE | `/products/{id}` | Delete product |
| GET | `/products/category/{category}` | Products by category |
| GET | `/customers/` | List customers |
| GET | `/customers/{id}` | Get customer |
| POST | `/customers/` | Register customer |
| GET | `/cart/{customer_id}` | View cart |
| POST | `/cart/{customer_id}/add` | Add to cart |
| DELETE | `/cart/{customer_id}/remove/{product_id}` | Remove from cart |
| DELETE | `/cart/{customer_id}/clear` | Clear cart |
| POST | `/orders/` | Create order |
| GET | `/orders/{id}` | Get order |
| GET | `/orders/customer/{customer_id}` | Customer orders |
| PATCH | `/orders/{id}/status` | Update order status |
| GET | `/analytics/dashboard` | Analytics dashboard |
| GET | `/health` | Health check |
