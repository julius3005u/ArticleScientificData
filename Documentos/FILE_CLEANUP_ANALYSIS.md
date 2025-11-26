# Análisis de Archivos para Limpieza
**Fecha**: 19 de Noviembre de 2025

## ✅ ARCHIVOS CRÍTICOS - NO BORRAR

### Manuscrito Principal
- ✅ **main_englishv09.tex** - Versión actual con track changes
- ✅ **main_englishv09.pdf** - PDF compilado con cambios resaltados
- ✅ **main_englishv08.tex** - Versión original previa (backup de referencia)
- ✅ **main_englishv08.pdf** - PDF de versión previa

### LaTeX Support Files (Necesarios)
- ✅ **wlscirep.cls** - Plantilla de Scientific Reports
- ✅ **naturemag-doi.bst** - Estilo bibliográfico
- ✅ **jabbrv.sty, jabbrv-ltwa-all.ldf, jabbrv-ltwa-en.ldf** - Abreviaciones de revistas
- ✅ **sample.bib** - Referencias bibliográficas

### Documentación de Revisión
- ✅ **FirstArticleRevision.md** - Requerimientos de revisores (CRÍTICO)
- ✅ **ReviewAnalysis.md** - Análisis detallado de comentarios
- ✅ **REVISION_SUMMARY.md** - Resumen de cambios realizados
- ✅ **TRACK_CHANGES_GUIDE.md** - Guía del sistema de track changes
- ✅ **ArticleUpdat1119.md** - Resumen de conversación actual

