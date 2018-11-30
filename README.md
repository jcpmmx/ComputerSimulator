# ComputerSimulator
> Originally developed as a take-home test project for Deviget.

### System requirements
- Python
- SQLite

### Built and tested with
- Python (v2.7)
- Django (v1.11)
- Django REST Framework (v3.7.1)
- SQLite

---

### About this solution

This simulator supports executing the following code:  
```
def print_tenten
  print(multiply(101, 10))
end
print(1009)
print_tenten()
```
whose output would be:  
```
1009 
1010
```

It supports these instructions:
- `MULT`: Pop the 2 arguments from the stack, multiply them and push the result back to the stack 
- `CALL addr`: Set the program counter (PC) to `addr`
- `RET`: Pop address from stack and set PC to address
- `STOP`: Exit the program 
- `PRINT`: Pop value from stack and print it 
- `PUSH arg`: Push argument to the stack 

The code should execute against: 

```ruby
PRINT_TENTEN_BEGIN = 50
MAIN_BEGIN = 0
def main
  # Create new computer with a stack of 100 addresses
  computer = Computer.new(100)
  # Instructions for the print_tenten function
  computer.set_address(PRINT_TENTEN_BEGIN).insert("MULT").insert("PRINT").insert("RET")
  # The start of the main function
  computer.set_address(MAIN_BEGIN).insert("PUSH", 1009).insert("PRINT")
  # Return address for when print_tenten function finishes
  computer.insert("PUSH", 6)
  # Setup arguments and call print_tenten
  computer.insert("PUSH", 101).insert("PUSH", 10).insert("CALL", PRINT_TENTEN_BEGIN)
  # Stop the program
  computer.insert("STOP")
  # Execute the program
  computer.set_address(MAIN_BEGIN).execute()
end
main() 
```

It also has support via API:
```bash
# Create new computer with a stack of 100 addresses
curl -XPOST -d'{"stack":100}' you-app-server/v1/computers
# Instructions for the print_tenten function
curl -XPATCH -d'{"addr: 50"}' you-app-server/v1/computers/{computer-id}/stack/pointer
curl -XPOST you-app-server/v1/computers/{computer-id}/stack/insert/MULT
curl -XPOST you-app-server/v1/computers/{computer-id}/stack/insert/PRINT
curl -XPOST you-app-server/v1/computers/{computer-id}/stack/insert/RET
# The start of the main function
curl -XPATCH -d'{"addr: 0"}' you-app-server/v1/computers/{computer-id}/stack/pointer
curl -XPOST -d'{"arg":1009}' you-app-server/v1/computers/{computer-id}/stack/insert/PUSH
curl -XPOST you-app-server/v1/computers/{computer-id}/stack/insert/PRINT
# Return address for when print_tenten function finishes
curl -XPOST -d'{"arg":6}' you-app-server/v1/computers/{computer-id}/stack/insert/PUSH
# Setup arguments and call print_tenten
curl -XPOST -d'{"arg":101}' you-app-server/v1/computers/{computer-id}/stack/insert/PUSH
curl -XPOST -d'{"arg":10}' you-app-server/v1/computers/{computer-id}/stack/insert/PUSH
curl -XPOST -d'{"addr":50}' you-app-server/v1/computers/{computer-id}/stack/insert/CALL
# Stop the program
curl -XPOST you-app-server/v1/computers/{computer-id}/stack/insert/STOP
# Execute the program
curl -XPATCH -d'{"addr":0}' you-app-server/v1/computers/{computer-id}/stack/pointer
curl -XPOST you-app-server/v1/computers/{computer-id}/exec
```

### Nice to haves
- Test cases, of course
