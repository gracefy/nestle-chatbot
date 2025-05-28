from common.constants import GRAPH_BRANDS_PATH, GRAPH_PRODUCTS_PATH, GRAPH_EDGES_PATH
from common.neo4j_client import get_neo4j_driver, close_driver
from common.utils import load_json


def upload_to_neo4j():
    driver = get_neo4j_driver()
    if not driver:
        print("Failed to connect to Neo4j. Please check your connection settings.")
        return

    brands = load_json(GRAPH_BRANDS_PATH)
    products = load_json(GRAPH_PRODUCTS_PATH)
    edges = load_json(GRAPH_EDGES_PATH)

    # product_names = [p["name"] for p in products]
    # print(len(product_names), len(set(product_names)))

    with driver.session() as session:
        # Upload brand nodes
        for brand in brands:
            query = (
                "MERGE (b:Brand {name: $name})\n" "SET b.url = $url, b.image = $image"
            )
            session.run(
                query,
                name=brand["name"],
                url=brand.get("url"),
                image=brand.get("image"),
            )

        # Upload product nodes
        for product in products:
            query = (
                "MERGE (p:Product {name: $name})\n"
                "SET p.url = $url,\n"
                "    p.image = $image,\n"
                "    p.description = $description,\n"
                "    p.product_size = $product_size,\n"
                "    p.product_line = $product_line,\n"
                "    p.label = $label"
            )
            session.run(
                query,
                name=product["name"],
                url=product.get("url"),
                image=product.get("image"),
                description=product.get("description"),
                product_size=product.get("product_size"),
                product_line=product.get("product_line"),
                label=product.get("label"),
            )

        # Upload edges
        for edge in edges:
            query = (
                "MATCH (b:Brand {name: $brand_name})\n"
                "MATCH (p:Product {name: $product_name})\n"
                "MERGE (b)-[r:HAS_PRODUCT]->(p)"
            )
            session.run(
                query,
                brand_name=edge["from_brand"],
                product_name=edge["to_product"],
            )

    close_driver()
    print("Graph data uploaded to Neo4j.")


if __name__ == "__main__":
    upload_to_neo4j()
