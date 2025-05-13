import hashlib
import math # Needed for ceiling division

class MD5:
    def __init__(self, book_id):
        self.book_id = book_id

    def md5_hex(self, data_string):
        """Computes MD5 hash and returns hex string."""
        m = hashlib.md5()
        # Ensure data is encoded to bytes, utf-8 is common
        m.update(data_string.encode('utf-8')) 
        return m.hexdigest()

    def encode16(self, t):
        """
        Replicates the JavaScript encode16 function logic.

        Args:
            t: The input string (typically the bookId as a string).

        Returns:
            A list containing two elements:
            - A string ('3' or '4') indicating the encoding type.
            - A list of strings representing the encoded parts.
        """
        if isinstance(t, int): # Ensure input is string
            t = str(t)
        elif not isinstance(t, str):
            # Handle non-string/non-int cases if necessary, 
            # though the original JS might just proceed/fail.
            # For simplicity, assuming string input based on encrypt$1 logic.
            pass 

        # Check if the string contains only digits
        if t.isdigit(): 
            # JavaScript: /^\d*$/.test(t)
            n = len(t)
            o = 9 # Chunk size
            i = [] # List to hold hex strings
            
            # Iterate through the string in chunks of size o (9)
            # JavaScript: for (var a = 0; a < n; a += o)
            for a in range(0, n, o):
                # var c = t.slice(a, Math.min(a + o, n));
                c_chunk = t[a:min(a + o, n)] 
                # i.push(parseInt(c).toString(16))
                try:
                    # Convert chunk to integer, then to hex string
                    hex_val = format(int(c_chunk), 'x') 
                    i.append(hex_val)
                except ValueError:
                    # Handle cases where chunk might be empty or invalid, though unlikely with isdigit check
                    print(f"Warning: Could not convert chunk '{c_chunk}' to int.")
                    i.append("") # Append empty string or handle error as appropriate
                    
            return ["3", i] # Returns ["3", [hex_chunk1, hex_chunk2, ...]]
        else:
            # Handle cases where the string contains non-digit characters
            e = "" # String to concatenate hex codes
            # JavaScript: for (var r = 0; r < t.length; r++)
            for char in t:
                # var s = t.charCodeAt(r).toString(16);
                # Get character code (Unicode code point) and convert to hex
                s_hex_code = format(ord(char), 'x') 
                e += s_hex_code # e = e + s
                
            # Returns ["4", [single_concatenated_hex_string]]
            return ["4", [e]] 


    def encrypt_book_id_for_url(self):
        """
        Replicates the JavaScript encrypt$1 function using the implemented encode16.
        """
        book_id = self.book_id

        if isinstance(book_id, int):
            book_id_str = str(book_id)
        elif isinstance(book_id, str):
            book_id_str = book_id
        else:
            # Handle non-string/non-int cases
            print(f"Warning: Input book_id '{book_id}' is not a string or int.")
            return None # Or raise an error

        # --- Start of encrypt$1 logic ---
        n = self.md5_hex(book_id_str) # var n = md5(t);
        
        o = n[:3] # var o = n.substr(0, 3);
        
        # var i = encode16(t);
        try:
            i = self.encode16(book_id_str) 
            if i is None or not isinstance(i, list) or len(i) != 2:
                raise ValueError("encode16 did not return expected format.")
            char_part_i0 = i[0] # Should be "3" or "4"
            string_array_part_i1 = i[1] # Should be a list of strings
            if not isinstance(string_array_part_i1, list):
                raise ValueError("Second element from encode16 is not a list.")

        except NotImplementedError:
            print("Cannot proceed: encode16 function is not implemented (should not happen here).")
            return None
        except ValueError as ve:
            print(f"Error processing encode16 result: {ve}")
            return None
        except Exception as e: # Catch other potential errors from encode16
            print(f"An unexpected error occurred during encode16: {e}")
            return None

        o += char_part_i0 # o += i[0];
        
        a = 2 
        # o += a + n.substr(n.length - a, a); 
        o += str(a) + n[-a:] # Use string slicing and str conversion

        # for (var c = i[1], e = 0; e < c.length; e++) { ... }
        c_list = string_array_part_i1 
        for e_idx, c_item_str in enumerate(c_list):
            # var r = c[e].length.toString(16);
            try:
                # Ensure c_item_str is a string before getting length
                if not isinstance(c_item_str, str):
                    raise TypeError(f"Item in encode16 result list is not a string: {c_item_str}")
                r_hex_len = format(len(c_item_str), 'x') 
            except TypeError as te:
                print(f"Error processing item from encode16 list: {te}")
                # Decide how to handle this error, e.g., skip item or return None
                continue # Skipping item for now

            # r.length === 1 && (r = "0" + r);
            if len(r_hex_len) == 1:
                r_hex_len = "0" + r_hex_len
            
            o += r_hex_len # o += r;
            o += c_item_str # o += c[e];
            
            # e < c.length - 1 && (o += "g")
            if e_idx < len(c_list) - 1:
                o += "g"
                
        s_target_len = 20
        # o.length < s && (o += n.substr(0, s - o.length))
        if len(o) < s_target_len:
            # Ensure we don't try to slice more than available in n
            needed = s_target_len - len(o)
            o += n[:needed] 
            
        # o += md5(o).substr(0, 3);
        o += self.md5_hex(o)[:3]
        
        return o

if __name__ == "__main__":
    book_id = 998091
    md5 = MD5(book_id=book_id)
    encrypt_id = md5.encrypt_book_id_for_url()
    print(encrypt_id)