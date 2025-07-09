import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import lzma
import shutil

def escolher_xz():
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos .xz", "*.xz")])
    entrada_xz.delete(0, tk.END)
    entrada_xz.insert(0, caminho)

def extrair_xz(caminho_xz):
    if not caminho_xz.endswith(".xz"):
        raise ValueError("Arquivo não é .xz")
    
    caminho_img = caminho_xz.replace(".xz", ".img")
    with lzma.open(caminho_xz, "rb") as xz_f:
        with open(caminho_img, "wb") as img_f:
            shutil.copyfileobj(xz_f, img_f)
    return caminho_img

def flashar():
    caminho_xz = entrada_xz.get()
    if not caminho_xz or not os.path.isfile(caminho_xz):
        messagebox.showerror("Erro", "Selecione um arquivo .xz válido.")
        return

    try:
        log_saida.delete("1.0", tk.END)
        log_saida.insert(tk.END, f"Extraindo: {caminho_xz}\n")
        caminho_img = extrair_xz(caminho_xz)
        log_saida.insert(tk.END, f"Imagem extraída: {caminho_img}\n")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao extrair .xz:\n{str(e)}")
        return

    comandos = [
        ["fastboot", "devices"],
        ["fastboot", "flash", "system", caminho_img]
    ]

    for cmd in comandos:
        try:
            log_saida.insert(tk.END, f"> {' '.join(cmd)}\n")
            resultado = subprocess.run(cmd, capture_output=True, text=True)
            log_saida.insert(tk.END, resultado.stdout + "\n")
            if resultado.stderr:
                log_saida.insert(tk.END, resultado.stderr + "\n")
        except Exception as e:
            log_saida.insert(tk.END, f"Erro ao executar {' '.join(cmd)}:\n{str(e)}\n")

    messagebox.showinfo("Concluído", "Flash finalizado!")

def deletar_product():
    particao = "product_a" if var_ab.get() else "product"
    cmd = ["fastboot", "delete-logical-partition", particao]
    try:
        log_saida.insert(tk.END, f"> {' '.join(cmd)}\n")
        resultado = subprocess.run(cmd, capture_output=True, text=True)
        log_saida.insert(tk.END, resultado.stdout + "\n")
        if resultado.stderr:
            log_saida.insert(tk.END, resultado.stderr + "\n")
        messagebox.showinfo("Feito", f"Partição '{particao}' apagada.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao apagar partição:\n{str(e)}")

# GUI
janela = tk.Tk()
janela.title("GSI Flasher com Delete Product (A/B opcional)")
janela.geometry("650x500")

# Seletor de arquivo
tk.Label(janela, text="Selecionar GSI Compactado (.xz):").pack(pady=5)
entrada_xz = tk.Entry(janela, width=70)
entrada_xz.pack()
tk.Button(janela, text="Procurar", command=escolher_xz).pack(pady=5)

# Checkbox A/B
var_ab = tk.BooleanVar()
check_ab = tk.Checkbutton(janela, text="A/B Ativo (apagar product_a)", variable=var_ab)
check_ab.pack(pady=5)

# Botão de flash
tk.Button(janela, text="🔁 Flashar GSI (em 'system')", bg="green", fg="white", command=flashar).pack(pady=10)

# Botão para deletar product/product_a
tk.Button(janela, text="❌ Apagar Partição Product", bg="red", fg="white", command=deletar_product).pack(pady=5)

# Log de saída
log_saida = tk.Text(janela, height=15, width=80)
log_saida.pack(pady=10)

janela.mainloop()
