# Generování herního světa

Aplikace využívá algoritmus Wave Function Collapse (WFC), který se používá především pro proceduralní generování obsahu. Jeho cílem je vytvořit náhodný, ale strukturovaný výstup na základě definovaných pravidel.

## Princip
1. Algoritmus pracuje s polem (ale tváříme se, že to je matice (grid)) reprezentující herní svět. Každý prvek matice může nabývat různých hodnot nebo stavů.
2. Začínáme s inicializaci gridu obsahující všechny možné hodnoty pro každý prvek (například různé typy terénu).
3. Algoritmus postupně "kolabuje" možné stavy prvků na základě definovaných pravidel.
4. Postupně opakujeme 3. krok, dokud není celá matice "kolabována" a není dosaženo konečného stavu.

## Instalace potřebných balíčků

Aplikace využívá balíček Pillow pro práci s obrázky

```bash
pip install Pillow
```

## Spuštění aplikace

```python
python wfc.py
```