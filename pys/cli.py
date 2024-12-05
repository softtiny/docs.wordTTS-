from numbers_to_words import  modify_long_text
def main():
    import sys
    
    # Check if --convert flag is present
    if "--convert" in sys.argv:
        # Get the last argument as input file path
        input_file = sys.argv[-1]
        
        try:
            # Read the input file
            with open(input_file, 'r') as f:
                content = f.read()
            
            # Modify the content (you can customize this part)
            modified_content =modify_long_text(content) # Example: convert to uppercase
            
            # Create output filename by adding '_converted' before extension
            output_file = input_file.rsplit('.', 1)
            output_file = f"{output_file[0]}_converted.{output_file[1]}"
            
            # Write to new file
            with open(output_file, 'w') as f:
                f.write(modified_content)
                
            print(f"Converted file saved as: {output_file}")
            
        except FileNotFoundError:
            print(f"Error: File '{input_file}' not found")
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print("--convert: with filepath")

main()