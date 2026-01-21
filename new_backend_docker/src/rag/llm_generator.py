"""
LLM Generator - Generate answers using free HuggingFace models
"""
import requests
import json

class LLMGenerator:
    def __init__(self):
        """Initialize with free HuggingFace inference"""
        # Using free HuggingFace Inference API
        self.model_url = "https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-4k-instruct"
        self.headers = {"Content-Type": "application/json"}

        # Fallback model if main doesn't work
        self.fallback_model = "https://api-inference.huggingface.co/models/google/flan-t5-large"

    def generate_answer(self, question: str, context: str) -> str:
        """Generate answer using free HuggingFace model"""
        try:
            # Prepare prompt
            prompt = self._create_prompt(question, context)

            # Call HuggingFace Inference API (FREE)
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 512,
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "do_sample": True
                }
            }

            response = requests.post(
                self.model_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                # Extract generated text
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                elif isinstance(result, dict):
                    generated_text = result.get('generated_text', '')
                else:
                    generated_text = str(result)

                # Clean up the response
                answer = self._extract_answer(generated_text, prompt)
                return answer
            else:
                print(f"API Error: {response.status_code}, trying fallback...")
                return self._generate_fallback_answer(question, context)

        except Exception as e:
            print(f"Error generating answer: {e}")
            return self._generate_fallback_answer(question, context)

    def _create_prompt(self, question: str, context: str) -> str:
        """Create prompt for the model"""
        prompt = f"""You are a helpful AI assistant for a Physical AI and Humanoid Robotics textbook. Answer the question based on the given context.

Context from the book:
{context}

Question: {question}

Provide a clear, informative answer based on the context above. If the context doesn't contain enough information, say so and provide general knowledge about the topic.

Answer:"""

        return prompt

    def _extract_answer(self, generated_text: str, original_prompt: str) -> str:
        """Extract the answer from generated text"""
        # Remove the prompt part if it's included
        if generated_text.startswith(original_prompt[:100]):
            answer = generated_text[len(original_prompt):].strip()
        else:
            answer = generated_text.strip()

        # Clean up
        answer = answer.split("Question:")[0].split("Context:")[0].strip()

        return answer if answer else "I apologize, but I couldn't generate a proper answer. Please try rephrasing your question."

    def _generate_fallback_answer(self, question: str, context: str) -> str:
        """Generate simple fallback answer without LLM"""
        # Extract key sentences from context
        sentences = context.split('. ')

        # Simple keyword matching
        question_words = set(question.lower().split())
        relevant_sentences = []

        for sentence in sentences[:5]:  # Take first 5 sentences
            sentence_words = set(sentence.lower().split())
            overlap = len(question_words & sentence_words)

            if overlap > 0:
                relevant_sentences.append((overlap, sentence))

        # Sort by relevance
        relevant_sentences.sort(reverse=True, key=lambda x: x[0])

        if relevant_sentences:
            best_sentence = relevant_sentences[0][1]
            return f"Based on the textbook, here's what I found: {best_sentence}."

        return "I found some relevant information in the textbook, but I need more specific context to answer your question accurately. Could you rephrase or provide more details about what you'd like to know?"
