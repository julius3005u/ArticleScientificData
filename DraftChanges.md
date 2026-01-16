# Manual de Track Changes en LaTeX

## Uso del paquete `changes` para control de revisiones

Este manual explica cómo usar el paquete `changes` de LaTeX para marcar adiciones, eliminaciones y comentarios durante el proceso de revisión de un artículo científico.

---

## 1. Configuración en el preámbulo

### Cargar el paquete

```latex
% ===== TRACK CHANGES PACKAGE =====
% Use [draft] to show changes with highlighting
% Use [final] to hide all markup for submission
\usepackage[draft]{changes}
\usepackage{xcolor}
```

**Opciones del paquete:**
- `[draft]` → Muestra todos los cambios con colores y marcas visuales
- `[final]` → Oculta todas las marcas para la versión de envío

### Definir autores de cambios

```latex
% Define authors for tracked changes
\definechangesauthor[name={Revision}, color=yellow]{REV}
```

- `name={Revision}` → Nombre que aparecerá en los comentarios
- `color=yellow` → Color de resaltado para este autor
- `{REV}` → Identificador corto del autor

### Comandos personalizados (opcional pero recomendado)

```latex
% Custom commands for easier tracking
\newcommand{\addtext}[1]{\added[id=REV]{#1}}
\newcommand{\deltext}[1]{\deleted[id=REV]{#1}}
\newcommand{\replacetext}[2]{\replaced[id=REV]{#1}{#2}}
\newcommand{\notetext}[1]{\comment[id=REV]{#1}}
\newcommand{\highlighttext}[1]{\highlight[id=REV]{#1}}
```

---

## 2. Comandos básicos

### Añadir texto nuevo

```latex
\addtext{Este texto fue añadido en la revisión.}
```
**Resultado en modo `[draft]`:** El texto aparece resaltado en el color del autor.

### Eliminar texto

```latex
\deltext{Este texto será eliminado.}
```
**Resultado en modo `[draft]`:** El texto aparece tachado.

### Reemplazar texto

```latex
\replacetext{texto nuevo}{texto original}
```
**Resultado en modo `[draft]`:** Muestra el texto original tachado y el nuevo resaltado.

### Añadir comentarios/notas

```latex
\notetext{Esta nota explica por qué se hizo este cambio.}
```
**Resultado en modo `[draft]`:** Aparece como nota al margen o en línea.

### Resaltar texto importante

```latex
\highlighttext{Este texto está resaltado para revisión.}
```

---

## 3. Ejemplos de uso real

### Ejemplo 1: Modificar una oración

**Antes:**
```latex
The analysis of temporal signals is fundamental.
```

**Con track changes:**
```latex
\deltext{The analysis of temporal signals is fundamental.}
\addtext{The analysis and simulation of temporal signals are fundamental 
across science and engineering.}
```

### Ejemplo 2: Añadir contenido nuevo con justificación

```latex
\addtext{CoSiBD comprises 2,500 high-resolution signals (5,000 samples each 
over the domain [0, 4$\pi$]) with corresponding subsampled versions at four 
resolution levels (150, 250, 500, and 1,000 samples).}
\notetext{Addresses reviewer requirement for proper data format documentation.}
```

### Ejemplo 3: Modificar parámetros en una tabla

```latex
\addtext{Amplitude Range} & \addtext{3--16} & \addtext{Range for amplitude envelope values} \\ \hline
\addtext{Vertical Offset} & \addtext{N(0, 3.0)} & \addtext{Normally distributed offset added to signals} \\ \hline
```

---

## 4. Flujo de trabajo recomendado

### Durante la revisión (modo draft)

1. Mantén `\usepackage[draft]{changes}` en el preámbulo
2. Usa `\addtext{}` para todo contenido nuevo
3. Usa `\deltext{}` para texto eliminado
4. Añade `\notetext{}` para explicar cambios importantes a los revisores
5. Compila el PDF → verás todos los cambios marcados

### Para envío final (modo final)

1. Cambia a `\usepackage[final]{changes}`
2. Compila el PDF → todos los cambios se aplican limpiamente:
   - Texto añadido aparece normal
   - Texto eliminado desaparece
   - Comentarios no se muestran

---

## 5. Colores disponibles

Puedes usar cualquier color de `xcolor`:

```latex
\definechangesauthor[name={Author1}, color=blue]{A1}
\definechangesauthor[name={Author2}, color=red]{A2}
\definechangesauthor[name={Author3}, color=green]{A3}
```

Colores comunes: `yellow`, `blue`, `red`, `green`, `orange`, `purple`, `cyan`, `magenta`

---

## 6. Múltiples autores

Para artículos con varios revisores:

```latex
\definechangesauthor[name={Julio}, color=blue]{JIF}
\definechangesauthor[name={Juan}, color=green]{JAL}
\definechangesauthor[name={Dhamar}, color=orange]{DAM}

% Uso
\added[id=JIF]{Texto añadido por Julio}
\deleted[id=JAL]{Texto eliminado por Juan}
\comment[id=DAM]{Comentario de Dhamar}
```

---

## 7. Tips y buenas prácticas

### ✅ Hacer

- Usar `\notetext{}` para explicar POR QUÉ se hizo un cambio
- Agrupar cambios relacionados con una sola nota explicativa
- Mantener versiones separadas: `paper_v09.tex` (draft) y `paper_v09_final.tex` (final)
- Probar la compilación en modo `[final]` antes de enviar

### ❌ Evitar

- No anidar comandos de cambios dentro de otros
- No usar track changes dentro de ecuaciones complejas (puede causar errores)
- No olvidar cambiar a `[final]` antes del envío

---

## 8. Solución de problemas

### Error: "Undefined control sequence"
**Causa:** Falta cargar el paquete o definir el autor  
**Solución:** Verifica que tengas `\usepackage{changes}` y `\definechangesauthor`

### Los cambios no se muestran
**Causa:** Está en modo `[final]`  
**Solución:** Cambia a `\usepackage[draft]{changes}`

### Colores no visibles en PDF
**Causa:** Falta el paquete xcolor  
**Solución:** Añade `\usepackage{xcolor}` después de `\usepackage{changes}`

---

## 9. Referencia rápida

| Acción | Comando |
|--------|---------|
| Añadir texto | `\addtext{nuevo texto}` |
| Eliminar texto | `\deltext{texto a eliminar}` |
| Reemplazar | `\replacetext{nuevo}{original}` |
| Comentario | `\notetext{explicación}` |
| Resaltar | `\highlighttext{texto importante}` |
| Modo borrador | `\usepackage[draft]{changes}` |
| Modo final | `\usepackage[final]{changes}` |

---

## 10. Plantilla completa del preámbulo

```latex
% ===== TRACK CHANGES PACKAGE =====
% Use [draft] to show changes with highlighting
% Use [final] to hide all markup for submission
\usepackage[draft]{changes}
\usepackage{xcolor}

% Define authors for tracked changes
\definechangesauthor[name={Revision}, color=yellow]{REV}

% Custom commands for easier tracking
\newcommand{\addtext}[1]{\added[id=REV]{#1}}
\newcommand{\deltext}[1]{\deleted[id=REV]{#1}}
\newcommand{\replacetext}[2]{\replaced[id=REV]{#1}{#2}}
\newcommand{\notetext}[1]{\comment[id=REV]{#1}}
\newcommand{\highlighttext}[1]{\highlight[id=REV]{#1}}
% ===== END TRACK CHANGES =====
```

---

**Documentación oficial:** [CTAN - changes package](https://ctan.org/pkg/changes)
