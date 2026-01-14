import logging
import os
import pickle

from src.ml import get_embeddings

logger = logging.getLogger(__name__)

tech_examples = [
    "The app won't launch after the update",  # software crash
    "How do I reset the password in the access control system?",  # configuration
    "The device won't connect to Bluetooth",  # connectivity issue
    "I get a 500 error when logging into my account",  # server error
    "My laptop overheats and shuts down",  # hardware issue
    "How do I set up a VPN on my work computer?",  # configuration
    "The scanner isn't recognized by the system",  # driver/compatibility
    "Why isn't two-factor authentication working?",  # security failure
    "Notifications aren't showing up in the app",  # UI/UX bug
    "How do I install a graphics card driver?",  # software installation
    "The site froze during payment",  # technical glitch
    "I can't upload a file, it says 'network error'",  # network failure
    "My microphone doesn't work in Zoom even though it's connected",  # device issue
    "Why doesn't the 'Submit' button work on the form?",  # UI bug
    "How do I clear my browser cache?",  # technical instruction
]


cust_examples = [
    "I want to cancel my order, it hasn't been shipped yet",  # order management
    "I received the wrong item from what I ordered",  # delivery error
    "How can I change my payment method?",  # account/payment
    "Where can I find my bill from last month?",  # documentation
    "Can I get a refund if the item doesn't suit me?",  # return policy
    "Why is my account blocked?",  # access issue
    "How do I renew my subscription?",  # service management
    "I didn't receive the order confirmation email",  # communication
    "How long does delivery take?",  # logistics
    "How can I contact support about a return?",  # support
    "Payment failed but the money was withdrawn",  # financial incident
    "I want to complain about the service quality",  # feedback
    "Where can I view my order history?",  # customer interface
    "I didn't get loyalty points for my purchase",  # loyalty program
    "How do I change the delivery address?",  # logistics
]


talk_examples = [
    "How are you?",
    "Hi",
    "What's new?",
    "What's the weather like today?",
    "Can you speak Belarusian?",
    "What's your favorite movie?",
    "What do you think about the future?",
    "Are you real?",
    "How old are you?",
    "Can you tell a joke?",
]


data = {
    "tech": get_embeddings(tech_examples),
    "cust": get_embeddings(cust_examples),
    "talk": get_embeddings(talk_examples),
}


def build_classification_base_embeddings():
    project_root = os.path.dirname(os.path.dirname(__file__))
    output_path = os.path.join(project_root, "embeddings.pkl")
    with open(output_path, "wb") as f:
        pickle.dump(data, f)
        logger.info("Embeddings saved to %s", output_path)
