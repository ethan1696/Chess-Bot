class Board_constants:
    # Make default starting board states
    def __init__(self):
        self.DEF_B_KN = int("01000010" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000", 2)
        
        self.DEF_B_BI = int("00100100" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000", 2)
        
        self.DEF_B_RO = int("10000001" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000", 2)
        self.DEF_B_PA = int("00000000" \
                        "11111111" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000", 2)
        
        self.DEF_B_QU = int("00001000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000", 2)
        
        self.DEF_B_KI = int("00010000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000", 2)
        
        self.DEF_W_KN = int("00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "01000010", 2)
        
        self.DEF_W_BI = int("00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00100100", 2)
        
        self.DEF_W_RO = int("00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "10000001", 2)
        self.DEF_W_PA = int("00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "11111111" \
                        "00000000", 2)
        
        self.DEF_W_QU = int("00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00001000", 2)
        
        self.DEF_W_KI = int("00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00010000", 2)
        
        self.DEF_ENP = int("00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000" \
                        "00000000", 2)
        
        self.LEFT_N_COL_MASK = [0b0000000000000000000000000000000000000000000000000000000000000000, 
                        0b0000000100000001000000010000000100000001000000010000000100000001, 
                        0b0000001100000011000000110000001100000011000000110000001100000011, 
                        0b0000011100000111000001110000011100000111000001110000011100000111, 
                        0b0000111100001111000011110000111100001111000011110000111100001111, 
                        0b0001111100011111000111110001111100011111000111110001111100011111, 
                        0b0011111100111111001111110011111100111111001111110011111100111111, 
                        0b0111111101111111011111110111111101111111011111110111111101111111, 
                        0b1111111111111111111111111111111111111111111111111111111111111111]
    
    