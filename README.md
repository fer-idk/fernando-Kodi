# Mini juego: La gallina cruzando la calle

Proyecto de práctica para un videojuego 2D sencillo en Python con Pygame. El objetivo es cruzar la calle evitando coches y avanzar entre niveles cada vez más difíciles.

## Requisitos
- Python 3.13
- Pygame instalado en el entorno virtual

## Cómo probar el juego

1. Abrir una terminal en la raíz del proyecto.
2. Crear el entorno virtual:
   ```powershell
   py -3.13 -m venv .venv
   ```
3. Activar el entorno virtual:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
4. Instalar las dependencias:
   ```powershell
   python -m pip install -r requirements.txt
   ```
5. Generar los recursos placeholder (sprites y sonidos iniciales):
   ```powershell
   python generar_assets.py
   ```
6. Ejecutar el juego:
   ```powershell
   python main.py
   ```

## Controles
- Mover: flechas o WASD
- Saltar: barra espaciadora
- Comenzar: Enter en la pantalla inicial

## Estructura del proyecto
- `main.py`: lógica principal del juego
- `generar_assets.py`: genera assets placeholder para el juego
- `requirements.txt`: dependencias del proyecto
- `.gitignore`: ignora archivos del entorno virtual y cachés de Python
- `assets/`: sprites y sonidos del juego

## Nota
Este proyecto está pensado como base inicial para continuar ampliando mecánicas, visuales y dificultad.

#PROMTS utilizados durante el proyeto 

1. Promt uno - La idea principal del juego, un promt donde especifico al agente Copilot la ieda central y de ella surgan ideas para crear el juego

2. "Eres un desarrollador de videojuegos senior con experiencia en Python y en el desarrollo de juegos 2D sencillos. Quiero que me ayudes a iniciar un proyecto de juego desde cero, con una estructura de carpetas y archivos limpia y un primer diseño jugable.

Contexto: la idea del juego ya está aprobada y es un proyecto pequeño, por lo que la estructura debe ser simple y no sobredimensionada. El proyecto debe organizarse así:

- `.venv/`: entorno virtual de Python (no se versiona).
- `assets/`: carpeta para imágenes, sonidos y otros recursos del juego.
- `main.py`: punto de entrada del juego.
- `requirements.txt`: dependencias del proyecto.
- `.gitignore`: ignorar `.venv/`, cachés de Python y otros archivos generados.

Tu tarea es, en este orden:

1. Define la distribución completa de carpetas y archivos, indicando el propósito de cada uno en una línea.
2. Escribe el contenido inicial de `requirements.txt` y `.gitignore`, y el código base de `main.py` que abra una ventana y ejecute un bucle principal funcional.
3. Propón los primeros diseños del juego (mecánica central, personaje o elemento principal, estilo visual) y crea los primeros niveles: al menos dos, con una progresión de dificultad clara, descritos de forma que puedan implementarse en código.

Mantén el alcance acotado a estos puntos: no añadas sistemas complejos, menús elaborados ni frameworks innecesarios. Usa Python con una librería 2D sencilla y justifica brevemente la elección. Responde en español, con código listo para copiar y pegar y secciones claramente separadas."

3. "Eres un desarrollador de videojuegos senior con experiencia en Python y Pygame. Necesito un script auxiliar que genere los recursos visuales y sonoros placeholder de un juego 2D, para poder sustituirlos más adelante por arte y audio definitivos.

Contexto: el proyecto es un juego 2D sencillo hecho con Pygame. Su estructura es `.venv/`, `assets/`, `main.py`, `requirements.txt` y `.gitignore`, y ya tiene definidos el personaje principal y un estilo visual. Ese diseño es la referencia para los placeholders. Aún no existen recursos gráficos ni sonoros reales, así que este script los creará.

Tu tarea es crear un script de Python independiente (por ejemplo, `generar_assets.py`) que escriba sus archivos dentro de la carpeta `assets/`:

1. **Sprites PNG placeholder**: figuras de colores sencillos con formas reconocibles para:
   - El jugador: una figura que se distinga a simple vista del resto, siguiendo el diseño del personaje principal en proporciones y color dominante.
   - Enemigos: una forma diferente a la del jugador, con un color que transmita peligro.
   - Plataformas: rectángulos de un color neutro, claramente separados del fondo.
2. **Efectos de sonido WAV básicos**:
   - Un sonido de salto: un tono corto con frecuencia ascendente.
   - Un sonido de colisión: un ruido o tono corto con frecuencia descendente.

Requisitos:
- Genera los PNG y WAV con las librerías estándar o con Pygame, sin dependencias adicionales. Si usas Pygame, justifícalo en una línea.
- Nombra los archivos de forma consistente (por ejemplo, `jugador.png`, `enemigo.png`, `plataforma.png`, `salto.wav`, `colision.wav`) para que sea fácil reemplazarlos después con el mismo nombre.
- Crea la carpeta `assets/` si no existe.
- Define los tamaños, colores y frecuencias como constantes al inicio del script, para poder ajustarlos sin tocar la lógica.
- Mantén el alcance acotado: no añadas música, animaciones, ni otros recursos no pedidos.

Responde en español, con el código completo listo para copiar y pegar, y una breve lista de cómo ejecutar el script y qué archivos genera."

4. "Continúa con la siguiente mejora real del juego. Ya tienes el proyecto del juego en esta conversación, así que aplica directamente el cambio elegido sobre ese código, sin rehacer lo que ya funciona.

Quiero que implementes, en este orden de prioridad, las tres mejoras propuestas:

1. **Animación de "nivel superado"**: cuando el jugador complete un nivel, muestra una animación breve y clara (texto o overlay con transición) que indique el éxito antes de pasar al siguiente nivel. Debe durar unos segundos y no bloquear la lógica del juego.

2. **Vidas y contador en pantalla**: añade un sistema de vidas que se muestre visualmente en pantalla junto a un contador (vidas restantes y, si encaja con el juego, puntuación o intentos). Define qué ocurre al perder una vida y cuándo termina la partida (game over), y reinicia correctamente el estado al empezar de nuevo.

3. **Tercer nivel más desafiante**: crea un nivel adicional con mayor dificultad que los anteriores (más enemigos, obstáculos más complejos o velocidad aumentada, según la mecánica existente), reutilizando el mismo sistema de niveles para que la transición entre niveles funcione igual.

Restricciones:
- Mantén el lenguaje, framework y estructura de archivos actuales; no introduzcas dependencias nuevas salvo que sea imprescindible.
- Integra las tres mejoras con el código existente sin romper los niveles, controles ni el flujo actual.
- Si algún detalle del proyecto no está claro, toma la opción más razonable y consistente con lo que ya existe.

Entrega los cambios por archivo, indicando qué se modifica o se añade en cada uno, y explica brevemente cómo probar cada mejora."