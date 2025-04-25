# acceptor.py

class Acceptor:
    
    def __init__(self, patterns, accepted_callback, refused_callback):
        self.prev_states = []
        self.accepted_callback = accepted_callback
        self.refused_callback = refused_callback
        self.authorized_patterns = patterns
        self.max_seq_length = len(patterns[0])
        
    def update(self, new_value):
        self.prev_states.append(new_value)
        if not self.is_accepting():
            self.refused_callback(self.prev_states)
            self.reset()
        else:
            if len(self.prev_states) == self.max_seq_length:
                self.accepted_callback()
                self.reset()

    def reset(self):
        self.prev_states = []
        
    def is_accepting(self):
        current_length = len(self.prev_states)
        for pattern in self.authorized_patterns:
            common_from_pattern = pattern[:current_length]
            if self.prev_states == common_from_pattern:
                return True
        return False

