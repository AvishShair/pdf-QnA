"""QA Engine using Google Gemini API"""

import logging
from typing import List, Dict, Tuple
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QAEngine:
    """Question Answering engine using Google Gemini"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        """
        Initialize QA Engine
        
        Args:
            api_key: Google Gemini API key
            model_name: Name of the Gemini model to use
        """
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel(model_name)
        self.logger = logger
        
        # Configure generation parameters
        self.generation_config = {
            'temperature': 0.7,
            'top_p': 0.8,
            'top_k': 40,
            'max_output_tokens': 2048,
        }
        
        # Safety settings
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]
    
    def answer_question(
        self,
        question: str,
        context_chunks: List[Tuple[str, Dict, float]],
        chat_history: List[Dict] = None
    ) -> Dict:
        """
        Answer a question based on context chunks
        
        Args:
            question: User's question
            context_chunks: List of (chunk_text, metadata, distance) tuples
            chat_history: Optional chat history for context
            
        Returns:
            Dictionary with answer, sources, and metadata
        """
        try:
            # Prepare context from chunks
            context = self._prepare_context(context_chunks)
            
            # Create prompt
            prompt = self._create_prompt(question, context, chat_history)
            
            # Generate response
            self.logger.info(f"Generating answer for question: {question[:50]}...")
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            
            # Extract answer
            answer = response.text if response.text else "I couldn't generate an answer. Please try rephrasing your question."
            
            # Prepare sources
            sources = self._prepare_sources(context_chunks)
            
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
                'answer': f"Error generating answer: {str(e)}",
                'sources': [],
                'question': question,
                'model': self.model_name,
                'error': str(e)
            }
    
    def _prepare_context(self, context_chunks: List[Tuple[str, Dict, float]]) -> str:
        """Prepare context from retrieved chunks"""
        if not context_chunks:
            return "No relevant context found."
        
        context_parts = []
        for i, (chunk, metadata, distance) in enumerate(context_chunks, 1):
            source_info = f"[Source {i}"
            if 'filename' in metadata:
                source_info += f" - {metadata['filename']}"
            if 'chunk_id' in metadata:
                source_info += f" - Chunk {metadata['chunk_id']}"
            source_info += "]"
            
            context_parts.append(f"{source_info}\n{chunk}\n")
        
        return "\n".join(context_parts)
    
    def _create_prompt(
        self,
        question: str,
        context: str,
        chat_history: List[Dict] = None
    ) -> str:
        """Create prompt for the model"""
        
        prompt_parts = []
        
        # System instruction
        prompt_parts.append(
            "You are a helpful AI assistant that answers questions based on the provided PDF documents. "
            "Your task is to provide accurate, clear, and concise answers based ONLY on the information "
            "given in the context below. If the answer cannot be found in the context, clearly state that."
        )
        
        # Add chat history if available
        if chat_history and len(chat_history) > 0:
            prompt_parts.append("\n### Previous Conversation:")
            for entry in chat_history[-3:]:  # Last 3 exchanges
                if entry['role'] == 'user':
                    prompt_parts.append(f"User: {entry['content']}")
                elif entry['role'] == 'assistant':
                    prompt_parts.append(f"Assistant: {entry['content']}")
        
        # Add context
        prompt_parts.append("\n### Context from PDF Documents:")
        prompt_parts.append(context)
        
        # Add current question
        prompt_parts.append("\n### Current Question:")
        prompt_parts.append(question)
        
        # Add instructions
        prompt_parts.append(
            "\n### Instructions:"
            "\n1. Answer the question based on the context provided above."
            "\n2. Be specific and cite relevant information from the sources."
            "\n3. If the context doesn't contain enough information, say so clearly."
            "\n4. Keep your answer clear, concise, and well-structured."
            "\n5. If appropriate, mention which source(s) your answer comes from."
        )
        
        prompt_parts.append("\n### Answer:")
        
        return "\n".join(prompt_parts)
    
    def _prepare_sources(self, context_chunks: List[Tuple[str, Dict, float]]) -> List[Dict]:
        """Prepare source information for display"""
        sources = []
        
        for i, (chunk, metadata, distance) in enumerate(context_chunks, 1):
            source = {
                'id': i,
                'text': chunk[:300] + "..." if len(chunk) > 300 else chunk,
                'full_text': chunk,
                'distance': round(distance, 4),
                'filename': metadata.get('filename', 'Unknown'),
                'chunk_id': metadata.get('chunk_id', i)
            }
            sources.append(source)
        
        return sources
    
    def simple_chat(self, message: str, chat_history: List[Dict] = None) -> str:
        """
        Simple chat without context (for general questions)
        
        Args:
            message: User message
            chat_history: Optional chat history
            
        Returns:
            Model response
        """
        try:
            # Create chat session
            chat = self.model.start_chat(history=[])
            
            # Add history if available
            if chat_history:
                for entry in chat_history[-5:]:
                    if entry['role'] == 'user':
                        chat.send_message(entry['content'])
            
            # Send current message
            response = chat.send_message(message)
            return response.text
            
        except Exception as e:
            self.logger.error(f"Error in simple chat: {str(e)}")
            return f"Error: {str(e)}"
    
    def test_connection(self) -> bool:
        """Test if the API connection works"""
        try:
            response = self.model.generate_content("Hello")
            return bool(response.text)
        except Exception as e:
            self.logger.error(f"API connection test failed: {str(e)}")
            return False