### Dataset y Código
- ✅ **SignalBuilderC/** - Biblioteca ACTIVA de generación (2,500 señales)
- ✅ **generate_dataset.py** - Script de generación del dataset
- ✅ **SignalBuilderV02/** - Biblioteca de referencia original
- ✅ **SignalBuilderV02_Architecture.md** - Documentación de arquitectura

### Visualizaciones
- ✅ **graphs/** - Gráficas incluidas en el paper
- ✅ **diagrams/** - Diagramas del proceso

---

## 🟡 ARCHIVOS TEMPORALES DE LaTeX - PUEDEN BORRARSE

### Archivos Auxiliares de Compilación
Estos se regeneran automáticamente al compilar:

- 🟡 **main_englishv09.aux** - Referencias cruzadas
- 🟡 **main_englishv09.log** - Log de compilación
- 🟡 **main_englishv09.fls** - Lista de archivos usados
- 🟡 **main_englishv09.fdb_latexmk** - Database de latexmk
- 🟡 **main_englishv09.out** - Marcadores de PDF
- 🟡 **main_englishv09.synctex.gz** - Sincronización editor-PDF (si existe)
- 🟡 **main_englishv09.bbl** - Bibliografía procesada
- 🟡 **main_englishv09.loc** - Lista de cambios
- 🟡 **main_englishv09.soc** - Cambios ordenados

### Archivos de Versión Previa (v08)
- 🟡 **main_englishv08.aux**
- 🟡 **main_englishv08.log**
- 🟡 **main_englishv08.fls**
- 🟡 **main_englishv08.fdb_latexmk**
- 🟡 **main_englishv08.out**
- 🟡 **main_englishv08.synctex.gz** (si existe)

### Archivos de main.tex (Muy Antiguos)
- 🟡 **main.aux** - De versión antigua sin usar

---

## 🔴 ARCHIVOS OBSOLETOS O REDUNDANTES - REVISAR ANTES DE BORRAR

### Versiones Antiguas del Manuscrito
- 🔴 **main_original.tex** - Versión muy antigua, probablemente obsoleta
  - **Acción recomendada**: Revisar si tiene algo único, sino borrar

### Archivos de Ejemplo/Demo
- 🔴 **example_file.txt** - Archivo de ejemplo/prueba
- 🔴 **example_notebook.ipynb** - Notebook de ejemplo
  - **Acción recomendada**: Borrar si no contienen trabajo importante

### Notebooks de Demo
- 🔴 **SignalBuilderC_demo.ipynb** - Demo de SignalBuilderC
- 🔴 **SignalBuilderV02_demo.ipynb** - Demo de V02
  - **Acción recomendada**: CONSERVAR si tienen ejemplos útiles de uso

### Biblioteca Antigua
- 🔴 **SignalBuilder/** - Primera versión, reemplazada por V02 y luego C
  - **Contenido**: .git/, LICENSE, README.md, notebooks/, results/, utils/
  - **Acción recomendada**: REVISAR si tiene código único, considerar archivar

### Proyecto time-series-srnet
- 🔴 **time-series-srnet/** - Repositorio de modelo de deep learning
  - **Contenido**: .git/, pyproject.toml, src/, scripts/, notebooks/
  - **Acción recomendada**: ¿Es parte del proyecto actual? Si no, puede moverse a otra ubicación

### Archivos Duplicados de Revisión
- 🔴 **FirstArticleRevision.odt** - Versión ODT (duplicado de .md)
- 🔴 **FirstArticleRevision.pdf** - PDF de requerimientos (duplicado de contenido en .md)
- 🔴 **ReviewAnalysis.odt** - Versión ODT (duplicado de .md)
  - **Acción recomendada**: Borrar .odt y .pdf si .md está completo

### Archivos de Bloqueo/Sistema
- 🔴 **.~lock.FirstArticleRevision.odt#** - Archivo de bloqueo temporal
- 🔴 **.DS_Store** - Metadata de macOS
  - **Acción recomendada**: Borrar (se regeneran automáticamente)

### Archivos de Bibliografía Redundantes
- 🔴 **sample_bib.bib** - ¿Duplicado de sample.bib?
  - **Acción recomendada**: Verificar si es diferente de sample.bib, sino borrar

### Scripts de Prueba
- 🔴 **test_signalbuilderc.py** - Script de testing
  - **Acción recomendada**: CONSERVAR si tiene tests útiles

---

## 📊 RESUMEN DE ACCIONES RECOMENDADAS

### BORRAR INMEDIATAMENTE (Archivos Temporales de LaTeX)
```bash
# Archivos auxiliares v09
rm main_englishv09.aux
rm main_englishv09.log
rm main_englishv09.fls
rm main_englishv09.fdb_latexmk
rm main_englishv09.out
rm main_englishv09.bbl
rm main_englishv09.loc
rm main_englishv09.soc
rm main_englishv09.synctex.gz  # si existe

# Archivos auxiliares v08
rm main_englishv08.aux
rm main_englishv08.log
rm main_englishv08.fls
rm main_englishv08.fdb_latexmk
rm main_englishv08.out
rm main_englishv08.synctex.gz  # si existe

# Archivo auxiliar antiguo
rm main.aux

# Archivos de sistema
rm .DS_Store
rm .~lock.FirstArticleRevision.odt#
```

### REVISAR Y DECIDIR

1. **main_original.tex**: Comparar con v08 y v09, borrar si está obsoleto
2. **example_file.txt, example_notebook.ipynb**: Borrar si son solo pruebas
3. **SignalBuilder/**: Archivar o borrar si no tiene código único
4. **time-series-srnet/**: Mover a otra ubicación si no es parte del proyecto actual
5. **FirstArticleRevision.odt/pdf, ReviewAnalysis.odt**: Borrar si .md está completo
6. **sample_bib.bib**: Comparar con sample.bib, borrar duplicado

### CONSERVAR DEFINITIVAMENTE

- **Manuscritos**: main_englishv09.tex/pdf, main_englishv08.tex/pdf
- **Código activo**: SignalBuilderC/, SignalBuilderV02/, generate_dataset.py
- **Documentación**: Todos los .md excepto duplicados
- **LaTeX support**: wlscirep.cls, naturemag-doi.bst, jabbrv*, sample.bib
- **Visualizaciones**: graphs/, diagrams/
- **Demos útiles**: SignalBuilderC_demo.ipynb, SignalBuilderV02_demo.ipynb (si tienen ejemplos)

---

## 📝 NOTAS IMPORTANTES

1. **Antes de borrar cualquier carpeta con .git/**: Verificar que no hay commits importantes sin respaldar
2. **Notebooks de demo**: Pueden ser valiosos para documentación futura
3. **test_signalbuilderc.py**: Útil para validación, mejor conservar
4. **Archivos .odt**: LibreOffice genera locks temporales, se pueden ignorar

---

## 🎯 ESPACIO A RECUPERAR ESTIMADO

- **Archivos temporales LaTeX**: ~5-10 MB
- **SignalBuilder/ (si se borra)**: Desconocido (depende de results/)
- **time-series-srnet/ (si se borra)**: Desconocido (depende de data/)
- **Archivos de sistema (.DS_Store, locks)**: < 1 MB
- **Duplicados .odt/.pdf**: ~5-10 MB

**Total estimado**: 20-30 MB + tamaño de repositorios antiguos

---

## ✅ COMANDO SEGURO PARA LIMPIEZA INICIAL

```bash
# Navegar al directorio
cd "/Users/julius3005/Library/CloudStorage/GoogleDrive-julius3005@gmail.com/My Drive/A2025-2026 Semestre 1/UCO/FirstArticle/ArticleScientificData"

# Borrar archivos temporales de LaTeX (se regeneran al compilar)
rm -f main_englishv09.aux main_englishv09.log main_englishv09.fls main_englishv09.fdb_latexmk main_englishv09.out main_englishv09.bbl main_englishv09.loc main_englishv09.soc main_englishv09.synctex.gz
rm -f main_englishv08.aux main_englishv08.log main_englishv08.fls main_englishv08.fdb_latexmk main_englishv08.out main_englishv08.synctex.gz
rm -f main.aux

# Borrar archivos de sistema
rm -f .DS_Store
rm -f .~lock.FirstArticleRevision.odt#

# Listar archivos restantes para decisión manual
echo "Archivos que requieren decisión manual:"
ls -lh example_* main_original.tex sample_bib.bib *.odt 2>/dev/null
```

Este comando borra solo archivos temporales seguros de eliminar.
