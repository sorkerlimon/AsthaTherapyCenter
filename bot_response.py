import json
import re
from datetime import datetime
from typing import Dict, List, Tuple

class TherapyCenterChatBot:
    """
    Astha Therapy Center Chatbot
    Provides automated responses for common patient inquiries
    """
    
    def __init__(self):
        self.responses = {
            # Greetings
            'greetings': [
                "Hi! Welcome to Astha Therapy Center. How can I help you today?",
                "Hello! I'm here to assist you with information about our therapy services. What would you like to know?",
                "Greetings! I'm the Astha Therapy Center assistant. How may I help you?",
            ],
            
            # Services
            'services': {
                'speech_therapy': "We offer comprehensive speech therapy services for children with speech delays, articulation disorders, and communication challenges. Our certified speech therapists work with children to improve their communication skills through fun and engaging activities.",
                'occupational_therapy': "Our occupational therapy services help children develop daily living skills, fine motor skills, sensory processing, and cognitive abilities. We focus on helping children participate more fully in daily activities.",
                'physical_therapy': "Our physical therapy services help children improve their gross motor skills, balance, coordination, and strength. We work with children with various physical challenges to help them reach their full potential.",
                'autism_support': "We provide specialized autism support services including behavioral therapy, social skills training, and individualized intervention programs designed specifically for children on the autism spectrum.",
                'early_intervention': "Our early intervention services are designed for infants and toddlers (0-3 years) who may have developmental delays or disabilities. Early intervention can make a significant difference in a child's development.",
                'behavioral_therapy': "We offer behavioral therapy services to help children develop positive behaviors, reduce challenging behaviors, and improve social interactions through evidence-based approaches."
            },
            
            # Contact Information
            'contact': {
                'phone': "You can reach us at +880 16816-52122 for appointments and inquiries.",
                'email': "You can email us at asthatherapycenter@gmail.com for any questions or to schedule an appointment.",
                'address': "We're located at P# 9/2, R# 05, B# B, Section # 06, Mirpur, Dhaka-1216, Bangladesh.",
                'hours': "Our working hours are Saturday to Thursday: 10:00 AM to 6:00 PM. We're closed on Fridays."
            },
            
            # Appointment
            'appointment': "To book an appointment, you can:\n1. Call us at +880 16816-52122\n2. Email us at asthatherapycenter@gmail.com\n3. Use our online booking form on the website\n\nOur team will get back to you within 24 hours to confirm your appointment.",
            
            # Pricing
            'pricing': "Our therapy session fees vary depending on the type of service and duration. Please contact us at +880 16816-52122 for detailed pricing information. We also offer package deals for multiple sessions.",
            
            # Age Groups
            'age_groups': "We provide therapy services for children from infancy (0 years) to 18 years old. Our therapists are specially trained to work with pediatric patients and adapt their approaches based on the child's age and developmental level.",
            
            # Insurance
            'insurance': "Please contact us directly at +880 16816-52122 to discuss insurance coverage and payment options. Our staff can help you understand what services may be covered.",
            
            # Emergency
            'emergency': "For emergency situations, please contact emergency services immediately. For urgent therapy-related concerns during business hours, call us at +880 16816-52122.",
            
            # Default responses
            'default': [
                "I'd be happy to help you with that! For detailed information, please contact us at +880 16816-52122 or email asthatherapycenter@gmail.com.",
                "That's a great question! Our team can provide you with specific information. Please call us at +880 16816-52122 or visit our clinic.",
                "I understand you need more information about that. Please feel free to contact our office at +880 16816-52122 for personalized assistance.",
            ],
            
            # Goodbye
            'goodbye': [
                "Thank you for contacting Astha Therapy Center! Have a wonderful day and feel free to reach out anytime.",
                "It was great helping you today! Don't hesitate to contact us at +880 16816-52122 if you have more questions.",
                "Goodbye! We look forward to serving you and your child's therapy needs.",
            ]
        }
        
        self.keywords = {
            'greetings': ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening'],
            'services': ['service', 'therapy', 'treatment', 'help', 'what do you do'],
            'speech_therapy': ['speech', 'speaking', 'talk', 'communication', 'language'],
            'occupational_therapy': ['occupational', 'daily skills', 'fine motor', 'sensory'],
            'physical_therapy': ['physical', 'movement', 'motor skills', 'balance', 'coordination'],
            'autism_support': ['autism', 'autistic', 'spectrum', 'behavioral'],
            'early_intervention': ['early intervention', 'infant', 'toddler', 'baby'],
            'behavioral_therapy': ['behavior', 'behaviour', 'social skills'],
            'appointment': ['appointment', 'book', 'schedule', 'visit', 'consultation'],
            'contact': ['contact', 'phone', 'call', 'email', 'address', 'location'],
            'hours': ['hours', 'time', 'when open', 'schedule'],
            'pricing': ['price', 'cost', 'fee', 'payment', 'how much'],
            'age': ['age', 'old', 'years', 'children'],
            'insurance': ['insurance', 'coverage', 'pay'],
            'emergency': ['emergency', 'urgent', 'immediate'],
            'goodbye': ['bye', 'goodbye', 'thank you', 'thanks', 'that\'s all']
        }
    
    def get_response(self, user_message: str) -> str:
        """
        Generate appropriate response based on user message
        """
        user_message = user_message.lower().strip()
        
        # Check for greetings first
        if self._contains_keywords(user_message, 'greetings'):
            return self._get_random_response('greetings')
        
        # Check for goodbye
        if self._contains_keywords(user_message, 'goodbye'):
            return self._get_random_response('goodbye')
        
        # Check for specific services
        for service in ['speech_therapy', 'occupational_therapy', 'physical_therapy', 
                       'autism_support', 'early_intervention', 'behavioral_therapy']:
            if self._contains_keywords(user_message, service):
                return self.responses['services'][service]
        
        # Check for contact information
        if self._contains_keywords(user_message, 'contact'):
            if 'phone' in user_message or 'call' in user_message:
                return self.responses['contact']['phone']
            elif 'email' in user_message:
                return self.responses['contact']['email']
            elif 'address' in user_message or 'location' in user_message:
                return self.responses['contact']['address']
            elif 'hours' in user_message or 'time' in user_message:
                return self.responses['contact']['hours']
            else:
                return f"{self.responses['contact']['phone']}\n\n{self.responses['contact']['email']}\n\n{self.responses['contact']['address']}"
        
        # Check for hours
        if self._contains_keywords(user_message, 'hours'):
            return self.responses['contact']['hours']
        
        # Check for appointment
        if self._contains_keywords(user_message, 'appointment'):
            return self.responses['appointment']
        
        # Check for pricing
        if self._contains_keywords(user_message, 'pricing'):
            return self.responses['pricing']
        
        # Check for age groups
        if self._contains_keywords(user_message, 'age'):
            return self.responses['age_groups']
        
        # Check for insurance
        if self._contains_keywords(user_message, 'insurance'):
            return self.responses['insurance']
        
        # Check for emergency
        if self._contains_keywords(user_message, 'emergency'):
            return self.responses['emergency']
        
        # Check for services in general
        if self._contains_keywords(user_message, 'services'):
            return ("We offer several therapy services:\n"
                   "• Speech Therapy\n"
                   "• Occupational Therapy\n"
                   "• Physical Therapy\n"
                   "• Autism Support\n"
                   "• Early Intervention\n"
                   "• Behavioral Therapy\n\n"
                   "Which service would you like to know more about?")
        
        # Default response
        return self._get_random_response('default')
    
    def _contains_keywords(self, message: str, category: str) -> bool:
        """
        Check if message contains keywords from a specific category
        """
        if category not in self.keywords:
            return False
        
        keywords = self.keywords[category]
        return any(keyword in message for keyword in keywords)
    
    def _get_random_response(self, category: str) -> str:
        """
        Get a random response from a category
        """
        import random
        responses = self.responses.get(category, self.responses['default'])
        return random.choice(responses)
    
    def get_initial_message(self) -> str:
        """
        Get the initial greeting message when chat starts
        """
        return "Hi! Welcome to Astha Therapy Center. How can I help you today? 😊\n\nI can provide information about:\n• Our therapy services\n• Appointment booking\n• Contact information\n• Working hours\n• Pricing\n\nWhat would you like to know?"

# Create chatbot instance
therapy_chatbot = TherapyCenterChatBot()

def get_bot_response(user_message: str) -> Dict:
    """
    Main function to get chatbot response
    Returns a dictionary with response and timestamp
    """
    try:
        response = therapy_chatbot.get_response(user_message)
        return {
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message
        }
    except Exception as e:
        return {
            'success': False,
            'response': "I'm sorry, I'm experiencing some technical difficulties. Please contact us directly at +880 16816-52122 for assistance.",
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def get_initial_greeting() -> str:
    """
    Get the initial greeting message
    """
    return therapy_chatbot.get_initial_message()