from kedro.pipeline import Pipeline, node, pipeline
from news_topic_classifier.nodes.preprocessing import clean_articles

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func = clean_articles,
            inputs = "intermediate_articles",     # Comes from catalog
            outputs = "processed_articles",
            name = "clean_articles_node"
        ),
    ])