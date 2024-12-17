# backend/app/services/nlp_service.py
import google.generativeai as genai
from typing import Dict, List, Any
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

class NLPService:
    def __init__(self):
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

        # Enhanced knowledge base with CouldYou? Cup information
        self.knowledge_base: Dict[str, Dict[str, Any]] = {
            "period": {
                "keywords": ["period", "menstruation", "bleeding", "cycle", "monthly"],
                "general": "Menstruation is a natural monthly process where the uterus sheds its lining.",
                "symptoms": [
                    "Cramps",
                    "Mood changes",
                    "Fatigue",
                    "Bloating",
                ],
                "duration": "Typically lasts 3-7 days",
                "cycle": "The menstrual cycle usually ranges from 21-35 days",
                "statistics": {
                    "poverty": "689 million people live in extreme poverty on $1.90 or less a day",
                    "usa": "1 in 4 menstruators in the USA cannot afford menstrual products",
                    "africa": "1 in 10 girls in Africa miss school due to menstruation",
                    "impact": "Girls not completing school costs countries $15-30 trillion in lost lifetime productivity & earnings"
                }
            },
            "cup": {
                "keywords": ["cup", "menstrual cup", "couldyou cup", "insert", "remove", "clean", "usage", "virgin", "how to use"],
                "general": "The CouldYou? Cup is a reusable menstrual cup that can be worn for up to 12 hours.",
                "warranty": "10+ years shelf and use life",
                "insertion": [
                    "1. Wash hands thoroughly with soap and water",
                    "2. Find a comfortable position (sit, squat, kneel, or stand)",
                    "3. Fold the cup using one of the recommended folding methods",
                    "4. Insert gently with the opening pointed towards your back",
                    "5. Ensure the cup opens fully by running your finger around it"
                ],
                "removal": [
                    "1. Wash hands with soap and water",
                    "2. Sit or squat and locate the base of the cup",
                    "3. Squeeze the base to break the seal",
                    "4. Gently remove while keeping upright",
                    "5. Empty, rinse, and reinsert"
                ],
                "cleaning": [
                    "Do not use soap or bleach",
                    "Rinse with clean water between uses",
                    "Boil for 5 minutes for thorough cleaning",
                    "Store in the provided cotton bag"
                ],
                "safety": [
                    "Safe to wear for up to 12 hours",
                    "Made from medical-grade silicone",
                    "Does not affect virginity",
                    "Cannot get lost inside the body",
                    "Very low risk of TSS compared to tampons"
                ]
            },
            "help": {
                "keywords": ["help", "support", "assistance", "need", "product", "contact", "question"],
                "resources": [
                    "CouldYou? provides menstrual products to those in need",
                    "Educational resources available at www.couldyoucup.org/resources",
                    "Community support programs",
                    "Contact: mycup@couldyou.org or call (888) 994-1961"
                ],
                "social_media": [
                    "Facebook: facebook.com/couldyoucup",
                    "Instagram: @couldyoucup",
                    "Twitter: @couldyoucup"
                ],
                "contact": "Visit https://couldyou.org for more information",
                "website": "https://couldyou.org"
            }
        }

        self.context_prompt = self.create_context_prompt()

    def create_context_prompt(self) -> str:
        context = [
            "You are a helpful assistant for CouldYou?, specializing in menstrual health education and the CouldYou? Cup.",
            "Provide accurate, compassionate responses based on this knowledge base.",
            "Always prioritize safety and proper usage instructions.",
            "\nABOUT COULDYOU?:",
            "CouldYou? is an organization dedicated to providing menstrual products and education to those in need.",
            "This is the link to the website https://couldyou.org"
            "\nKEY FACTS:",
        ]

        # Add statistics
        for stat_key, stat_value in self.knowledge_base["period"]["statistics"].items():
            context.append(f"- {stat_value}")

        # Add cup information
        context.append("\nCOULDYOU? CUP INFORMATION:")
        context.append(self.knowledge_base["cup"]["general"])
        context.append("Safety Features:")
        context.extend([f"- {safety}" for safety in self.knowledge_base["cup"]["safety"]])

        return "\n".join(context)



    async def get_gemini_response(self, user_input: str) -> str:
        try:
            # Enhanced prompt with more specific guidance
            prompt = f"""{self.context_prompt}

User Question: {user_input}

Please provide a helpful, accurate, and compassionate response. If the question is about:
- Cup usage: Include safety reminders and proper steps
- Medical concerns: Recommend consulting a healthcare professional
- Product support: Provide contact information
- General education: Include relevant statistics and facts

Response:"""

            response = self.model.generate_content(prompt)
            formatted_response = self.format_response(response.text)

            return formatted_response
        except Exception as e:
            print(f"Error getting Gemini response: {e}")
            return self.get_fallback_response(user_input)


    def get_fallback_response(self, text: str) -> str:
        intent = self.analyze_intent(text)
        matching_category = self.find_matching_category(text)

        if matching_category:
            return self.format_response(self.knowledge_base[matching_category])

        return "I'm here to help answer questions about menstrual health and period poverty. You can ask about periods, symptoms, or support resources."

    async def process_input(self, text: str, language: str = "en") -> Dict[str, Any]:
        try:
            response_text = await self.get_gemini_response(text)
            return {
                "type": "chat",
                "content": response_text
            }
        except Exception as e:
            print(f"Error in process_input: {e}")
            return {
                "type": "simple",
                "content": self.get_fallback_response(text)
            }

    def analyze_intent(self, text: str) -> str:
        text = text.lower()
        if any(word in text for word in ["what", "how", "explain", "tell", "which", "why"]):
            return "information"
        elif any(word in text for word in ["help", "need", "support", "where", "get", "find"]):
            return "help"
        elif any(word in text for word in ["thank", "thanks", "appreciate", "grateful"]):
            return "gratitude"
        return "general"

    def find_matching_category(self, text: str) -> str:
        text = text.lower()
        for category, info in self.knowledge_base.items():
            if "keywords" in info:
                if any(keyword in text for keyword in info["keywords"]):
                    return category
        return None

    def format_response(self, content: str, topic: str = None) -> str:
        """Format the response with proper markdown structure"""

        if topic:
            content = f"## {topic}\n\n{content}"

        # Format sections
        sections = content.split('\n\n')
        formatted_sections = []

        for section in sections:
            # Format lists
            if section.strip().startswith('•'):
                lines = section.split('\n')
                formatted_lines = [f"* {line.strip('• ')}" for line in lines]
                formatted_sections.append('\n'.join(formatted_lines))
            # Format important information
            elif section.lower().startswith(('important:', 'note:', 'warning:')):
                formatted_sections.append(f"> {section}")
            else:
                formatted_sections.append(section)

        return '\n\n'.join(formatted_sections)
