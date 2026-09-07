"""Intégration Baserow <-> Claude Code — YEBA FORMATIONS.

Bibliothèque cliente souveraine (données hébergées UE) pour piloter Baserow
depuis Claude Code : création de bases, tables, champs et lignes.
"""

from .client import BaserowClient, BaserowError

__all__ = ["BaserowClient", "BaserowError"]
