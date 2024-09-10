import math
import streamlit as st

class PasswordStrengthChecker:
    def check_strength(self, password):
        # Check length
        if len(password) < 12:
            return "Password should be at least 12 characters long."
        
        # Check for uppercase letters
        if not re.search(r'[A-Z]', password):
            return "Password should include at least one uppercase letter."
        
        # Check for lowercase letters
        if not re.search(r'[a-z]', password):
            return "Password should include at least one lowercase letter."
        
        # Check for numbers
        if not re.search(r'[0-9]', password):
            return "Password should include at least one number."
        
        # Check for symbols
        if not re.search(r'[!@#$%^&*()_+{}\[\]:;"\'<>,.?/\\|`~]', password):
            return "Password should include at least one symbol."
        
        return "Password is strong."

    def generate_password(self, length, use_uppercase, use_lowercase, use_numbers, use_symbols):
        characters = ""
        if use_uppercase:
            characters += string.ascii_uppercase
        if use_lowercase:
            characters += string.ascii_lowercase
        if use_numbers:
            characters += string.digits
        if use_symbols:
            characters += string.punctuation
        
        if not characters:
            return "Please select at least one type of character."
        
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def calculate_cracking_time(self, length, use_uppercase, use_lowercase, use_numbers, use_symbols, guesses_per_second=1e9):
        characters = 0
        if use_uppercase:
            characters += 26
        if use_lowercase:
            characters += 26
        if use_numbers:
            characters += 10
        if use_symbols:
            characters += 32
        
        if characters == 0:
            return "Please select at least one type of character."
        
        entropy = length * math.log2(characters)
        total_combinations = 2 ** entropy
        time_seconds = total_combinations / guesses_per_second
        
        return entropy, time_seconds

    def run(self):
        st.header("check your password ")
        
        # Password strength check
        password = st.text_input("Enter your password", type="password")
        
        if st.button("Check Strength"):
            if password:
                strength_message = self.check_strength(password)
                st.write(strength_message)
            else:
                st.warning("Please enter a password.")
        
        st.subheader("Generate a Strong Password")
        
        # Password generation settings
        length = st.slider("Password Length", min_value=8, max_value=24, value=12)
        use_uppercase = st.checkbox("Include Uppercase Letters", value=True)
        use_lowercase = st.checkbox("Include Lowercase Letters", value=True)
        use_numbers = st.checkbox("Include Numbers", value=True)
        use_symbols = st.checkbox("Include Symbols", value=True)
        
        if st.button("Generate Password"):
            generated_password = self.generate_password(length, use_uppercase, use_lowercase, use_numbers, use_symbols)
            st.write("Generated Password:")
            st.code(generated_password)
            
            # Estimate cracking time
            entropy, time_seconds = self.calculate_cracking_time(length, use_uppercase, use_lowercase, use_numbers, use_symbols)
            if isinstance(time_seconds, str):
                st.write(time_seconds)
            else:
                time_readable = self.seconds_to_readable(time_seconds)
                st.write(f"Estimated Cracking Time: {time_readable}")
                st.write(f"Entropy: {entropy:.2f} bits")
    
    def seconds_to_readable(self, seconds):
        """Convert seconds to a human-readable format."""
        if seconds < 60:
            return f"{seconds:.2f} seconds"
        elif seconds < 3600:
            return f"{seconds / 60:.2f} minutes"
        elif seconds < 86400:
            return f"{seconds / 3600:.2f} hours"
        elif seconds < 31536000:
            return f"{seconds / 86400:.2f} days"
        else:
            return f"{seconds / 31536000:.2f} years"
        


