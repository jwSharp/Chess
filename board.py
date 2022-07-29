# Updated board  7/29

import pygame
import math

from config import *
import piece


class Board:
    def __init__(self, window_surface, *pieces: piece.Piece):
        self.window_surface = panel
        self._update_pieces(pieces)
        self._reset_selected()
        self.current_turn = starting_turn
        self.feedback_blocks = {}

    def __str__(self):
        return f"an 8 by 8 board with values of\nsize: {self.window_surface.size}\npieces on board: {[p.piece_name for p in self.pieces]}\ncurrent turn: {self.current_turn}\nselected block: {self.selected_block}\nselected piece: {self.selected_piece}"

    def __repr__(self):
        return f"size: {self.window_surface.size}\npieces on board: {[p.piece_name for p in self.pieces]}\ncurrent turn: {self.current_turn}\nselected block: {self.selected_block}\nselected piece: {self.selected_piece}"

    def set_window_surface(self, window_surface):
        self.window_surface = window_surface

    ### Display ###

    def draw(self):
        start_x = WIDTH / 5
        start_y = 11
        sq_width = 96
        sq_height = 98
        for i in range(1, 9):
            if i % 2 == 1:
                for j in range(0, 4):
                    pygame.draw.rect(self.surface, TAN, ((start_x, start_y), (sq_width, sq_height)))
                    start_x += sq_width
                    pygame.draw.rect(self.surface, BROWN, ((start_x, start_y), (sq_width, sq_height)))
                    start_x += sq_width
            else:
                for j in range(0, 4):
                    pygame.draw.rect(self.surface, BROWN, ((start_x, start_y), (sq_width, sq_height)))
                    start_x += sq_width
                    pygame.draw.rect(self.surface, TAN, ((start_x, start_y), (sq_width, sq_height)))
                    start_x += sq_width
            start_x = 256
            start_y += sq_height

        for piece in self.pieces:
            piece.draw(self, window_surface)

    def draw_pieces(self):  # belongs in piece classes
        """Draws pieces on the board; calculates every piece position by the
        (board_panels block size) * piece position.
        Image gets scaled when the piece is holded."""
        image = None
        holded_image = None
        h_x, h_y = 0, 0
        for piece in self.pieces:
            if piece.pos == None:
                continue
            x, y = piece.pos
            x_pos = x * self.window_surface.width / 8 + (self.window_surface.x + 5)
            y_pos = y * self.window_surface.height / 8 + (self.window_surface.y + 5)
            img_width = self.window_surface.width / 8 - 10
            img_height = self.window_surface.height / 8 - 10
            image = piece.sprite
            image = pygame.transform.smoothscale(image, (img_width, img_height))
            # if piece.turn == self.current_turn:
            #     image = pygame.transform.rotate(image, 180)
            if (
                    self.selected_piece == piece
                    and self.selected_piece.pos != self.selected_piece.current_pos
            ):
                holded_image = image
                holded_image = pygame.transform.smoothscale(
                    holded_image,
                    (holded_image.get_width() * 1.4, holded_image.get_height() * 1.4),
                )
                h_x, h_y = x_pos - 10, y_pos - 10
            else:
                SCREEN.blit(image, (x_pos, y_pos))
        if holded_image != None:
            SCREEN.blit(holded_image, (h_x, h_y))

    def draw_letters(
            self, text_color=BLACK, font_size=18, font_name: pygame.font = "Arial"
    ):
        letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
        block_size = self.window_surface.width / 8
        for i in range(8):
            x_pos_left = self.window_surface.x - block_size / 2
            x_pos_right = self.window_surface.x + self.window_surface.width + block_size / 2
            gap = i * block_size + block_size / 2
            y_pos_bottom = self.window_surface.top - block_size / 2
            y_pos_top = self.window_surface.bottom + block_size / 2

            font = pygame.font.SysFont(font_name, font_size)

            letter_label = font.render(letters[i], False, text_color)
            number_label = font.render(str(8 - i), False, text_color)
            SCREEN.blit(
                letter_label,
                (self.window_surface.x + gap, y_pos_top - font.get_height() / 2),
            )
            SCREEN.blit(
                letter_label,
                (self.window_surface.x + gap, y_pos_bottom - font.get_height() / 2),
            )
            SCREEN.blit(
                number_label,
                (x_pos_left - number_label.get_width() / 2, self.window_surface.y + gap),
            )
            SCREEN.blit(
                number_label,
                (x_pos_right - number_label.get_width() / 2, self.window_surface.y + gap),
            )

    ### Movement ###

    def drag_piece(self, x, y):
        """Changes the position of the held piece to the mouse position until drop_piece runs."""
        block_size = self.window_surface.width / 8
        x = (x - self.window_surface.x) / block_size - 0.5
        y = (y - self.window_surface.y) / block_size - 0.5
        for i in self.pieces:
            if (
                    self.selected_block == i.current_pos
                    and not self.holding_piece
                    and not i.captured
            ):
                self.holding_piece = True
                self.selected_piece = i
                return
        if self.selected_piece is not None:
            self.pieces[self.pieces.index(self.selected_piece)].pos = (x, y)

    def drop_piece(self, x, y):
        """Calculates the grid point of the mouse position, after this method called
        it will snap the piece position to the grid point."""
        # converts x, y to grid position
        block_x, block_y = self._get_grid_position(x, y)
        if self.selected_piece == None:
            return False

        piece_positions = [p.current_pos for p in self.pieces]

        if (
                self.selected_piece.current_pos
                == self.pieces[self.pieces.index(self.selected_piece)].move_piece(
            block_x, block_y, self.current_turn, self.pieces
        )
                and self.selected_block != None
        ):
            self.pieces[self.pieces.index(self.selected_piece)].move_piece(
                self.selected_block[0],
                self.selected_block[1],
                self.current_turn,
                self.pieces,
            )
            return False

        if (block_x, block_y) in self.capturables:
            self.pieces[piece_positions.index((block_x, block_y))].destroy_piece()
            # self.pieces.remove(self.pieces[piece_positions.index((block_x, block_y))])
            self.next_turn()
            self._reset_selected()
            return True

        if (block_x, block_y) != self.selected_block:
            self.next_turn()
            self._reset_selected()
            return True
        self._reset_selected()
        return False

    def select_block(self, x: float, y: float):
        """Selects the block or the piece, if the block is selected it will be highlighted.
    if a piece is already selected the next selected block will be the piece move or piece capture if possible.
    if no movement possible when the piece is selected, it will deselect the piece."""
        piece_positions = [i.current_pos for i in self.pieces]
        if self.drop_piece(x, y) == True:
            return
        x, y = self._get_grid_position(x, y)
        if (x, y) not in self.movable_blocks or (x, y) not in self.capturables:
            self._reset_selected()
        if (x >= 0 and x <= 7) and (y >= 0) and (y <= 7):
            self.selected_block = (x, y)
            if self.selected_block in piece_positions:
                if (
                        self.pieces[piece_positions.index(self.selected_block)].turn
                        == self.current_turn
                ):
                    self.selected_piece = self.pieces[
                        piece_positions.index(self.selected_block)
                    ]
                    self.movable_blocks = self.selected_piece.get_movement(self.pieces)
                    self.capturables = self.selected_piece.get_capturables(self.pieces)
                else:
                    self.draw_feedback(self.selected_block, RED, True)
                    self._reset_selected(True)
        return (x, y)

    def add_sets(self, ref_piece: piece.Piece, positions: (str, str) = ("0|7", "6")):
        piece_positions = [i.current_pos for i in self.pieces]
        pos_x = [
            x
            for x in range(
                min([int(j) for j in positions[0].split("|")]),
                max([int(j) for j in positions[0].split("|")]) + 1,
            )
        ]
        pos_y = [
            y
            for y in range(
                min([int(j) for j in positions[1].split("|")]),
                max([int(j) for j in positions[1].split("|")]) + 1,
            )
        ]
        for l in range(max([len(pos_x), len(pos_y)])):
            x = pos_x[-1] if pos_x.index(pos_x[-1]) < l else pos_x[l]
            y = pos_y[-1] if pos_y.index(pos_y[-1]) < l else pos_y[l]
            if (x, y) not in piece_positions:
                self.pieces.append(
                    piece.Piece(
                        ref_piece.sprite,
                        (x, y),
                        ref_piece.piece_name,
                        ref_piece.turn,
                        ref_piece.piece_moves,
                        ref_piece.different_attacks,
                    )
                )

    def next_turn(self):
        if self.current_turn < max(self.turns):
            self.current_turn += 1
        else:
            self.current_turn = min(self.turns)
        self._update_pieces(self.pieces)
        self.flip_places()

    def flip_places(self):  # not chess accurate, maybe just rotate the board?
        for piece in self.pieces:
            piece.reflect_place()

    def draw_feedback(self, xy: (int, int), color, reset_feedbacks):
        if reset_feedbacks:
            self.feedback_blocks = {xy: color}
        else:
            self.feedback_blocks[xy] = color

    def _reset_selected(self, keep_feedback=False):
        self.selected_piece = None
        self.holding_piece = False
        self.selected_block = None
        self.movable_blocks = []
        self.capturables = []
        if not keep_feedback:
            self.feedback_blocks = {}

    def _update_pieces(self, pieces):  # make sure these lists are updated when capture?
        self.pieces = list(pieces)
        self.piece_images = [p.sprite for p in self.pieces]
        self.captured_pieces = [p for p in self.pieces if p.captured]
        self.turns = [p.turn for p in self.pieces]

    def _get_grid_position(self, x: float, y: float):
        block_size = self.window_surface.width / 8
        x = int((x - self.window_surface.x) / block_size)
        y = int((y - self.window_surface.y) / block_size)
        return x, y

    ### Handle PyGame Events ###

    def handle_events(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click to select a block
                self.select_block(x, y)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # release left click to drop the piece
                self.drop_piece(x, y)
        elif pygame.mouse.get_pressed()[0]:  # if dragging, move the piece
            self.drag_piece(x, y)

        def update(self):
            pass

