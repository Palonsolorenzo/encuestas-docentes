"""
Catálogo de ítems de encuestas docentes y propuestas de acciones de mejora
para ítems con valoración inferior a 3.5 puntos.
"""

SURVEY_ITEMS = [
    {
        "id": 1,
        "code": "IT01",
        "dimension": "Planificación y Guía Docente",
        "short_title": "Presentación de Guía y Criterios",
        "text": "Da a conocer la guía docente, los objetivos de la asignatura y los criterios de evaluación al inicio del curso.",
        "diagnosis_under_35": "Los estudiantes perciben incertidumbre sobre las reglas del curso, la ponderación de las notas o los objetivos formativos desde el comienzo.",
        "action_short_term": "Dedicar la primera sesión (o video introductorio en campus virtual) a explicar en detalle la guía docente, el cronograma y el desglose porcentual de la evaluación continua y final.",
        "action_medium_term": "Elaborar una infografía / resumen visual ('Guía rápida de la asignatura') fijada permanentemente en la cabecera del aula virtual con fechas clave y criterios de calificación.",
        "kpi": ">= 95% de alumnos confirman lectura de la guía; puntuación en encuesta >= 3.8",
        "responsible": "Profesor/a responsable de la asignatura"
    },
    {
        "id": 2,
        "code": "IT02",
        "dimension": "Planificación y Guía Docente",
        "short_title": "Cumplimiento de la Planificación",
        "text": "El desarrollo de las clases y actividades se ajusta a lo previsto en la planificación y cronograma.",
        "diagnosis_under_35": "Sensación de improvisación, retrasos en el temario o cambios sobrevenidos de fechas de entregas y exámenes.",
        "action_short_term": "Ajustar el calendario de temas desde el inicio con márgenes de holgura. Notificar cualquier ajuste con un mínimo de 15 días de antelación justificando el motivo académico.",
        "action_medium_term": "Coordinación con la dirección de carrera para evitar solapamientos con entregas de otras asignaturas del mismo curso.",
        "kpi": "Desviación del cronograma inferior al 10%; puntuación en encuesta >= 3.8",
        "responsible": "Profesor/a y Coordinador/a de Titulación"
    },
    {
        "id": 3,
        "code": "IT03",
        "dimension": "Planificación y Guía Docente",
        "short_title": "Bibliografía y Recursos",
        "text": "La bibliografía y las fuentes recomendadas son accesibles, útiles y actualizadas.",
        "diagnosis_under_35": "Bibliografía obsoleta, difícil de localizar en la biblioteca digital/física o excesivamente densa sin orientación de lectura.",
        "action_short_term": "Verificar enlaces activos a la biblioteca digital institucional y añadir lecturas breves, artículos de impacto recientes y recursos multimedia en abierto.",
        "action_medium_term": "Segmentar la bibliografía en 'Lecturas obligatorias guiadas' (con preguntas de reflexión) y 'Lecturas complementarias voluntarias'.",
        "kpi": "100% de enlaces verificados y operativos en biblioteca electrónica.",
        "responsible": "Profesor/a de la asignatura"
    },
    {
        "id": 4,
        "code": "IT04",
        "dimension": "Planificación y Guía Docente",
        "short_title": "Ajuste de Carga de Trabajo (ECTS)",
        "text": "El volumen de trabajo y dedicación exigido guarda proporción con los créditos ECTS de la asignatura.",
        "diagnosis_under_35": "Sobrecarga de tareas o lecturas desmedidas que sobrepasan las 25-30 horas por crédito ECTS asignado.",
        "action_short_term": "Auditar la carga real de horas no presenciales exigidas por semana. Simplificar enunciados y sustituir tareas redundantes por entregables sintéticos.",
        "action_medium_term": "Coordinar con la Comisión de Calidad y el claustro del curso para balancear el calendario conjunto de trabajos y prácticas.",
        "kpi": "Horas estimadas de dedicación del estudiante ajustadas a 25 h/ECTS.",
        "responsible": "Profesor/a y Comisión de Garantía de Calidad"
    },
    {
        "id": 5,
        "code": "IT05",
        "dimension": "Metodología y Explicación",
        "short_title": "Claridad en las Explicaciones",
        "text": "Explica con claridad y orden los conceptos y temas del programa.",
        "diagnosis_under_35": "Dificultad de los alumnos para comprender las exposiciones, falta de estructura didáctica o ritmo desorganizado.",
        "action_short_term": "Iniciar cada tema con un mapa conceptual y los 3 objetivos clave de la sesión. Cerrar con un resumen de conclusiones y preguntas de verificación.",
        "action_medium_term": "Participar en talleres de innovación y oratoria docente universitaria; incorporar recursos visuales y píldoras explicativas de refuerzo.",
        "kpi": "Incremento de al menos +0.8 puntos en la siguiente oleada de encuestas.",
        "responsible": "Profesor/a y Servicio de Formación Docente"
    },
    {
        "id": 6,
        "code": "IT06",
        "dimension": "Metodología y Explicación",
        "short_title": "Estructura de las Sesiones",
        "text": "Estructura y organiza adecuadamente las sesiones docentes presenciales/síncronas.",
        "diagnosis_under_35": "Sesiones monótonas o que se alargan sin transiciones claras entre teoría y práctica.",
        "action_short_term": "Dividir las sesiones en bloques de máximo 20-25 minutos (presentación teórica -> actividad/ejercicio breve -> puesta en común).",
        "action_medium_term": "Publicar un breve guion previo de cada sesión en el campus para que el alumno acuda preparado (enfoque de clase invertida / flipped classroom).",
        "kpi": "Cumplimiento del orden del día de la sesión en el 90% de clases.",
        "responsible": "Profesor/a de la asignatura"
    },
    {
        "id": 7,
        "code": "IT07",
        "dimension": "Metodología y Explicación",
        "short_title": "Fomento de la Participación",
        "text": "Fomenta la participación activa, el espíritu crítico y el debate en las sesiones.",
        "diagnosis_under_35": "Clases unidireccionales de tipo magistral pasivo sin oportunidades para que los alumnos intervengan o debatan.",
        "action_short_term": "Introducir dinámicas de votación en tiempo real (Mentimeter, Wooclap, Kahoot) y preguntas abiertas de resolución en parejas o pequeños grupos.",
        "action_medium_term": "Asignar roles de moderación o presentación breve de noticias/casos de actualidad relacionados con la asignatura.",
        "kpi": "Participación activa de al menos el 60% de los estudiantes matriculados.",
        "responsible": "Profesor/a de la asignatura"
    },
    {
        "id": 8,
        "code": "IT08",
        "dimension": "Metodología y Explicación",
        "short_title": "Aplicación Práctica y Ejemplos",
        "text": "Utiliza ejemplos prácticos y aplicaciones al mundo real para facilitar la comprensión.",
        "diagnosis_under_35": "Exceso de abstracción teórica sin conexión evidente con la práctica profesional o laboral.",
        "action_short_term": "Acompañar cada bloque teórico con un caso práctico real, noticia reciente o simulación del entorno profesional de la titulación.",
        "action_medium_term": "Invitar a un profesional en activo o alumni a impartir una masterclass o analizar un reto real de la industria.",
        "kpi": "Al menos 1 caso práctico real aplicado por cada tema evaluado.",
        "responsible": "Profesor/a de la asignatura"
    },
    {
        "id": 9,
        "code": "IT09",
        "dimension": "Metodología y Explicación",
        "short_title": "Ritmo de Impartición",
        "text": "El ritmo de impartición de las materias es adecuado para el seguimiento del grupo.",
        "diagnosis_under_35": "Sensación de velocidad excesiva en temas complejos o lentitud reiterativa que desmotiva.",
        "action_short_term": "Hacer pausas deliberadas cada 15 minutos para testear el nivel de asimilación; no avanzar sin confirmar la comprensión de los pilares básicos.",
        "action_medium_term": "Ofrecer materiales de nivelación y tutoriales asíncronos para alumnos que necesiten reforzar conocimientos previos.",
        "kpi": "Encuesta intermedia rápida (Semana 4-5) para calibrar el ritmo docente.",
        "responsible": "Profesor/a de la asignatura"
    },
    {
        "id": 10,
        "code": "IT10",
        "dimension": "Metodología y Explicación",
        "short_title": "Resolución de Dudas",
        "text": "Resuelve las dudas planteadas por los estudiantes de manera clara y orientadora.",
        "diagnosis_under_35": "Respuestas cortantes, ambiguas o sensación de que no se resuelven las dificultades reales de los alumnos.",
        "action_short_term": "Habilitar un foro temático de dudas en el campus virtual con compromiso de respuesta en < 48 horas laborales; responder con ejemplos paso a paso.",
        "action_medium_term": "Crear un documento de 'Preguntas Frecuentes (FAQ)' que recopile las dudas más habituales antes de las pruebas evaluativas.",
        "kpi": "Tiempo medio de respuesta a dudas en foros < 36 horas; satisfacción >= 4.0.",
        "responsible": "Profesor/a de la asignatura"
    },
    {
        "id": 11,
        "code": "IT11",
        "dimension": "Recursos y Campus Virtual",
        "short_title": "Organización del Aula Virtual",
        "text": "El aula virtual está bien organizada, ordenada y facilita el estudio autónomo.",
        "diagnosis_under_35": "Estructura caótica en Moodle/Canvas, archivos sueltos sin orden cronológico o carpetas vacías.",
        "action_short_term": "Reestructurar el aula virtual por semanas o bloques temáticos con una plantilla estandarizada: 'Objetivos -> Materiales -> Tareas -> Foro'.",
        "action_medium_term": "Adoptar las pautas de diseño instruccional y accesibilidad web establecidas por el Departamento de Educación Online.",
        "kpi": "100% de los temas con estructura modular homologada.",
        "responsible": "Profesor/a y Soporte Campus Virtual"
    },
    {
        "id": 12,
        "code": "IT12",
        "dimension": "Recursos y Campus Virtual",
        "short_title": "Calidad de los Materiales Didácticos",
        "text": "Los materiales didácticos facilitados en la plataforma son de calidad, claros y actualizados.",
        "diagnosis_under_35": "Presentaciones con textos saturados, apuntes antiguos o materiales escaneados de baja legibilidad.",
        "action_short_term": "Actualizar presentaciones con formatos limpios, infografías y fuentes tipográficas legibles; revisar que no haya erratas conceptuales.",
        "action_medium_term": "Elaborar guías de estudio propias en PDF interactivo con hipervínculos, glosario y autoevaluaciones.",
        "kpi": "Renovación y revisión anual del 100% del material descargable.",
        "responsible": "Profesor/a de la asignatura"
    },
    {
        "id": 13,
        "code": "IT13",
        "dimension": "Recursos y Campus Virtual",
        "short_title": "Recursos Multimedia y Grabaciones",
        "text": "Las actividades virtuales y grabaciones complementan adecuadamente la formación.",
        "diagnosis_under_35": "Problemas de audio/video en grabaciones, enlaces rotos o falta de recursos interactivos.",
        "action_short_term": "Verificar calidad técnica del micrófono y cámara en grabaciones; titular y clasificar las grabaciones con la fecha y temática tratada.",
        "action_medium_term": "Incorporar microvídeos (3-5 minutos) que expliquen los conceptos más complejos o ejercicios típicos de examen.",
        "kpi": "Tasa de incidencias técnicas en recursos audiovisuales < 5%.",
        "responsible": "Profesor/a y Equipo Técnico Audiovisual"
    },
    {
        "id": 14,
        "code": "IT14",
        "dimension": "Recursos y Campus Virtual",
        "short_title": "Puntualidad en Publicación de Tareas",
        "text": "Cumple con los plazos previstos para la publicación de tareas, enunciados y contenidos.",
        "diagnosis_under_35": "Publicación tardía de enunciados de prácticas dejando poco margen a los alumnos para su resolución.",
        "action_short_term": "Publicar todos los enunciados de actividades con un mínimo de 10 a 14 días naturales antes de la fecha límite de entrega.",
        "action_medium_term": "Programar la apertura automática de todas las actividades al inicio del cuatrimestre desde la configuración de la plataforma.",
        "kpi": "Cero retrasos en la publicación de enunciados respecto al cronograma.",
        "responsible": "Profesor/a de la asignatura"
    },
    {
        "id": 15,
        "code": "IT15",
        "dimension": "Evaluación y Feedback",
        "short_title": "Coherencia de Criterios de Evaluación",
        "text": "Los criterios y sistemas de evaluación aplicados coinciden estrictamente con los anunciados.",
        "diagnosis_under_35": "Sensación de arbitrariedad en la calificación o aplicación de penalizaciones/condiciones no contempladas en la guía.",
        "action_short_term": "Publicar una rúbrica analítica detallada junto al enunciado de cada práctica, explicitando los niveles de logro (insuficiente, regular, bueno, excelente).",
        "action_medium_term": "Validar con la Coordinación de Titulación la coherencia entre el sistema de evaluación publicado y las actas finales.",
        "kpi": "Rúbricas publicadas en el 100% de las pruebas evaluables.",
        "responsible": "Profesor/a y Coordinador/a de Titulación"
    },
    {
        "id": 16,
        "code": "IT16",
        "dimension": "Evaluación y Feedback",
        "short_title": "Adecuación del Nivel de Examen/Pruebas",
        "text": "Las pruebas de evaluación y exámenes se ajustan al nivel y contenidos impartidos en clase.",
        "diagnosis_under_35": "Percepción de que los exámenes son mucho más difíciles o abordan contenidos que no se explicaron ni trabajaron en las sesiones.",
        "action_short_term": "Realizar una prueba de autoevaluación o simulacro previo de examen con tipología similar de preguntas para alinear expectativas.",
        "action_medium_term": "Hacer matriz de alineamiento curricular entre resultados de aprendizaje, actividades explicadas y preguntas de examen.",
        "kpi": "Correlación consistente entre rendimiento en evaluación continua y examen final.",
        "responsible": "Profesor/a de la asignatura"
    },
    {
        "id": 17,
        "code": "IT17",
        "dimension": "Evaluación y Feedback",
        "short_title": "Calidad del Feedback / Retroalimentación",
        "text": "Ofrece retroalimentación (feedback) cualitativa y constructiva sobre las calificaciones y trabajos.",
        "diagnosis_under_35": "Entrega de calificaciones numéricas sin comentarios que expliquen los errores ni cómo mejorar en futuras entregas.",
        "action_short_term": "Incluir en cada corrección al menos dos comentarios cualitativos: 'Punto fuerte' y 'Aspecto prioritario a mejorar en la siguiente entrega'.",
        "action_medium_term": "Utilizar herramientas de retroalimentación de la plataforma (comentarios en rúbrica o breves audios/vídeos de feedback general para el grupo).",
        "kpi": "100% de entregables evaluados con comentarios cualitativos personalizados.",
        "responsible": "Profesor/a de la asignatura"
    },
    {
        "id": 18,
        "code": "IT18",
        "dimension": "Evaluación y Feedback",
        "short_title": "Plazos de Corrección y Calificación",
        "text": "La corrección y calificación de los ejercicios y exámenes se realiza en los plazos reglamentarios.",
        "diagnosis_under_35": "Demoras excesivas en publicar notas, impidiendo a los alumnos aprender de sus errores antes de la siguiente entrega.",
        "action_short_term": "Comprometerse a devolver las notas y feedback en un plazo máximo estricto de 15 días naturales (o antes de la siguiente entrega evaluable).",
        "action_medium_term": "Escalonar las fechas de entrega si hay múltiples grupos para gestionar la carga de corrección de forma sostenible.",
        "kpi": "Cumplimiento del plazo máximo de publicación de notas en el 100% de pruebas.",
        "responsible": "Profesor/a de la asignatura"
    },
    {
        "id": 19,
        "code": "IT19",
        "dimension": "Atención al Alumnado y Tutoría",
        "short_title": "Disponibilidad y Tutorías",
        "text": "Muestra disponibilidad y accesibilidad para la atención a los alumnos en tutorías o consultas.",
        "diagnosis_under_35": "Dificultad para concertar tutorías, falta de horarios compatibles o desatención de mensajes privados.",
        "action_short_term": "Establecer franjas semanales fijas de tutoría (presencial y videoconferencia) y habilitar agenda de citas online (Calendly / Teams / Moodle).",
        "action_medium_term": "Realizar sesiones periódicas grupales de 'resolución de dudas en directo' previas a hitos evaluativos importantes.",
        "kpi": "Horario de tutorías publicado y operativo; respuesta a solicitudes en < 24-48 h.",
        "responsible": "Profesor/a de la asignatura"
    },
    {
        "id": 20,
        "code": "IT20",
        "dimension": "Atención al Alumnado y Tutoría",
        "short_title": "Trato Respetuoso y Cordial",
        "text": "El trato, la comunicación y la relación mantenida con los estudiantes es cordial, motivadora y respetuosa.",
        "diagnosis_under_35": "Tono distante, desmotivador o falta de empatía percibida ante las consultas del alumnado.",
        "action_short_term": "Cuidar el tono de las comunicaciones por email y foros; adoptar un enfoque proactivo, empático y orientado a la solución.",
        "action_medium_term": "Reunión de mediación con la Coordinación de Titulación y representantes de curso para recoger percepciones y restablecer clima de confianza.",
        "kpi": "Ausencia de reclamaciones formales sobre trato; valoración en encuesta >= 4.0.",
        "responsible": "Profesor/a y Coordinador/a de Titulación"
    },
    {
        "id": 21,
        "code": "IT21",
        "dimension": "Atención al Alumnado y Tutoría",
        "short_title": "Preocupación por el Aprendizaje",
        "text": "Se preocupa por el progreso del aprendizaje y apoya a los estudiantes ante sus dificultades.",
        "diagnosis_under_35": "Sensación de desinterés hacia el rendimiento global o falta de seguimiento a alumnos con dificultades.",
        "action_short_term": "Identificar a mitad de cuatrimestre a los alumnos con baja participación o calificaciones de riesgo y enviarles un mensaje personalizado de orientación.",
        "action_medium_term": "Implementar planes de refuerzo y orientación académica en coordinación con el servicio de tutoría académica institucional.",
        "kpi": "Tasa de retención y presentación a examen > 80%.",
        "responsible": "Profesor/a y Tutor/a de Titulación"
    },
    {
        "id": 22,
        "code": "IT22",
        "dimension": "Satisfacción Global",
        "short_title": "Satisfacción Global con la Docencia",
        "text": "En general, estoy satisfecho/a con la labor docente desarrollada por el profesor/a en la asignatura.",
        "diagnosis_under_35": "Descontento generalizado acumulado derivado de fallos en metodología, evaluación o comunicación durante el curso.",
        "action_short_term": "Revisión integral de los ítems con peor valoración en la encuesta y elaboración de un Plan de Acción Docente individualizado para el próximo semestre.",
        "action_medium_term": "Plan de mentoría docente con un profesor senior destacado del departamento y revisión periódica con la Dirección Académica.",
        "kpi": "Alcanzar una satisfacción global >= 3.8 en el siguiente curso académico.",
        "responsible": "Profesor/a, Director/a de Departamento y Decanato"
    },
    {
        "id": 23,
        "code": "IT23",
        "dimension": "Satisfacción Global",
        "short_title": "Utilidad y Valor Formativo",
        "text": "Considero que esta asignatura ha sido formativa, valiosa y relevante para mi perfil profesional.",
        "diagnosis_under_35": "Los estudiantes no perciben la aplicabilidad o importancia de los contenidos para su futuro laboral y profesional.",
        "action_short_term": "Conectar explícitamente cada tema y proyecto de la asignatura con competencias demandadas en el mercado laboral y salidas profesionales.",
        "action_medium_term": "Actualizar el temario en la próxima verificación de la memoria académica, incorporando herramientas tecnológicas actuales del sector.",
        "kpi": "Valoración de utilidad formativa >= 3.8.",
        "responsible": "Claustro docente y Coordinación de Titulación"
    }
]

