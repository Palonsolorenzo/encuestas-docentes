"""
Generador de archivos Excel de demostración con datos realistas
para pruebas inmediatas de la aplicación de encuestas docentes.
"""

import os
import io
import numpy as np
import pandas as pd
from recommendations import SURVEY_ITEMS

def generate_sample_subject_dataframe(subject_profile: str, n_students: int = 25) -> pd.DataFrame:
    """
    Genera un DataFrame simulando las respuestas de los alumnos a los 23 ítems.
    Perfiles: 'excelente', 'medio', 'problemas_metodologia', 'problemas_evaluacion', 'bueno'
    """
    np.random.seed(abs(hash(subject_profile)) % 100000)
    data = {}
    
    for item in SURVEY_ITEMS:
        item_id = item["id"]
        col_header = f"{item['code']}: {item['short_title']}"
        
        # Determinar media esperada según el perfil y el ítem
        if subject_profile == 'excelente':
            target_mean = np.random.uniform(4.3, 4.8)
        elif subject_profile == 'bueno':
            target_mean = np.random.uniform(3.9, 4.4)
        elif subject_profile == 'medio':
            # Algunos ítems en torno a 3.4
            if item_id in [4, 14]:
                target_mean = np.random.uniform(3.0, 3.4)
            else:
                target_mean = np.random.uniform(3.6, 4.1)
        elif subject_profile == 'problemas_metodologia':
            # Ítems de explicación, ritmo y dudas bajos (< 3.5)
            if item_id in [5, 6, 8, 9, 10, 22]:
                target_mean = np.random.uniform(2.6, 3.3)
            else:
                target_mean = np.random.uniform(3.5, 4.0)
        elif subject_profile == 'problemas_evaluacion':
            # Ítems de feedback, exámenes y plazos de notas bajos (< 3.5)
            if item_id in [15, 16, 17, 18]:
                target_mean = np.random.uniform(2.7, 3.3)
            else:
                target_mean = np.random.uniform(3.8, 4.3)
        else:
            target_mean = 3.8

        # Simular distribución con target_mean y escala 1-5
        probs = _calculate_likert_probs(target_mean)
        
        # Simular respuestas
        responses = np.random.choice([1, 2, 3, 4, 5], size=n_students, p=probs).tolist()
        
        # Insertar algunos 'N/S' ocasionales (entre 0% y 8%)
        n_ns = np.random.binomial(n_students, 0.04)
        if n_ns > 0:
            ns_indices = np.random.choice(n_students, size=n_ns, replace=False)
            for idx in ns_indices:
                responses[idx] = "N/S"
                
        data[col_header] = responses

    return pd.DataFrame(data)

def _calculate_likert_probs(target_mean: float) -> list:
    """Calcula probabilidades para valores 1..5 ajustadas a una media objetivo."""
    # Centrar distribución
    mean_val = max(1.5, min(4.8, target_mean))
    raw_weights = [np.exp(-0.8 * abs(v - mean_val)**1.8) for v in [1, 2, 3, 4, 5]]
    total = sum(raw_weights)
    return [w / total for w in raw_weights]

def generate_sample_files_bundle(degree_name: str = "Grado en ADE") -> list:
    """
    Genera un conjunto de archivos Excel en memoria (BytesIO) listos para cargar.
    Retorna lista de tuplas: (nombre_archivo, BytesIO_buffer)
    """
    subjects_config = [
        {"filename": "Dirección Estratégica.xlsx", "profile": "excelente", "n": 30},
        {"filename": "Contabilidad Financiera.xlsx", "profile": "problemas_evaluacion", "n": 28},
        {"filename": "Marketing Digital.xlsx", "profile": "bueno", "n": 24},
        {"filename": "Microeconomía Intermedia.xlsx", "profile": "problemas_metodologia", "n": 32},
        {"filename": "Derecho Mercantil.xlsx", "profile": "medio", "n": 26},
        {"filename": "Estadística Empresarial.xlsx", "profile": "bueno", "n": 22}
    ]
    
    files_bundle = []
    
    for conf in subjects_config:
        df = generate_sample_subject_dataframe(conf["profile"], conf["n"])
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # El nombre de la pestaña es la titulación
            df.to_excel(writer, sheet_name=degree_name, index=False)
        output.seek(0)
        files_bundle.append((conf["filename"], output))
        
    return files_bundle

def save_sample_files_to_disk(target_dir: str, degree_name: str = "Grado en ADE") -> list:
    """Guarda los archivos de demostración en un directorio en disco."""
    os.makedirs(target_dir, exist_ok=True)
    bundle = generate_sample_files_bundle(degree_name)
    saved_paths = []
    
    for filename, buf in bundle:
        dest_path = os.path.join(target_dir, filename)
        with open(dest_path, "wb") as f:
            f.write(buf.getvalue())
        saved_paths.append(dest_path)
        
    return saved_paths
