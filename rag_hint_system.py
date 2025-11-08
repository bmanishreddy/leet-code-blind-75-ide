"""
RAG-based hint system using problem solutions knowledge base + LLM.
"""
import json
import os
from typing import Dict, List

class RAGHintSystem:
    def __init__(self, knowledge_base_path: str = None, llm_model_path: str = None):
        """Initialize RAG system with knowledge base and LLM."""
        if knowledge_base_path is None:
            knowledge_base_path = os.path.join(os.path.dirname(__file__), 'knowledge_base.json')
        
        if llm_model_path is None:
            # Use Deepseek-Coder-1.3B (code-specialized, fast, small)
            llm_model_path = os.path.join(os.path.dirname(__file__), 'models', 'deepseek-coder-1.3b-instruct.Q4_K_M.gguf')
        
        self.knowledge_base = {}
        self.llm = None
        self.llm_model_path = llm_model_path
        self.llm_loading_attempted = False  # Track if we've tried to load
        
        self.load_knowledge_base(knowledge_base_path)
        # Don't load LLM at startup - load it lazily when first hint is requested
    
    def load_knowledge_base(self, path: str):
        """Load the knowledge base from JSON file."""
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    self.knowledge_base = json.load(f)
                print(f"✅ Loaded knowledge base with {len(self.knowledge_base)} problems")
            else:
                print(f"⚠️  Knowledge base not found at {path}. Run download_solutions.py first.")
        except Exception as e:
            print(f"❌ Error loading knowledge base: {e}")
    
    def load_llm(self):
        """Load the LLM for intelligent hint generation."""
        try:
            if os.path.exists(self.llm_model_path):
                from llama_cpp import Llama
                import platform
                
                # Detect Apple Silicon and use Metal GPU acceleration
                is_apple_silicon = platform.system() == 'Darwin' and platform.machine() == 'arm64'
                gpu_layers = 28 if is_apple_silicon else 0  # Deepseek-1.3B has fewer layers
                
                print(f"🔄 Loading Deepseek-Coder-1.3B from {self.llm_model_path}...")
                if is_apple_silicon:
                    print(f"🚀 Apple Silicon detected! Using Metal GPU acceleration ({gpu_layers} layers)")
                
                self.llm = Llama(
                    model_path=self.llm_model_path,
                    n_ctx=4096,  # Deepseek supports larger context
                    n_threads=4,
                    n_gpu_layers=gpu_layers,  # Use Metal GPU on Apple Silicon
                    use_mlock=True,  # Keep model in RAM for faster inference
                    n_batch=512,  # Batch size for prompt processing
                    logits_all=False,  # Only compute logits for last token (fixes corruption)
                    vocab_only=False,
                    verbose=False  # Reduce terminal spam
                )
                print("✅ LLM loaded successfully with GPU acceleration!")
            else:
                print(f"⚠️  LLM model not found at {self.llm_model_path}")
        except Exception as e:
            print(f"⚠️  Could not load LLM: {e}")
            print("📝 Falling back to knowledge-base only hints")
    
    def get_hint(self, question: Dict, user_code: str, hint_type: str = 'general') -> str:
        """
        Get context-aware hint using RAG + LLM.
        
        Args:
            question: Problem details
            user_code: User's current code
            hint_type: 'general', 'specific', or 'next_step'
        
        Returns:
            Contextual hint based on problem and user's progress
        """
        # Get problem slug or title
        title = question.get('title', '').lower()
        problem_id = question.get('id', '')
        
        # Try to find in knowledge base
        problem_kb = None
        for slug, data in self.knowledge_base.items():
            if slug in title or title.replace(' ', '-') in slug:
                problem_kb = data
                break
        
        if not problem_kb:
            # Fallback to generic hints
            return self._generic_hint(question, user_code, hint_type)
        
        # Analyze user's code progress
        code_progress = self._analyze_code_progress(user_code)
        
        # Try to load LLM lazily if not already loaded
        if not self.llm_loading_attempted:
            print("🔄 Loading LLM on first hint request...")
            self.load_llm()
            self.llm_loading_attempted = True
        
        # Try to use LLM for intelligent hints
        if self.llm and user_code.strip():
            try:
                llm_hint = self._generate_llm_hint(question, problem_kb, user_code, code_progress, hint_type)
                if llm_hint:
                    return llm_hint
            except Exception as e:
                print(f"LLM hint generation failed: {e}")
        
        # Fallback to template-based hints
        if hint_type == 'general':
            return self._generate_general_hint(problem_kb, code_progress)
        elif hint_type == 'specific':
            return self._generate_specific_hint(problem_kb, code_progress)
        else:  # next_step
            return self._generate_next_step_hint(problem_kb, code_progress)
    
    def _analyze_code_progress(self, code: str) -> Dict:
        """Analyze user's code to understand their progress."""
        progress = {
            'has_code': len(code.strip()) > 50,
            'has_loop': 'for ' in code or 'while ' in code,
            'has_dict': '{' in code or 'dict(' in code.lower(),
            'has_set': 'set(' in code,
            'has_list': '[' in code or 'list(' in code.lower(),
            'has_function': 'def ' in code,
            'has_return': 'return ' in code,
            'has_if': 'if ' in code,
            'line_count': len([l for l in code.split('\n') if l.strip()])
        }
        return progress
    
    def _generate_general_hint(self, problem_kb: Dict, progress: Dict) -> str:
        """Generate a general approach hint."""
        approach = problem_kb.get('approach', 'Problem Solving')
        pattern = problem_kb.get('pattern', 'General')
        key_insight = problem_kb.get('key_insight', '')
        time_complexity = problem_kb.get('time_complexity', 'O(n)')
        explanation = problem_kb.get('explanation', '')
        
        hint = f"💡 **{approach}**\n\n"
        
        if key_insight:
            hint += f"**Key Insight:** {key_insight}\n\n"
        
        if explanation:
            # Take first sentence of explanation
            first_sentence = explanation.split('.')[0] + '.'
            hint += f"{first_sentence}\n\n"
        
        hint += f"**Pattern:** {pattern}\n"
        hint += f"**Time Complexity:** {time_complexity}"
        
        return hint
    
    def _generate_specific_hint(self, problem_kb: Dict, progress: Dict) -> str:
        """Generate specific implementation hint."""
        approach = problem_kb.get('approach', '')
        explanation = problem_kb.get('explanation', '')
        hints = problem_kb.get('hint_sequence', [])
        pattern = problem_kb.get('pattern', '')
        
        # Choose hint based on progress
        if not progress['has_code'] and hints:
            return f"🎯 **{approach}**\n\n{hints[0]}"
        elif progress['has_code'] and len(hints) > 1:
            return f"🎯 **{approach}**\n\n{hints[1]}"
        elif len(hints) > 2:
            return f"🎯 **{approach}**\n\n{hints[2]}"
        elif hints:
            return f"🎯 **{approach}**\n\n{hints[0]}"
        
        # Fallback with explanation
        if explanation:
            return f"🎯 **{approach}**\n\n{explanation[:200]}..."
        
        return f"🎯 **{approach}**\n\nUse the {pattern} pattern to solve this efficiently."
    
    def _generate_next_step_hint(self, problem_kb: Dict, progress: Dict) -> str:
        """Generate concrete next step hint."""
        hints = problem_kb.get('hint_sequence', [])
        pattern = problem_kb.get('pattern', '')
        approach = problem_kb.get('approach', '')
        
        # Progressive hints based on code progress
        if not progress['has_function']:
            return "📝 **Next Step**\n\nDefine your solution method in the Solution class. Look at the problem signature to see what parameters it needs."
        
        # Pattern-specific hints
        if 'Hash' in pattern or 'Map' in pattern:
            if not progress['has_dict']:
                return f"📝 **Next Step**\n\nFor this {approach} problem, initialize a hash map to track values you've seen. This will give you O(1) lookups."
        
        if 'Two Pointer' in pattern:
            if not progress['has_loop']:
                return f"📝 **Next Step**\n\nSort your input array first, then use two pointers (left and right) to scan through it. Start left at 0 and right at len-1."
        
        if 'Sliding Window' in pattern:
            if not progress['has_loop']:
                return f"📝 **Next Step**\n\nCreate a sliding window with two pointers (start and end). Expand the window by moving 'end', and shrink it by moving 'start' when needed."
        
        if 'Binary Search' in pattern:
            if not progress['has_loop']:
                return f"📝 **Next Step**\n\nImplement binary search with left=0, right=len-1. In each iteration, calculate mid and decide which half to search."
        
        # Use hint sequence
        if not progress['has_loop'] and hints:
            return f"📝 **Next Step**\n\n{hints[0] if hints else 'Start iterating through your input data.'}"
        elif progress['has_loop'] and len(hints) > 1:
            return f"📝 **Next Step**\n\n{hints[1]}"
        elif len(hints) > 2:
            return f"📝 **Next Step**\n\n{hints[2]}"
        elif hints:
            return f"📝 **Next Step**\n\n{hints[-1]}"
        
        # Final fallback
        if progress['has_loop'] and not progress['has_return']:
            return "📝 **Next Step**\n\nYou're close! Now implement the core logic inside your loop and make sure to return the final result."
        
        return f"📝 **Next Step**\n\nImplement the {approach} logic. Remember to handle edge cases and return the result."
    
    def _generate_llm_hint(self, question: Dict, problem_kb: Dict, user_code: str, code_progress: Dict, hint_type: str) -> str:
        """Generate intelligent hint using LLM with RAG context."""
        # Build context from knowledge base
        approach = problem_kb.get('approach', '')
        key_insight = problem_kb.get('key_insight', '')
        pattern = problem_kb.get('pattern', '')
        time_complexity = problem_kb.get('time_complexity', '')
        explanation = problem_kb.get('explanation', '')
        
        # Add hint sequence for reference
        hint_sequence = problem_kb.get('hint_sequence', [])
        hints_text = ""
        if hint_sequence:
            hints_text = "\nKnown Hints:\n"
            for i, h in enumerate(hint_sequence[:2]):  # Only use first 2 hints
                hints_text += f"- {h}\n"
        
        # Analyze what user has done
        progress_summary = []
        if code_progress['has_function']:
            progress_summary.append("defined function")
        if code_progress['has_loop']:
            progress_summary.append("added loop")
        if code_progress['has_dict']:
            progress_summary.append("using dictionary")
        if code_progress['has_return']:
            progress_summary.append("has return")
        
        progress_text = ", ".join(progress_summary) if progress_summary else "just started"
        
        # Build a focused, directive prompt
        if hint_type == 'general':
            instruction = f"""Give a brief hint about the APPROACH to solve "{question.get('title', '')}".
            
Mention:
1. The algorithm pattern ({pattern})
2. One key insight: {key_insight if key_insight else 'what makes this problem solvable'}
3. Expected complexity: {time_complexity if time_complexity else 'O(n) or better'}

Format: 2-3 short sentences. Be direct and specific to THIS problem."""
        
        elif hint_type == 'specific':
            instruction = f"""The student has {progress_text}. Give a SPECIFIC implementation hint.

Known approach: {approach}
{hints_text}

Tell them ONE specific thing to implement next. Be concrete, not abstract."""
        
        else:  # next_step
            instruction = f"""The student has {progress_text}. Tell them the EXACT NEXT CODE to write.

Known approach: {approach}

Be very specific: "Initialize a hash map called 'seen' to store..." NOT "consider using a data structure"."""
        
        # Simplified, focused prompt
        prompt = f"""Problem: {question.get('title', '')} ({question.get('difficulty', '')})

{instruction}

Hint:"""
        
        try:
            response = self.llm(
                prompt,
                max_tokens=150,
                temperature=0.5,  # Lower temperature for more focused output
                top_p=0.85,
                top_k=40,  # Add top_k for more deterministic output
                repeat_penalty=1.2,  # Discourage repetition
                stop=["Problem:", "Student:", "\n\n\n", "```"],  # Better stop sequences
                echo=False
            )
            
            hint = response['choices'][0]['text'].strip()
            
            # Filter out meta-commentary
            if not hint or len(hint) < 20 or any(bad in hint.lower() for bad in [
                'your advice', 'this hint', 'the student should', 'i suggest', 'i recommend',
                'you should help', 'provide guidance', 'give advice'
            ]):
                # LLM gave unhelpful output, use knowledge base instead
                print(f"⚠️ LLM output too generic, using knowledge base")
                return None  # Will trigger fallback
            
            # Clean up the hint
            hint = hint.replace('Hint:', '').strip()
            
            # Add emoji based on hint type
            emoji = {'general': '💡', 'specific': '🎯', 'next_step': '📝'}.get(hint_type, '💡')
            return f"{emoji} **{approach}**\n\n{hint}"
            
        except Exception as e:
            print(f"Error generating LLM hint: {e}")
            return None
    
    def _generic_hint(self, question: Dict, user_code: str, hint_type: str) -> str:
        """Fallback generic hints when problem not in KB."""
        category = question.get('category', '').lower()
        
        if hint_type == 'general':
            return f"💡 Category: {category}\n\nThink about what data structure best fits this problem type."
        elif hint_type == 'specific':
            return "🎯 Break the problem into smaller steps and solve each one."
        else:
            return "📝 Start by writing out the function signature and thinking about your approach."

# Global instance
rag_system = RAGHintSystem()

