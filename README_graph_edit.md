## Graph Editing API Usage Guide

This guide describes how to use the Graph Editing API to manually add or update nodes and relationships in the Neo4j graph database.

These APIs can be used to extend the knowledge graph beyond the data imported from scraping.

---

## Available Endpoints

All endpoints are prefixed with `/graph`.

| Method | Path               | Description                  |
| ------ | ------------------ | ---------------------------- |
| POST   | /graph/add-brand   | Add or update a brand node   |
| POST   | /graph/add-product | Add or update a product node |
| POST   | /graph/add-edge    | Create HAS_PRODUCT relation  |

## Endpoint Details

### 1. Add Brand Node

**POST** `/graph/add-brand`

Adds or updates a brand node in the graph.

**Request Body:**

```json
{
  "name": "Smarties",
  "url": "https://example.com/smarties",
  "image": "https://example.com/smarties.jpg"
}
```

### 2. Add Product Node

**POST** `/graph/add-product`

Adds or updates a product node. All fields are optional except `name`.

**Request Body:**

```json
{
  "name": "Mini Smarties",
  "brand": "Smarties",
  "url": "https://example.com/mini-smarties",
  "image": "https://example.com/mini.jpg",
  "description": "Bite-sized colorful candies",
  "product_size": "12g",
  "product_line": "Mini",
  "label": "snack"
}
```

### 3. Add Relationship (Edge)

**POST** `/graph/add-edge`

Creates a `HAS_PRODUCT` relationship from a Brand to a Product node.

**Request Body:**

```json
{
  "from_brand": "Smarties",
  "to_product": "Mini Smarties"
}
```

---

## API Response

All endpoints return a standard structure:

```json
{
  "status": "Node created.",
  "stats": {
    "nodes_created": 1,
    "properties_set": 7
  }
}
```

Or:

```json
{
  "status": "Relationship created.",
  "stats": {
    "relationships_created": 1
  }
}
```

---

## How to Test

You can test these APIs in the following ways:

### 1. Swagger UI

Visit:

```
http://localhost:8000/docs
```

Or the deployed site:

```
https://<your-cloud-run-url>/docs
```

- Expand the `Graph Editing` section
- Click "Try it out" on any endpoint
- Fill in sample data and click "Execute"

### 2. Postman

You can also use Postman to test the APIs.

- Open [Postman](https://www.postman.com/) and create a new request.
- Set the method to POST and enter the URL `http://localhost:8000/graph/add-brand` (or the deployed URL).
- In the `Body` tab, select `raw` → `JSON`, then paste:

```json
{
  "name": "Smarties",
  "url": "https://example.com/smarties",
  "image": "https://example.com/smarties.jpg"
}
```

- Click "Send" to execute the request and view the response.

### 3. curl (CLI)

```bash
curl -X POST http://localhost:8000/graph/add-brand \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Smarties",
    "url": "https://example.com/smarties",
    "image": "https://example.com/smarties.jpg"
  }'
```

---

## Notes

- These changes are persistent and modify the actual Neo4j database.
- Avoid duplicating existing brands/products—use unique names or test values.

---

For more technical details, see the implementation in [`backend/api/graph_editing.py`](backend/api/graph_editing.py).
