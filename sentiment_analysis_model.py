from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = "/home/ramtin/Desktop/projects/sentiment_analysis/distilbert"
        self.sentiment_analyzer = pipeline("sentiment-analysis", model=model_path)

    def analyze(self, text):
        if not text:
            return {"label": "NEUTRAL", "score": 0.0}
        return self.sentiment_analyzer(text)[0]
