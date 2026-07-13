import re


class SignalDetector:

    def detect(self, customer_message: str):

        if not customer_message:

            return {
                "intent": None,
                "emotion": "neutral",
                "urgency": "normal"
            }

        text = customer_message.lower().strip()

        # -----------------------------------------
        # Intent
        # -----------------------------------------

        intent = self._detect_intent(text)

        # -----------------------------------------
        # Emotion
        # -----------------------------------------

        emotion = self._detect_emotion(text)

        # -----------------------------------------
        # Urgency
        # -----------------------------------------

        urgency = self._detect_urgency(text)

        return {

            "intent": intent,

            "emotion": emotion,

            "urgency": urgency

        }

    # =====================================================
    # Intent Detection
    # =====================================================

    def _detect_intent(self, text):

        yes_words = [

            "yes",

            "yeah",

            "yep",

            "sure",

            "okay",

            "ok",

            "correct",

            "please continue",

            "go ahead"

        ]

        no_words = [

            "no",

            "nope",

            "not interested",

            "don't",

            "do not",

            "busy",

            "later"

        ]

        callback_words = [

            "call later",

            "call tomorrow",

            "call next week",

            "call me later",

            "another time"

        ]

        if any(word in text for word in callback_words):

            return "CALLBACK"

        if any(word in text for word in yes_words):

            return "YES"

        if any(word in text for word in no_words):

            return "NO"

        return "UNKNOWN"

    # =====================================================
    # Emotion Detection
    # =====================================================

    def _detect_emotion(self, text):

        positive = [

            "good",

            "great",

            "fine",

            "nice",

            "happy",

            "excellent"

        ]

        negative = [

            "angry",

            "upset",

            "bad",

            "frustrated",

            "annoyed"

        ]

        if any(word in text for word in positive):

            return "positive"

        if any(word in text for word in negative):

            return "negative"

        return "neutral"

    # =====================================================
    # Urgency Detection
    # =====================================================

    def _detect_urgency(self, text):

        urgent_words = [

            "urgent",

            "immediately",

            "right now",

            "asap"

        ]

        if any(word in text for word in urgent_words):

            return "high"

        return "normal"