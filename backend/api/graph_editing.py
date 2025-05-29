from fastapi import APIRouter, HTTPException, status
from backend.models.graph_models import BrandNode, ProductNode, HasProductEdge
from common.neo4j_client import get_neo4j_driver
from backend.models.response_models import GraphStats, GraphAddResponse

router = APIRouter()
graph_driver = get_neo4j_driver()


@router.post("/add-brand", response_model=GraphAddResponse)
def add_brand_node(data: BrandNode):
    """
    Add a new Brand node to the Neo4j graph.
    """
    if not data.name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Brand name is required"
        )

    try:
        query = """
        MERGE (b:Brand {name: $name})
        SET b.url = $url, b.image = $image
        """
        with graph_driver.session() as session:
            result = session.run(query, name=data.name, url=data.url, image=data.image)
            summary = result.consume()

        return _build_node_response(summary)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add brand: {str(e)}",
        )


@router.post("/add-product", response_model=GraphAddResponse)
def add_product_node(data: ProductNode):
    """
    Add a new Product node to the Neo4j graph.
    """
    if not data.name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Product name is required"
        )

    try:
        query = """
        MERGE (p:Product {name: $name})
        SET p.brand = $brand, p.url = $url, p.image = $image,
            p.description = $description,
            p.product_size = $product_size,
            p.product_line = $product_line,
            p.label = $label
        """
        with graph_driver.session() as session:
            result = session.run(query, **data.dict())
            summary = result.consume()

        return _build_node_response(summary)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add product: {str(e)}",
        )


@router.post("/add-edge", response_model=GraphAddResponse)
def add_product_edge(data: HasProductEdge):
    """
    Create a HAS_PRODUCT relationship from Brand to Product.
    """
    if not data.from_brand.strip() or not data.to_product.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both brand and product names are required",
        )

    try:
        query = """
        MATCH (b:Brand {name: $from_brand})
        MATCH (p:Product {name: $to_product})
        MERGE (b)-[r:HAS_PRODUCT]->(p)
        RETURN r
        """
        with graph_driver.session() as session:
            result = session.run(
                query, from_brand=data.from_brand, to_product=data.to_product
            )
            summary = result.consume()

        return _build_edge_response(summary)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add edge: {str(e)}",
        )


# Build API response for node-related operations
def _build_node_response(summary) -> GraphAddResponse:
    if summary.counters.nodes_created == 1:
        status_msg = "Node created."
    elif summary.counters.properties_set > 0:
        status_msg = "Node updated."
    else:
        status_msg = "No change (already exists with same data)."

    return GraphAddResponse(
        status=status_msg,
        stats=GraphStats(
            nodes_created=summary.counters.nodes_created,
            properties_set=summary.counters.properties_set,
        ),
    )


# Build API response for edge-related operations
def _build_edge_response(summary) -> GraphAddResponse:
    if summary.counters.relationships_created == 1:
        status_msg = "Relationship created."
    else:
        status_msg = "No change (relationship already exists)."

    return GraphAddResponse(
        status=status_msg,
        stats=GraphStats(relationships_created=summary.counters.relationships_created),
    )
