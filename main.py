import re
import json
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
import requests
import gzip
from io import StringIO
import pandas as pd
import seaborn as sns


class NASALogAnalyzer:
    def __init__(self):
        # URL del dataset de logs de la NASA de julio 1995
        self.log_url = "https://raw.githubusercontent.com/elastic/examples/master/Common%20Data%20Formats/nginx_logs/nginx_logs"
        self.log_pattern = r'(\S+) - - \[([^\]]+)\] "(\S+) (\S+) (\S+)" (\d{3}) (\d+|-)'
        self.data = []

    def download_logs(self):
        """Descarga los logs desde la URL."""
        print("Descargando logs...")
        response = requests.get(self.log_url)
        if response.status_code == 200:
            return response.text.split('\n')
        else:
            raise Exception("No se pudieron descargar los logs")

    def parse_logs(self):
        """Parsea los logs descargados y extrae la información relevante."""
        print("Analizando logs...")
        lines = self.download_logs()

        for line in lines:
            if not line.strip():
                continue

            match = re.match(self.log_pattern, line)
            if match:
                host, timestamp, method, path, protocol, status, bytes_sent = match.groups()

                # Convertir timestamp
                try:
                    date = datetime.strptime(timestamp, '%d/%b/%Y:%H:%M:%S %z')
                    date_str = date.strftime('%Y-%m-%d')
                except ValueError:
                    date_str = timestamp

                # Manejar casos donde bytes_sent es '-'
                if bytes_sent == '-':
                    bytes_sent = 0
                else:
                    bytes_sent = int(bytes_sent)

                log_entry = {
                    'host': host,
                    'timestamp': date_str,
                    'method': method,
                    'path': path,
                    'protocol': protocol,
                    'status': int(status),
                    'bytes_sent': bytes_sent
                }
                self.data.append(log_entry)

        print(f"Se procesaron {len(self.data)} entradas de log")

    def save_json(self, output_file):
        """Guarda los datos parseados en formato JSON."""
        with open(output_file, 'w') as f:
            json.dump(self.data, f, indent=2)
        print(f"Datos guardados en {output_file}")

    def plot_http_methods(self):
        """Genera un gráfico de torta mejorado de métodos HTTP."""
        methods = [entry['method'] for entry in self.data]
        method_counts = Counter(methods)

        plt.figure(figsize=(10, 6))
        colors = sns.color_palette('husl', n_colors=len(method_counts))
        plt.pie(method_counts.values(), labels=method_counts.keys(),
                autopct='%1.1f%%', colors=colors, shadow=True)
        plt.title('Distribución de Métodos HTTP en Logs NASA', pad=20)
        plt.savefig('nasa_http_methods.png', bbox_inches='tight', dpi=300)
        plt.close()

    def plot_status_codes(self):
        """Genera un gráfico de barras mejorado de códigos de estado."""
        status_codes = [entry['status'] for entry in self.data]
        status_counts = Counter(status_codes)

        plt.figure(figsize=(12, 6))
        sns.barplot(x=list(status_counts.keys()), y=list(status_counts.values()))
        plt.title('Distribución de Códigos de Estado HTTP en Logs NASA')
        plt.xlabel('Código de Estado')
        plt.ylabel('Cantidad de Solicitudes')
        plt.xticks(rotation=0)

        # Agregar etiquetas de valor en cada barra
        for i, v in enumerate(status_counts.values()):
            plt.text(i, v, str(v), ha='center', va='bottom')

        plt.savefig('nasa_status_codes.png', bbox_inches='tight', dpi=300)
        plt.close()

    def plot_daily_requests(self):
        """Genera un gráfico de líneas mejorado de solicitudes por día."""
        daily_requests = defaultdict(int)
        for entry in self.data:
            daily_requests[entry['timestamp']] += 1

        dates = sorted(daily_requests.keys())
        counts = [daily_requests[date] for date in dates]

        plt.figure(figsize=(15, 6))
        sns.lineplot(x=dates, y=counts, marker='o')
        plt.title('Solicitudes Diarias en Logs NASA')
        plt.xlabel('Fecha')
        plt.ylabel('Número de Solicitudes')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)

        plt.savefig('nasa_daily_requests.png', bbox_inches='tight', dpi=300)
        plt.close()

    def plot_top_paths(self, top_n=10):
        """Genera un gráfico de barras horizontales de las rutas más solicitadas."""
        paths = [entry['path'] for entry in self.data]
        path_counts = Counter(paths).most_common(top_n)

        plt.figure(figsize=(12, 8))
        paths, counts = zip(*path_counts)

        # Eliminar 'palette' ya que no es necesario
        sns.barplot(x=counts, y=paths)

        plt.title(f'Top {top_n} Rutas más Solicitadas')
        plt.xlabel('Cantidad de Solicitudes')
        plt.ylabel('Ruta')

        plt.savefig('nasa_top_paths.png', bbox_inches='tight', dpi=300)
        plt.show()
        plt.close()

    def generate_report(self):
        """Genera un informe detallado con estadísticas."""
        total_requests = len(self.data)
        methods = Counter([entry['method'] for entry in self.data])
        status_codes = Counter([entry['status'] for entry in self.data])
        unique_hosts = len(set([entry['host'] for entry in self.data]))
        total_bytes = sum([entry['bytes_sent'] for entry in self.data])

        # Calcular los paths más comunes
        paths = Counter([entry['path'] for entry in self.data]).most_common(10)

        report = {
            'total_requests': total_requests,
            'unique_hosts': unique_hosts,
            'total_bytes_transferred': total_bytes,
            'average_bytes_per_request': total_bytes / total_requests if total_requests > 0 else 0,
            'http_methods': dict(methods),
            'status_codes': dict(status_codes),
            'top_10_paths': dict(paths)
        }

        with open('nasa_report.json', 'w') as f:
            json.dump(report, f, indent=2)

        print("Reporte generado en nasa_report.json")


def main():
    try:
        # Crear instancia del analizador
        analyzer = NASALogAnalyzer()

        # Procesar logs
        analyzer.parse_logs()
        analyzer.save_json('nasa_logs_processed.json')

        # Generar visualizaciones
        print("Generando visualizaciones...")
        analyzer.plot_http_methods()
        analyzer.plot_status_codes()
        analyzer.plot_daily_requests()
        analyzer.plot_top_paths()

        # Generar reporte
        analyzer.generate_report()

        print("Análisis completado exitosamente!")

    except Exception as e:
        print(f"Error durante el análisis: {str(e)}")


if __name__ == "__main__":
    main()