# Referencia CSS - Sistema de Diseño T-Radar

## 📋 Descripción General

Este documento describe el sistema centralizado de colores y estilos utilizado en la aplicación T-Radar. Todos los estilos están centralizados para facilitar el mantenimiento y cambios futuros.

## 📁 Archivos Principales

### 1. **src/assets/main.css**
Archivo principal que contiene todas las variables CSS y estilos globales.

**Secciones:**
- Colores primarios (marca)
- Colores secundarios
- Colores de fondo y texto
- Colores de componentes específicos
- Estilos de iconos
- Transiciones y efectos

---

## 🎨 Variables CSS Disponibles

### Colores Primarios (Naranja - Marca)

```css
--color-primary: #F18E52;           /* Naranja principal */
--color-primary-light: #FCB88F;     /* Naranja claro (hover) */
--color-primary-dark: #E67A35;      /* Naranja oscuro (activo) */
```

**Componentes afectados:**
- Botones primarios
- Iconos principales
- Acciones principales

### Colores Secundarios

```css
--color-secondary: #CEA32C;         /* Dorado */
--color-tertiary: #E2CE9C;          /* Beige/crema */
--color-quaternary: #784A27;        /* Marrón oscuro */
```

### Fondos y Textos - Light Mode (Predeterminado)

```css
--bg-color: #FFFFFF;                /* Fondo principal blanco */
--bg-color-secondary: #F5F5F5;      /* Fondo secundario gris */
--text-color: #000000;              /* Texto principal negro */
--text-color-secondary: #666666;    /* Texto secundario */
--text-color-muted: #999999;        /* Texto deshabilitado */
--border-color: #E0E0E0;            /* Bordes claro */
```

### Chat (BandurriaSidebar, BandurriaChat)

```css
--chat-bg: #FFFFFF;                 /* Fondo del chat */
--chat-user-bg: #F18E52;            /* Mensajes usuario = naranja */
--chat-user-text: #FFFFFF;          /* Texto usuario = blanco */
--chat-bot-bg: #E8E8E8;             /* Mensajes bot = gris */
--chat-bot-text: #333333;           /* Texto bot = gris oscuro */
--chat-input-border: #F18E52;       /* Focus del textarea */
--chat-button-hover: rgba(241, 142, 82, 0.1); /* Shadow del textarea */
```

**Ubicación en código:**
- `src/components/BandurriaSidebar.vue` - Classes `.chat-user-message`, `.chat-bot-message`
- `src/components/BandurriaChat.vue` - (obsoleto, usar BandurriaSidebar)

### Dashboard (Paneles.vue)

```css
--chart-bar-color: #F18E52;         /* Barras gráfico */
--metric-growth-bg: #FEF3E2;        /* Fondo crecimiento */
--metric-growth-icon: #F18E52;      /* Icono crecimiento */
--metric-milestone-bg: #EFF6FF;     /* Fondo hitos */
--metric-milestone-icon: #3B82F6;   /* Icono hitos */
```

**Ubicación en código:**
- `src/components/Paneles.vue` - Class `.chart-bar`

### Iconos

```css
--icon-primary: #F18E52;            /* Iconos naranja (principal) */
--icon-secondary: #3B82F6;          /* Iconos azul */
--icon-accent: #10B981;             /* Iconos verde */
```

**Clase CSS:** `.icon-primary`, `.icon-secondary`, `.icon-accent`

**Componentes que la usan:**
- BandurriaSidebar.vue
- Paneles.vue
- Barra2.vue

### Botones y Controles

```css
--button-primary-bg: #F18E52;       /* Fondo botón naranja */
--button-primary-text: #FFFFFF;     /* Texto blanco */
--button-hover-opacity: 0.9;        /* Opacidad hover */
--button-disabled-opacity: 0.5;     /* Opacidad deshabilitado */
```

---

## 🌙 Dark Mode

Se activa automáticamente cuando:
- Se añade class `dark` al elemento
- Se añade atributo `data-theme="dark"`

**Variables que cambian en dark mode:**

```css
[data-theme="dark"] {
  --bg-color: #1B1B1B;              /* Fondo oscuro */
  --bg-color-secondary: #2D2D2D;    /* Fondo secundario */
  --text-color: #FFFFFF;            /* Texto blanco */
  --text-color-secondary: #B0B0B0;  /* Texto gris claro */
  --border-color: #404040;          /* Bordes más claros */
}
```

---

## 📚 Clases CSS Reutilizables

