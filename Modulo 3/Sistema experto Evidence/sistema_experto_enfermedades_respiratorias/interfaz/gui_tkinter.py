"""
interfaz/gui_tkinter.py
Interfaz gráfica del Sistema Experto usando Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from typing import Dict
from datetime import datetime

# Importar módulos del proyecto
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import COLORES, VENTANA, UMBRALES_CERTEZA, NOMBRE_SISTEMA
from modelos.pacientes import Paciente
from logica.validacion import Validador
from utils.helpers import obtener_nivel_certeza, formatear_porcentaje
from utils.exportar import exportar_a_texto


class SistemaExpertoGUI:
    """
    Clase principal de la interfaz gráfica
    """
    
    def __init__(self, root, base_conocimientos, motor_inferencia):
        """
        Inicializa la interfaz gráfica
        
        Args:
            root: Ventana principal de Tkinter
            base_conocimientos: Instancia de BaseConocimientos
            motor_inferencia: Instancia de MotorInferencia
        """
        self.root = root
        self.bc = base_conocimientos
        self.motor = motor_inferencia
        self.paciente = Paciente()
        
        # Variables de la interfaz
        self.vars = {}
        self.ultimo_diagnostico = None
        
        # Configurar ventana
        self._configurar_ventana()
        
        # Crear interfaz
        self.crear_interfaz()
    
    def _configurar_ventana(self):
        """Configura las propiedades de la ventana principal"""
        self.root.title(VENTANA['titulo'])
        self.root.geometry(f"{VENTANA['ancho']}x{VENTANA['alto']}")
        self.root.configure(bg=COLORES['fondo'])
        
        # Centrar ventana en la pantalla
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (VENTANA['ancho'] // 2)
        y = (self.root.winfo_screenheight() // 2) - (VENTANA['alto'] // 2)
        self.root.geometry(f"{VENTANA['ancho']}x{VENTANA['alto']}+{x}+{y}")
    
    def crear_interfaz(self):
        """Crea todos los componentes de la interfaz"""
        # Crear header
        self._crear_header()
        
        # Crear contenedor principal
        main_container = tk.Frame(self.root, bg=COLORES['fondo'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Crear panel izquierdo (formulario)
        self._crear_panel_izquierdo(main_container)
        
        # Crear panel derecho (resultados)
        self._crear_panel_derecho(main_container)
    
    def _crear_header(self):
        """Crea el encabezado de la aplicación"""
        header = tk.Frame(self.root, bg=COLORES['primario'], height=100)
        header.pack(fill=tk.X)
        
        tk.Label(
            header, 
            text="🫁 " + NOMBRE_SISTEMA, 
            font=('Arial', 20, 'bold'), 
            bg=COLORES['primario'], 
            fg=COLORES['blanco']
        ).pack(pady=10)
        
        tk.Label(
            header, 
            text="Inteligencia Artificial para el diagnóstico de enfermedades respiratorias", 
            font=('Arial', 11), 
            bg=COLORES['primario'], 
            fg=COLORES['blanco']
        ).pack()
    
    def _crear_panel_izquierdo(self, parent):
        """Crea el panel izquierdo con el formulario de entrada"""
        left_panel = tk.Frame(parent, bg=COLORES['blanco'], relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Canvas con scrollbar
        canvas = tk.Canvas(left_panel, bg=COLORES['blanco'])
        scrollbar = ttk.Scrollbar(left_panel, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORES['blanco'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Crear secciones del formulario
        self._crear_seccion_datos_paciente(scrollable_frame)
        self._crear_seccion_sintomas(scrollable_frame)
        self._crear_seccion_hallazgos(scrollable_frame)
        self._crear_seccion_factores_riesgo(scrollable_frame)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones de acción
        self._crear_botones_accion(left_panel)
    
    def _crear_panel_derecho(self, parent):
        """Crea el panel derecho con los resultados"""
        right_panel = tk.Frame(parent, bg=COLORES['blanco'], relief=tk.RAISED, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Título
        tk.Label(
            right_panel, 
            text="📋 Resultados del Diagnóstico", 
            font=('Arial', 16, 'bold'), 
            bg=COLORES['blanco'], 
            fg=COLORES['primario']
        ).pack(pady=10)
        
        # Advertencia
        self._crear_advertencia(right_panel)
        
        # Área de resultados
        self.resultado_text = scrolledtext.ScrolledText(
            right_panel, 
            wrap=tk.WORD, 
            font=('Consolas', 10), 
            bg='#f8f9fa', 
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.resultado_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botón de exportar
        tk.Button(
            right_panel,
            text="💾 Exportar Resultados",
            command=self.exportar_resultados,
            bg=COLORES['secundario'],
            fg=COLORES['blanco'],
            font=('Arial', 11, 'bold'),
            cursor='hand2',
            state=tk.DISABLED
        ).pack(pady=10, padx=10, fill=tk.X)
        
        self.btn_exportar = right_panel.winfo_children()[-1]
    
    def _crear_advertencia(self, parent):
        """Crea el mensaje de advertencia"""
        warning_frame = tk.Frame(parent, bg=COLORES['advertencia'], relief=tk.RAISED, bd=1)
        warning_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            warning_frame, 
            text="⚠️ IMPORTANTE: Este es un sistema de apoyo diagnóstico.\n"
                 "No reemplaza la evaluación de un profesional médico.", 
            font=('Arial', 9), 
            bg=COLORES['advertencia'], 
            fg=COLORES['texto_advertencia'], 
            justify=tk.LEFT
        ).pack(padx=10, pady=5)
    
    def _crear_seccion_datos_paciente(self, parent):
        """Crea la sección de datos del paciente"""
        frame = self._crear_frame_seccion(parent, "👤 Datos del Paciente")
        
        # Edad
        row_edad = tk.Frame(frame, bg=COLORES['blanco'])
        row_edad.pack(fill=tk.X, pady=5)
        tk.Label(row_edad, text="Edad:", bg=COLORES['blanco'], 
                font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        var_edad = tk.StringVar()
        self.vars['edad'] = var_edad
        tk.Entry(row_edad, textvariable=var_edad, width=10, 
                font=('Arial', 10)).pack(side=tk.RIGHT)
        
        # Sexo
        row_sexo = tk.Frame(frame, bg=COLORES['blanco'])
        row_sexo.pack(fill=tk.X, pady=5)
        tk.Label(row_sexo, text="Sexo:", bg=COLORES['blanco'], 
                font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        var_sexo = tk.StringVar()
        self.vars['sexo'] = var_sexo
        ttk.Combobox(row_sexo, textvariable=var_sexo, 
                    values=['Masculino', 'Femenino', 'Otro'], 
                    state='readonly', width=15).pack(side=tk.RIGHT)
    
    def _crear_seccion_sintomas(self, parent):
        """Crea la sección de síntomas principales"""
        frame = self._crear_frame_seccion(parent, "🩺 Síntomas Principales")
        
        sintomas = [
            ('sibilancias', 'Sibilancias'),
            ('tos_nocturna', 'Tos nocturna'),
            ('tos_productiva', 'Tos productiva'),
            ('tos_seca', 'Tos seca'),
            ('disnea', 'Disnea (falta de aire)'),
            ('disnea_ejercicio', 'Disnea con ejercicio'),
            ('fiebre', 'Fiebre (>38.5°C)'),
            ('dolor_toracico', 'Dolor torácico'),
            ('fatiga', 'Fatiga intensa'),
            ('perdida_olfato', 'Pérdida olfato/gusto')
        ]
        
        self._crear_checkboxes(frame, sintomas)
    
    def _crear_seccion_hallazgos(self, parent):
        """Crea la sección de hallazgos físicos"""
        frame = self._crear_frame_seccion(parent, "🔬 Hallazgos Físicos")
        
        hallazgos = [
            ('crepitantes', 'Crepitantes en auscultación'),
            ('ronquidos', 'Ronquidos'),
            ('sat_baja', 'Saturación O₂ < 92%'),
            ('consolidacion', 'Consolidación en Rx')
        ]
        
        self._crear_checkboxes(frame, hallazgos)
    
    def _crear_seccion_factores_riesgo(self, parent):
        """Crea la sección de factores de riesgo"""
        frame = self._crear_frame_seccion(parent, "⚠️ Factores de Riesgo")
        
        factores = [
            ('tabaquismo', 'Historial de tabaquismo'),
            ('alergias', 'Antecedentes de alergias'),
            ('contaminantes', 'Exposición a contaminantes'),
            ('infeccion_previa', 'Infección vías superiores previa'),
            ('sintomas_cronicos', 'Síntomas > 3 meses')
        ]
        
        self._crear_checkboxes(frame, factores)
    
    def _crear_frame_seccion(self, parent, titulo):
        """Crea un frame para una sección del formulario"""
        frame = tk.LabelFrame(
            parent, 
            text=titulo, 
            font=('Arial', 12, 'bold'),
            bg=COLORES['blanco'], 
            fg=COLORES['primario'], 
            padx=10, 
            pady=10
        )
        frame.pack(fill=tk.X, padx=20, pady=10)
        return frame
    
    def _crear_checkboxes(self, parent, items):
        """Crea checkboxes en un frame"""
        for key, text in items:
            var = tk.BooleanVar()
            self.vars[key] = var
            tk.Checkbutton(
                parent, 
                text=text, 
                variable=var, 
                bg=COLORES['blanco'], 
                font=('Arial', 10),
                activebackground=COLORES['blanco']
            ).pack(anchor=tk.W, pady=2)
    
    def _crear_botones_accion(self, parent):
        """Crea los botones de acción"""
        btn_frame = tk.Frame(parent, bg=COLORES['blanco'])
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Botón de diagnóstico
        tk.Button(
            btn_frame, 
            text="🔍 REALIZAR DIAGNÓSTICO", 
            command=self.realizar_diagnostico,
            bg=COLORES['primario'], 
            fg=COLORES['blanco'], 
            font=('Arial', 14, 'bold'),
            relief=tk.RAISED, 
            bd=3, 
            cursor='hand2',
            padx=20, 
            pady=10
        ).pack(fill=tk.X, pady=(0, 5))
        
        # Botón de limpiar
        tk.Button(
            btn_frame, 
            text="🗑️ Limpiar Formulario", 
            command=self.limpiar_formulario,
            bg='#6c757d', 
            fg=COLORES['blanco'], 
            font=('Arial', 11, 'bold'),
            relief=tk.RAISED, 
            bd=2, 
            cursor='hand2',
            padx=10, 
            pady=5
        ).pack(fill=tk.X)
    
    def obtener_datos_paciente(self) -> Dict:
        """Obtiene los datos ingresados del paciente"""
        datos = {}
        
        # Edad
        try:
            datos['edad'] = int(self.vars.get('edad', tk.StringVar()).get() or 0)
        except ValueError:
            datos['edad'] = 0
        
        # Sexo
        datos['sexo'] = self.vars.get('sexo', tk.StringVar()).get()
        
        # Checkboxes
        for key, var in self.vars.items():
            if isinstance(var, tk.BooleanVar):
                datos[key] = var.get()
        
        return datos
    
    def realizar_diagnostico(self):
        """Ejecuta el diagnóstico y muestra resultados"""
        # Obtener datos
        datos = self.obtener_datos_paciente()
        
        # Validar datos
        valido, errores = Validador.validar_paciente(datos)
        if not valido:
            messagebox.showwarning(
                "Datos incompletos", 
                "Por favor corrija los siguientes errores:\n\n" + "\n".join(f"• {e}" for e in errores)
            )
            return
        
        # Cargar datos en el paciente
        self.paciente.from_dict(datos)
        
        # Ejecutar motor de inferencia
        diagnosticos = self.motor.diagnosticar(self.paciente.to_dict())
        
        # Guardar para exportar
        self.ultimo_diagnostico = diagnosticos
        
        # Mostrar resultados
        self.mostrar_resultados(diagnosticos)
        
        # Habilitar botón de exportar
        self.btn_exportar.config(state=tk.NORMAL)
    
    def mostrar_resultados(self, diagnosticos):
        """Muestra los resultados del diagnóstico"""
        self.resultado_text.delete(1.0, tk.END)
        
        if not diagnosticos:
            self.resultado_text.insert(
                tk.END, 
                "\n❌ No se pudo determinar un diagnóstico con los datos proporcionados.\n\n"
                "Por favor, verifique los síntomas ingresados o consulte con un profesional médico."
            )
            return
        
        # Encabezado
        self.resultado_text.insert(tk.END, "=" * 70 + "\n", 'separador')
        self.resultado_text.insert(tk.END, "RESULTADOS DEL DIAGNÓSTICO\n", 'titulo_principal')
        self.resultado_text.insert(tk.END, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n", 'info')
        self.resultado_text.insert(tk.END, "=" * 70 + "\n\n", 'separador')
        
        # Mostrar cada diagnóstico
        for i, d in enumerate(diagnosticos, 1):
            enfermedad_info = self.bc.obtener_enfermedad(d['enfermedad'])
            porcentaje = formatear_porcentaje(d['certeza'])
            nivel, color = obtener_nivel_certeza(porcentaje)
            
            # Encabezado del diagnóstico
            self.resultado_text.insert(tk.END, f"DIAGNÓSTICO #{i}: {enfermedad_info['nombre']}\n", 'titulo')
            self.resultado_text.insert(tk.END, f"Certeza: {porcentaje}% ", 'certeza')
            self.resultado_text.insert(tk.END, f"({nivel})\n", 'nivel')
            self.resultado_text.insert(tk.END, "-" * 70 + "\n\n", 'separador')
            
            # Descripción
            self.resultado_text.insert(tk.END, f"📄 Descripción:\n{enfermedad_info['descripcion']}\n\n")
            
            # Razonamiento
            self.resultado_text.insert(tk.END, "🧠 Razonamiento del Sistema:\n", 'subtitulo')
            for regla in d['reglas']:
                self.resultado_text.insert(tk.END, f"   {regla}\n")
            self.resultado_text.insert(tk.END, "\n")
            
            # Recomendaciones
            self.resultado_text.insert(tk.END, "💊 Recomendaciones Clínicas:\n", 'subtitulo')
            for rec in d['recomendaciones']:
                self.resultado_text.insert(tk.END, f"   {rec}\n")
            self.resultado_text.insert(tk.END, "\n" + "=" * 70 + "\n\n")
        
        # Configurar tags de formato
        self._configurar_tags_texto()
    
    def _configurar_tags_texto(self):
        """Configura los estilos de texto"""
        self.resultado_text.tag_config('titulo_principal', font=('Arial', 14, 'bold'), 
                                      foreground=COLORES['primario'])
        self.resultado_text.tag_config('titulo', font=('Arial', 12, 'bold'), 
                                      foreground=COLORES['primario'])
        self.resultado_text.tag_config('subtitulo', font=('Arial', 11, 'bold'), 
                                      foreground=COLORES['secundario'])
        self.resultado_text.tag_config('certeza', font=('Arial', 11, 'bold'))
        self.resultado_text.tag_config('nivel', font=('Arial', 10))
        self.resultado_text.tag_config('separador', foreground='#cccccc')
        self.resultado_text.tag_config('info', foreground='#6c757d')
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        # Limpiar campos de texto
        for key, var in self.vars.items():
            if isinstance(var, tk.StringVar):
                var.set("")
            elif isinstance(var, tk.BooleanVar):
                var.set(False)
        
        # Limpiar resultados
        self.resultado_text.delete(1.0, tk.END)
        
        # Deshabilitar botón de exportar
        self.btn_exportar.config(state=tk.DISABLED)
        
        # Reiniciar paciente
        self.paciente = Paciente()
        self.ultimo_diagnostico = None
    
    def exportar_resultados(self):
        """Exporta los resultados a un archivo de texto"""
        if not self.ultimo_diagnostico:
            messagebox.showwarning("Sin resultados", "No hay diagnóstico para exportar")
            return
        
        # Abrir diálogo para guardar archivo
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            initialfile=f"diagnostico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if filename:
            try:
                # Generar contenido
                contenido = exportar_a_texto(self.ultimo_diagnostico, self.paciente.to_dict())
                
                # Guardar archivo
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                
                messagebox.showinfo("Éxito", f"Resultados exportados correctamente a:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar el archivo:\n{str(e)}")