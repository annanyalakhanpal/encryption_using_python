def create_polybius_square():
    """Creates a 5x5 Polybius square."""
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    square = []
    row = []
    for char in alphabet:
        row.append(char)
        if len(row) == 5:
            square.append(row)
            row = []
    return square

def find_index_in_square(char, square):
    """Finds the row and column index of a character in the Polybius square."""
    for row_index, row in enumerate(square):
        if char in row:
            return row_index + 1, row.index(char) + 1
    return None, None  # Character not found

def polybius_encrypt(plaintext):
    """Encrypts plaintext using the basic Polybius cipher."""
    square = create_polybius_square()
    ciphertext = ""
    for char in plaintext.upper():
        if char.isalpha():
            row, col = find_index_in_square(char, square)
            if row is None:  # Handle characters not in the alphabet 
                continue
            # Ensure two-digit format for row and column
            row_str = str(row) if row >= 0 else '01'
            col_str = str(col) if col >= 0 else '01'
            ciphertext += row_str + col_str
        else:
            ciphertext += char  # Handle non-alphabetic characters
    return ciphertext


def vigenere_encrypt(plaintext, key):
    """Encrypts plaintext using Vigenère cipher with a key."""
    ciphertext = ""
    key_index = 0  # Track the current index in the key
    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index].upper()) - ord('A')
            new_char = chr((ord(char.upper()) + shift - ord('A')) % 26 + ord('A'))
            ciphertext += new_char.lower() if char.islower() else new_char
            key_index = (key_index + 1) % len(key)  # Move to the next key character
        else:
            ciphertext += char
    return ciphertext


def validate_key(key):
    """Checks if the key contains only uppercase letters."""
    for char in key:
        if not char.isalpha() or not char.isupper():
            return False
    return True


def hybrid_encrypt(plaintext, key):
    """Encrypts plaintext using a hybrid of Vigenère and Polybius ciphers."""
    if not validate_key(key):
        raise ValueError("Key must contain only uppercase letters")
    vignere_text = vigenere_encrypt(plaintext, key)
    return polybius_encrypt(vignere_text)


def polybius_decrypt(ciphertext, key):
    """Decrypts Polybius ciphertext using the given key."""
    square = create_polybius_square()
    plaintext = ""
    i = 0
    while i < len(ciphertext):
        row = int(ciphertext[i]) - 1
        col = int(ciphertext[i + 1]) - 1
        char = square[row][col]
        plaintext += char
        i += 2
    return plaintext


def vigenere_decrypt(ciphertext, key):
    """Decrypts Vigenère ciphertext using the given key."""
    plaintext = ""
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index].upper()) - ord('A')
            new_char = chr((ord(char.upper()) - shift - ord('A') + 26) % 26 + ord('A'))
            plaintext += new_char.lower() if char.islower() else new_char
            key_index = (key_index + 1) % len(key)  # Update key index only for alphabetic characters
        else:
            plaintext += char
    return plaintext


def hybrid_decrypt(ciphertext, key):
    """Decrypts ciphertext using a hybrid of Vigenère and Polybius ciphers."""
    polybius_text = polybius_decrypt(ciphertext, key)
    return vigenere_decrypt(polybius_text, key)

def main():
 """
  Prompts the user for encryption or decryption, validates input,
  and calls the appropriate functions.
  """
 while True:
    print("Enter 'E' to encrypt or 'D' to decrypt, or 'Q' to quit:")
    choice = input().upper()

    if choice == 'Q':
      break
    elif choice in ('E', 'D'):
      plaintext = input("Enter your message: ")
      
      if choice == 'E':
        # Get key for encryption 
        key = input("Enter your encryption key (uppercase letters only): ")
        if not validate_key(key):
          print("Invalid key. Key must contain only uppercase letters.")
          continue
        ciphertext = hybrid_encrypt(plaintext, key)
        print("Encrypted ciphertext:", ciphertext)
      else:
        # Get key for decryption  
        key = input("Enter your decryption key (uppercase letters only): ")
        if not validate_key(key):
          print("Invalid key. Key must contain only uppercase letters.")
          continue
        decrypted_text = hybrid_decrypt(plaintext, key)
        print("Decrypted text:", decrypted_text)
    else:
      print("Invalid choice. Please enter 'E', 'D', or 'Q'.")

if __name__ == "__main__":
  main()