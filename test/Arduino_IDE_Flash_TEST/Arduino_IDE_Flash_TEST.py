import serial
import time
import sys

# STK500v1 Protocol Constants
STK_OK              = b'\x10'
STK_INSYNC          = b'\x14'
CRC_EOP             = b'\x20'
STK_GET_SYNC        = b'\x30'
STK_GET_PARAMETER   = b'\x41'
STK_SET_DEVICE      = b'\x42'
STK_SET_DEVICE_EXT  = b'\x45'
STK_ENTER_PROGMODE  = b'\x50'
STK_LEAVE_PROGMODE  = b'\x51'
STK_LOAD_ADDRESS    = b'\x55'
STK_UNIVERSAL       = b'\x56'
STK_PROG_PAGE       = b'\x64'
STK_READ_PAGE       = b'\x74'  
STK_READ_SIGN       = b'\x75'

SIG_ATMEGA328P = b'\x1E\x95\x0F'
PORT = '/dev/ttyV1'
BAUD = 115200 

def wait_for_eop(ser):
    while True:
        if ser.read(1) == CRC_EOP:
            break

def Emulate_bootloader():
    print(f"Starting STK500 Bootloader Emulator on {PORT}...")
    
    # Create 32KB of virtual Flash Memory (initially all 0xFF, like a real wiped MCU)
    virtual_flash = bytearray([0xFF] * 32768)
    current_address = 0
    
    try:
        ser = serial.Serial(PORT, BAUD, timeout=None)
    except Exception as e:
        print(f"Error opening port: {e}")
        sys.exit(1)

    try:
        while True:
            cmd = ser.read(1)
            
            if cmd == STK_GET_SYNC:
                wait_for_eop(ser)
                ser.write(STK_INSYNC + STK_OK)
                
            elif cmd == STK_GET_PARAMETER:
                param = ser.read(1)
                wait_for_eop(ser)
                ser.write(STK_INSYNC + b'\x03' + STK_OK)

            elif cmd == STK_SET_DEVICE:
                ser.read(20)
                wait_for_eop(ser)
                ser.write(STK_INSYNC + STK_OK)

            elif cmd == STK_SET_DEVICE_EXT:
                ser.read(5)
                wait_for_eop(ser)
                ser.write(STK_INSYNC + STK_OK)
                
            elif cmd == STK_UNIVERSAL:
                ser.read(4)
                wait_for_eop(ser)
                ser.write(STK_INSYNC + STK_OK)
                
            elif cmd == STK_ENTER_PROGMODE:
                wait_for_eop(ser)
                print("\n[+] Entering Programming Mode...")
                ser.write(STK_INSYNC + STK_OK)
                
            elif cmd == STK_READ_SIGN:
                wait_for_eop(ser)
                ser.write(STK_INSYNC + SIG_ATMEGA328P + STK_OK)
                
            elif cmd == STK_LOAD_ADDRESS:
                addr_low = ser.read(1)
                addr_high = ser.read(1)
                wait_for_eop(ser)
                
                # STK500 sends Word addresses. Multiply by 2 to get Byte addresses.
                word_address = (int.from_bytes(addr_high, 'big') << 8) | int.from_bytes(addr_low, 'big')
                current_address = word_address * 2
                ser.write(STK_INSYNC + STK_OK)
                
            elif cmd == STK_PROG_PAGE:
                length_high = ser.read(1)
                length_low = ser.read(1)
                mem_type = ser.read(1)
                
                page_size = (int.from_bytes(length_high, 'big') << 8) | int.from_bytes(length_low, 'big')
                payload = ser.read(page_size)
                wait_for_eop(ser)
                
                # Save the code into our virtual memory!
                virtual_flash[current_address : current_address + page_size] = payload
                print(f" -> Wrote {page_size} bytes to 0x{current_address:04X}")
                
                ser.write(STK_INSYNC + STK_OK)

            elif cmd == STK_READ_PAGE:
                length_high = ser.read(1)
                length_low = ser.read(1)
                mem_type = ser.read(1)
                
                page_size = (int.from_bytes(length_high, 'big') << 8) | int.from_bytes(length_low, 'big')
                wait_for_eop(ser)
                
                # Read the code from our virtual memory to prove to avrdude we saved it
                data = virtual_flash[current_address : current_address + page_size]
                print(f" <- Verified {page_size} bytes at 0x{current_address:04X}")
                
                ser.write(STK_INSYNC + data + STK_OK)
                
            elif cmd == STK_LEAVE_PROGMODE:
                            wait_for_eop(ser)
                            print("[+] Upload and Verify Complete! Virtual MCU has the code.")
                            
                            # --- NEW: Dump the virtual flash memory to a binary file ---
                            dump_filename = "arduino_flash_dump.bin"
                            
                            # Optional: We can trim the empty 0xFF bytes at the end to make the file smaller.
                            # Find the last byte that isn't 0xFF (empty memory)
                            last_used_byte = 32767
                            while last_used_byte >= 0 and virtual_flash[last_used_byte] == 0xFF:
                                last_used_byte -= 1
                            
                            # Write only the used portion of the memory (plus a little padding) to the file
                            with open(dump_filename, "wb") as f:
                                f.write(virtual_flash[:last_used_byte + 1])
                            
                            print(f"[+] Memory successfully dumped to {dump_filename} ({last_used_byte + 1} bytes).")
                            # -----------------------------------------------------------
                            
                            ser.write(STK_INSYNC + STK_OK)
                
            elif cmd != b'':
                print(f"[!] Warning: Received unknown command: {cmd.hex()}")

    except KeyboardInterrupt:
        print("\nEmulator stopped.")
    finally:
        ser.close()