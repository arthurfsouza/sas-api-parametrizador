from leia import SentimentIntensityAnalyzer 

def preprocess_text(text):
    return text.lower()

def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()

    try:
        preprocessed_text = preprocess_text(text)
        sentiment_scores = sia.polarity_scores(preprocessed_text)

        return sentiment_scores
    except OSError as e:
        print("Erro durante a análise de sentimento:", e)
        return None

def scale_sentiment_score(sentiment_score):
    sentiment_score_scaled = ((sentiment_score["compound"] + 1) / 2) * 5

    return sentiment_score_scaled

def execute(input_text):
    sentiment_scores = analyze_sentiment(input_text)

    if sentiment_scores:
        sentiment_score_scaled = scale_sentiment_score(sentiment_scores)

        print("Texto:", input_text)
        print("Pontuação de Sentimento (0-5):", sentiment_score_scaled)

        return sentiment_score_scaled

    return None

positive_input_text = "Eu amo absolutamente tudo sobre este filme! A história é incrível, os personagens são cativantes e a cinematografia é deslumbrante. Não consigo encontrar uma única falha. Simplesmente perfeito em todos os aspectos."
negative_input_text = "Este filme é terrível. A história é confusa, os personagens são mal desenvolvidos e a direção é péssima."

positive_input_text = "Eu estou feliz 😀"
negative_input_text = "Eu não estou feliz! Este filme é terrível!"

execute(input_text=positive_input_text)
execute(input_text=negative_input_text)