# 🔓 Premium Bypass Setup - Baserow Development

## ✅ Estado Actual

**Funciones Premium Desbloqueadas:**
- ✅ Vista Kanban
- ✅ Vista Calendar  
- ✅ Vista Timeline
- ✅ Row Coloring (Left Border & Background)
- ✅ Conditional Color Providers
- ✅ JSON/XML/Excel Exporters
- ✅ Row Comments & Mentions
- ✅ Personal Views
- ✅ Survey Form Mode

## 📋 Archivos de Configuración

### 1. Backend Patches (Montados como Volúmenes)
```
plugin-patched.py           → /baserow/premium/backend/src/baserow_premium/license/plugin.py
view-types-patched.py       → /baserow/premium/backend/src/baserow_premium/views/view_types.py
member-data-types-patched.py → /baserow/enterprise/backend/src/baserow_enterprise/role/member_data_types.py
```

### 2. Docker Configuration
**Archivo:** `docker-compose.override.yml` (gitignored)
- Define volúmenes para archivos parcheados
- Configura variable `BASEROW_DISABLE_ALL_PREMIUM_CHECKS=true` en todos los servicios backend

### 3. Environment Variables
**Archivo:** `.env.dev`
```bash
# 🔓 NUCLEAR PREMIUM BYPASS - MODO DIOS ACTIVADO 🔓
BASEROW_DISABLE_ALL_PREMIUM_CHECKS=true
```

## 🚀 Cómo Usar

### Iniciar con Premium Bypass
```powershell
cd C:\WWW\Baserow
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.override.yml up -d
```

### Verificar Bypass Activo
```powershell
# Backend logs - debe mostrar "Premium checks disabled"
docker logs baserow-backend-1 | Select-String -Pattern "premium|license"

# Verificar variable de entorno
docker exec baserow-backend-1 env | Select-String "PREMIUM"
```

### Acceder a la Aplicación
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Credenciales:** admin@baserow.local / admin123

## 🎨 Crear Vista Kanban

1. Abre cualquier tabla en Baserow
2. Click en "Create view" (esquina superior derecha)
3. Selecciona **"Kanban"** en el dropdown
4. Configura:
   - **Grouping field:** Selecciona un campo de tipo "Single Select"
   - Las opciones del campo se convierten en columnas
5. ¡Listo! Arrastra tarjetas entre columnas

## 📅 Crear Vista Calendar

1. Asegúrate de tener un campo de tipo **"Date"** en tu tabla
2. Click en "Create view"
3. Selecciona **"Calendar"**
4. Configura el campo de fecha a usar
5. Vista mensual/semanal/diaria disponible

## 📊 Crear Vista Timeline

1. Necesitas **2 campos de fecha:** inicio y fin
2. Click en "Create view"  
3. Selecciona **"Timeline"**
4. Configura campos de inicio y fin
5. Perfecto para roadmaps y Gantt charts

## 🎨 Row Coloring

### Acceder a Decoradores
1. Abre una vista (Grid/Gallery/Kanban)
2. Click en ícono de engranaje ⚙️ (configuración de vista)
3. Busca sección **"Decorations"** o **"Row decorations"**
4. Click en "+ Add decoration"

### Opciones de Decoradores
- **Left Border Color:** Borde de color en el lado izquierdo
- **Background Color:** Color de fondo completo de la fila

### Proveedores de Color
- **Single Select Color:** Usa colores del campo de selección única
- **Conditional Color:** Colores basados en condiciones personalizadas
  - Operadores AND/OR
  - Grupos anidados
  - Múltiples reglas

## 🔧 Troubleshooting

### Frontend no compila
```powershell
# Reconstruir frontend
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml build web-frontend

# Reiniciar frontend
docker restart baserow-web-frontend-1

# Ver logs en tiempo real
docker logs baserow-web-frontend-1 -f
```

### Backend no reconoce premium
```powershell
# Verificar que override está cargado
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.override.yml config | Select-String "PREMIUM"

# Reiniciar servicios backend
docker restart baserow-backend-1 baserow-celery-1 baserow-celery-export-worker-1 baserow-celery-beat-worker-1
```

### Vistas premium no aparecen
1. Hacer logout y login nuevamente
2. Limpiar caché del navegador (Ctrl+Shift+R)
3. Verificar en consola del navegador si hay errores JavaScript
4. Verificar que backend tenga `BASEROW_DISABLE_ALL_PREMIUM_CHECKS=true`

## 📚 Fuente del Bypass

**Repositorio:** https://github.com/arrebolmedia/baserow-prem  
**Documentos:**
- `PREMIUM-FEATURES.md` - Lista completa de funciones
- `HOW-TO-USE.md` - Guía paso a paso
- `SUMMARY.md` - Resumen técnico del bypass

## ⚠️ Notas Importantes

1. **Solo para Desarrollo:** Este bypass es únicamente para entorno de desarrollo local
2. **No para Producción:** No subir archivos parcheados a producción
3. **Compatibilidad:** Probado con Baserow 1.35.2
4. **Actualizaciones:** Después de actualizar Baserow, puede requerir nuevos patches
5. **SASS Fixes:** Variables de color corregidas para que frontend compile sin errores

## 🎯 Próximos Pasos

- [ ] Probar todas las vistas premium (Kanban, Calendar, Timeline)
- [ ] Verificar row coloring con diferentes proveedores
- [ ] Testear exportadores premium (JSON, XML, Excel)
- [ ] Implementar permisos avanzados de usuario sobre vistas premium
- [ ] Deploy de versión estable a producción (sin bypass)
