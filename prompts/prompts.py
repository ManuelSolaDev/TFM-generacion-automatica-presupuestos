cleaner_prompt_template = """
Estás a punto de recibir un texto que proviene de la transcripción de una conversación entre dos personas durante una reunión. Este texto puede contener errores de transcripción, como palabras mal escritas o frases incoherentes, debido a la conversión automática de audio a texto.

La reunión trata sobre el desarrollo de una aplicación web. Uno de los participantes es el encargado de recopilar todos los requisitos funcionales de la aplicación, mientras que el otro es el cliente que desea que se le desarrolle dicha aplicación. Tu tarea es limpiar y corregir este texto para que sea coherente, claro y refleje con precisión toda la información discutida en la reunión. Es fundamental que mantengas toda la información relevante y no omitas ningún detalle importante.

Instrucciones específicas:

Corrección de errores: Identifica y corrige cualquier error de transcripción, incluyendo palabras mal escritas, frases incompletas o incoherentes, y problemas de puntuación.

Claridad y coherencia: Asegúrate de que el texto final sea claro, con una secuencia lógica de ideas, y que las respuestas y preguntas entre los dos interlocutores se mantengan consistentes y comprensibles.

Conservación de la información: No debes omitir ninguna información relevante discutida en la reunión. Si encuentras partes del texto que parecen irrelevantes o confusas, asegúrate de interpretarlas de la mejor manera posible para que reflejen fielmente la intención original de la conversación.

Finalmente, el texto limpio debe reflejar fielmente la conversación original, permitiendo que cualquier lector entienda claramente los requisitos y las decisiones discutidas en la reunión.

Esta es la transcripción que debes limpiar:

{audio_transcription}

"""


functional_requirements_definer_prompt_template = """
Estás a punto de recibir un texto que ha sido limpiado y corregido a partir de la transcripción de una conversación en una reunión. Este texto contiene toda la información discutida entre dos personas: un representante encargado de recopilar requisitos funcionales y un cliente que desea desarrollar una aplicación web.

Tu tarea es extraer de este texto un listado exhaustivo y detallado de los requisitos funcionales del proyecto de software. Estos requisitos deben reflejar de la manera más precisa posible todas las características, funcionalidades, y aspectos técnicos necesarios para desarrollar y presupuestar correctamente la aplicación web.

Es fundamental que identifiques y describas no solo las funcionalidades visibles para el usuario final, sino también todos los aspectos técnicos esenciales para el desarrollo completo del sistema, incluyendo pero no limitándose a:

1. Diseño e implementación de bases de datos: Describe las necesidades de almacenamiento, estructuras de datos, y cualquier requerimiento específico en términos de bases de datos.

2. Seguridad: Incluye todos los requisitos relacionados con la seguridad del sistema, como la autenticación, autorización, cifrado de datos, y protección contra amenazas.

3. Diseño e implementación de la infraestructura: Detalla los requisitos para la infraestructura necesaria, como servidores, entornos de desarrollo, despliegue, escalabilidad y redundancia.

4. Diseño e implementación de la API: Describe las necesidades para la creación de interfaces de programación de aplicaciones (API) que permitan la comunicación entre diferentes partes del sistema, si es necesario.

5. Gestión de usuarios, roles y permisos: Asegúrate de incluir cómo se gestionarán los usuarios, sus roles dentro del sistema, y los permisos asociados a cada rol.

6. Diseño e implementación de la interfaz de usuario: Describe los requisitos relacionados con la interfaz de usuario, como la navegación, la usabilidad, el diseño visual, y la experiencia del usuario. 

7. Cualquier otro aspecto técnico relevante: Incluye cualquier otro requisito técnico que pueda ser necesario para la correcta implementación y funcionamiento de la aplicación, como integraciones con otros sistemas, pruebas, y mantenimiento.

Instrucciones específicas:

1. Identificación de requisitos: Lee cuidadosamente el texto y extrae todos los requisitos funcionales y técnicos discutidos. Asegúrate de identificar y listar todas las características, funcionalidades, y necesidades técnicas del sistema.

2. Claridad y precisión: Redacta los requisitos de forma clara y precisa, utilizando un lenguaje técnico adecuado. Cada requisito debe ser fácilmente comprensible y no debe dar lugar a interpretaciones ambiguas.

3. Estructura de los requisitos: Presenta los requisitos de manera estructurada, utilizando listas numeradas o viñetas para que sea fácil revisarlos. Si hay dependencias o relaciones entre los requisitos, asegúrate de indicarlas claramente.

4. Completitud: Asegúrate de que todos los aspectos importantes del sistema estén cubiertos. Si algún requisito no está explícito en el texto pero es claramente inferido a partir de la conversación, inclúyelo, indicando que es una interpretación basada en la discusión.

5. Validación: Revisa el listado final para asegurarte de que refleja de manera precisa y completa las expectativas del cliente, y que cualquier lector pueda entender claramente qué es lo que se debe desarrollar.

El resultado final debe ser un documento que incluya todos los requisitos funcionales y técnicos necesarios para el desarrollo de la aplicación web, permitiendo un presupuesto completo y preciso para el proyecto.

Este es el texto limpio que debes analizar para extraer los requisitos funcionales:

{cleaned_audio_transcription}

"""


