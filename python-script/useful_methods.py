def calculate_crc_for_bytes_list(byte_list):        
        key = 40961 # 1010 0000 0000 0001    
        result_crc = None
        initial_crc = 65535 #0xFFFF
        for i in range(len(byte_list)):
            result_crc = byte_list[i] ^ initial_crc if result_crc is None else byte_list[i] ^ result_crc

            for j in range(0,8):
                should_XOR_with_key = True if result_crc % 2 == 1 else False
                result_crc = result_crc >> 1

                if should_XOR_with_key:
                    result_crc = result_crc ^ key
        

        crc_significant_byte = result_crc >> 8
        crc_least_byte = result_crc & 0xFF
        return [result_crc,crc_least_byte, crc_significant_byte]