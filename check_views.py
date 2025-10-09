from baserow.contrib.database.views.registries import view_type_registry
from django.conf import settings

print("🔍 Verificando funcionalidades premium disponibles...")
print("")

# Verificar apps instaladas
print("📦 Apps premium instaladas:")
premium_apps = [app for app in settings.INSTALLED_APPS if 'premium' in app or 'enterprise' in app]
for app in premium_apps:
    print(f"  ✅ {app}")

print("")
print("🎯 Tipos de vista disponibles:")

view_types = view_type_registry.get_all()
premium_views = []

for view_type in view_types:
    view_name = view_type.type
    if view_name in ['kanban', 'calendar', 'timeline']:
        premium_views.append(view_name)
        print(f"  ✅ {view_name.title()} View (PREMIUM)")
    else:
        print(f"  📋 {view_name.title()} View (Standard)")

print("")
print(f"📊 Vistas premium disponibles: {len(premium_views)}")
if 'kanban' in premium_views:
    print("🎉 ¡Vista Kanban está DISPONIBLE!")
else:
    print("❌ Vista Kanban NO está disponible")