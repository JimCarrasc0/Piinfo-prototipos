import json
import requests
import sys
import time
from datetime import datetime
from typing import List, Dict, Optional

class InstagramScraper:
    def __init__(self, username: str, sessionid: str):
        self.username = username
        self.sessionid = sessionid
        self.base_url = "https://www.instagram.com/api/v1/users/web_profile_info/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-IG-App-ID": "936619743392459",
        }
        self.cookies = {
            "sessionid": sessionid
        }
    
    def fetch_profile_data(self) -> Optional[Dict]:
        """Obtiene los datos del perfil de Instagram"""
        try:
            params = {"username": self.username}
            print(f"Consultando perfil: {self.username}")
            
            response = requests.get(
                self.base_url,
                params=params,
                headers=self.headers,
                cookies=self.cookies,
                timeout=30
            )
            
            if response.status_code == 200:
                print("✓ Datos obtenidos correctamente")
                return response.json()
            else:
                print(f"✗ Error en la consulta: {response.status_code}")
                print(f"Mensaje: {response.text[:200]}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Error de conexión: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"✗ Error al parsear JSON: {e}")
            return None
    
    def extract_publications(self, profile_data: Dict) -> List[Dict]:
        """Extrae y procesa las publicaciones del perfil"""
        try:
            user_data = profile_data.get("data", {}).get("user", {})
            
            # Obtener publicaciones del timeline
            timeline_media = user_data.get("edge_owner_to_timeline_media", {})
            timeline_edges = timeline_media.get("edges", [])
            
            # Obtener publicaciones de IGTV
            igtv_media = user_data.get("edge_felix_video_timeline", {})
            igtv_edges = igtv_media.get("edges", [])
            
            publications = []
            
            # Procesar publicaciones del timeline
            for edge in timeline_edges:
                publication = self._process_publication(edge.get("node", {}))
                if publication:
                    publications.append(publication)
            
            # Procesar publicaciones de IGTV
            for edge in igtv_edges:
                publication = self._process_publication(edge.get("node", {}))
                if publication:
                    publications.append(publication)
            
            # Ordenar por fecha (más recientes primero)
            publications.sort(
                key=lambda x: datetime.strptime(x["fecha_publicacion"], "%Y-%m-%d %H:%M:%S") 
                if x["fecha_publicacion"] != "Fecha no disponible" 
                else datetime.min,
                reverse=True
            )
            
            return publications
            
        except Exception as e:
            print(f"✗ Error al extraer publicaciones: {e}")
            return []
    
    def _process_publication(self, node: Dict) -> Optional[Dict]:
        """Procesa una publicación individual"""
        try:
            # ID de la publicación
            post_id = node.get("id")
            if not post_id:
                return None
            
            # Descripción
            caption_edges = node.get("edge_media_to_caption", {}).get("edges", [])
            description = ""
            if caption_edges and len(caption_edges) > 0:
                description = caption_edges[0].get("node", {}).get("text", "")
            
            # Likes
            likes = node.get("edge_media_preview_like", {}).get("count", 0)
            if likes == 0:
                likes = node.get("edge_liked_by", {}).get("count", 0)
            
            # Comentarios
            comments = node.get("edge_media_to_comment", {}).get("count", 0)
            
            # Tipo de publicación
            typename = node.get("__typename", "")
            product_type = node.get("product_type", "")
            
            if typename == "GraphSidecar":
                pub_type = "Sidecar (Múltiples imágenes)"
            elif typename == "GraphVideo":
                if product_type == "igtv":
                    pub_type = "IGTV"
                elif product_type == "clips":
                    pub_type = "Reel/Clip"
                else:
                    pub_type = "Video"
            elif typename == "GraphImage":
                pub_type = "Imagen"
            else:
                pub_type = typename
            
            # Fecha
            timestamp = node.get("taken_at_timestamp", 0)
            if timestamp:
                date_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            else:
                date_str = "Fecha no disponible"
            
            # Crear objeto de publicación
            publication = {
                "id_publicacion": post_id,
                "descripcion": description,
                "likes": likes,
                "comentarios": comments,
                "tipo_publicacion": pub_type,
                "fecha_publicacion": date_str
            }
            
            return publication
            
        except Exception as e:
            print(f"✗ Error al procesar publicación: {e}")
            return None
    
    def save_to_file(self, publications: List[Dict], filename: str = "publicaciones.json"):
        """Guarda las publicaciones en un archivo JSON"""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(publications, f, indent=2, ensure_ascii=False)
            print(f"✓ Publicaciones guardadas en: {filename}")
            print(f"✓ Total de publicaciones: {len(publications)}")
            return True
        except Exception as e:
            print(f"✗ Error al guardar archivo: {e}")
            return False
    
    def display_summary(self, publications: List[Dict]):
        """Muestra un resumen de las publicaciones"""
        if not publications:
            print("✗ No hay publicaciones para mostrar")
            return
        
        print("\n" + "="*80)
        print("RESUMEN DE PUBLICACIONES")
        print("="*80)
        print(f"Total de publicaciones: {len(publications)}")
        
        # Estadísticas por tipo
        type_stats = {}
        for pub in publications:
            pub_type = pub["tipo_publicacion"]
            type_stats[pub_type] = type_stats.get(pub_type, 0) + 1
        
        print("\nDistribución por tipo:")
        for pub_type, count in type_stats.items():
            percentage = (count / len(publications)) * 100
            print(f"  {pub_type}: {count} ({percentage:.1f}%)")
        
        # Totales
        total_likes = sum(pub["likes"] for pub in publications)
        total_comments = sum(pub["comentarios"] for pub in publications)
        
        print(f"\nTotal de likes: {total_likes:,}")
        print(f"Total de comentarios: {total_comments:,}")
        
        if len(publications) > 0:
            avg_likes = total_likes / len(publications)
            avg_comments = total_comments / len(publications)
            print(f"Promedio de likes por publicación: {avg_likes:.1f}")
            print(f"Promedio de comentarios por publicación: {avg_comments:.1f}")
        
        # Mostrar primeras 3 publicaciones
        print("\n" + "-"*80)
        print("PRIMERAS 3 PUBLICACIONES:")
        print("-"*80)
        
        for i, pub in enumerate(publications[:3], 1):
            print(f"\nPublicación {i}:")
            print(f"  ID: {pub['id_publicacion']}")
            print(f"  Tipo: {pub['tipo_publicacion']}")
            print(f"  Fecha: {pub['fecha_publicacion']}")
            print(f"  Likes: {pub['likes']:,} | Comentarios: {pub['comentarios']}")
            
            desc = pub['descripcion'].replace('\n', ' ')
            if len(desc) > 100:
                print(f"  Descripción: {desc[:100]}...")
            else:
                print(f"  Descripción: {desc}")

def main():
    """Función principal"""
    print("="*80)
    print("INSTAGRAM PUBLICATION SCRAPER")
    print("="*80)
    
    # Configuración
    if len(sys.argv) == 3:
        username = sys.argv[1]
        sessionid = sys.argv[2]
    else:
        # Solicitar datos si no se pasan como argumentos
        username = input("Ingresa el nombre de usuario de Instagram: ").strip()
        sessionid = input("Ingresa tu sessionid de Instagram: ").strip()
    
    if not username or not sessionid:
        print("✗ Error: Se requiere nombre de usuario y sessionid")
        print("Uso: python instagram_scraper.py <username> <sessionid>")
        sys.exit(1)
    
    # Crear scraper
    scraper = InstagramScraper(username, sessionid)
    
    # Obtener datos del perfil
    start_time = time.time()
    profile_data = scraper.fetch_profile_data()
    
    if not profile_data:
        print("✗ No se pudieron obtener los datos del perfil")
        sys.exit(1)
    
    # Extraer publicaciones
    publications = scraper.extract_publications(profile_data)
    
    if not publications:
        print("✗ No se encontraron publicaciones")
        sys.exit(1)
    
    # Mostrar resumen
    scraper.display_summary(publications)
    
    # Guardar en archivo
    output_file = "publicaciones.json"
    success = scraper.save_to_file(publications, output_file)
    
    elapsed_time = time.time() - start_time
    print(f"\n✓ Tiempo total de ejecución: {elapsed_time:.2f} segundos")
    
    if success:
        print("\n" + "="*80)
        print(f"✓ Proceso completado exitosamente!")
        print(f"✓ Archivo generado: {output_file}")
        print("="*80)

if __name__ == "__main__":
    main()