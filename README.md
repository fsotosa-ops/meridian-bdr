# 🎯 Meridian-BDR

**Agente de prospección automatizado para BDRs**

El BDR configura, Meridian trabaja. Despierta con leads calificados en tu Google Sheet.

---

## 🚀 Inicio Rápido

### 1. Instalar dependencias

```bash
python -m venv .venv
source .venv/bin/activate  # En Mac/Linux
pip install -r requirements.txt
playwright install chromium
```

### 2. Configurar credenciales

```bash
cp .env.example .env
```

Edita `.env` con tus API keys:
- `GOOGLE_SHEET_ID`: ID de tu Google Sheet
- `GEMINI_API_KEY`: De Google AI Studio
- `SERPER_API_KEY`: De serper.dev (2,500 búsquedas gratis/mes)

### 3. Configurar Google Sheets API

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un proyecto y habilita Google Sheets API
3. Crea credenciales OAuth 2.0
4. Descarga `credentials.json` a la carpeta del proyecto

### 4. Preparar tu Google Sheet

Crea dos pestañas:

**Pestaña `Config`:**

| A | B |
|---|---|
| Parámetro | Valor |
| ICP | Empresas importadoras de México, volumen mínimo $1M USD... |
| Research Queries | {company} importador México, {company} importaciones volumen USD |
| Sales Nav URL | https://www.linkedin.com/sales/search/... |
| Max Pages | 3 |
| Max Leads/Day | 50 |
| Auto Run | No |
| Last Run | |

**Pestaña `Leads`:**

| A | B | C | D | E | F | G | H | I | J | K |
|---|---|---|---|---|---|---|---|---|---|---|
| Fecha | Nombre | Cargo | Empresa | LinkedIn | Score | Fit | Razón | Info Importaciones | Status | Notas BDR |

---

## 📖 Uso

```bash
# Ver estado actual
python main.py status

# Extraer leads de Sales Navigator
python main.py scrape

# Investigar y calificar leads
python main.py research

# Ejecutar todo el pipeline
python main.py full
```

---

## 🔄 Flujo de Trabajo Recomendado

### Opción A: Manual (recomendado inicialmente)

1. **Mañana temprano**: `python main.py full`
2. **Durante el día**: Revisa leads con Status "🔍 Revisar"
3. **Valida y mueve** los buenos a tu CRM

### Opción B: Automático (con cron)

```bash
# Editar crontab
crontab -e

# Agregar línea (ejecuta a las 6 AM)
0 6 * * * cd /path/to/meridian-bdr && /path/to/.venv/bin/python main.py full >> logs/cron.log 2>&1
```

---

## 🛡️ Mejores Prácticas Anti-Ban

1. **No excedas 50 leads/día** de Sales Navigator
2. **Máximo 3 páginas** por sesión de scraping
3. **No corras el scraper más de 2 veces al día**
4. **Usa tu cuenta personal** de LinkedIn (no cuentas nuevas)
5. **La primera vez**, haz login manual cuando se abra el navegador

---

## 📊 Costos Estimados

| Servicio | Plan Gratis | Uso típico (100 leads/mes) |
|----------|-------------|---------------------------|
| Serper.dev | 2,500 búsquedas | ~200 búsquedas |
| Gemini | Muy barato | ~$0.02 |
| **Total** | | **~$0.02/mes** |

---

## 🏗️ Estructura del Proyecto

```
meridian-bdr/
├── main.py              # Orquestador principal
├── requirements.txt     # Dependencias
├── .env                 # Credenciales (no commitear)
├── credentials.json     # OAuth Google (no commitear)
├── token.json           # Token generado (no commitear)
├── data/
│   └── browser_session/ # Sesión de Chrome (no commitear)
└── src/
    ├── scraper.py       # Extractor de Sales Navigator
    ├── researcher_api.py # Investigador con Serper
    ├── brain.py         # Evaluador con Gemini
    └── sheets.py        # Interface con Google Sheets
```

---

## 🤝 Soporte

¿Problemas? Revisa:

1. ¿Tienes todas las API keys en `.env`?
2. ¿El Sheet tiene las pestañas `Config` y `Leads`?
3. ¿Hiciste login en LinkedIn la primera vez?

---

**Hecho con ☕ para BDRs que prefieren cerrar deals que hacer research.**
