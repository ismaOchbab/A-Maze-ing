#!/usr/bin/env python3

from typing import Self


class CellDirectionException(Exception):
    pass


class Cell:
    "Represents a single maze cell with walls on 4 sides"
    def __init__(obj: Self,
                 N: int = 1,
                 E: int = 1,
                 S: int = 1,
                 W: int = 1) -> None:
        """
        initializes the cell with all borders set to 1 (closed cell)
        """
        if not all(obj.validate_direction(d)
                   for d in (N, E, S, W)):
            raise CellDirectionException(
                "Invalid direction value (must be 0 or 1)")
        obj.N = N
        obj.E = E
        obj.S = S
        obj.W = W
        obj.protected = False

    @staticmethod
    def validate_direction(direction: int) -> bool:
        return direction in (0, 1)

    def has_wall(obj: Self, direction: str) -> bool:
        return getattr(obj, f"{direction}") == 1

    def remove_wall(obj: Self, direction: str) -> None:
        if direction in ('N', 'E', 'S', 'W'):
            setattr(obj, f"{direction}", 0)
        else:
            raise CellDirectionException(
                f"Invalid direction {direction}")

    def add_wall(obj: Self, direction: str) -> None:
        if direction in ('N', 'E', 'S', 'W'):
            setattr(obj, f"{direction}", 1)
        else:
            raise CellDirectionException(
                f"Invalid direction {direction}")

    def directions(obj: Self) -> dict[str, int]:
        return {
            'N': obj.N,
            'E': obj.E,
            'S': obj.S,
            'W': obj.W
        }

    def set_direction(obj: Self, direction: str, value: int) -> None:
        if not obj.validate_direction(value):
            raise CellDirectionException(
                f"Invalid direction value : {value}"
            )
        if direction in ('N', 'E', 'S', 'W'):
            setattr(obj, f'{direction}', value)
        else:
            raise CellDirectionException(
                f"Invalid direction {direction}"
            )

    def get_hex_value(obj: Self) -> str:
        """ Returns the hex value of the current cell
        Order Ordre: W, S, E, N (bits 3,2,1,0)"""
        bin_str = f"{obj.N}{obj.E}{obj.S}{obj.W}"
        return hex(int(bin_str, 2))[2:].upper()
