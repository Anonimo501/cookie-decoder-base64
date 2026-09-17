#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔐 CIFRADO VISIBLE 🔐
Base64 → (texto hex) → Hex real → Texto plano → Editar → Hex → Base64
"""

import base64
import sys
import os


class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"


def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print(f"""{C.CYAN}{C.BOLD}
╔══════════════════════════════════════════════════════════╗
║                🔐  CIFRADO  VISIBLE  🔐                  ║
║     Base64  →  Hex  →  Texto  →  Editar  →  Base64       ║
╚══════════════════════════════════════════════════════════╝
{C.RESET}""")


def ayuda():
    print(f"""{C.YELLOW}{C.BOLD}📖 AYUDA{C.RESET}

{C.GREEN}¿Qué hace este script?{C.RESET}
  Toma una cadena en Base64 cuyo contenido decodificado es
  una cadena de texto en hexadecimal. La convierte a texto
  plano, te permite editarla y la vuelve a cifrar.

{C.GREEN}Flujo:{C.RESET}
  Base64  ➜  Texto hex  ➜  Bytes  ➜  Texto plano
          ➜  [Editas]  ➜  Texto hex  ➜  Base64

{C.GREEN}Ejemplo:{C.RESET}
  Base64       : NmI2NzY1NGI2NjRmNzg3MjZhNzQ3NDYxNmY2NzYyNjU3Nw==
  Texto hex    : 6b67654b664f78726a7474616f67626577
  Texto plano  : kgeKfOxrjttaogbew

{C.GREEN}Uso:{C.RESET}
  python3 cifrado_visible.py
  python3 cifrado_visible.py <cadena_base64>
""")


def pausa():
    input(f"\n{C.DIM}Presiona ENTER para continuar...{C.RESET}")


def pedir_base64():
    print(f"{C.YELLOW}Ingresa la cadena en Base64 (o escribe 'ayuda'):{C.RESET}")
    entrada = input(f"{C.MAGENTA}➤ {C.RESET}").strip()
    if entrada.lower() in ("ayuda", "help", "-h", "--help"):
        ayuda()
        return None
    return entrada


# ---------- Conversiones ----------

def b64_a_texto_hex(b64_str):
    """Base64 -> string ASCII que contiene el hex."""
    datos = base64.b64decode(b64_str, validate=True)
    return datos.decode("ascii")


def texto_hex_a_texto_plano(texto_hex):
    """'6b67654b...' -> 'kgeKfOxr...'"""
    texto_hex = texto_hex.strip().replace(" ", "").replace("\n", "")
    if len(texto_hex) % 2 != 0:
        raise ValueError("El hex tiene un número impar de caracteres.")
    datos = bytes.fromhex(texto_hex)
    return datos.decode("latin-1")


def texto_plano_a_texto_hex(texto):
    """'kgeKfOxr...' -> '6b67654b...'"""
    return texto.encode("latin-1").hex()


def texto_hex_a_b64(texto_hex):
    """'6b67654b...' -> Base64 final."""
    datos = texto_hex.encode("ascii")  # ¡OJO! los caracteres hex son ASCII
    return base64.b64encode(datos).decode("ascii")


# ---------- Vistas ----------

def mostrar_proceso(b64_original, texto_hex, texto):
    print(f"\n{C.CYAN}{C.BOLD}══════════ PROCESO ══════════{C.RESET}\n")
    print(f"{C.BLUE}[1] Base64 original :{C.RESET}")
    print(f"    {C.WHITE}{b64_original}{C.RESET}\n")

    print(f"{C.BLUE}[2] Hex (decodificado) :{C.RESET}")
    print(f"    {C.WHITE}{texto_hex}{C.RESET}\n")

    print(f"{C.BLUE}[3] Texto plano :{C.RESET}")
    print(f"    {C.GREEN}{C.BOLD}{texto}{C.RESET}\n")


def mostrar_resultado_final(texto_editado, texto_hex_final, b64_final):
    print(f"\n{C.CYAN}{C.BOLD}══════════ RESULTADO FINAL ══════════{C.RESET}\n")
    print(f"{C.BLUE}[1] Texto editado :{C.RESET}")
    print(f"    {C.GREEN}{texto_editado}{C.RESET}\n")

    print(f"{C.BLUE}[2] Hex (sin espacios) :{C.RESET}")
    print(f"    {C.WHITE}{texto_hex_final}{C.RESET}\n")

    print(f"{C.BLUE}[3] Base64 final :{C.RESET}")
    print(f"    {C.MAGENTA}{C.BOLD}{b64_final}{C.RESET}\n")


def editar_texto(texto_original):
    print(f"{C.YELLOW}{C.BOLD}✏️  EDICIÓN DEL TEXTO PLANO{C.RESET}")
    print(f"{C.DIM}Texto actual: {C.GREEN}{texto_original}{C.RESET}")
    print(f"{C.DIM}(Deja vacío para conservar el original){C.RESET}\n")

    nuevo = input(f"{C.MAGENTA}Nuevo texto ➤ {C.RESET}")
    if nuevo == "":
        return texto_original
    return nuevo


# ---------- Lógica principal ----------

def procesar(b64_original):
    try:
        texto_hex = b64_a_texto_hex(b64_original)
    except Exception as e:
        print(f"{C.RED}❌ Error: la cadena Base64 no es válida.{C.RESET}")
        print(f"{C.DIM}Detalle: {e}{C.RESET}")
        return

    try:
        texto = texto_hex_a_texto_plano(texto_hex)
    except Exception as e:
        print(f"{C.RED}❌ Error: el contenido decodificado no es un hex válido.{C.RESET}")
        print(f"{C.DIM}Detalle: {e}{C.RESET}")
        print(f"{C.DIM}Contenido obtenido: {texto_hex}{C.RESET}")
        return

    mostrar_proceso(b64_original, texto_hex, texto)

    texto_editado = editar_texto(texto)

    texto_hex_final = texto_plano_a_texto_hex(texto_editado)
    b64_final = texto_hex_a_b64(texto_hex_final)

    mostrar_resultado_final(texto_editado, texto_hex_final, b64_final)


def main():
    limpiar()
    banner()

    if len(sys.argv) > 1:
        b64 = sys.argv[1].strip()
    else:
        b64 = pedir_base64()
        if b64 is None:
            pausa()
            return

    if not b64:
        print(f"{C.RED}❌ No ingresaste ninguna cadena.{C.RESET}")
        pausa()
        return

    procesar(b64)

    while True:
        print(f"\n{C.DIM}¿Deseas procesar otra cadena? (s/n){C.RESET}")
        op = input(f"{C.MAGENTA}➤ {C.RESET}").strip().lower()
        if op in ("s", "si", "sí", "y", "yes"):
            limpiar()
            banner()
            b64 = pedir_base64()
            if b64 is None:
                pausa()
                return
            if b64:
                procesar(b64)
        else:
            print(f"\n{C.CYAN}👋 ¡Hasta luego!{C.RESET}\n")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{C.YELLOW}⚠️  Interrumpido por el usuario.{C.RESET}\n")
        sys.exit(0)
