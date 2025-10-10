import requests
import json

# URLs
BASE_URL = "http://localhost:8000"

# Intentar registrar un nuevo usuario
print("🔐 Registrando nuevo usuario...")
register_url = f"{BASE_URL}/api/auth/register/"
register_data = {
    "name": "Test User",
    "email": "premium@test.com",
    "password": "testpassword123",
    "language": "en"
}

response = requests.post(register_url, json=register_data)
if response.status_code in [200, 201]:
    user_data = response.json()
    token = user_data.get("access_token") or user_data.get("token")
    print(f"✅ Usuario registrado y autenticado")
    print(f"   Token: {token[:30]}...")
    print(f"   Email: {user_data.get('email')}")
    
    # Headers para las siguientes peticiones
    headers = {
        "Authorization": f"JWT {token}",
        "Content-Type": "application/json"
    }
    
    # Crear una nueva base de datos/workspace
    print("\n📦 Creando workspace...")
    workspace_url = f"{BASE_URL}/api/workspaces/"
    workspace_data = {"name": "Premium Test Workspace"}
    response = requests.post(workspace_url, json=workspace_data, headers=headers)
    
    if response.status_code in [200, 201]:
        workspace = response.json()
        workspace_id = workspace["id"]
        print(f"✅ Workspace creado: {workspace['name']} (ID: {workspace_id})")
        
        # Crear una aplicación de base de datos
        print("\n🗄️ Creando base de datos...")
        database_url = f"{BASE_URL}/api/applications/workspace/{workspace_id}/"
        database_data = {
            "name": "Premium Test Database",
            "type": "database"
        }
        response = requests.post(database_url, json=database_data, headers=headers)
        
        if response.status_code in [200, 201]:
            database = response.json()
            database_id = database["id"]
            print(f"✅ Base de datos creada: {database['name']} (ID: {database_id})")
            
            # Crear una tabla
            print("\n📋 Creando tabla...")
            table_url = f"{BASE_URL}/api/database/tables/database/{database_id}/"
            table_data = {
                "name": "Proyectos",
                "data": [
                    ["Nombre", "Estado", "Prioridad"],
                    ["Proyecto A", "Nuevo", "Alta"],
                    ["Proyecto B", "En Progreso", "Media"],
                    ["Proyecto C", "Completado", "Baja"]
                ],
                "first_row_header": True
            }
            response = requests.post(table_url, json=table_data, headers=headers)
            
            if response.status_code in [200, 201]:
                table = response.json()
                table_id = table["id"]
                print(f"✅ Tabla creada: {table['name']} (ID: {table_id})")
                
                # Obtener campos de la tabla
                print("\n🔍 Obteniendo campos...")
                fields_url = f"{BASE_URL}/api/database/fields/table/{table_id}/"
                response = requests.get(fields_url, headers=headers)
                
                if response.status_code == 200:
                    fields = response.json()
                    print(f"✅ {len(fields)} campos encontrados:")
                    
                    text_field_id = None
                    for field in fields:
                        print(f"   - {field['name']} (ID: {field['id']}, Type: {field['type']})")
                        if field['type'] == 'text' and 'Estado' in field['name']:
                            text_field_id = field['id']
                    
                    if text_field_id:
                        # Convertir el campo de texto a single_select
                        print(f"\n🔄 Convirtiendo campo 'Estado' a Single Select...")
                        update_field_url = f"{BASE_URL}/api/database/fields/{text_field_id}/"
                        update_data = {
                            "type": "single_select",
                            "select_options": [
                                {"value": "Nuevo", "color": "blue"},
                                {"value": "En Progreso", "color": "yellow"},
                                {"value": "Completado", "color": "green"},
                                {"value": "Cancelado", "color": "red"}
                            ]
                        }
                        response = requests.patch(update_field_url, json=update_data, headers=headers)
                        
                        if response.status_code == 200:
                            updated_field = response.json()
                            print(f"✅ Campo convertido a Single Select (ID: {updated_field['id']})")
                            
                            # Ahora intentar crear vista KANBAN
                            print(f"\n🎴 🔓 CREANDO VISTA KANBAN (PREMIUM)...")
                            kanban_view_data = {
                                "name": "Vista Kanban Premium",
                                "type": "kanban",
                                "single_select_field": updated_field['id']
                            }
                            
                            create_view_url = f"{BASE_URL}/api/database/views/table/{table_id}/"
                            response = requests.post(create_view_url, json=kanban_view_data, headers=headers)
                            
                            if response.status_code in [200, 201]:
                                view = response.json()
                                print(f"\n🎉 ✅ ¡¡¡ÉXITO!!! VISTA KANBAN CREADA:")
                                print(f"   - ID: {view['id']}")
                                print(f"   - Nombre: {view['name']}")
                                print(f"   - Tipo: {view['type']}")
                                print(f"   - Campo de agrupación: {view.get('single_select_field')}")
                                print(f"\n🔓 🔓 🔓 BYPASS PREMIUM FUNCIONANDO 🔓 🔓 🔓")
                                print(f"\n✨ Accede a http://localhost:3000 para ver la vista Kanban")
                                print(f"   Email: premium@test.com")
                                print(f"   Password: testpassword123")
                            else:
                                print(f"\n❌ Error al crear vista Kanban:")
                                print(f"   Status: {response.status_code}")
                                print(f"   Response: {json.dumps(response.json(), indent=2)}")
                        else:
                            print(f"❌ Error al actualizar campo: {response.status_code} - {response.text}")
                    else:
                        print("\n⚠️ No se encontró el campo 'Estado'")
                else:
                    print(f"❌ Error al obtener campos: {response.status_code} - {response.text}")
            else:
                print(f"❌ Error al crear tabla: {response.status_code} - {response.text}")
        else:
            print(f"❌ Error al crear base de datos: {response.status_code} - {response.text}")
    else:
        print(f"❌ Error al crear workspace: {response.status_code} - {response.text}")
elif response.status_code == 400:
    error_data = response.json()
    if error_data.get("error") == "ERROR_EMAIL_ALREADY_EXISTS":
        print("⚠️ Usuario ya existe. Intentando login...")
        
        # Intentar login
        login_url = f"{BASE_URL}/api/user/token-auth/"
        login_data = {
            "email": "premium@test.com",
            "password": "testpassword123"
        }
        response = requests.post(login_url, json=login_data)
        if response.status_code == 200:
            token = response.json()["token"]
            print(f"✅ Login exitoso. Token: {token[:30]}...")
            print("\n✨ Usuario ya tiene datos. Accede a http://localhost:3000")
            print("   Email: premium@test.com")
            print("   Password: testpassword123")
        else:
            print(f"❌ Error en login: {response.status_code} - {response.text}")
    else:
        print(f"❌ Error en registro: {response.status_code} - {json.dumps(error_data, indent=2)}")
else:
    print(f"❌ Error en registro: {response.status_code} - {response.text}")