budgeter_prompt_template = """
Estás a punto de recibir un listado detallado de requisitos funcionales y técnicos para el desarrollo de una aplicación web. Este listado incluye todas las características, funcionalidades, y aspectos técnicos necesarios para la implementación completa del sistema, incluyendo pero no limitándose a diseño e implementación de bases de datos, seguridad, infraestructura, APIs, gestión de usuarios, roles y permisos, así como cualquier otro aspecto relevante para el desarrollo y mantenimiento de la aplicación.

Tu tarea es generar un presupuesto detallado para el desarrollo de este proyecto. El presupuesto debe ser preciso y reflejar los costos asociados a cada uno de los requisitos funcionales y técnicos mencionados, teniendo en cuenta todos los elementos que pueden influir en el costo total del proyecto. El precio por hora para este proyecto es de 60€.

Instrucciones específicas:

Desglose de costos: Calcula los costos para cada uno de los requisitos funcionales y técnicos. Esto incluye, pero no se limita a:

Desarrollo de funcionalidades: Estimación de horas de trabajo necesarias y multiplicación por el precio por hora (60€) para cada funcionalidad descrita.
Diseño e implementación de bases de datos: Costos relacionados con la planificación, diseño, implementación, y mantenimiento de la base de datos, basados en el número de horas requeridas y el precio por hora.
Seguridad: Costos asociados con la implementación de medidas de seguridad, como autenticación, cifrado de datos, y protección contra amenazas.
Infraestructura: Estimación de los costos de servidores, almacenamiento en la nube, escalabilidad, redundancia y otras necesidades de infraestructura, basados en las horas de trabajo y cualquier costo de hardware o servicios.
Desarrollo de APIs: Costos relacionados con el diseño, desarrollo y mantenimiento de APIs.
Gestión de usuarios, roles y permisos: Estimación del tiempo y costos asociados con la creación y gestión de sistemas de usuario, roles, y permisos.
Pruebas y aseguramiento de la calidad: Costos relacionados con las pruebas del sistema para garantizar su correcto funcionamiento.
Mantenimiento y soporte: Estimación de los costos a largo plazo para mantenimiento y soporte del sistema.
Costos adicionales: Considera cualquier otro costo asociado que pueda surgir durante el desarrollo del proyecto, como la integración con otros sistemas, adquisición de licencias de software, o capacitación de usuarios.

Desglose de tiempos: Proporciona una estimación del tiempo necesario para completar cada una de las fases del proyecto, lo que ayudará a estimar los costos en función del tiempo.

Margen de error para imprevistos: Incluye un margen adicional en el presupuesto para cubrir posibles imprevistos o cambios en los requisitos. Este margen debe reflejar un porcentaje razonable del costo total (por ejemplo, un 10-15%) para asegurar que el proyecto pueda cubrir gastos no planificados.

Resumen del presupuesto: Al final, proporciona un resumen claro del presupuesto total, desglosado por categorías principales, y resalta cualquier área que pueda tener una mayor variabilidad en el costo. Asegúrate de incluir tanto el costo base como el costo con el margen de error incluido.

Consideraciones adicionales: Incluye cualquier comentario o advertencia sobre posibles variaciones en el presupuesto debido a factores como cambios en los requisitos o desafíos técnicos imprevistos.

El resultado final debe ser un documento de presupuesto detallado y preciso que permita al cliente y al equipo de desarrollo entender claramente los costos asociados con el proyecto, incluyendo un margen para imprevistos, y tomar decisiones informadas sobre la inversión necesaria.

Este es el listado detallado de requisitos funcionales y técnicos para el desarrollo de una aplicación web:

{functional_requirements}

"""
