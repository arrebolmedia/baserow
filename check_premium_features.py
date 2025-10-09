#!/usr/bin/env python3
"""
Script para verificar si las funcionalidades premium como Kanban están disponibles
"""
import os
import sys

# Añadir el path del backend de Baserow
sys.path.append('/baserow/backend/src')
sys.path.append('/baserow/premium/backend/src')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'baserow.config.settings.dev')

import django
django.setup()

from django.conf import settings
from baserow.contrib.database.views.registries import view_type_registry

def check_premium_features():
    print("🔍 Verificando funcionalidades premium disponibles...\n")
    
    # Verificar que plugins premium estén instalados
    print("📦 Apps instaladas:")
    installed_apps = settings.INSTALLED_APPS
    
    premium_related = [app for app in installed_apps if 'premium' in app or 'enterprise' in app]
    if premium_related:
        for app in premium_related:
            print(f"  ✅ {app}")
    else:
        print("  ❌ No se encontraron apps premium")
    
    print("\n🎯 Tipos de vista disponibles:")
    view_types = view_type_registry.get_all()
    
    premium_views = []
    standard_views = []
    
    for view_type in view_types:
        view_name = view_type.type
        if view_name in ['kanban', 'calendar', 'timeline']:
            premium_views.append(view_name)
            print(f"  ✅ {view_name.title()} View (PREMIUM)")
        else:
            standard_views.append(view_name)
            print(f"  📋 {view_name.title()} View (Standard)")
    
    print(f"\n📊 Resumen:")
    print(f"  Standard views: {len(standard_views)}")
    print(f"  Premium views: {len(premium_views)}")
    
    if 'kanban' in [v for v in premium_views]:
        print("\n🎉 ¡Vista Kanban está disponible!")
        return True
    else:
        print("\n❌ Vista Kanban NO está disponible")
        return False

def check_permission_managers():
    print("\n🔐 Verificando Permission Managers:")
    from baserow.core.registries import permission_manager_type_registry
    
    managers = permission_manager_type_registry.get_all()
    for manager in managers:
        print(f"  📋 {manager.type}")
        if 'view_ownership' in manager.type:
            print(f"    ✅ Premium permission manager detectado!")

if __name__ == "__main__":
    try:
        kanban_available = check_premium_features()
        check_permission_managers()
        
        if kanban_available:
            print("\n🚀 Listo para usar funcionalidades premium!")
            sys.exit(0)
        else:
            print("\n⚠️  Funcionalidades premium no disponibles")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)