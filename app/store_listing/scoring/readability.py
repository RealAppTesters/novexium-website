import re


class ReadabilityScorer:
    """Score text readability"""
    
    def score(self, text: str) -> int:
        if not text:
            return 0
        
        score = 0
        max_score = 0
        
        # 1. Word count
        word_count = len(text.split())
        if 100 <= word_count <= 300:
            score += 30
        elif 50 <= word_count < 100:
            score += 20
        else:
            score += 10
        max_score += 30
        
        # 2. Sentence length
        sentences = re.split(r'[.!?]+', text)
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        
        if 10 <= avg_sentence_length <= 20:
            score += 25
        elif 5 <= avg_sentence_length < 10:
            score += 15
        else:
            score += 5
        max_score += 25
        
        # 3. Paragraph structure
        paragraphs = text.split('\n\n')
        if len(paragraphs) >= 2:
            score += 25
        elif len(paragraphs) >= 1:
            score += 15
        max_score += 25
        
        # 4. Bullet points or structure
        if '•' in text or '-' in text:
            score += 20
        max_score += 20
        
        return int(round((score / max_score) * 100 if max_score > 0 else 0))
