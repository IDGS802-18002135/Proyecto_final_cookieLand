from io import open

class manejadorArchivo:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo

    def insertar(self, palabra1):
        try:
            p = palabra1.strip().split(":")
            
            resp = self.verificar(p[0])
            if resp == "insertar":
                with open(self.nombre_archivo, 'a') as archivo_texto:
                    archivo_texto.write(f'{palabra1}\n')
                return "Agregado con exito"
            else:
                return "Producto existente en lista"
        except Exception as e:
            return f"Error al insertar: {e}"
    def mostrar_contenido(self):
        resultados = []
        with open(self.nombre_archivo, 'r') as archivo_texto:
            for linea in archivo_texto.readlines():
                    resultados.append(linea.rstrip())
        
        if resultados:
            return resultados
        else:
            return ''

    def eliminar(self, indice):
        try:
            with open(self.nombre_archivo, 'r') as archivo_texto:
                lineas = archivo_texto.readlines()

            with open(self.nombre_archivo, 'w') as archivo_texto:
                for i, linea in enumerate(lineas, 1):  # Comienza la enumeración desde 1
                    if i != indice:
                        archivo_texto.write(linea)
    
            return f'Eliminado exitosamente'
        except Exception as e:
            print(f'Error al eliminar el renglón: {e}')
            return f'Error al eliminar el renglón: {e}'
        
    def verificar(self,dato):
        try:
                with open(self.nombre_archivo,'r') as archivo:
                    lineas = archivo.readlines()
                  
                for linea in lineas:
                    if linea.strip().split(":")[0] == dato:
                        return f'La galleta {dato} ya ha sido agregada a la lista.'
                        
                return 'insertar'
        except Exception as e:
             print(f'Error al verificar el renglón: {e}')
             return f'Error al eliminar el renglón: {e}'         
         
    def eliminar_todo(self):
        try:
            with open(self.nombre_archivo, 'w') as archivo_texto:
                archivo_texto.write('')
               
            return 'Todo el contenido del archivo ha sido eliminado exitosamente.'
        except Exception as e:
            return f'Error al eliminar todo el contenido: {e}'
    def modificar(self,indice,dato):
        try:
                with open(self.nombre_archivo,'r') as archivo:
                    lineas = archivo.readlines()
                    
                with open(self.nombre_archivo,"w") as archivo:
                    for i, linea in enumerate(lineas,1):
                        if i == indice:
                            archivo.write(dato + '\n')  # Agrega un salto de línea al final de la línea modificada
                        else:
                            archivo.write(linea)
                            
                            
                return f'Renglón en el índice {indice} modificado exitosamente.'
        except Exception as e:
             print(f'Error al eliminar el renglón: {e}')
             return f'Error al eliminar el renglón: {e}'             
                                