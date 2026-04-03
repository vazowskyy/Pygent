from functions.get_file_content import get_file_content

def test():

    result = get_file_content("calculator", "lorem.txt")
    print(f"File lenghth: {len(result)}")
    last_line = result.split("\n")[-1]
    print(f"Last line: {last_line}")

    result = get_file_content("calculator", "main.py")
    print(f"\n\nFile main.py")
    print(result)
    
    result = get_file_content("calculator", "pkg/calculator.py")
    print(f"\n\nFile pkg/calculator.py")
    print(result)

    result = get_file_content("calculator", "/bin/cat")
    print(f"\n\nFile /bin/cat")
    print(result)

    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print(f"\n\n\File pkg/does_not_exist.py")
    print(result)



if __name__ == '__main__':
    test() 


