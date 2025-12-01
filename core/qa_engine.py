"""Enhanced QA Engine with streaming support"""

import logging
from typing import List, Dict, Tuple, Optional, Iterator
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancedQAEngine:
    """Enhanced QA Engine with streaming and better context handling"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash-exp"):
        """
        Initialize QA Engine
        
        Args:
            api_key: Google Gemini API key
            model_name: Model name (default: gemini-2.0-flash-exp)
        """
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=api_key)
        
        # Initialize model
        # Note: for the current google-generativeai SDK, you pass the short model name
        # (e.g. "gemini-2.0-flash-exp") rather than "models/...".
        self.model = genai.GenerativeModel(self.model_name)
        self.logger = logger
        
        # Generation config
        self.generation_config = {
            'temperature': 0.7,
            'top_p': 0.8,
            'top_k': 40,
            'max_output_tokens': 2048,
        }
        
        # Safety settings
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
    
    def answer_question(
        self,
        question: str,
        context: str,
        sources: List[Dict],
        chat_history: Optional[List[Dict]] = None,
        stream: bool = False
    ) -> Dict:
        """
        Answer question with context (non-streaming)
        
        Args:
            question: User question
            context: Retrieved context
            sources: Source list
            chat_history: Previous conversation
            stream: Whether to stream (for streaming, use answer_question_stream)
            
        Returns:
            Dictionary with answer and metadata
        """
        try:
            prompt = self._create_prompt(question, context, chat_history)
            
            self.logger.info(f"Generating answer for: {question[:50]}...")
            
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            
            answer = response.text if response.text else "I couldn't generate an answer."
            
            return {
                'success': True,
                'answer': answer,
                'sources': sources,
                'question': question,
                'model': self.model_name,
                'error': None
            }
            
        except Exception as e:
            self.logger.error(f"Error generating answer: {str(e)}")
            return {
                'success': False,
                'answer': f"Error: {str(e)}",
                'sources': sources,
                'question': question,
                'model': self.model_name,
                'error': str(e)
            }
    
    def answer_question_stream(
        self,
        question: str,
        context: str,
        sources: List[Dict],
        chat_history: Optional[List[Dict]] = None
    ) -> Iterator[str]:
        """
        Stream answer tokens in real-time
        
        Args:
            question: User question
            context: Retrieved context
            sources: Source list
            chat_history: Previous conversation
            
        Yields:
            Token chunks as they are generated
        """
        try:
            prompt = self._create_prompt(question, context, chat_history)
            
            # Generate with streaming
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings,
                stream=True
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            self.logger.error(f"Error in streaming: {str(e)}")
            yield f"Error: {str(e)}"
    
    def summarize(
        self,
        text: str,
        summary_type: str = "full"
    ) -> str:
        """
        Generate summary
        
        Args:
            text: Text to summarize
            summary_type: Type of summary (full, key_points, glossary)
            
        Returns:
            Summary text
        """
        try:
            if summary_type == "full":
                prompt = f"Provide a comprehensive summary of the following text:\n\n{text[:8000]}"
            elif summary_type == "key_points":
                prompt = f"Extract and list the key points from the following text:\n\n{text[:8000]}"
            elif summary_type == "glossary":
                prompt = f"Create a glossary of important terms and their definitions from the following text:\n\n{text[:8000]}"
            else:
                prompt = f"Summarize the following text:\n\n{text[:8000]}"
            
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            
            return response.text if response.text else "Could not generate summary."
            
        except Exception as e:
            self.logger.error(f"Error generating summary: {str(e)}")
            return f"Error: {str(e)}"
    
    def summarize_pages(
        self,
        pages: List[Dict],
        page_numbers: List[int]
    ) -> str:
        """
        Summarize specific pages
        
        Args:
            pages: List of page dictionaries
            page_numbers: List of page numbers to summarize
            
        Returns:
            Summary text
        """
        try:
            # Extract text from selected pages
            selected_text = []
            for page in pages:
                if page.get('page') in page_numbers:
                    selected_text.append(f"Page {page['page']}:\n{page.get('text', '')}")
            
            combined_text = "\n\n".join(selected_text)
            
            if not combined_text:
                return "No text found for selected pages."
            
            return self.summarize(combined_text, summary_type="full")
            
        except Exception as e:
            self.logger.error(f"Error summarizing pages: {str(e)}")
            return f"Error: {str(e)}"
    
    def _create_prompt(
        self,
        question: str,
        context: str,
        chat_history: Optional[List[Dict]] = None
    ) -> str:
        """Create prompt for the model"""
        prompt_parts = []
        
        # System instruction
        prompt_parts.append(
            "You are a helpful AI assistant that answers questions based on provided PDF documents. "
            "Provide accurate, clear, and concise answers based ONLY on the context below. "
            "If the answer cannot be found in the context, clearly state that."
        )
        
        # Add chat history (last 5-10 turns)
        if chat_history:
            prompt_parts.append("\n### Previous Conversation:")
            for entry in chat_history[-10:]:  # Last 10 messages
                role = entry.get('role', '')
                content = entry.get('content', '')
                if role == 'user':
                    prompt_parts.append(f"User: {content}")
                elif role == 'assistant':
                    prompt_parts.append(f"Assistant: {content}")
        
        # Add context
        prompt_parts.append("\n### Context from PDF Documents:")
        prompt_parts.append(context)
        
        # Add current question
        prompt_parts.append("\n### Current Question:")
        prompt_parts.append(question)
        
        # Instructions
        prompt_parts.append(
            "\n### Instructions:"
            "\n1. Answer based on the context provided."
            "\n2. Be specific and cite sources when possible."
            "\n3. If information is not in the context, say so clearly."
            "\n4. Keep your answer clear, concise, and well-structured."
            "\n5. Mention source document and page number when relevant."
        )
        
        prompt_parts.append("\n### Answer:")
        
        return "\n".join(prompt_parts)
    
    def test_connection(self) -> bool:
        """Test API connection"""
        try:
            response = self.model.generate_content("Hello")
            return bool(response.text)
        except Exception as e:
            self.logger.error(f"API connection test failed: {str(e)}")
            return False

