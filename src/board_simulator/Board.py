from Board_constants import Board_constants

class Board:

    WHITE = 0
    BLACK = 1
    
    MASK64 = 0xffffffffffffffff

    class Board_Exception(Exception):
        def __init__(self, message):
            super().__init__(message)

    def __init__(self, board_state=None):
        self.bc = Board_constants()
        if(board_state == None):
            self.board_state = {'W_KN': self.bc.DEF_W_KN, 
                                'W_BI': self.bc.DEF_W_BI, 
                                'W_RO': self.bc.DEF_W_RO, 
                                'W_PA': self.bc.DEF_W_PA, 
                                'W_QU': self.bc.DEF_W_QU, 
                                'W_KI': self.bc.DEF_W_KI, 
                                'W_EN': self.bc.DEF_ENP,
                                'W_CA': [True, True],
                                'B_KN': self.bc.DEF_B_KN, 
                                'B_BI': self.bc.DEF_B_BI, 
                                'B_RO': self.bc.DEF_B_RO, 
                                'B_PA': self.bc.DEF_B_PA, 
                                'B_QU': self.bc.DEF_B_QU, 
                                'B_KI': self.bc.DEF_B_KI,
                                'B_EN': self.bc.DEF_ENP,
                                'B_CA': [True, True]}
        else:
            self.board_state = board_state

    def _coord2bitmapID(self, coord):
        """
        Returns the index on the bitmap for a coordinate

        Args:
            coord (int array): coordinates to be converted
        
        Returns:
            int: bitmap_id corresponding to coord
        """
        return coord[0] * 8 + coord[1]
    
    def _bitmapID2coord(self, bitmap_id):
        """
        Returns the coordinate on the bitmap for an index

        Args:
            bitmal_id (int): bitmap index to be converted
        
        Returns:
            int array: Coordinates corresponding to bitmap_id
        """
        return [bitmap_id // 8, bitmap_id % 8]
    
    def _set_bitmap_state(self, bitmap, coord, piece_state):
        """
        Sets the bitmap state at a certain coordinate

        Args:
            bitmap (int): The bitmap to have its state set. 
            coord (int array): coordinates of the piece state to be set
            piece_state (bool): what to change the piece state to

        Returns:
            int: new bitmap with the state at coord set correctly
        """
        if coord[0] < 0 or coord[0] > 7 or coord[1] < 0 or coord[1] > 7:
            return bitmap
        
        bitmap_id = self._coord2bitmapID(coord)
        coord_mask = (1 << bitmap_id) & Board.MASK64

        if piece_state:
            return bitmap | coord_mask
        else:
            return bitmap & (~coord_mask)
    
    def _set_piece_state(self, piece, coord, piece_state):
        """
        Sets the piece state at a certain coordinate

        Args:
            coord (int array): coordinates of the piece state to be set
            piece (string): piece type to have its state changed
            piece_state (bool): what to change the piece state to
        """

        self.board_state[piece] = self._set_bitmap_state(self.board_state[piece], coord, piece_state)
    
    def get_piece_at(self, coord):
        """
        Returns the piece that is at coord

        Args:
            coord (int array): coordinates to search for piece
        
        Returns:
            int: piece that is at coord, or -1 if there is no piece at coord
        """

        bitmap_id = self._coord2bitmapID(coord)

        piece_mask = (1 << bitmap_id) & Board.MASK64

        for key in self.board_state:
            if key == 'W_CA' or key == 'B_CA':
                continue
            if self.board_state[key] & piece_mask:
                return key
        
        return None

    def make_move(self, coord1, coord2, promotion=None):
        """
        Moves piece at coord1 to coord2. If there is a piece at coord2, that piece gets removed (taken)

        Args:
            coord1 (int array): coordinates of source
            coord2 (int array): coordinates of destination
            promotion (string): The type of piece a pawn promotes to (None if no promotion). Dont add the side modifiers, just the piece. The side modifier will be added automatically. For example use 'QU' instead of 'W_QU'
        """

        moved_piece = self.get_piece_at(coord1)
        destination_piece = self.get_piece_at(coord2)
        if (moved_piece == None):
            raise self.Board_Exception("No piece at first coordinate")
        
        #Castling
        if(moved_piece == 'W_KI' or moved_piece == 'B_KI') \
            and (abs(coord1[1] - coord2[1]) > 1):
            if moved_piece == 'W_KI':
                self.board_state['W_CA'] = [False, False]
            else:
                self.board_state['B_CA'] = [False, False]
            
            if(coord2[1] == 2):
                self.make_move([coord1[0], 0], [coord1[0], 3])
            if(coord2[1] == 6):
                self.make_move([coord1[0], 7], [coord1[0], 5])

        #Update castle states
        if(moved_piece == 'W_RO'):
            if(coord1 == [0, 0]):
                self.board_state['W_CA'][0] = False
            if(coord1 == [0, 7]):
                self.board_state['W_CA'][1] = False
            
        if(moved_piece == 'B_RO'):
            if(coord1 == [7, 0]):
                self.board_state['B_CA'][0] = False
            if(coord1 == [7, 7]):
                self.board_state['B_CA'][1] = False

        if (moved_piece == 'W_KI'):
            self.board_state['W_CA'] = [False, False]
        if (moved_piece == 'B_KI'):
            self.board_state['B_CA'] = [False, False]
                

        # en passants
        if (destination_piece == 'B_EN'):
            self._set_piece_state('B_PA', [coord2[0] - 1, coord2[1]], False)
        elif (destination_piece == 'W_EN'):
            self._set_piece_state('W_PA', [coord2[0] + 1, coord2[1]], False)

        if (moved_piece == 'W_PA' and coord1[0] == 1 and coord2[0] == 3):
            self._set_piece_state('W_EN', [coord2[0] - 1, coord2[1]], True)
        elif (moved_piece == 'B_PA' and coord1[0] == 6 and coord2[0] == 4):
            self._set_piece_state('B_EN', [coord2[0] + 1, coord2[1]], True)
        else:
            self.board_state['W_EN'] = 0
            self.board_state['B_EN'] = 0

        self._set_piece_state(moved_piece, coord1, False)
        self._set_piece_state(moved_piece, coord2, True)
        if(destination_piece != None):
            self._set_piece_state(destination_piece, coord2, False)

        # pawn promotion
        if (moved_piece == 'W_PA' and coord2[0] == 7):
            promote_to = 'W_QU' if promotion == None else 'W_' + promotion
            self._set_piece_state(promote_to, coord2, True)
            self._set_piece_state('W_PA', coord2, False)
        if (moved_piece == 'B_PA' and coord2[0] == 0):
            promote_to = 'B_QU' if promotion == None else 'B_' + promotion
            self._set_piece_state(promote_to, coord2, True)
            self._set_piece_state('B_PA', coord2, False)
    
    def in_check(self, victim_side, c_king_coord=None):
        """
        Checks if a side is in check

        Args:
            victim_side (int): side of the side to check whether the king is in check
            king_coord (int list): location of custom king coordinate
        
        Returns:
            bool: True if in check, False otherwise
        """

        side = 'W' if victim_side == Board.WHITE else 'B'
        opside = 'B' if victim_side == Board.WHITE else 'W'

        # find the king coordinates

        king_bitmap = self.board_state[f"{side}_KI"]

        left, right = 0, 63
        while left < right:
            mid = (left + right) // 2
            if king_bitmap >> mid:
                left = mid + 1
            else:
                right = mid
        
        king_coord = self._bitmapID2coord(left - 1)

        if c_king_coord != None:
            king_coord = c_king_coord

        # check for pawn check
        y_offset = 1 if side == 'W' else -1

        pa_mask = self._set_bitmap_state(0, [king_coord[0] + y_offset, king_coord[1] + 1], True)
        pa_mask = self._set_bitmap_state(pa_mask, [king_coord[0] + y_offset, king_coord[1] - 1], True)

        if (self.board_state[f"{opside}_PA"]) & pa_mask:   
            return True

        # check for knight check
        kn_mask = 0
        kn_offset = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]]
        for offset in kn_offset:
            kn_mask = self._set_bitmap_state(kn_mask, [king_coord[0] + offset[0], king_coord[1] + offset[1]], True)

        if (self.board_state[f"{opside}_KN"]) & kn_mask: 
            return True

        # check for king check
        ki_mask = 0
        ki_offset = [[1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [0, 1], [-1, 0], [0, -1]]
        for offset in ki_offset:
            ki_mask = self._set_bitmap_state(ki_mask, [king_coord[0] + offset[0], king_coord[1] + offset[1]], True)

        if (self.board_state[f"{opside}_KI"]) & ki_mask: 
            return True

        # Utility function for checking queens/rooks/bishops
        def check_qrb(offset_y, offset_x, fr, ho):
            working_coord = [king_coord[0] + offset_y, king_coord[1] + offset_x]

            while (working_coord[0] >= 0 and working_coord[0] <= 7 and working_coord[1] >= 0 and working_coord[1] <= 7):
                w_coord_mask = self._set_bitmap_state(0, working_coord, True)
                if(fr & w_coord_mask):
                    return True
                if(ho & w_coord_mask):
                    return False
                working_coord[0] += offset_y
                working_coord[1] += offset_x
            
            return True

        # check for queens/rooks

        friendly = 0
        if side == 'W':
            friendly = self.board_state['W_BI'] \
                | self.board_state['W_RO'] \
                | self.board_state['W_KN'] \
                | self.board_state['W_PA'] \
                | self.board_state['W_QU'] \
                | self.board_state['B_KI'] \
                | self.board_state['B_KN'] \
                | self.board_state['B_PA'] \
                | self.board_state['B_BI']
        else:
            friendly = self.board_state['B_BI'] \
                | self.board_state['B_RO'] \
                | self.board_state['B_KN'] \
                | self.board_state['B_PA'] \
                | self.board_state['B_QU'] \
                | self.board_state['W_KI'] \
                | self.board_state['W_KN'] \
                | self.board_state['W_PA'] \
                | self.board_state['W_BI']
        hostile = 0

        if side == 'W':
            hostile = self.board_state['B_RO'] \
                | self.board_state['B_QU'] 
        else:
            hostile = self.board_state['W_RO'] \
                | self.board_state['W_QU'] 
        
        if ((not check_qrb(0, 1, friendly, hostile)) \
            or (not check_qrb(0, -1, friendly, hostile)) \
            or (not check_qrb(1, 0, friendly, hostile)) \
            or (not check_qrb(-1, 0, friendly, hostile))):
            return True

        #Check for queens/bishops
        friendly = 0
        if side == 'W':
            friendly = self.board_state['W_BI'] \
                | self.board_state['W_RO'] \
                | self.board_state['W_KN'] \
                | self.board_state['W_PA'] \
                | self.board_state['W_QU'] \
                | self.board_state['B_KI'] \
                | self.board_state['B_KN'] \
                | self.board_state['B_PA'] \
                | self.board_state['B_RO']
        else:
            friendly = self.board_state['B_BI'] \
                | self.board_state['B_RO'] \
                | self.board_state['B_KN'] \
                | self.board_state['B_PA'] \
                | self.board_state['B_QU'] \
                | self.board_state['W_KI'] \
                | self.board_state['W_KN'] \
                | self.board_state['W_PA'] \
                | self.board_state['W_RO']
        hostile = 0

        if side == 'W':
            hostile = self.board_state['B_BI'] \
                | self.board_state['B_QU'] 
        else:
            hostile = self.board_state['W_BI'] \
                | self.board_state['W_QU'] 
        

        if ((not check_qrb(1, 1, friendly, hostile)) \
            or (not check_qrb(1, -1, friendly, hostile)) \
            or (not check_qrb(-1, 1, friendly, hostile)) \
            or (not check_qrb(-1, -1, friendly, hostile))):
            return True

        
        return False

    def move_is_legal(self, coord1, coord2, mover_side):
        """
        Checks if certain move is legal given the move and the side. This does not actually make the move

        Args:
            coord1 (int array): coordinates of source
            coord2 (int array): coordinates of destination
            mover_side (int): determine whether move is legal for this side (Board.WHITE or Board.BLACK)

        Returns:
            bool: True if the move is legal and false otherwise
        """
        side = 'W' if mover_side == Board.WHITE else 'B'
        opside = 'B' if mover_side == Board.WHITE else 'W'

        # store old pieces
        old_board_state = self.board_state.copy()

        # make the move
        self.make_move(coord1, coord2)

        if(self.in_check(mover_side)):
            self.board_state = old_board_state
            return False

        self.board_state = old_board_state
        return True

    def can_castle(self, side):
        """
        Checks if a side can castle on each side

        Args:
            side (int): Get whether this side can castle on left/right (Board.WHITE or Board.BLACK)
        
        Returns:
            bool list: in structure [can castle queenside, can castle kingside]
        """
        sides = 'W' if side == Board.WHITE else 'B'
        row = 0 if side == Board.WHITE else 7

        if(self.in_check(side)):
            return [False, False]

        castles = [True, True]
        
        #Queenside
        castles[0] = castles[0] and (self.get_piece_at([row, 1]) == None)
        castles[0] = castles[0] and (self.get_piece_at([row, 2]) == None)
        castles[0] = castles[0] and (self.get_piece_at([row, 3]) == None)
        castles[0] = castles[0] and (not self.in_check(side, [row, 2]))

        #Kingside
        castles[1] = castles[1] and (self.get_piece_at([row, 5]) == None)
        castles[1] = castles[1] and (self.get_piece_at([row, 6]) == None)
        castles[1] = castles[1] and (not self.in_check(side, [row, 6]))

        return castles
    
    def get_all_moves(self, side):
        """
        Returns a list of all possible moves. Each move is stored as [(coord1, coord2), new_Board] where a piece moves from coord1 to coord2 resulting in a Board new_board

        Args:
            side (int): Get all the possible moves for this side (Board.WHITE or Board.BLACK)

        Returns:
            list: List of all possible moves in format [(coord1, coord2), new_Board]
        """
        move_list = []

        def shift_board(bitmap, x_shift, y_shift):
            res = bitmap
            if(y_shift >= 0):
                res = (res << (y_shift * 8)) & self.MASK64
            else:
                res = res >> (-y_shift * 8) & self.MASK64

            if(x_shift >= 0):
                res = (res << x_shift) & self.MASK64
                res = res & (~self.bc.LEFT_N_COL_MASK[x_shift])
            else:
                res = (res >> (-x_shift)) & self.MASK64
                res = res & (self.bc.LEFT_N_COL_MASK[8 + x_shift])
            return res 

        #Finds least significant 1 bit position
        def find_lsb(n):
            if n == 0:
                return None  # No bits are set

            bit_position = 0

            powers_of_2 = [32, 16, 8, 4, 2, 1]
            masks = [0xFFFFFFFF, 0xFFFF, 0xFF, 0xF, 0x3, 0x1]

            for i in range(6):
                if (n & masks[i]) == 0:
                    n >>= powers_of_2[i]
                    bit_position += powers_of_2[i]

            return bit_position

        def move_to_board(coord1, coord2):
            # Make move
            old_board_state = self.board_state.copy()
            self.make_move(coord1, coord2)

            c1 = coord1[:]
            c2 = coord2[:]

            res = [[c1, c2], Board(self.board_state)]

            # Unmake move
            self.board_state = old_board_state
            
            return res

        sides = 'W' if side == Board.WHITE else 'B'
        opsides = 'B' if side == Board.WHITE else 'W'
        piece_maps = {'W' : self.board_state['W_KN'] \
                        | self.board_state['W_BI'] \
                        | self.board_state['W_RO'] \
                        | self.board_state['W_PA'] \
                        | self.board_state['W_KI'] \
                        | self.board_state['W_QU'], 
                    'B' : self.board_state['B_KN'] \
                        | self.board_state['B_BI'] \
                        | self.board_state['B_RO'] \
                        | self.board_state['B_PA'] \
                        | self.board_state['B_KI'] \
                        | self.board_state['B_QU'], 
                    'ALL' : self.board_state['W_KN'] \
                        | self.board_state['W_BI'] \
                        | self.board_state['W_RO'] \
                        | self.board_state['W_PA'] \
                        | self.board_state['W_KI'] \
                        | self.board_state['W_QU'] \
                        | self.board_state['B_KN'] \
                        | self.board_state['B_BI'] \
                        | self.board_state['B_RO'] \
                        | self.board_state['B_PA'] \
                        | self.board_state['B_KI'] \
                        | self.board_state['B_QU']}

        #Pawn moves

        def update_pawns(moved_map, x_offset, y_offset):
            while (moved_map != 0):
                pawn_id = find_lsb(moved_map)
                moved_map = moved_map & (~(1 << pawn_id))
                end_coord = self._bitmapID2coord(pawn_id)
                start_coord = [end_coord[0] - y_offset, end_coord[1] - x_offset]
                if(self.move_is_legal(start_coord, end_coord, side)):
                    move_list.append(move_to_board(start_coord, end_coord))

        #Move forward once
        y_offset1 = 1 if side == Board.WHITE else -1

        pa_moved_map1 = shift_board(self.board_state[f"{sides}_PA"], 0, y_offset1)
        pa_blockers1 = piece_maps['ALL'] & (~self.board_state[f"{sides}_PA"])
        pa_moved_map1 = pa_moved_map1 & (~pa_blockers1)
        update_pawns(pa_moved_map1, 0, y_offset1)

        #Move forward twice
        y_offset2 = 1 if side == Board.WHITE else -1

        pa_moved_map2 = shift_board(self.board_state[f"{sides}_PA"] & (self.bc.DEF_W_PA if side == Board.WHITE else self.bc.DEF_B_PA), 0, y_offset2)
        pa_blockers2 = piece_maps['ALL'] & (~self.board_state[f"{sides}_PA"])
        pa_moved_map2 = pa_moved_map2 & (~pa_blockers2)
        pa_moved_map2 = shift_board(pa_moved_map2, 0, y_offset2) & (~pa_blockers2)

        update_pawns(pa_moved_map2, 0, 2 * y_offset2)

        #Move forward + right
        y_offset3 = 1 if side == Board.WHITE else -1
        x_offset3 = 1

        capturable3 = piece_maps[opsides] & self.board_state[f"{opsides}_EN"]
        pa_moved_map3 = shift_board(self.board_state[f"{sides}_PA"], x_offset3, y_offset3)
        pa_moved_map3 = pa_moved_map3 & capturable3

        update_pawns(pa_moved_map3, x_offset3, y_offset3)

        #Move forward + left
        y_offset4 = 1 if side == Board.WHITE else -1
        x_offset4 = -1

        capturable4 = piece_maps[opsides] & self.board_state[f"{opsides}_EN"]
        pa_moved_map4 = shift_board(self.board_state[f"{sides}_PA"], x_offset4, y_offset4)
        pa_moved_map4 = pa_moved_map4 & capturable4

        update_pawns(pa_moved_map4, x_offset4, y_offset4)

        #Knight Moves

        kn_offsets = [[1, 2], [1, -2], [-1, 2], [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1]]
        kn_blockers = piece_maps[sides]

        knight_map = self.board_state[f"{sides}_KN"]
        while(knight_map != 0):
            kn_id = find_lsb(knight_map)
            kn_coord = self._bitmapID2coord(kn_id)
            knight_map = knight_map & (~(1 << kn_id))
            for offset in kn_offsets:
                end_coord = [kn_coord[0] + offset[0], kn_coord[1] + offset[1]]
                if(end_coord[0] < 0 or end_coord[0] > 7 or end_coord[1] < 0 or end_coord[1] > 7):
                    continue
                end_map = (1 << self._coord2bitmapID(end_coord)) & kn_blockers
                if(end_map == 0 and self.move_is_legal(kn_coord, end_coord, side)):
                    move_list.append(move_to_board(kn_coord, end_coord))
        
        #King moves

        ki_offsets = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]
        ki_coord = self._bitmapID2coord(find_lsb(self.board_state[f"{sides}_KI"]))
        ki_blockers = piece_maps[sides]

        for offset in ki_offsets:
            end_coord = [ki_coord[0] + offset[0], ki_coord[1] + offset[1]]
            if(end_coord[0] < 0 or end_coord[0] > 7 or end_coord[1] < 0 or end_coord[1] > 7):
                continue
            end_map = (1 << self._coord2bitmapID(end_coord)) & ki_blockers
            if(end_map == 0 and self.move_is_legal(ki_coord, end_coord, side)):
                move_list.append(move_to_board(ki_coord, end_coord))

        # Utility function for moving queens/rooks/bishops
        def move_qrb(start_coord, offset_y, offset_x, fr, ho):
            working_coord = [start_coord[0] + offset_y, start_coord[1] + offset_x]

            while (working_coord[0] >= 0 and working_coord[0] <= 7 and working_coord[1] >= 0 and working_coord[1] <= 7):
                w_coord_mask = self._set_bitmap_state(0, working_coord, True)
                if(fr & w_coord_mask):
                    break
                if(self.move_is_legal(start_coord, working_coord, side)):
                    move_list.append(move_to_board(start_coord, working_coord))
                    
                if(ho & w_coord_mask):
                    break
                working_coord[0] += offset_y
                working_coord[1] += offset_x
        
        #Moving bishops
        friendly = piece_maps[sides]
        hostile = piece_maps[opsides]
        bishop_map = self.board_state[f"{sides}_BI"]
        while(bishop_map != 0):
            bi_id = find_lsb(bishop_map)
            bi_coord = self._bitmapID2coord(bi_id)
            bishop_map = bishop_map & (~(1 << bi_id))

            move_qrb(bi_coord, 1, 1, friendly, hostile)
            move_qrb(bi_coord, 1, -1, friendly, hostile)
            move_qrb(bi_coord, -1, 1, friendly, hostile)
            move_qrb(bi_coord, -1, -1, friendly, hostile)

        #Moving rooks
        rook_map = self.board_state[f"{sides}_RO"]

        while(rook_map != 0):
            ro_id = find_lsb(rook_map)
            ro_coord = self._bitmapID2coord(ro_id)
            rook_map = rook_map & (~(1 << ro_id))

            move_qrb(ro_coord, 1, 0, friendly, hostile)
            move_qrb(ro_coord, -1, 0, friendly, hostile)
            move_qrb(ro_coord, 0, 1, friendly, hostile)
            move_qrb(ro_coord, 0, -1, friendly, hostile)

        #Moving queen
        queen_map = self.board_state[f"{sides}_QU"]

        while(queen_map != 0):
            qu_id = find_lsb(queen_map)
            qu_coord = self._bitmapID2coord(qu_id)
            queen_map = queen_map & (~(1 << qu_id))

            move_qrb(qu_coord, 1, 0, friendly, hostile)
            move_qrb(qu_coord, -1, 0, friendly, hostile)
            move_qrb(qu_coord, 0, 1, friendly, hostile)
            move_qrb(qu_coord, 0, -1, friendly, hostile)
            move_qrb(qu_coord, 1, 1, friendly, hostile)
            move_qrb(qu_coord, -1, 1, friendly, hostile)
            move_qrb(qu_coord, 1, -1, friendly, hostile)
            move_qrb(qu_coord, -1, -1, friendly, hostile)

        #Castling
        castles = self.can_castle(side)
        castle_row = 0 if side == Board.WHITE else 7

        if castles[0]:
            start_coord = [castle_row, 4]
            end_coord = [castle_row, 2]
            move_list.append(move_to_board(start_coord, end_coord))
        if castles[1]:
            start_coord = [castle_row, 4]
            end_coord = [castle_row, 6]
            move_list.append(move_to_board(start_coord, end_coord))
        return move_list

    def print_board(self):
        """
        Prints the board state
        """
        piece_names = {'W_PA' : 'P', 'W_KN' : 'N', 'W_BI' : 'B', 'W_RO' : 'R', 'W_QU' : 'Q', 'W_KI' : 'K', 
                       'B_PA': 'p', 'B_KN': 'n', 'B_BI': 'b', 'B_RO': 'r', 'B_QU': 'q', 'B_KI': 'k'}
        
        buffer = ""
        for i in range(0, 8):
            for j in range(0, 8):
                piece = self.get_piece_at([7 - i, j])
                if(piece == None or piece == 'W_EN' or piece == 'B_EN'):
                    buffer += " "
                else: 
                    buffer += piece_names[piece]
            buffer +='\n'
        
        print(buffer)

    def print_bitmap(self, bitmap):
        """
        Prints a bitmap in an 8x8 board

        Args:
            bitmap (int): The bitmap to be printed
        """
        buffer = ""
        for i in range(0, 8):
            for j in range(0, 8):
                cur_bit = (bitmap >> ((7 - i) * 8 + j)) & 1
                buffer += str(cur_bit)
            buffer += '\n'
        print(buffer)
