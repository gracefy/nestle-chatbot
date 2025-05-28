from pathlib import Path
from scripts.graph.schema import BrandNode, ProductNode, HasProductEdge
from common.constants import (
    PRODUCTS_PATH,
    GRAPH_PROCESSED_DIR,
    GRAPH_BRANDS_PATH,
    GRAPH_PRODUCTS_PATH,
    GRAPH_EDGES_PATH,
)
from common.utils import save_json, load_json


def clean_graph_data():
    """Clean and prepare graph data from raw products JSON."""
    raw_products = load_json(PRODUCTS_PATH)

    brands = {}
    products = []
    edges = []

    for item in raw_products:
        brand_name = item.get("brand")
        if not brand_name:
            print(f"Skipped product: {item.get('title')}")
            continue

        # Create brand node if not exists
        if brand_name not in brands:
            brands[brand_name] = BrandNode(name=brand_name)

        # Create product node
        product = ProductNode(
            name=item.get("title"),
            brand=brand_name,
            url=item.get("url"),
            image=item.get("images", [None])[0] if item.get("images") else None,
            description=item.get("description"),
            product_size=item.get("product_size"),
            product_line=item.get("product_line"),
            label=item.get("labels", [None])[0] if item.get("labels") else None,
        )

        products.append(product)

        # Create edge Brand -> Product
        edges.append(HasProductEdge(from_brand=brand_name, to_product=product.name))

    # Ensure output dir exists
    Path(GRAPH_PROCESSED_DIR).mkdir(parents=True, exist_ok=True)

    # Save cleaned data
    brands = [b.model_dump() for b in brands.values()]
    products = [p.model_dump() for p in products]
    edges = [e.model_dump() for e in edges]

    save_json(brands, GRAPH_BRANDS_PATH)
    save_json(products, GRAPH_PRODUCTS_PATH)
    save_json(edges, GRAPH_EDGES_PATH)

    print(
        f"Graph data cleaned and saved: \n"
        f"Total Brands: {len(brands)}, Total Products: {len(products)}, Total Edges: {len(edges)}"
    )


if __name__ == "__main__":
    clean_graph_data()
