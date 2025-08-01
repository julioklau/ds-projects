from kedro.pipeline import Pipeline
from news_topic_classifier.pipelines.data_preprocessing import pipeline as data_preprocessing

def register_pipelines() -> dict[str, Pipeline]:
    return {
        "dp": data_preprocessing.create_pipeline(),
        "__default__": data_preprocessing.create_pipeline(),
    }