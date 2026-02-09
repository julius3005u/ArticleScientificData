# Instrucciones de Compilación - Artículo CoSiBD

## 📋 Archivos Principales

- **main_englishv09.tex** - Versión con marcado de cambios (`\addtext{}`, `\notetext{}`)
- **main_englishv09_final.tex** - Versión limpia para envío final
- **referencias.bib** - Base de datos bibliográfica consolidada (26 referencias)
- **naturemag-doi.bst** - Estilo bibliográfico para Nature Scientific Data

---

## 🔧 Proceso de Compilación Completo

Para generar el PDF con las referencias bibliográficas correctamente formateadas:

### Opción 1: Compilación Manual (Terminal)

```bash
# 1. Primera pasada de LaTeX (genera archivos auxiliares)
pdflatex main_englishv09_final.tex

# 2. Ejecutar BibTeX (procesa referencias.bib)
bibtex main_englishv09_final

# 3. Segunda pasada de LaTeX (incorpora bibliografía)
pdflatex main_englishv09_final.tex

# 4. Tercera pasada de LaTeX (resuelve referencias cruzadas)
pdflatex main_englishv09_final.tex
```

### Opción 2: Script Automatizado

Crear un archivo `compile.sh`:

```bash
#!/bin/bash
FILE="main_englishv09_final"
pdflatex $FILE && bibtex $FILE && pdflatex $FILE && pdflatex $FILE
echo "✅ Compilación completada: ${FILE}.pdf"
```

Ejecutar:
```bash
chmod +x compile.sh
./compile.sh
```

### Opción 3: Usando latexmk (recomendado)

```bash
latexmk -pdf -pdflatex="pdflatex -interaction=nonstopmode" main_englishv09_final.tex
```

---

## 📚 Estructura de Referencias

### Archivo referencias.bib

Contiene 26 referencias bibliográficas organizadas alfabéticamente:

- **Journals**: Nature, IEEE, ACM, Scientific Data, etc.
- **Conferences**: IEEE COINS 2024, ICDM 2017, etc.
- **Books**: Springer (Schumaker, De Boor)
- **Datasets**: VCTK Corpus, EEG grasp-and-lift
- **Preprints**: arXiv (Goodfellow, Zhang, Kuleshov)

### Estilo Bibliográfico

El estilo `naturemag-doi.bst` formatea las referencias según los requisitos de **Nature Scientific Data**:

- Números de citación en orden de aparición
- DOIs incluidos cuando están disponibles
- Formato: Apellido, Iniciales. Título. *Revista* **Volumen**, páginas (año).

---

## ⚠️ Errores Esperados Durante Compilación

### Primera pasada (pdflatex):
```
Warning: Citation 'Karacan2024' undefined
Warning: Reference 'fig:generation_process' undefined
```
**✅ NORMAL** - Se resolverán en pasadas posteriores.

### Después de bibtex:
```
Warning: There were undefined references
```
**✅ NORMAL** - Requiere segunda/tercera pasada de pdflatex.

### Errores REALES a resolver:
```
Cannot find reference `fig:generation_process`
Cannot find reference `LastPage`
```
**⚠️ IMPORTANTE** - Figuras/tablas faltantes que necesitan resolverse.

---

## 🔍 Verificación de Compilación Exitosa

Después de compilar completamente, verificar:

1. **Archivo .bbl generado**:
   ```bash
   ls -lh main_englishv09_final.bbl
   ```
   Debe existir y contener ~26 referencias formateadas.

2. **Sin warnings de referencias**:
   Buscar en el log:
   ```bash
   grep "Citation.*undefined" main_englishv09_final.log
   ```
   No debe mostrar referencias bibliográficas indefinidas.

3. **PDF generado correctamente**:
   ```bash
   ls -lh main_englishv09_final.pdf
   ```
   Tamaño esperado: ~500-800 KB

---

## 📝 Mantenimiento de Referencias

### Agregar nueva referencia:

1. Editar `referencias.bib`:
   ```bibtex
   @article{NuevaRef2025,
     author = {Apellido, Nombre},
     title = {Título del artículo},
     journal = {Nombre de la Revista},
     volume = {10},
     pages = {1--10},
     year = {2025},
     doi = {10.xxxx/xxxx}
   }
   ```

2. Citar en el .tex:
   ```latex
   \cite{NuevaRef2025}
   ```

3. Recompilar:
   ```bash
   pdflatex main_englishv09_final
   bibtex main_englishv09_final
   pdflatex main_englishv09_final
   pdflatex main_englishv09_final
   ```

### Verificar referencias citadas vs definidas:

```bash
# Referencias citadas en el .tex
grep -o '\\cite{[^}]*}' main_englishv09_final.tex | sort -u

# Referencias definidas en el .bib
grep "^@" referencias.bib | grep -o '{[^,]*' | tr -d '{' | sort
```

---

## 🎯 Ventajas de BibTeX vs Bibliografía Manual

| Aspecto | BibTeX (actual) | Manual (anterior) |
|---------|-----------------|-------------------|
| **Tamaño .tex** | 547 líneas | 624 líneas (-12%) |
| **Mantenimiento** | Centralizado | Duplicado por artículo |
| **Formato** | Automático | Manual (propenso a errores) |
| **Reutilización** | Total | Copiar/pegar |
| **Estilo** | Consistente | Inconsistencias posibles |

---

## 🚀 Checklist Pre-Envío

- [ ] Compilar con `latexmk` o secuencia completa pdflatex→bibtex→pdflatex×2
- [ ] Verificar que todas las citas aparecen en la bibliografía
- [ ] Confirmar formato DOI correcto en todas las referencias
- [ ] Revisar que no hay warnings de "undefined citation"
- [ ] Verificar numeración secuencial de referencias [1], [2], ...
- [ ] Comprobar que `main_englishv09_final.pdf` compila sin errores
- [ ] Adjuntar `referencias.bib` junto al .tex al enviar a la revista

---

## 📧 Soporte

Para problemas de compilación:
1. Revisar el archivo `.log` generado
2. Buscar líneas con "Error" o "Fatal"
3. Verificar que `naturemag-doi.bst` está presente
4. Confirmar que `referencias.bib` está en el mismo directorio

**Fecha de creación**: Noviembre 25, 2025  
**Última actualización**: Noviembre 25, 2025
