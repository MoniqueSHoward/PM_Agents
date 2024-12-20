from typing import List, Dict, Optional, Callable
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import psutil
import logging
import gc
import time
from datetime import datetime

from agent_types import TextChunk, ChunkGroup  # Updated import

class ParallelProcessor:
    """Handles text processing with chunk grouping support"""
    def __init__(self, 
                 words_threshold: int = 1000,
                 context_window: int = 25,
                 max_retries: int = 3,
                 memory_threshold: float = 0.9,
                 chunk_cooldown: int = 15,
                 group_size: int = 3):
        self.words_threshold = words_threshold
        self.context_window = context_window
        self.max_retries = max_retries
        self.memory_threshold = memory_threshold
        self.chunk_cooldown = chunk_cooldown
        self.group_size = group_size
        self.logger = logging.getLogger(__name__)
        
        # Download required NLTK data
        try:
            nltk.download('punkt', quiet=True)
        except Exception as e:
            self.logger.warning(f"Failed to download NLTK data: {str(e)}")

    def create_chunks(self, text: str) -> List[TextChunk]:
        """Split text into chunks while maintaining sentence integrity"""
        chunks = []
        words = word_tokenize(text)
        sentences = sent_tokenize(text)
        
        if len(words) <= self.words_threshold:
            return [TextChunk(
                id=0,
                content=text,
                preceding_context="",
                following_context="",
                start_position=0,
                end_position=len(text),
                word_count=len(words)
            )]

        current_chunk = []
        current_words = 0
        chunk_id = 0
        start_pos = 0
        
        for sentence in sentences:
            sentence_words = word_tokenize(sentence)
            
            if current_words + len(sentence_words) > self.words_threshold and current_chunk:
                # Create chunk with context
                chunk_text = ' '.join(current_chunk)
                end_pos = start_pos + len(chunk_text)
                
                # Get context
                preceding_context = self._get_context(text, start_pos, True)
                following_context = self._get_context(text, end_pos, False)
                
                chunks.append(TextChunk(
                    id=chunk_id,
                    content=chunk_text,
                    preceding_context=preceding_context,
                    following_context=following_context,
                    start_position=start_pos,
                    end_position=end_pos,
                    word_count=current_words
                ))
                
                current_chunk = [sentence]
                current_words = len(sentence_words)
                start_pos = text.find(sentence, end_pos)
                chunk_id += 1
            else:
                current_chunk.append(sentence)
                current_words += len(sentence_words)
        
        # Handle last chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append(TextChunk(
                id=chunk_id,
                content=chunk_text,
                preceding_context=self._get_context(text, start_pos, True),
                following_context="",
                start_position=start_pos,
                end_position=len(text),
                word_count=current_words
            ))
        
        return chunks

    def create_chunk_groups(self, chunks: List[TextChunk]) -> List[ChunkGroup]:
        """Organize chunks into logical groups with shared context"""
        if not chunks:
            return []
            
        groups = []
        group_id = 0
        
        # Process chunks in groups
        for i in range(0, len(chunks), self.group_size):
            group_chunks = chunks[i:i + self.group_size]
            
            # Calculate group metadata
            total_words = sum(chunk.word_count for chunk in group_chunks)
            start_position = group_chunks[0].start_position
            end_position = group_chunks[-1].end_position
            
            # Get context overlap between chunks in group
            context_overlap = self._extract_group_context(group_chunks)
            
            # Create group metadata
            metadata = {
                'created_at': datetime.now().isoformat(),
                'chunk_count': len(group_chunks),
                'avg_chunk_size': total_words / len(group_chunks),
                'context_quality': self._assess_context_quality(group_chunks)
            }
            
            # Create chunk group
            group = ChunkGroup(
                id=group_id,
                chunks=group_chunks,
                total_words=total_words,
                context_overlap=context_overlap,
                start_position=start_position,
                end_position=end_position,
                metadata=metadata
            )
            
            groups.append(group)
            group_id += 1
            
        return groups

    def _extract_group_context(self, chunks: List[TextChunk]) -> str:
        """Extract shared context between chunks in a group"""
        if len(chunks) <= 1:
            return ""
            
        # Find overlapping content between adjacent chunks
        overlaps = []
        for i in range(len(chunks) - 1):
            current_chunk = chunks[i]
            next_chunk = chunks[i + 1]
            
            # Get the end of current chunk and start of next chunk
            overlap = self._find_overlap(
                current_chunk.content[-self.context_window*10:],
                next_chunk.content[:self.context_window*10]
            )
            
            if overlap:
                overlaps.append(overlap)
                
        return ' ... '.join(overlaps)

    def _find_overlap(self, text1: str, text2: str) -> str:
        """Find overlapping content between two text segments"""
        words1 = word_tokenize(text1)
        words2 = word_tokenize(text2)
        
        # Look for common phrases
        overlap = ""
        min_overlap = 3  # Minimum words for meaningful overlap
        
        for i in range(len(words1) - min_overlap + 1):
            for j in range(len(words2) - min_overlap + 1):
                k = 0
                while (i + k < len(words1) and 
                       j + k < len(words2) and 
                       words1[i + k] == words2[j + k]):
                    k += 1
                if k >= min_overlap:
                    candidate = ' '.join(words1[i:i + k])
                    if len(candidate) > len(overlap):
                        overlap = candidate
                        
        return overlap

    def _assess_context_quality(self, chunks: List[TextChunk]) -> float:
        """Assess the quality of context preservation in a group of chunks"""
        if len(chunks) <= 1:
            return 1.0
            
        scores = []
        for i in range(len(chunks) - 1):
            current_chunk = chunks[i]
            next_chunk = chunks[i + 1]
            
            # Check context continuity
            if current_chunk.following_context and next_chunk.preceding_context:
                # Calculate similarity between contexts
                overlap = self._find_overlap(
                    current_chunk.following_context,
                    next_chunk.preceding_context
                )
                if overlap:
                    # Score based on overlap length relative to context window
                    score = len(word_tokenize(overlap)) / self.context_window
                    scores.append(min(score, 1.0))
                else:
                    scores.append(0.0)
                    
        return sum(scores) / len(scores) if scores else 1.0

    def process_text_parallel(self, text: str, processor_func: Callable) -> List[Dict]:
        """Process text using chunk groups"""
        # Create initial chunks
        chunks = self.create_chunks(text)
        if not chunks:
            return []
            
        # Organize chunks into groups
        chunk_groups = self.create_chunk_groups(chunks)
        self.logger.info(f"Created {len(chunk_groups)} chunk groups")
        
        processed_results = []
        
        for group in chunk_groups:
            self.logger.info(f"Processing group {group.id} with {len(group.chunks)} chunks")
            
            # Wait for memory to be available
            if not self._wait_for_memory():
                self.logger.error("Memory usage too high, stopping processing")
                break
            
            # Process each chunk in the group
            group_results = []
            for chunk in group.chunks:
                result = self._process_chunk_with_retries(chunk, processor_func)
                if result:
                    group_results.append(result)
            
            # Merge results from the group
            if group_results:
                merged_result = self._merge_group_results(group_results, group)
                processed_results.append(merged_result)
            
            # Force cleanup after each group
            gc.collect()
            
            # Cooldown period between groups
            time.sleep(self.chunk_cooldown)
        
        return processed_results

    def _merge_group_results(self, results: List[Dict], group: ChunkGroup) -> Dict:
        """Merge results from chunks in a group"""
        merged = {
            'group_id': group.id,
            'chunk_count': len(group.chunks),
            'total_words': group.total_words,
            'context_quality': group.metadata['context_quality'],
            'results': results,
            'start_position': group.start_position,
            'end_position': group.end_position,
            'processed_at': datetime.now().isoformat()
        }
        return merged

    def _process_chunk_with_retries(self, chunk: TextChunk, processor_func: Callable) -> Optional[Dict]:
        """Process a single chunk with retry logic"""
        for attempt in range(self.max_retries):
            try:
                if not self._check_memory_usage():
                    if not self._wait_for_memory():
                        raise MemoryError(
                            f"Insufficient memory to process chunk {chunk.id}"
                        )
                
                result = processor_func(chunk)
                return result
                
            except Exception as e:
                self.logger.error(
                    f"Error processing chunk {chunk.id} (attempt {attempt + 1}): {str(e)}"
                )
                if attempt < self.max_retries - 1:
                    self.logger.info(f"Retrying chunk {chunk.id}")
                    gc.collect()
                    time.sleep(5)
        return None

    def _check_memory_usage(self) -> bool:
        """Check if memory usage is below threshold"""
        try:
            memory = psutil.virtual_memory()
            return (memory.percent / 100) < self.memory_threshold
        except Exception as e:
            self.logger.error(f"Error checking memory usage: {str(e)}")
            return False

    def _wait_for_memory(self) -> bool:
        """Wait for memory to become available"""
        wait_time = 5
        total_wait = 0
        max_wait = 30
        
        while total_wait < max_wait:
            gc.collect()
            if self._check_memory_usage():
                return True
            
            self.logger.warning(
                f"Memory usage high ({psutil.virtual_memory().percent}%), "
                f"waiting {wait_time}s..."
            )
            
            time.sleep(wait_time)
            total_wait += wait_time
            wait_time = min(wait_time * 1.5, max_wait - total_wait)
        
        return False

    def _get_context(self, text: str, position: int, before: bool = True) -> str:
        """Get preceding or following context around a position"""
        if before:
            text_slice = text[max(0, position - self.context_window * 10):position]
            words = word_tokenize(text_slice)[-self.context_window:]
            return ' '.join(words)
        else:
            text_slice = text[position:position + self.context_window * 10]
            words = word_tokenize(text_slice)[:self.context_window]
            return ' '.join(words)

# Example usage if run directly
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Example processor function
    def example_processor(text: str) -> str:
        return ' '.join(text.split())
    
    # Initialize processor
    processor = ParallelProcessor(
        words_threshold=2000,
        context_window=25,
        max_retries=3,
        memory_threshold=0.8
    )
    
    # Example text processing
    sample_text = "..." # Add sample text here
    results = processor.process_text_parallel(sample_text, example_processor)
    
    # Print results
    print(f"Processed {len(results)} chunks successfully")