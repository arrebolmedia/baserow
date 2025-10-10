import requests
import json

# URLs
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/user/token-auth/"
LIST_TABLES_URL = f"{BASE_URL}/api/database/tables/database/"
CREATE_VIEW_URL = f"{BASE_URL}/api/database/views/table/"

# Credenciales
credentials = {
    "email": "admin@baserow.local",
    "password": "admin123"
}

# 1. Obtener token JWT
print("🔐 Obteniendo token JWT...")
response = requests.post(LOGIN_URL, json=credentials)
if response.status_code == 200:
    token = response.json()["token"]
    print(f"✅ Token obtenido: {token[:20]}...")
else:
    print(f"❌ Error: {response.status_code} - {response.text}")
    exit(1)

# Headers para las siguientes peticiones
headers = {
    "Authorization": f"JWT {token}",
    "Content-Type": "application/json"
}

# 2. Listar todas las bases de datos para encontrar tablas
print("\n📊 Listando bases de datos...")
databases_url = f"{BASE_URL}/api/applications/"
response = requests.get(databases_url, headers=headers)
if response.status_code == 200:
    apps = response.json()
    print(f"✅ Encontradas {len(apps)} aplicaciones")
    
    # Buscar la primera base de datos
    database = None
    for app in apps:
        if app.get("type") == "database":
            database = app
            break
    
    if database:
        database_id = database["id"]
        print(f"📁 Base de datos: {database['name']} (ID: {database_id})")
        
        # 3. Listar tablas de esta base de datos
        print(f"\n📋 Listando tablas de la base de datos {database_id}...")
        tables_url = f"{BASE_URL}/api/database/tables/database/{database_id}/"
        response = requests.get(tables_url, headers=headers)
        
        if response.status_code == 200:
            tables = response.json()
            print(f"✅ Encontradas {len(tables)} tablas:")
            for table in tables:
                print(f"  - {table['name']} (ID: {table['id']})")
            
            if tables:
                # Usar la primera tabla
                table = tables[0]
                table_id = table["id"]
                print(f"\n🎯 Usando tabla: {table['name']} (ID: {table_id})")
                
                # 4. Verificar campos de la tabla
                print(f"\n🔍 Verificando campos de la tabla {table_id}...")
                fields_url = f"{BASE_URL}/api/database/fields/table/{table_id}/"
                response = requests.get(fields_url, headers=headers)
                
                if response.status_code == 200:
                    fields = response.json()
                    print(f"✅ Campos encontrados:")
                    
                    single_select_field = None
                    for field in fields:
                        print(f"  - {field['name']} (ID: {field['id']}, Type: {field['type']})")
                        if field['type'] == 'single_select':
                            single_select_field = field
                    
                    if single_select_field:
                        print(f"\n✅ Campo Single Select encontrado: {single_select_field['name']} (ID: {single_select_field['id']})")
                        
                        # 5. Intentar crear vista Kanban
                        print(f"\n🎴 Intentando crear vista KANBAN...")
                        kanban_view_data = {
                            "name": "Vista Kanban Premium",
                            "type": "kanban",
                            "single_select_field": single_select_field['id']
                        }
                        
                        create_view_url = f"{BASE_URL}/api/database/views/table/{table_id}/"
                        response = requests.post(create_view_url, json=kanban_view_data, headers=headers)
                        
                        if response.status_code in [200, 201]:
                            view = response.json()
                            print(f"🎉 ✅ ÉXITO! Vista Kanban creada:")
                            print(f"   - ID: {view['id']}")
                            print(f"   - Nombre: {view['name']}")
                            print(f"   - Tipo: {view['type']}")
                            print(f"   - Campo de agrupación: {view.get('single_select_field')}")
                            print(f"\n🔓 BYPASS PREMIUM FUNCIONANDO!")
                        else:
                            print(f"❌ Error al crear vista Kanban:")
                            print(f"   Status: {response.status_code}")
                            print(f"   Response: {response.text}")
                    else:
                        print("\n⚠️ No hay campos Single Select. Creando uno...")
                        # Crear un campo single select primero
                        create_field_url = f"{BASE_URL}/api/database/fields/table/{table_id}/"
                        field_data = {
                            "name": "Estado",
                            "type": "single_select",
                            "select_options": [
                                {"value": "Nuevo", "color": "blue"},
                                {"value": "En Progreso", "color": "yellow"},
                                {"value": "Completado", "color": "green"},
                                {"value": "Cancelado", "color": "red"}
                            ]
                        }
                        
                        response = requests.post(create_field_url, json=field_data, headers=headers)
                        if response.status_code in [200, 201]:
                            new_field = response.json()
                            print(f"✅ Campo creado: {new_field['name']} (ID: {new_field['id']})")
                            
                            # Ahora crear la vista Kanban
                            print(f"\n🎴 Creando vista KANBAN con el nuevo campo...")
                            kanban_view_data = {
                                "name": "Vista Kanban Premium",
                                "type": "kanban",
                                "single_select_field": new_field['id']
                            }
                            
                            create_view_url = f"{BASE_URL}/api/database/views/table/{table_id}/"
                            response = requests.post(create_view_url, json=kanban_view_data, headers=headers)
                            
                            if response.status_code in [200, 201]:
                                view = response.json()
                                print(f"🎉 ✅ ÉXITO! Vista Kanban creada:")
                                print(f"   - ID: {view['id']}")
                                print(f"   - Nombre: {view['name']}")
                                print(f"   - Tipo: {view['type']}")
                                print(f"   - Campo de agrupación: {view.get('single_select_field')}")
                                print(f"\n🔓 BYPASS PREMIUM FUNCIONANDO!")
                            else:
                                print(f"❌ Error al crear vista Kanban:")
                                print(f"   Status: {response.status_code}")
                                print(f"   Response: {response.text}")
                        else:
                            print(f"❌ Error al crear campo: {response.status_code} - {response.text}")
                else:
                    print(f"❌ Error al obtener campos: {response.status_code} - {response.text}")
            else:
                print("⚠️ No hay tablas en esta base de datos")
        else:
            print(f"❌ Error al listar tablas: {response.status_code} - {response.text}")
    else:
        print("⚠️ No se encontró ninguna base de datos")
else:
    print(f"❌ Error al listar aplicaciones: {response.status_code} - {response.text}")
