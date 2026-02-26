def remove_ml_from_file_simple(filename):
    with open(filename, 'r') as file:
        content = file.read()
    
    modified_content = content.replace(',ml;', ';')
    
    with open(filename, 'w') as file:
        file.write(modified_content)

    print(f"Finished processing the file: {filename}")

file_to_process = 'AI-FOR-HEALTH\Data\AP01\Flow - 30-05-2024.txt'
remove_ml_from_file_simple(file_to_process)