def get_item_info(item_number: int) -> dict:
    """Devuelve la información de un ítem por su número (1 a 23)."""
    for item in SURVEY_ITEMS:
        if item["id"] == item_number:
            return item
    return {
        "id": item_number,
        "code": f"IT{item_number:02d}",
        "dimension": "Dimensión General",
        "short_title": f"Ítem {item_number}",
        "text": f"Ítem de encuesta número {item_number}",
        "diagnosis_under_35": "Valoración deficiente por debajo del estándar de calidad mínimo fijado (3.5 puntos).",
        "action_short_term": "Revisar los contenidos y procedimientos docentes de este aspecto para el próximo semestre.",
        "action_medium_term": "Coordinar con la dirección académica medidas de refuerzo metodológico.",
        "kpi": "Mejora de valoración hasta superar los 3.5 puntos.",
        "responsible": "Profesor/a responsable"
    }

def get_dimension_color(dimension: str) -> str:
    """Devuelve un color consistente para cada dimensión pedagógica."""
    colors = {
        "Planificación y Guía Docente": "#2563EB",   # Azul
        "Metodología y Explicación": "#059669",      # Esmeralda
        "Recursos y Campus Virtual": "#D97706",      # Ámbar
        "Evaluación y Feedback": "#DC2626",          # Rojo / Coral
        "Atención al Alumnado y Tutoría": "#7C3AED", # Violeta
        "Satisfacción Global": "#0891B2"             # Cian
    }
    return colors.get(dimension, "#4B5563")