### Icons

```css
.icon-primary   /* Color naranja (#F18E52) */
.icon-secondary /* Color azul (#3B82F6) */
.icon-accent    /* Color verde (#10B981) */
```

**Uso:**
```html
<TrendingUp class="size-6 icon-primary" />
```

### Chat (BandurriaSidebar.vue)

```css
.btn-chat-trigger    /* Botón flotante para abrir chat (mobile) */
.chat-user-message   /* Estilos mensajes usuario */
.chat-bot-message    /* Estilos mensajes bot */
.btn-chat-send       /* Botón enviar mensaje */
.chat-textarea:focus /* Enfoque textarea */
```

### Dashboard (Paneles.vue)

```css
.chart-bar /* Barras del gráfico de engagement */
```

---

## 🔧 Cómo Modificar Colores

### Para cambiar el color naranja principal en toda la app:

1. Abre: `src/assets/main.css`
2. Busca la sección "COLORES PRIMARIOS"
3. Cambia el valor de `--color-primary: #F18E52;`

**Ejemplo:** Cambiar de naranja a azul:
```css
--color-primary: #3B82F6;  /* Antes: #F18E52 */
```

Esto afectará automáticamente a:
- Botones primarios
- Iconos naranja
- Mensajes del usuario en el chat
- Barras del gráfico
- Botón flotante del chat

### Para cambiar el color de los mensajes del usuario en el chat:

1. Abre: `src/assets/main.css`
2. Busca: `--chat-user-bg: #F18E52;`
3. Cambia el valor

### Para cambiar colores específicos por componente:

#### Botón flotante del chat:
```css
/* En src/assets/main.css */
--button-primary-bg: #F18E52;
--button-primary-text: #FFFFFF;
```

#### Barras del gráfico:
```css
/* En src/assets/main.css */
--chart-bar-color: #F18E52;
```

---

## 📦 Estructura de Archivos Relacionados

```
src/
├── assets/
│   └── main.css              ← Variables y estilos globales
├── components/
│   ├── BandurriaSidebar.vue  ← Usa: .btn-chat-trigger, .chat-user-message, etc
│   ├── Paneles.vue           ← Usa: .chart-bar
│   └── Barra2.vue            ← Usa: .icon-primary
└── style.css                 ← Configuración Tailwind (no modificar colores aquí)
```

---

## 🎯 Resumen de Componentes y sus Variables

| Componente | Archivo | Variables Utilizadas |
|-----------|---------|----------------------|
| BandurriaSidebar | `src/components/BandurriaSidebar.vue` | `--button-primary-bg`, `--chat-user-bg`, `--chat-bot-bg`, `--icon-primary` |
| Paneles | `src/components/Paneles.vue` | `--chart-bar-color`, `--icon-primary` |
| Barra2 | `src/components/Barra2.vue` | `--icon-primary` |
| All | Global | `--bg-color`, `--text-color`, `--border-color` |

---

## 🚀 Ejemplo: Cambiar paleta completa

Para cambiar toda la paleta de naranja a azul:

**Paso 1:** Abre `src/assets/main.css`

**Paso 2:** Reemplaza las variables:
```css
:root {
  /* ANTES */
  --color-primary: #F18E52;
  --icon-primary: #F18E52;
  --chat-user-bg: #F18E52;
  --chart-bar-color: #F18E52;
  --button-primary-bg: #F18E52;
  
  /* DESPUÉS */
  --color-primary: #3B82F6;
  --icon-primary: #3B82F6;
  --chat-user-bg: #3B82F6;
  --chart-bar-color: #3B82F6;
  --button-primary-bg: #3B82F6;
}
```

**Resultado:** Toda la aplicación cambiaría de naranja a azul automáticamente.

---

## ✅ Checklist para Futuros Cambios

- [ ] ¿Modificaste variables en `main.css`?
- [ ] ¿Probaste light mode?
- [ ] ¿Probaste dark mode?
- [ ] ¿Verificaste todos los componentes que usan la variable?
- [ ] ¿Compiló correctamente? (`pnpm run build`)
- [ ] ¿Se ve bien en mobile? (Resize del navegador)

---

## 📞 Soporte

Si necesitas cambiar un color o estilo:

1. Busca la variable en `src/assets/main.css`
2. Lee el comentario que indica qué componentes afecta
3. Realiza el cambio
4. Compila con `pnpm run build`
5. Verifica en el navegador

¡Los cambios se aplican automáticamente en toda la app!
