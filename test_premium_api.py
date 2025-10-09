#!/usr/bin/env python3
"""
Script simple para verificar funcionalidades premium via API
"""
import requests
import json

# Configuración
BASE_URL = "http://localhost:8000"
EMAIL = "admin@baserow.local"
PASSWORD = "admin123"

def get_auth_token():
    """Obtiene token de autenticación"""
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login/", json={
            "email": EMAIL,
            "password": PASSWORD
        })
        
        if response.status_code == 200:
            data = response.json()
            return data.get('access_token')
        else:
            print(f"❌ Error de login: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def check_view_types(token):
    """Verifica tipos de vista disponibles"""
    try:
        headers = {"Authorization": f"JWT {token}"}
        
        # Crear workspace para probar
        workspace_response = requests.post(f"{BASE_URL}/api/workspaces/", 
            headers=headers, 
            json={"name": "Test Premium Workspace"}
        )
        
        if workspace_response.status_code == 200:
            workspace = workspace_response.json()
            print(f"✅ Workspace creado: {workspace['name']}")
            
            # Crear aplicación
            app_response = requests.post(f"{BASE_URL}/api/applications/", 
                headers=headers,
                json={
                    "type": "database",
                    "workspace_id": workspace['id'],
                    "name": "Test Database"
                }
            )
            
            if app_response.status_code == 200:
                app = app_response.json()
                print(f"✅ Database creada: {app['name']}")
                
                # Crear tabla
                table_response = requests.post(f"{BASE_URL}/api/database/tables/", 
                    headers=headers,
                    json={
                        "database_id": app['id'],
                        "name": "Test Table"
                    }
                )
                
                if table_response.status_code == 200:
                    table = table_response.json()
                    print(f"✅ Tabla creada: {table['name']}")
                    
                    # Añadir campo Single Select para Kanban
                    field_response = requests.post(f"{BASE_URL}/api/database/fields/", 
                        headers=headers,
                        json={
                            "table_id": table['id'],
                            "type": "single_select",
                            "name": "Estado"
                        }
                    )
                    
                    if field_response.status_code == 200:
                        field = field_response.json()
                        print(f"✅ Campo Single Select creado: {field['name']}")
                        
                        # Intentar crear vista Kanban
                        kanban_response = requests.post(f"{BASE_URL}/api/database/views/", 
                            headers=headers,
                            json={
                                "table_id": table['id'],
                                "type": "kanban",
                                "name": "Vista Kanban Test",
                                "single_select_field": field['id']
                            }
                        )
                        
                        if kanban_response.status_code == 200:
                            kanban_view = kanban_response.json()
                            print(f"🎉 ¡Vista Kanban creada exitosamente!: {kanban_view['name']}")
                            print(f"   - ID: {kanban_view['id']}")
                            print(f"   - Tipo: {kanban_view['type']}")
                            return True
                        else:
                            print(f"❌ Error creando vista Kanban: {kanban_response.status_code}")
                            print(f"Response: {kanban_response.text}")
                            return False
                    
        return False
        
    except Exception as e:
        print(f"❌ Error verificando vistas: {e}")
        return False

def main():
    print("🔍 Verificando funcionalidades premium de Baserow...")
    print("=" * 50)
    
    # Obtener token
    token = get_auth_token()
    if not token:
        print("❌ No se pudo autenticar")
        return
    
    print(f"✅ Login exitoso")
    
    # Verificar vistas premium
    kanban_works = check_view_types(token)
    
    print("=" * 50)
    if kanban_works:
        print("🎉 ¡FUNCIONALIDADES PREMIUM ACTIVADAS!")
        print("   ✅ Vista Kanban disponible y funcional")
    else:
        print("⚠️  Funcionalidades premium no disponibles")

if __name__ == "__main__":
    main()