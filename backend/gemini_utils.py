# gemini_utils.`py

import google.generativeai as genai

# ✅ Step 1: Set your API key
genai.configure(api_key="enter_your_api_key")

# ✅ Step 2: Load Gemini 2.0 Flash model (only once)
model = genai.GenerativeModel("gemini-2.0-flash")

# ✅ Step 3: Define reusable function
def send_to_gemini(conversation):
    try:
        formatted = []
        for turn in conversation:
            if turn["role"] == "system":
                continue  # Skip system messages
            formatted.append({
                "role": turn["role"],
                "parts": [turn["content"]]
            })

        # Generate response
        response = model.generate_content(formatted)
        
        # Check if response is valid
        if not response or not response.text:
            print("❌ Warning: Empty response from Gemini")
            return "I'm sorry, I couldn't generate a response. Please try again.", 0, 0

        # Token usage tracking with proper error handling
        prompt_toks = 0
        response_toks = 0
        
        try:
            if hasattr(response, 'usage_metadata') and response.usage_metadata:
                prompt_toks = getattr(response.usage_metadata, 'prompt_token_count', 0)
                # candidates_token_count can be int or list; handle both
                ctc = getattr(response.usage_metadata, 'candidates_token_count', 0)
                if isinstance(ctc, list) and ctc:
                    response_toks = ctc[0]
                elif isinstance(ctc, int):
                    response_toks = ctc
                else:
                    response_toks = 0
        except Exception:
            prompt_toks = 0
            response_toks = 0

        return response.text, prompt_toks, response_toks
        
    except Exception as e:
        print(f"❌ Error calling Gemini API: {e}")
        return "I'm sorry, there was an error processing your request. Please try again.", 0, 0
